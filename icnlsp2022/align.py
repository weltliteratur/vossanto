# align tags of sentence and translated sentence (output from translate.py is needed) with simalign
# please see https://github.com/cisnlp/simalign/tree/master on how to use simalign

import argparse
import ast
import re

import pandas as pd
from nltk.tokenize import TreebankWordTokenizer
from simalign import SentenceAligner


# load input files (original file and file including translations)
def read_data(path_orig, path_translated):
    data_orig = pd.read_csv(path_orig, delimiter="\t")
    translations = pd.read_csv(path_translated, delimiter="\t")
    data_orig["translation"] = translations["translated_sents"]
    return data_orig


# format data
def format_data(data):
    data_unstacked = data.explode(["aligned_translated_tuples"])[["aligned_translated_tuples"]]
    data_unstacked[["word", "tag"]] = data_unstacked.aligned_translated_tuples.apply(
        lambda x: pd.Series({"word": x[0], "tag": x[1]}))
    return data_unstacked


# align tags from original sentence to translated sentence
def align(data):
    # check column due to different naming and tokenizes annotated sentece
    if "annotated_sent" in data:
        splitted = TreebankWordTokenizer().tokenize(data['annotated_sent'])
    else:
        splitted = TreebankWordTokenizer().tokenize(str(data['annotated'])) if "*" in str(
            data['annotated']) else TreebankWordTokenizer().tokenize(str(data['sentence']))

    # remove special annotation characters from tokens
    splitted = [re.sub("(\*|\/|\|)", "", s) for s in splitted]
    # tokenize translated sentence
    splitted_translation = TreebankWordTokenizer().tokenize(str(data['translation']))
    # compute alignments
    alignments = aligner.get_word_aligns(splitted, splitted_translation)
    alignment = alignments["itermax"]
    tuples = ast.literal_eval(data["tuples"])
    tag_lst = []

    # assign aligned tags to tokenized translated sentence
    for k, word in enumerate(splitted_translation):
        orig_idx = [t[0] for t in alignment if t[1] == k]
        if len(orig_idx) > 1:
            tags = set([t[1] for i, t in enumerate(tuples) if i in orig_idx])
            if len(tags) == 1:
                tag = tags.pop()
            elif "O" in tags:
                tags.remove("O")
                tag = tags.pop()
            else:
                tag = tags.pop()
        elif len(orig_idx) == 1:
            tag = tuples[orig_idx[0]][1]
        else:
            tag = "O"
        tag_lst.append(tag)

    # formatting
    aligned_translated_tuples = [(word, tag_lst[i]) for i, word in enumerate(splitted_translation)]
    aligned_translated_tuples.append(("", ""))
    return aligned_translated_tuples


# post-processing: boundary words between source and modifier is cleared from false tag alignments
def post_processing(data):
    tuples = data["aligned_translated_tuples"]
    #     print(type(tuples))
    for i, t in enumerate(tuples):
        if i + 1 < len(tuples):
            if "SRC" in t[1] and "MOD" in tuples[i + 1][1] and tuples[i + 1][0] in ["of", "for", "among"]:
                tuples[i + 1] = (tuples[i + 1][0], "O")
    return tuples


# save data
def save_data(data, path):
    data[["word", "tag"]].to_csv(path, sep=" ",
                                 index=False, header=False)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='aligns tags of sentence-pairs')
    parser.add_argument('input', type=str, help='input file')
    parser.add_argument('-t', '--translated', type=str,
                        help='path to file including translations (output file from translate.py)')
    parser.add_argument('-o', '--output', type=str,
                        help='path to output file')
    parser.add_argument('-l', '--lang', type=str,
                        help='language of the input file (de/en)')
    args = parser.parse_args()

    data = read_data(args.input, args.translated)

    aligner = SentenceAligner(model="xlmr", token_type="bpe", matching_methods="mai")
    data["aligned_translated_tuples"] = data.apply(align, axis=1)
    if args.lang == "de":
        data["aligned_translated_tuples"] = data.apply(post_processing, axis=1)
    data = format_data(data)
    save_data(data, args.output)

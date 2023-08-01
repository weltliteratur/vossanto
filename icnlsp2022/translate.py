# based on https://github.com/pytorch/fairseq/tree/main/examples/translation
# translate sentences (en-ger/ger-en) using fairseq transformer model

import argparse
import ast

import pandas as pd
import torch
from unidecode import unidecode


# load input files
def load_data(path, lang="de"):
    df = pd.read_csv(path, sep="\t")
    if lang == "de":
        df["sentence"] = df.sentence.apply(unidecode)
    df["tags"] = df.tuples.apply(lambda x: [t[1] for t in ast.literal_eval(x)])
    return df


# translate sentences in both directions (en-ger/ger-en)
def translate(sents, lang="de", cuda=False):
    sents = list(sents)
    if lang == "de":
        translator = torch.hub.load('pytorch/fairseq', 'transformer.wmt19.de-en',
                                    checkpoint_file='model1.pt:model2.pt:model3.pt:model4.pt',
                                    tokenizer='moses', bpe='fastbpe')
    else:
        translator = torch.hub.load('pytorch/fairseq', 'transformer.wmt19.en-de',
                                    checkpoint_file='model1.pt:model2.pt:model3.pt:model4.pt',
                                    tokenizer='moses', bpe='fastbpe')
    if cuda:
        translator.cuda()
    translator.eval()
    translated = translator.translate(sents)
    return pd.Series(translated)


# save necessary data
def save_translated_data(data, path):
    data[["sentence", "translated_sents", "tags"]].to_csv(path, sep="\t", index=False)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='translates sentences using fairseq transformer model')
    parser.add_argument('input', type=str, help='input file')
    parser.add_argument('-o', '--output', type=str, default="translated.tsv",
                        help='path to output file')
    parser.add_argument('-l', '--lang', type=str, default="en",
                        help='language of the input file (de/en)')
    args = parser.parse_args()

    assert args.lang in ['de', 'en'], "Unsupported language. Please choose either 'de' or 'en'."

    data = load_data(args.input, args.lang)
    data["translated_sents"] = translate(data.sentence, lang=args.lang, cuda=True)
    save_translated_data(data, args.output)

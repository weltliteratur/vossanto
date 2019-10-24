# Reads the files produced by check_wikidata.py
# and filters by popularity measure

import re
import argparse
import os
import sys
import gzip
import csv

version = "0.0.3"

# type your pattern in here
pattern = "theof"
first_pattern = "the"
second_pattern = "of"

re_quotes = re.compile('""')
re_csvquotes = re.compile("|")

# regex
regex = r".*\b" + re.escape(first_pattern) + r"\s+(.*)$"
re_the = re.compile(regex)

# to remove control characters, seepycha
# https://stackoverflow.com/questions/92438/stripping-non-printable-characters-from-a-string-in-python
control_chars = "".join(map(chr, list(range(0, 32)) + list(range(127, 160))))
control_char_re = re.compile("[%s]" % re.escape(control_chars))


def remove_control_chars(s):
    return control_char_re.sub("", s)


def clean(s):
    s = s[1:-1]
    # unquote
    s = re_quotes.sub('"', s)
    # remove non-printable characters
    # TODO: does not work properly for U+200E (which is changed to E2)
    # check with "Q29841121"     "Alexander Howe<U+200E>"
    s = remove_control_chars(s)
    return s


# reads entity list with sitelinks
def get_sitelinks(fname, sep="\t"):
    items = dict()
    id_with_no_sl = 0
    # format: "Q863081"       "Billy ""The Kid"" Emerson"
    with open(fname, "rt", encoding="utf-8") as f:
        for line in f:
            # extract parts
            itemId, sitelinks = line.strip().split(sep, 1)
            itemId_raw = itemId
            # remove surrounding quotes
            itemId = clean(itemId)
            sitelinks = int(sitelinks)
            # print(itemId,itemId_raw)
            # ignore duplicates
            if itemId not in items and sitelinks > 0:
                items[itemId] = sitelinks
                # print(itemId,sitelinks)
            else:
                # print(itemId, "ERROR")
                id_with_no_sl += 1

    return items


# reads entity list with aliases and filters with help of entity-sitelink list
def get_ids_and_labels(fname_alias, fname_sl, sep="\t"):
    items = dict()
    sitelinks = get_sitelinks(fname_sl)
    # format: "Q863081"       "Billy ""The Kid"" Emerson"
    with open(fname_alias, "rt", encoding="utf-8") as f:
        for line in f:
            # extract parts
            itemId, label = line.strip().split(sep, 1)
            itemId = clean(itemId)
            label = clean(label)
            label = label.lower()
            if label not in items and itemId in sitelinks:
                items[label] = itemId
            elif (
                itemId in sitelinks
                and items[label] in sitelinks
                and sitelinks[itemId] > sitelinks[items[label]]
            ):
                items[label] = itemId
    return items


# reads and filters human entity list
def get_items(fname, fname_alias, fname_sl, sep="\t"):
    items = dict()
    synonyms = dict()
    all_ids = get_ids_and_labels(fname_alias, fname_sl)
    # format: "Q863081"       "Billy ""The Kid"" Emerson"
    with open(fname, "rt", encoding="utf-8") as f:
        for line in f:
            # extract parts
            itemId, itemLabels = line.strip().split(sep, 1)
            itemLabels = itemLabels.split(sep)
            itemLabel = itemLabels.pop(0)
            # remove surrounding quotes
            itemId = clean(itemId)
            itemLabel = clean(itemLabel)
            itemLabel = itemLabel.lower()
            # ignore duplicates
            if itemLabel in all_ids and all_ids[itemLabel] == itemId:
                if itemLabel not in items:
                    items[itemLabel] = itemId
                elif int(itemId[1:]) < int(items[itemLabel][1:]):
                    # ensure that we always use the item with the lowest id
                    items[itemLabel] = itemId
                # handle synonyms
                for syn in itemLabels:
                    syn = clean(syn)
                    syn = syn.lower()
                    # conditions as before (but merged with or)
                    if syn in all_ids and all_ids[syn] == itemId:
                        if syn not in synonyms or int(itemId[1:]) < int(
                            items[itemLabel][1:]
                        ):
                            # we store the itemLabel such that we can easily
                            # print it and get the corresponding itemId via
                            # items
                            synonyms[syn] = itemLabel
    return items, synonyms


if __name__ == "__main__":

    parser = argparse.ArgumentParser(
        description="Find entries matching humans.",
        formatter_class=argparse.ArgumentDefaultsHelpFormatter,
    )
    parser.add_argument("phrases", type=str, help="output from theof.py")
    parser.add_argument("wikidata", type=str, help="Wikidata entities (humans)")
    parser.add_argument("alias", type=str, help="all Wikidata entities")
    parser.add_argument("sitelinks", type=str, help="Wikidata entities with sitelinks")
    parser.add_argument(
        "-o", "--output", type=str, help="output tsv file", default=None
    )
    parser.add_argument(
        "-v", "--version", action="version", version="%(prog)s " + version
    )

    args = parser.parse_args()

    # read items
    items, synonyms = get_items(args.wikidata, args.alias, args.sitelinks)
    print("read", len(items), "unique item labels", file=sys.stderr)

    # read phrases
    with open(args.phrases, "r") as inputfile, open(args.output, "w") as outputfile:
        reader = csv.reader(inputfile, delimiter="\t")
        writer = csv.writer(outputfile, delimiter="\t", quoting=csv.QUOTE_ALL)
        for line in reader:
            # print(line)
            article = line[0]
            phrase = line[3]
            sentence = line[5]
            item_normal = phrase
            item = item_normal.lower()
            # check if exists
            if item in items:
                # print(article, items[item], phrase, item, item, sentence, sep='\t')
                writer.writerow([article, items[item], phrase, item, item, sentence])
            elif item in synonyms:
                # print(article, items[synonyms[item]], phrase, item, synonyms[item], sentence, sep='\t')
                writer.writerow(
                    [
                        article,
                        items[synonyms[item]],
                        phrase,
                        item,
                        synonyms[item],
                        sentence,
                    ]
                )
            else:
                # check if the phrase itself contains "the"
                for match in re_the.findall(item_normal):
                    match = match.lower()
                    if match in items:
                        # print(article, items[match], phrase, match, match, sentence, sep='\t')
                        writer.writerow(
                            [article, items[match], phrase, match, match, sentence]
                        )
                    elif match in synonyms:
                        # print(article, items[synonyms[match]], phrase, match, synonyms[match], sentence, sep='\t')
                        writer.writerow(
                            [
                                article,
                                items[synonyms[match]],
                                phrase,
                                match,
                                synonyms[match],
                                sentence,
                            ]
                        )

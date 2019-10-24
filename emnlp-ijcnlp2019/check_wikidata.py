#!/usr/bin/python3 -u
# -*- coding: utf-8 -*-

#
# Reads the file produced by theof.py and the list of Wikidata
# entities with an "instance of" property of "human" and prints all
# lines which match such an entity.

import re
import argparse
import os
import sys
import gzip
import csv

version = "0.0.3"

re_quotes = re.compile("\"\"")
re_csvquotes = re.compile("|")

# here we have to type in the first part of the pattern for detection of the pattern within the found candidate ( the character calls it ''the Mondrian of -> the Mondrian of)
re_the = re.compile(r".*\bthe\s+(.*)$")

# to remove control characters, see
# https://stackoverflow.com/questions/92438/stripping-non-printable-characters-from-a-string-in-python
control_chars = ''.join(map(chr, list(range(0,32)) + list(range(127,160))))
control_char_re = re.compile('[%s]' % re.escape(control_chars))

def remove_control_chars(s):
    return control_char_re.sub('', s)

def clean(s):
    s = s[1:-1]
    # unquote
    s = re_quotes.sub("\"", s)
    # remove non-printable characters
    # TODO: does not work properly for U+200E (which is changed to E2)
    # check with "Q29841121"     "Alexander Howe<U+200E>"
    s = remove_control_chars(s)
    return s

# read Wikidata entity file into map
def get_items(fname, sep='\t'):
    items = dict()
    synonyms = dict()
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
            # ignore duplicates
            if itemLabel not in items:
                items[itemLabel] = itemId
            elif int(itemId[1:]) < int(items[itemLabel][1:]):
                # ensure that we always use the item with the lowest id
                items[itemLabel] = itemId
            # handle synonyms
            for syn in itemLabels:
                syn = clean(syn)
                # conditions as before (but merged with or)
                if syn not in synonyms or int(itemId[1:]) < int(items[itemLabel][1:]):
                    # we store the itemLabel such that we can easily
                    # print it and get the corresponding itemId via
                    # items
                    synonyms[syn] = itemLabel
    return items, synonyms

# read blacklist
def get_blacklist(fname, sep='\t'):
    items = set()
    # format: Lone Ranger\t7
    with open(fname, "r", encoding="utf-8") as f:
        for line in f:
            # extract parts
            item, count = line.strip().split(sep)
            items.add(item)
    return items

if __name__ == '__main__':

    parser = argparse.ArgumentParser(description='Find entries matching humans.', formatter_class=argparse.ArgumentDefaultsHelpFormatter)
    parser.add_argument('phrases', type=str, help='output from theof.py')
    parser.add_argument('wikidata', type=str, help='Wikidata entities')
    parser.add_argument('-o', '--output', type=str, help='output tsv file', default=None)
    parser.add_argument('-b', '--blacklist', type=str, help="blacklist names")
    parser.add_argument('-v', '--version', action="version", version="%(prog)s " + version)

    args = parser.parse_args()

    # read items
    items, synonyms = get_items(args.wikidata)
    print("read", len(items), "unique item labels", file=sys.stderr)
    # read blacklist
    if args.blacklist:
        blacklist = get_blacklist(args.blacklist)
        print("read", len(blacklist), "blacklist labels", file=sys.stderr)
    else:
        blacklist = set()

    # read phrases
    with open(args.phrases, "r") as inputfile, open(args.output, 'w') as outputfile:
        reader=csv.reader(inputfile,delimiter='\t')
        # write everything into a file
        writer = csv.writer(outputfile, delimiter='\t', quoting=csv.QUOTE_ALL)
        for line in reader:
            article=line[0]
            phrase=line[1]
            sentence=line[2]
            # the John Doe of -> strip "the" and "of"
            item = ' '.join(phrase.split()[1:-1])
            if item in items and item not in blacklist:
                print(article, items[item], phrase, item, item, sentence, sep='\t')
                writer.writerow([article, items[item], phrase, item, item, sentence])
            elif item in synonyms and item not in blacklist:
                print(article, items[synonyms[item]], phrase, item, synonyms[item], sentence, sep='\t')
                writer.writerow([article, items[synonyms[item]], phrase, item, synonyms[item], sentence])
            else:
                # check if the phrase itself contains "the"
                for match in re_the.findall(item):
                    if match in items and match not in blacklist:
                        print(article, items[match], phrase, match, match, sentence, sep='\t')
                        writer.writerow([article, items[match], phrase, match, match, sentence])
                    elif match in synonyms and match not in blacklist:
                        print(article, items[synonyms[match]], phrase, match, synonyms[match], sentence, sep='\t')
                        writer.writerow([article, items[synonyms[match]], phrase, match, synonyms[match],sentence])
                    

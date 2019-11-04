#!/usr/bin/python3
# -*- coding: utf-8 -*-

#
# Reads a TSV file and reformats it into Emacs org-mode. Extends the tsv2org script from rja and is valid for only one big tsv file
# containing all data from all years (nyt corpus)
#
# Usage:
#
# Author msc, rja

import re
import csv
import fileinput
import argparse


def get_nyt_link(year, id):
    file = "michel/nyt_" + str(year) + "_links.tsv"
    with open(file, "r") as inputfile:
        reader = csv.reader(inputfile, delimiter="\t")
        for line in reader:
            if line[0] == id:
                return line[1]
        else:
            return "no link available"


re_articleid = re.compile(r"nyt_corpus_([0-9]{4})\.har([0-9/]+)\.xml")

lst = []
if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="Find entries matching humans.",
        formatter_class=argparse.ArgumentDefaultsHelpFormatter,
    )
    parser.add_argument("candidates", type=str, help="output from check_wikidata.py")
    args = parser.parse_args()

    with open(args.candidates, "r") as inputfile:
        reader = csv.reader(inputfile, delimiter="\t")
        next(reader, None)
        for line in reader:
            label = line[0]
            articleid = line[1]
            itemid = line[2]
            wiki_page = line[3]
            phrase = line[4]
            item = line[5]
            itemCanon = line[6]
            sentence = line[7]
            annotated = line[8]
            annotated = annotated.replace("|", "")
            m = re_articleid.match(articleid)
            articledate = m.group(1) + m.group(2)
            year = m.group(1).split("/")[0]
            link = get_nyt_link(year, articleid)
            if label == "F":
                lst.append(
                    [
                        "+[[https://www.wikidata.org/wiki/"
                        + itemid
                        + "]["
                        + itemCanon
                        + "]]",
                        "([[" + link + "]",
                        "[" + articledate + "]])",
                        sentence.strip() + "+",
                        year,
                    ]
                )
            else:
                lst.append(
                    [
                        "[[https://www.wikidata.org/wiki/"
                        + itemid
                        + "]["
                        + itemCanon
                        + "]]",
                        "([[" + link + "]",
                        "[" + articledate + "]])",
                        annotated.strip(),
                        year,
                    ]
                )
lst = sorted(lst, key=lambda x: x[2])

i = 0
year = "0"
print()
for line in lst:
    i += 1
    year_line = str(line[4])
    if year_line == year:
        print(str(i) + ". ", line[0], line[1] + line[2], line[3])
    else:
        year = year_line
        print("** " + line[4])
        print(str(i) + ". ", line[0], line[1] + line[2], line[3])

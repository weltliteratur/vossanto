#!/usr/bin/python3
# -*- coding: utf-8 -*-

#
# Reads a TSV file and reformats it into Emacs org-mode.
#
# Usage:
# 
# Author: rja 
#
# Changes:
# 2018-08-21 (rja)
# - added strip() for sentence
# 2017-05-11 (rja)
# - removed dependency to extraction regex and simplified source highlighting
# - added column for canonical item label
# 2017-05-09 (rja)
# - initial version 

import re
import fileinput

re_articleid = re.compile(r"nyt_corpus_([0-9]{4})\.har([0-9/]+)\.xml")

if __name__ == '__main__':
    for line in fileinput.input():
        articleid, itemid, phrase, item, itemCanon, sentence = line.strip().split("\t", 5)
        # clean up the parts
        m = re_articleid.match(articleid)
        articleid = m.group(1) + m.group(2)

        # print result
        print("1.", "[[https://www.wikidata.org/wiki/" + itemid + "][" + itemCanon + "]]", "(" + articleid + ")", re.sub("(the " + item + " of)", "*\\1*", sentence.strip()))
    

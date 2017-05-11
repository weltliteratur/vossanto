#!/usr/bin/python
# -*- coding: utf-8 -*-

#
# Reads a TSV file and reformats it into Markdown.
#
# Usage:
# 
# Author: rja 
#
# Changes:
# 2017-05-09 (rja)
# - initial version 

from __future__ import print_function
import re
import fileinput

re_articleid = re.compile(r"nyt_corpus_([0-9]{4})\.har([0-9/]+)\.xml")
# first version
# re_theof = re.compile("(\\bthe\\s([A-Z][a-z]+\\s+){1,3}of\\b)")
re_theof = re.compile("(\\bthe\\s(\\w+\\s+){1,5}?of\\b)", re.UNICODE)

if __name__ == '__main__':
    for line in fileinput.input():
        articleid, itemid, phrase, item, sentence = line.strip().split("\t", 4)
        # clean up the parts
        m = re_articleid.match(articleid)
        articleid = m.group(1) + m.group(2)

        # print result
        print("1. ", "[[https://www.wikidata.org/wiki/" + itemid + "][" + item + "]]", "(" + articleid + ")", re_theof.sub("*\\1*", sentence))
    

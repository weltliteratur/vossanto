#!/usr/bin/python
# -*- coding: utf-8 -*-

#
# Clean and analyse POS/NER patterns.
#
# Usage:
#
# Author: rja
#
# Changes:
# 2017-05-05 (rja)
# - initial version

from __future__ import print_function
import re
import fileinput

re_clean_ner = re.compile("\(([A-Z]+) .+?\)")
re_clean_sla = re.compile("\w+/([A-Z]+)")

# read lines from STDIN
def get_lines():
    for line in fileinput.input():
        yield line

# apply a string function to a list of strings
def iter(lines, f):
    for line in lines:
        yield f(line)

# remove newline
def clean_basic(s):
    return s.strip()

# (PERSON John Doe) -> PERSON
def clean_ner(s):
    return re_clean_ner.sub('\\1', s)

# remove ./. and the like at the end
def clean_end(s):
    if s[-3:] in (',/,', './.'):
        return s[:-3]
    return s

# clean everything after "of/IN" or "from/in"
def clean_modifier(s):
    if " of/IN " in s:
        a, sep, b = s.rpartition(" of/IN ")
        sep = "of"
    elif " from/IN " in s:
        a, sep, b = s.rpartition(" from/IN ")
        sep = "from"
    else:
        return s
    # clean b
    return " ".join([a, sep, ] + [re_clean_sla.sub("\\1", token) for token in b.split()])

# ,/, -> ,
def clean_comma(s):
    i = s.find(" ,/,")
    if i < 0:
        return s
    return s[0:i] + s[i+3:]

# a/b -> b
def clean_pos(s):
    return re_clean_sla.sub("\\1", s)

if __name__ == '__main__':
    lines = get_lines()
    lines = iter(lines, clean_basic)
    lines = iter(lines, clean_ner)
    lines = iter(lines, clean_end)
#    lines = iter(lines, clean_modifier)
    lines = iter(lines, clean_comma)
    lines = iter(lines, clean_pos)
    
    for line in lines:
        print(line)

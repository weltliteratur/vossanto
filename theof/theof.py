#!/usr/bin/python -u
# -*- coding: utf-8 -*-

#
# Reads files from the NYT corpus. Supports reading from a TAR archive.
#
# Usage:
#
# Author: rja
#
# Changes:
# 2017-05-10 (rja)
# - added parameter -r to select the regex to use (default: 4)
# - refactored using generators
# 2017-05-09 (rja)
# - extended regex pattern
# 2017-05-08 (rja)
# - initial version copied from nyt.py

from __future__ import print_function
import re
import xml.etree.ElementTree as ET
import tarfile
import argparse
import os
import sys
import codecs
import nltk
from nltk.tokenize import sent_tokenize

version = "0.0.2"

# convert all output into a byte string to be safe when redirecting
# UTF8Writer = codecs.getwriter('utf8')
# sys.stdout = UTF8Writer(sys.stdout)

# remove line breaks and tabs from text
re_ws = re.compile('[\n\t\r]+')
re_theof = {
    # 1: simple match
    1: re.compile("(\\bthe\\s([A-Z][a-z]+\\s+){1,3}of\\b)"),
    # 2: more than three words
    2: re.compile("(\\bthe\\s([A-Z][a-z]+\\s+)+of\\b)"),
    # 3: lower-case characters and at most five words
    3: re.compile("(\\bthe\\s([A-Za-z]+\\s+){1,5}of\\b)"),
    # 4: all unicode characters (+non-greedy)
    4: re.compile("(\\bthe\\s(\\w+\\s+){1,5}?of\\b)", re.UNICODE),
    # 5: all unicode characters and .-,'
    5: re.compile("(\\bthe\\s+([\\w.,'-]+\\s+){1,5}?of\\b)", re.UNICODE)
}

# convert NYT XML to text
def xml2str(f):
    tree = ET.parse(f)
    root = tree.getroot()
    # path to the heading
    heading = root.findall("./body/body.head/")
    head = ""
    for block in heading:
        head = ET.tostring(block, encoding="utf-8", method="text").decode("utf-8")

    # path to the main text block
    content = root.findall("./body/body.content/")
    body = ""
    for block in content:
        if block.attrib["class"] == "full_text":
            # strip XML
            body = body + "\n" + ET.tostring(block, encoding="utf-8", method="text").decode("utf-8")
    return head + "\n\n" + body

# convert a list of XML files into texts
def gen_text(files):
    for f, fname in files:
        yield fname, xml2str(f)

# extract sentences for texts
def gen_sentences(texts):
    for fname, text in texts:
        for sentence in sent_tokenize(text):
            yield fname, sentence

# apply the regex
def gen_regex(texts, regex, groupid=0):
    for fname, text in texts:
        for match in regex.findall(text):
            yield fname, match[groupid], text

# remove control characters
def gen_rm_ctrl(texts):
    for fname, match, sentence in texts:
        yield fname, re_ws.sub(' ', match), re_ws.sub(' ', sentence)

# generate a list of files from various input
def gen_files(path):
    if os.path.splitext(path)[1] == ".xml":
        # XML input: just one file
        yield open(path, "rt"), path
    elif os.path.isdir(path):
        # read all files in the directory
        for fname in os.listdir(path):
            fname = path + "/" + fname
            if os.path.isfile(fname):
                yield open(fname, "rt"), fname
    else:
        # read TAR file
        tar = tarfile.open(path, "r:gz")
        for tarinfo in tar:
            if tarinfo.isreg():
                yield tar.extractfile(tarinfo), tarinfo.name

def print_matches(matches, sep='\t'):
    for fname, match, sentence in matches:
        print(fname, match, sentence, sep=sep)

if __name__ == '__main__':

    parser = argparse.ArgumentParser(description='Find Vossantos in the NYT corpus.', formatter_class=argparse.ArgumentDefaultsHelpFormatter)
    parser.add_argument('input', type=str, help='input TAR/XML file or directory')
    parser.add_argument('-r', '--regex', type=int, help='select regex', default=4)
    parser.add_argument('-v', '--version', action="version", version="%(prog)s " + version)

    args = parser.parse_args()

    files = gen_files(args.input)
    texts = gen_text(files)
    sents = gen_sentences(texts)
    match = gen_regex(sents, re_theof[args.regex])
    match = gen_rm_ctrl(match)
    print_matches(match)

#!/usr/bin/python3 -u
# -*- coding: utf-8 -*-

#
# Reads files from the NYT corpus. Supports reading from a TAR archive.
#
# Usage:
#
# Author: rja
#
# Changes:
# 2018-08-21 (rja)
# - added tokenisation at line endings before sentence tokenisation
# 2018-08-20 (rja)
# - migrated to Python 3
# 2018-02-21 (rja)
# - changed default regex to 5 (as in paper)
# 2017-07-21 (rja)
# - fixed extraction of heading: take complete heading, avoid trailing slash
# 2017-07-19 (rja)
# - added option -c to disable NLTK sentence tokenisation
# - moved control character cleansing before regex application
# - added sys.path fix to avoid loading org.py as a module (by a dependency of tarfile)
# 2017-06-14 (rja)
# - fixed extraction of heading
# 2017-05-10 (rja)
# - added parameter -r to select the regex to use (default: 4)
# - refactored using generators
# 2017-05-09 (rja)
# - extended regex pattern
# 2017-05-08 (rja)
# - initial version copied from nyt.py

import sys
# remove current directory from search path to avoid org.py is loaded
# as a module
sys.path = sys.path[1:]
import re
import xml.etree.ElementTree as ET
import tarfile
import argparse
import os
import codecs
import nltk
from nltk.tokenize import sent_tokenize

version = "0.0.4"

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

# convert NYT XML to text
def xml2str(f):
    tree = ET.parse(f)
    root = tree.getroot()

    # path to the heading
    #
    # ./body/body.head/hedline vs. ./body/body.head/
    # ./body/body.head/ and ./body/body.head/hedline include only the
    # heading itself, not the first introductory sentence which we get
    # with ./body/body.head
    heading = root.findall("./body/body.head")
    head = ""
    for block in heading:
        head += ET.tostring(block, encoding="utf-8", method="text").decode("utf-8")

    # path to the main text block
    content = root.findall("./body/body.content/")
    body = ""
    for block in content:
        if block.attrib["class"] == "full_text":
            # strip XML
            body += "\n" + ET.tostring(block, encoding="utf-8", method="text").decode("utf-8")
    return head + "\n\n" + body

# convert a list of XML files into texts
def gen_text(files):
    for f, fname in files:
        yield fname, xml2str(f)

# remove control characters
def gen_rm_ctrl(texts):
    for cols in texts:
        #yield [re_ws.sub(' ', col) for col in cols]
        res = []
        for col in cols:
            if isinstance(col, int):
                res.append(col)
            else:
                res.append(re_ws.sub(' ', col))
        yield res

# extract sentences for texts
def gen_sentences(texts):
    for fname, text in texts:
        # split at line breaks, since the XML preserved paragraphs
        for line in text.splitlines():
            for sentence in sent_tokenize(line):
                yield fname, sentence

# apply the regex
def gen_regex(texts, regex, groupid=0):
    for fname, text in texts:
        for m in regex.finditer(text):
            # also return the start position of the matches
            yield fname, m.group(groupid), m.start(groupid), text

# limit length of text around match
def gen_limit(texts, chars=sys.maxsize):
    for fname, match, index, text in texts:
        # reduce text to chars characters before and after match
        yield fname, match, index, text[max(0,index-chars):min(index+len(match)+chars,len(text))]

def print_matches(matches, sep='\t'):
    for fname, match, index, text in matches:
        print(fname, match, text, sep=sep)

if __name__ == '__main__':

    parser = argparse.ArgumentParser(description='Find Vossantos in the NYT corpus.', formatter_class=argparse.ArgumentDefaultsHelpFormatter)
    parser.add_argument('input', type=str, help='input TAR/XML file or directory')
    parser.add_argument('-r', '--regex', type=int, metavar="R", help='select regex', default=5)
    parser.add_argument('-s', '--sep', type=str, metavar="S", help='column separator', default='\t')
    parser.add_argument('-c', '--chars', type=int, metavar="C", default=None, help='disable sentence tokenisation and instead print C characters before and after a match')
    parser.add_argument('-v', '--version', action="version", version="%(prog)s " + version)

    args = parser.parse_args()

    files = gen_files(args.input)
    texts = gen_text(files)

    if args.chars is not None:
        # avoid sentence tokenisation using NLTK
        texts = gen_rm_ctrl(texts)
        match = gen_regex(texts, re_theof[args.regex])
        match = gen_limit(match, args.chars)
    else:
        sents = gen_sentences(texts)
        match = gen_regex(sents, re_theof[args.regex])
        match = gen_rm_ctrl(match)
    print_matches(match, args.sep)

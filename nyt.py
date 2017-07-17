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
# 2017-06-27 (rja)
# - added option "--sentence" to print the complete sentence
# 2017-05-08 (rja)
# - added option "--ignore-case" to enable/disable re.IGNORECASE in regex search
# - added option "--group" to specify the regex group to extract
# 2017-05-05 (rja)
# - added option "--pattern" to print the mattern instead of the matched text
# - added option to read all files in a directory
# 2016-06-12 (rja)
# - initial version
# - added "-u" to brint unbuffered output to STDOUT

from __future__ import print_function
import re
import xml.etree.ElementTree as ET
import tarfile
import argparse
import os
import sys
import codecs
import vossanto

version = "0.0.4"

# remove line breaks and tabs from text
re_ws = re.compile('[\n\t\r]+')


# convert all output into a byte string to be safe when redirecting
UTF8Writer = codecs.getwriter('utf8')
sys.stdout = UTF8Writer(sys.stdout)

# convert NYT XML to text
def xml2str(f, fname):
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

def xml2vossanto(f, fname, **kwargs):
    # process contained file
    txt = xml2str(f, fname)
    if txt:
        # find vossanto
        try:
            for v in vossanto.text2vossanto(txt):
                # print vossanto
                if v:
                    parts = [fname] + v[0:3]
                    if kwargs["pattern"]:
                        parts.append(v[3])
                    if kwargs["sentence"]:
                        parts.append(re_ws.sub(' ', v[4]).strip())
                    print('\t'.join(parts))
        except UnicodeDecodeError:
            print(fname, "UnicodeDecodeError")

def xml2regex(f, fname, **kwargs):
    # process contained file
    txt = xml2str(f, fname)
    if txt:
        # find regex
        try:
            for match in kwargs["regex"].findall(txt):
                # print match
                if isinstance(match, tuple):
                    print(fname, match[kwargs["group"]].strip(), sep='\t')
                else:
                    print(fname, match.strip(), sep='\t')
        except UnicodeDecodeError:
            print(fname, "UnicodeDecodeError")


if __name__ == '__main__':

    parser = argparse.ArgumentParser(description='Find Vossantos in the NYT corpus.', formatter_class=argparse.ArgumentDefaultsHelpFormatter)
    parser.add_argument('input', type=str, help='input TAR or XML file or directory with XML files')
    parser.add_argument('-r', '--regex', dest="regex", type=str, help='search for regex and output matches')
    parser.add_argument('-p', '--pattern', action="store_true", help='print pattern')
    parser.add_argument('-s', '--sentence', action="store_true", help='print sentence')
    parser.add_argument('-g', '--group', type=int, default=0, help='regex group to return')
    parser.add_argument('-i', '--ignore-case', action="store_true", help="ignore case")
    parser.add_argument('-v', '--version', action="version", version="%(prog)s " + version)

    args = parser.parse_args()

    if args.regex:
        if args.ignore_case:
            regex = re.compile(args.regex, re.IGNORECASE)
        else:
            regex = re.compile(args.regex)
        sfunc = xml2regex
    else:
        regex = None
        sfunc = xml2vossanto

    if os.path.isfile(args.input) and os.path.splitext(args.input)[1] == ".xml":
        # XML input: just one file
        with open(args.input, "rt") as f:
            sfunc(f, args.input, regex=regex, pattern=args.pattern, group=args.group, sentence=args.sentence)
    elif os.path.isdir(args.input):
        # read all files in the directory
        for fname in os.listdir(args.input):
            fname = args.input + "/" + fname
            if os.path.isfile(fname):
                with open(fname, "rt") as f:
                    sfunc(f, fname, regex=regex, pattern=args.pattern, group=args.group, sentence=args.sentence)
    else:
        # read TAR file
        tar = tarfile.open(args.input, "r:gz")
        for tarinfo in tar:
            if tarinfo.isreg():
                sfunc(tar.extractfile(tarinfo), tarinfo.name, regex=regex, pattern=args.pattern, group=args.group, sentence=args.sentence)

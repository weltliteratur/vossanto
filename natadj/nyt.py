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
# 2017-05-05 (rja)
# - initial version copied from ../nyt.py

from __future__ import print_function
import re
import xml.etree.ElementTree as ET
import tarfile
import argparse
import os
import sys
import codecs
import countries

version = "0.0.1"

# convert all output into a byte string to be safe when redirecting
UTF8Writer = codecs.getwriter('utf8')
sys.stdout = UTF8Writer(sys.stdout)

# remove line breaks and tabs from text
re_ws = re.compile('[\n\t\r]+')

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

def natadj(na, f, fname):
    # process contained file
    txt = xml2str(f, fname)
    if txt:
        # find matches
        try:
            for v in na.match_simple(txt):
                # print match
                if v:
                    print(fname, re_ws.sub(' ', v), sep='\t')
        except UnicodeDecodeError:
            print(fname, "UnicodeDecodeError")

            
if __name__ == '__main__':

    parser = argparse.ArgumentParser(description='Find Vossantos in the NYT corpus.', formatter_class=argparse.ArgumentDefaultsHelpFormatter)
    parser.add_argument('input', type=str, help='input TAR file')
    parser.add_argument('-c', '--countries', type=str, help='list of country adjectives')
    parser.add_argument('-v', '--version', action="version", version="%(prog)s " + version)

    args = parser.parse_args()

    na = countries.NationalAdjectives(args.countries)

    if os.path.splitext(args.input)[1] == ".xml":
        # XML input: just one file
        with open(args.input, "rt") as f:
            natadj(na, f, args.input)
    else:
        # read TAR file
        tar = tarfile.open(args.input, "r:gz")
        for tarinfo in tar:
            if tarinfo.isreg():
                natadj(na, tar.extractfile(tarinfo), tarinfo.name)

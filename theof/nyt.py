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
# 2017-05-12 (rja)
# - initial version copied from theof.py

from __future__ import print_function
import re
import xml.etree.ElementTree as ET
import tarfile
import argparse
import os
import sys
import codecs

version = "0.0.1"

# remove line breaks and tabs from text
re_ws = re.compile('[\n\t\r]+')

# convert NYT XML to text
def gen_parts(files, heading, text, url, category):
    for f, fname in files:
        result = [fname]

        tree = ET.parse(f)
        root = tree.getroot()

        if heading:
            h = ""
            for block in root.findall("./body/body.head/"):
                h = ET.tostring(block, encoding="utf-8", method="text").decode("utf-8")
            result.append(h)

        if text:
            t = ""
            for block in root.findall("./body/body.content/"):
                if block.attrib["class"] == "full_text":
                    # strip XML
                    t = t + "\n" + ET.tostring(block, encoding="utf-8", method="text").decode("utf-8")
            result.append(t)

        if url:
            u = ""
            for tag in root.findall("./head/pubdata/"):
                if tag.attrib["ex-ref"]:
                    u = tag.attrib["ex-ref"]
            result.append(u)

        if category:
            c = ""
            for tag in root.findall("./head/meta"):
                if tag.attrib["name"] == "online_sections":
                    c = tag.attrib["content"]
            result.append(c)
            
        yield result

# apply the regex
def gen_grep(parts, reg):
    regex = re.compile(reg)
    for part in parts:
        # skip filename
        if any([regex.search(part[i]) for i in range(1, len(part))]):
            yield part

# remove control characters
def gen_rm_ctrl(texts):
    for parts in texts:
        yield [re_ws.sub(' ', p).strip() for p in parts]

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

def print_lines(parts, sep='\t'):
    for parts in parts:
        print(sep.join(parts))

if __name__ == '__main__':

    parser = argparse.ArgumentParser(description='Reading the NYT corpus.', formatter_class=argparse.ArgumentDefaultsHelpFormatter)
    parser.add_argument('input', type=str, help='input TAR/XML file or directory')
    parser.add_argument('-t', '--title', action="store_true", help='extract title')
    parser.add_argument('-b', '--body', action="store_true", help='extract body text')
    parser.add_argument('-u', '--url', action="store_true", help='extract URL')
    parser.add_argument('-c', '--category', action="store_true", help='extract category')
    parser.add_argument('-g', '--grep', type=str, metavar="REGEX", help='match regex')
    parser.add_argument('-s', '--separator', type=str, metavar="SEP", help='output column separator', default='\t')
    parser.add_argument('-n', '--normalise-ws', action="store_true", help='normalise whitespace')
    parser.add_argument('-v', '--version', action="version", version="%(prog)s " + version)

    args = parser.parse_args()

    files = gen_files(args.input)
    parts = gen_parts(files, args.title, args.body, args.url, args.category)
    if args.grep:
        parts = gen_grep(parts, args.grep)
    if args.normalise_ws:
        parts = gen_rm_ctrl(parts)
    print_lines(parts, args.separator)

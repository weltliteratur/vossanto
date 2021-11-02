#!/usr/bin/python3 -u
# -*- coding: utf-8 -*-

#
# Reads files from the NYT corpus. Supports reading from a TAR archive.
#
# Usage: nyt.py -h
#
# Changes:
# 2021-11-02 (rja)
# - small code cleanups
# 2018-07-10 (rja)
# - added alternative year extraction
# 2018-05-18 (rja)
# - restricted directory input to XML files
# - fixed URL extraction
# - added date extraction
# 2017-08-17 (rja)
# - made file path handling os independent
# 2017-06-14 (rja)
# - added support to extract desk and (normalised) author information
# - fixed extraction of heading
# 2017-05-12 (rja)
# - initial version copied from theof.py

from __future__ import print_function
import re
import xml.etree.ElementTree as ET
import tarfile
import argparse
import os

version = "0.0.4"

# remove line breaks and tabs from text
re_ws = re.compile('[\n\t\r]+')


# convert NYT XML to text
def gen_parts(files, heading, text, url, category, desk, author, date):
    for f, fname in files:
        result = [fname]

        tree = ET.parse(f)
        root = tree.getroot()

        if heading:
            h = ""
            for block in root.findall("./body/body.head/hedline"):
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
            for tag in root.findall("./head/pubdata"):
                if tag.attrib["ex-ref"]:
                    u = tag.attrib["ex-ref"]
            result.append(u)

        if category:
            c = ""
            for tag in root.findall("./head/meta"):
                if tag.attrib["name"] == "online_sections":
                    c = tag.attrib["content"]
            result.append(c)

        if desk:
            d = ""
            for tag in root.findall("./head/meta"):
                if tag.attrib["name"] == "dsk":
                    d = tag.attrib["content"]
            result.append(d)

        if author:
            a = ""
            for tag in root.findall("./body/body.head/byline"):
                if tag.attrib["class"] == "normalized_byline":
                    a = ET.tostring(tag, encoding="utf-8", method="text").decode("utf-8")
                    # always try to normalise author names
                    a = a.strip().title()
            result.append(a)

        if date:
            y = ""
            m = ""
            d = ""
            for tag in root.findall("./head/meta"):
                if tag.attrib["name"] == "publication_year":
                    y = tag.attrib["content"]
                if tag.attrib["name"] == "publication_month":
                    m = tag.attrib["content"]
                    if len(m) < 2:
                        m = "0" + m
                if tag.attrib["name"] == "publication_day_of_month":
                    d = tag.attrib["content"]
                    if len(d) < 2:
                        d = "0" + d
            ymd = "-".join([y, m, d])
            if len(ymd) == 10:
                result.append(ymd)
            else:
                # sometimes the date is found as <pubdata date.publication="19910121T000000" ...>
                for tag in root.findall("./head/pubdata"):
                    if tag.attrib["date.publication"]:
                        pubdate = tag.attrib["date.publication"]
                        y = pubdate[:4]
                        m = pubdate[4:6]
                        d = pubdate[6:8]
                        ymd = "-".join([y, m, d])
                if len(ymd) == 10:
                    result.append(ymd)
                else:
                    result.append("")

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
def gen_files(paths):
    for path in paths:
        if os.path.splitext(path)[1] == ".xml":
            # XML input: just one file
            yield open(path, "rt"), path
        elif os.path.isdir(path):
            # read all files in the directory
            for fname in os.listdir(path):
                # restrict to XML files
                if os.path.splitext(fname)[1] == ".xml":
                    fname = os.path.join(path, fname)
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
    parser.add_argument('input', type=str, help='input TAR/XML file or directory', nargs='+')
    parser.add_argument('-a', '--author', action="store_true", help='extract author')
    parser.add_argument('-b', '--body', action="store_true", help='extract body text')
    parser.add_argument('-c', '--category', action="store_true", help='extract category')
    parser.add_argument('-d', '--desk', action="store_true", help='extract desk')
    parser.add_argument('-e', '--date', action="store_true", help='extract date')
    parser.add_argument('-t', '--title', action="store_true", help='extract title')
    parser.add_argument('-u', '--url', action="store_true", help='extract URL')
    parser.add_argument('-g', '--grep', type=str, metavar="REGEX", help='match regex')
    parser.add_argument('-s', '--separator', type=str, metavar="SEP", help='output column separator', default='\t')
    parser.add_argument('-n', '--normalise-ws', action="store_true", help='normalise whitespace')
    parser.add_argument('-v', '--version', action="version", version="%(prog)s " + version)

    args = parser.parse_args()

    files = gen_files(args.input)
    parts = gen_parts(files, args.title, args.body, args.url, args.category, args.desk, args.author, args.date)
    if args.grep:
        parts = gen_grep(parts, args.grep)
    if args.normalise_ws:
        parts = gen_rm_ctrl(parts)
    print_lines(parts, args.separator)

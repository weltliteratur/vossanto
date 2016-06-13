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

version = "0.0.1"

# convert all output into a byte string to be safe when redirecting
UTF8Writer = codecs.getwriter('utf8')
sys.stdout = UTF8Writer(sys.stdout)

# convert NYT XML to text
def xml2str(f, fname):
    tree = ET.parse(f)
    root = tree.getroot()
    # path to the main text block
    content = root.findall("./body/body.content/")
    for block in content:
        if block.attrib["class"] == "full_text":
            # strip XML
            return ET.tostring(block, encoding="utf-8", method="text").decode("utf-8")

    return None

def xml2vossanto(f, fname):
    # process contained file
    txt = xml2str(f, fname)
    if txt:
        # find vossanto
        try:
            for v in vossanto.text2vossanto(txt):
                # print vossanto
                if v:
                    print(fname, v[0], v[1], v[2], sep='\t')
        except UnicodeDecodeError:
            print(fname, "UnicodeDecodeError")

if __name__ == '__main__':

    parser = argparse.ArgumentParser(description='Find Vossantos in the NYT corpus.', formatter_class=argparse.ArgumentDefaultsHelpFormatter)
    parser.add_argument('input', type=str, help='input TAR file')
    parser.add_argument('-v', '--version', action="version", version="%(prog)s " + version)

    args = parser.parse_args()

    
    if os.path.splitext(args.input)[1] == ".xml":
        # XML input: just one file
        with open(args.input, "rt") as f:
            xml2vossanto(f, args.input)
    else:
        # read TAR file
        tar = tarfile.open(args.input, "r:gz")
        for tarinfo in tar:
            if tarinfo.isreg():
                xml2vossanto(tar.extractfile(tarinfo), tarinfo.name)
            

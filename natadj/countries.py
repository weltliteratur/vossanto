#!/usr/bin/python
# -*- coding: utf-8 -*-

#
# Detection of national adjectives + person in texts
#
# Usage:
# 
# Author: rja 
#
# Changes:
# 2017-05-05 (rja)
# - initial version 

from __future__ import print_function
import argparse
import codecs
import sys

import nltk
from nltk.corpus import treebank
from nltk.tokenize import wordpunct_tokenize, sent_tokenize, word_tokenize
from nltk.sem.relextract import tree2semi_rel, semi_rel2reldict
from nltk.tree import Tree

version = "0.0.1"

# convert all output into a byte string to be safe when redirecting
UTF8Writer = codecs.getwriter('utf8')
sys.stdout = UTF8Writer(sys.stdout)
sys.stderr = UTF8Writer(sys.stderr)

class NationalAdjectives:

    def __init__(self, f, debug=False):
        self.debug = debug
        self.adjectives = self.read_file(f)
        self.adjectives_lower = {adj.lower(): self.adjectives[adj] for adj in self.adjectives}

    # check for existing entry and if less prominent, replace it
    def add_adjective(self, adjectives, adjective, url, pos):
        if adjective in adjectives:
            if self.debug:
                print(adjective, "for", (url, pos), "clashes with", adjectives[adjective], file=sys.stderr)
            if pos < adjectives[adjective][1]:
                adjectives[adjective] = (url, pos)
                if self.debug:
                    print("  replaced", file=sys.stderr)
        else:
            adjectives[adjective] = (url, pos)

    # read a file of country adjective url tuples into a dictionary
    def read_file(self, f, sep='\t'):
        adjectives = dict()
        with codecs.open(f, "r", "utf-8") as f:
            for line in f:
                country, adjective, url = line.strip().split(sep)
                # We store the position of the adjective such that we can
                # favor more common ones against "2nd choice". The reason
                # is, that there a few cases where two different countries
                # have the same adjective.
                if " " in adjective:
                    # handle different cases
                    if "," in adjective:
                        for i, p in enumerate(adjective.split(',')):
                            self.add_adjective(adjectives, p.strip(), url, i + 1)
                    elif " or " in adjective:
                        for i, p in enumerate(adjective.split(" or ")):
                            self.add_adjective(adjectives, p.strip(), url, i + 1)
                    else:
                        # regular name
                        self.add_adjective(adjectives, adjective, url, 1)
                else:
                    self.add_adjective(adjectives, adjective, url, 1)
        # remove URL positions
        for key in adjectives:
            adjectives[key] = adjectives[key][0]
        return adjectives
    
    # match the string against pattern natadj + person
    def match(self, s, ner=True):
        for sentence in sent_tokenize(s):
            yield self.match_sentence(sentence, ner)
            
    # POS/NER based matching
    def match_sentence(self, s, ner=True):
        words = word_tokenize(s)

        # POS
        tagged = nltk.pos_tag(words)

        # NER
        if ner:
            entities = nltk.chunk.ne_chunk(tagged)
        else:
            entities = tagged

        # prepare for matching
        ttext, taglist, txtlist = self.tags2str(entities)

        return ttext, taglist, txtlist

    # simple text-based matching
    def match_simple(self, s):
        for sentence in sent_tokenize(s):
            if self.match_simple_sentence(sentence):
                yield sentence

    def match_simple_sentence(self, sentence):
        # this is inefficient, for better solutions check
        # https://stackoverflow.com/questions/3260962/
        sentence = sentence.lower()
        return any("the " + adj in sentence for adj in self.adjectives_lower)

    # convert parse tree generated by nltk.chunk.ne_chunk() into a string
    def tags2str(self, tags):
        parts = []
        taglist = []
        txtlist = []
        for tag in tags:
            if isinstance(tag, Tree):
                taglist.append(tag.label())
                txtlist.append(" ".join([t[0] for t in tag.leaves()]))
                parts.append("(" + tag.label() + " " + " ".join([t[0] for t in tag.leaves()]) + ")")
            else:
                taglist.append(tag[1])
                txtlist.append(tag[0])
                parts.append(tag[0] + "/" + tag[1])
        return " ".join(parts), taglist, txtlist

    # test detection using the pattern "the ADJECTIVE <person>"
    def test(self, person, ner):
        cases = dict()
        for adj in na.adjectives:
            # test string
            # s = "He is the " + adj + " " + person + "."
            s = "the " + adj + " " + person
            # match
            t, tagl, txtl = na.match_sentence(s, ner)
            # analyse
            pat = ' '.join(tagl[1:])
            if pat not in cases:
                cases[pat] = (set(), t)
            cases[pat][0].add(t)

        # print table
        for pat in cases:
            print(len(pat.split(' ')), len(cases[pat][0]), pat, cases[pat][1], sep='\t')
            
if __name__ == '__main__':

    parser = argparse.ArgumentParser(description='Test reading of national adjectives', formatter_class=argparse.ArgumentDefaultsHelpFormatter)
    parser.add_argument('input', type=str, help='input TSV file')
    parser.add_argument('-t', '--test', type=str, help='test string')
    parser.add_argument('-n', '--ner', action="store_true", help='enable NER')
    parser.add_argument('-p', '--print', action="store_true", help='print list of adjectives')
    parser.add_argument('-j', '--just-annotate', action="store_true", help='just annotate the input sentence ')
    parser.add_argument('-v', '--version', action="version", version="%(prog)s " + version)

    args = parser.parse_args()

    na = NationalAdjectives(args.input)

    if args.test:
        # print statistics for the test phrase "the ADJECTIVE <args.test>"
        na.test(args.test, args.ner)
    elif args.print:
        # print the list of adjectives
        for adj in na.adjectives:
            print(adj, na.adjectives[adj], sep='\t')
    else:
        # process input from STDIN
        for line in sys.stdin:
            if args.just_annotate:
                # print annotations
                for ttext, taglist, txtlist in na.match(line):
                    print(ttext)
            else:
                # match against the adjective list
                matches = na.match_simple(line)
                if matches:
                    print("\t".join(matches))

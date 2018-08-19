#!/usr/bin/python3
# -*- coding: utf-8 -*-

#
# Reads source-modifier pairs and outputs a graphviz .dot file.
#
# Usage:
# 
# Author: rja 
#
# Changes:
# 2018-08-17 (rja)
# - initial version 

import fileinput
import math
import random
from collections import Counter

def filter_graph(sources, modifiers, edges):
    filtered_sources = dict()
    filtered_modifiers = dict()
    filtered_edges = dict()
    for source, modifier in edges:
        # filter edges
        if sources[source] > 14 and modifiers[modifier] > 0:
            filtered_edges[(source, modifier)] = edges[(source, modifier)]
            filtered_sources[source] = sources[source]
            filtered_modifiers[modifier] = modifiers[modifier]
    return filtered_sources, filtered_modifiers, filtered_edges

def build_graph(input):
    sources = Counter()
    modifiers = Counter()
    edges = Counter()
    for line in input:
        parts = line.strip().split('\t')
        if len(parts) == 2:
            source, modifier = parts
            # count
            sources[source] += 1
            modifiers[modifier] += 1
            # add edge
            edges[(source, modifier)] += 1
    return sources, modifiers, edges

def escape_label(s):
    return s.replace('"', '\\"')

# see https://stackoverflow.com/questions/28999287/generate-random-colors-rgb/28999469
def random_color():
    levels = range(128,256,16)
    return "#" + "".join(["{:02x}".format(random.choice(levels)) for _ in range(3)])

def print_graph(sources, modifiers, edges):
    print("digraph D {")
    # config
    print('  graph [outputorder="edgesfirst",overlap=false,sep="+10,10"];')
    print('  node [fontname="Arial",style=filled];')
    
    # vertices
    vertices = dict()
    vid = 0
    colormap = dict()
    for source in sources:
        vid += 1
        # store vertex
        vertices["s_" + source] = vid
        # store color
        color = random_color()
        colormap[vid] = color
        # attributes
        weight = sources[source]
        fs = max(weight, 10)
        print(vid, '[label="' + escape_label(source) + '",width=' + str(math.log(weight) + 1) + ',fontsize=' + str(fs) + ',color="' + color + '"];')

    for modifier in modifiers:
        vid += 1
        vertices["m_" + modifier] = vid
        weight = modifiers[modifier]
        fs = max(weight, 10)
        print(vid, '[label="' + escape_label(modifier) + '", color="yellow", width=' + str(math.log(weight) + 1) + ',fontsize=' + str(fs) + '];')

    # edges
    for source, modifier in edges:
        sid = vertices["s_" + source]
        mid = vertices["m_" + modifier]
        weight = edges[(source, modifier)]
        print(sid, "->", mid, '[weight=' + str(weight) + ',penwidth=' + str(weight + 1) + ',color="' + colormap[sid] + '"];')

    print("}")
    
if __name__ == '__main__':
    # build graph
    sources, modifiers, edges = build_graph(fileinput.input())
    
    # filter graph
    sources, modifiers, edges = filter_graph(sources, modifiers, edges)
    
    # print graph
    print_graph(sources, modifiers, edges)
            

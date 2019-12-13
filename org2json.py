#!/usr/bin/python3
# -*- coding: utf-8 -*-

#
# Reformat org data into json
#

# Author: msc


from org import gen_candidates, gen_truefalse, gen_filter_sources, gen_rm_ctrl, print_csv
import re
import argparse
import sys
import json


# selects the wanted parts of the VA, saves them into a dict with an id, beginning by 0
def select_parts_dict(parts, syear, sdate, said, sfid, saurl, ssourceId, ssourceLabel, ssourcePhrase, smodifier, stext,
                 swikidata, sstatus, sclassification, sline):
    id=0
    if any([syear, sdate, said, sfid, saurl, ssourceId, ssourceLabel, ssourcePhrase, smodifier, stext, swikidata,
            sstatus, sline]):
        for year, date, aid, fid, aurl, sourceId, sourceLabel, sourcePhrase, modifier, sentence, trueVoss, newVoss, status, line in parts:
            result = {}
            result['id'] = id
            id+=1
            if syear:
                #result.append(year)
                result['year']=year
            if sdate:
                #result.append(date)
                result['date'] = date
            if said:
                #result.append(aid)
                result['aid'] = aid
            if sfid:
                #result.append(fid)
                result['fid'] = fid
            if ssourceId:
                #result.append(sourceId)
                result['sourceId'] = sourceId
            if ssourceLabel:
                #result.append(sourceLabel)
                result['sourceLabel'] = sourceLabel
            if ssourcePhrase:
                #result.append(sourcePhrase)
                result['sourcePhrase'] = sourcePhrase
            if smodifier:
                #result.append(modifier)
                result['modifier'] = modifier
            if stext:
                #result.append(sentence)
                result['sentence'] = sentence
            if swikidata:
                #result.append("[[https://www.wikidata.org/wiki/" + sourceId + "][" + sourceLabel + "]]")
                result['wikidata'] = "[[https://www.wikidata.org/wiki/" + sourceId + "][" + sourceLabel + "]]"
            if saurl:
                #result.append(aurl)
                result['aurl'] = aurl
            if sstatus:
                #result.append(status)
                result['status'] = status
            if sclassification:
                #result.append(trueVoss)
                result['trueVoss'] = ytrueVossear
            if sline:
                #result.append(line.strip())
                result['line'] = line.strip()
            yield result

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Manipulate Vossantos in org files.', formatter_class=argparse.ArgumentDefaultsHelpFormatter)
    parser.add_argument('file', type=argparse.FileType('r', encoding='utf-8'), nargs='?', default=sys.stdin, help='org mode file to process')
    # what shall be printed
    parser.add_argument('-a', '--articleid', action="store_true", help="output article id")
    parser.add_argument('-b', '--status', action="store_true", help="output status of false positives")
    parser.add_argument('-c', '--classification', action="store_true", help="output classification (True/False)")
    parser.add_argument('-d', '--date', action="store_true", help="output date")
    parser.add_argument('-f', '--fileid', action="store_true", help="output file id")
    parser.add_argument('-g', '--original', action="store_true", help="output original line")
    parser.add_argument('-i', '--sourceid', action="store_true", help="output Wikidata source id")
    parser.add_argument('-l', '--sourcelabel', action="store_true", help="output source")
    parser.add_argument('-o', '--modifier', action="store_true", help="output modifier")
    parser.add_argument('-p', '--sourcephrase', action="store_true", help="output source phrase") # as it appears in the text
    parser.add_argument('-t', '--text', action="store_true", help="output text")
    parser.add_argument('-u', '--url', action="store_true", help="output article URL")
    parser.add_argument('-w', '--wikidata', action="store_true", help="output link to Wikidata")
    parser.add_argument('-y', '--year', action="store_true", help="output year")
    # filtering options
    parser.add_argument('-T', '--true', action="store_true", help="output only true Vossantos")
    parser.add_argument('-F', '--false', action="store_true", help="output only false positives")
    parser.add_argument('--ignore-source-ids', type=argparse.FileType('r', encoding='utf-8'), metavar="FILE", help='ignore candidates with a source id contained in FILE')
    # output format options
    parser.add_argument('-n', '--new', type=str, metavar="S", help="string to mark new entries", default='> ')
    parser.add_argument('-C', '--clean', action="store_true", help="clean whitespace")
    parser.add_argument('-H', '--heading', action="store_true", help="print year heading")
    parser.add_argument('-s', '--separator', type=str, metavar="SEP", help="output separator", default='\t')
    # special options
    parser.add_argument('-m', '--merge', type=argparse.FileType('r', encoding='utf-8'), metavar="FILE", help='file to merge')
    parser.add_argument('-U', '--include-urls', type=argparse.FileType('r', encoding='utf-8'), metavar="FILE", help='file with article URLs')
#    parser.add_argument('-v', '--version', action="version", version="%(prog)s " + version)

    args = parser.parse_args()
    parts = gen_candidates(args.file)
    parts = gen_truefalse(parts, args.true, args.false)
    parts = gen_filter_sources(parts, args.ignore_source_ids)
    parts = select_parts_dict(parts, args.year, args.date, args.articleid, args.fileid, args.url, args.sourceid,
                         args.sourcelabel, args.sourcephrase, args.modifier, args.text, args.wikidata, args.status,
                         args.classification, args.original)
    if args.clean:
        parts = gen_rm_ctrl(parts)

    first = False
    # write data into json file
    with open('data.json','w') as f:
        print("[", file=f)
        for p in parts:
            if not first:
                first= True
            else:
                print(',', file=f)
            json.dump(p, f)
        print("]", file=f)
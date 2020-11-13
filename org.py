#!/usr/bin/python3
# -*- coding: utf-8 -*-

#
# Process (extract, filter, merge) Vossantos in an org mode file.
#
# Usage: Without any arguments, extracts all Vossanto canidates from
# the given org file.
#
# Author: rja
#
# Changes:
# 2019-12-18 (rja)
# - added field sourceImageLicense
# 2019-12-16 (rja)
# - added option "--images" to enrich URLs for Wikipedia Commons images
# 2019-12-14 (rja)
# - added help message for --fields
# - renamed field "wikidata" to "sourceUrl"
# - added field aUrlId
# - cleaned up JSON output
# - added options --desks and --authors
# 2019-12-13 (rja)
# - refactored iteration over parts from array to dict
# - changed handling of command line parameters for selecting columns
# - fixed source phrase and modifier extraction
# - added JSON export
# - reorganised help messages
# - added generation of unique id (useful for JSON)
# - re-added original line (as we need it for conversion to markdown using pandoc)
# 2019-12-13 (ms)
# - moved file to parent dir
# - updated sourcephrase and modifier extraction (see extract_sourcephrase / extract_modifier) -> generalization from theof
# - stripped original line that is added to "parts"
# 2019-02-15 (rja)
# - added "-g" option to output original line and "-H" to print year headings
# - bumped version from 0.0.6 to 0.7.0 for semantic versioning
# 2018-10-24 (rja)
# - added option "--ignore-source-ids" to ignore candidates where the
#   source id is contained in the given file
# 2018-10-08 (rja)
# - added option "-c" to output classification (True/False) and renamned
#   existing "-c" to "-C"
# 2018-09-11 (rja)
# - normalising "None" to "" in output
# 2018-08-22 (rja)
# - added extraction of status that explains false positives
# 2018-08-21 (rja)
# - added extraction of source phrase as it appears in the text
# - key uses source phrase instead of source label and ignores modifier markup ('/')
# - key now uses all characters from sentence (not just the first 40)
# 2018-08-16 (rja)
# - added date extraction
# 2018-08-15 (rja)
# - improved modifier extraction
# 2018-08-09 (rja)
# - added option -o to output modifier
# 2018-03-02 (rja)
# - added option -U to include article URLs from file
# - added option -u to extract article URLs
# - annotated line regexp
# 2017-05-17 (rja)
# - simplified file parameters to support reading from STDIN
# 2017-05-14 (rja)
# - added options for selection
# 2017-05-13 (rja)
# - renamed from mergeorg.py and extended for extraction and filtering
# - migrated to Python3
# 2017-05-11 (rja)
# - initial version

import re
import argparse
import sys
import json
from collections import OrderedDict, Counter

version = "0.8.6"

# 1. [[https://www.wikidata.org/wiki/Q83484][Anthony Quinn]] (1987/01/02/0000232) ''I sometimes feel like *the Anthony Quinn of* my set.''
line_re_str = """
^                     # beginning of string
(?P<newmark>> )?      # new candidates are marked with "> "line
(?P<id>[0-9]+)\.      # all candidates are numbered
[ !]+                 # space and/or !
\+?                   # modifier for false positive
\[\[.+/               # start of Wikidata URL
(?P<wdid>[^/]+)       # Wikidata id
\]\[                  # separators
(?P<wdlabel>.+)       # Wikidata label
\]\]                  # end of Wikidata URL
\                     # space
\(                    # beginning of file id
(?P<article>          # beginning of full article part
(\[\[)?               # opening markup for article URL
(?P<aurl>http.+?)?    # article URL
(\]\[)?               # separators for article URL
(?P<fid>              # full file id
(?P<year>\\d{4})      # year
/                     # separator
(?P<month>\\d{2})     # month
/                     # separator
(?P<day>\\d{2})       # day
/                     # separator
(?P<aid>\\d+)         # article id
)                     # end of full file id
(\]\])?               # closing markup for article URL
)                     # end of full article part
\)                    # end of file id
\                     # space
(?P<sentence>.+?[^+]) # sentence
(?P<truefalse>\+)?    # false positive indicator
(\ \(                 # beginning of status token explaining false positives
(?P<status>[WD]+)     # a combination of characters
\))?                  # end of (optional) token
$                     # end of string
"""
re_line = re.compile(line_re_str, re.VERBOSE)

# to extract the modifier (enclosed in /.../) from the sentence
re_modifier = re.compile("\\* ['\"]*/(.+?)/([^0-9A-Za-z]|$)")

# to extract the exact source phrase (enclosed in * ... *) from the sentence
re_sourcephrase = re.compile("\\*\w+ (.+?) \w+\\*")

# to remove markup from the sentences
re_clean = re.compile(r"[*/.\s]")

# remove line breaks and tabs from text
re_ws = re.compile('[\n\t\r]+')

# to extract article URL ids
re_aurlid = re.compile(r'http://query\.nytimes\.com/gst/fullpage\.html\?res=(.+)')

# reads the file into which the other file shall be merged
# all non-vossanto lines are returned in lines,
# all following (vossanto) lines are indexed in index using
# a key generated by match_line
def read_file(flines):
    lines = []
    index = None
    for line in flines:
        # different handling for lines before and after the heading
        if line.startswith("* results"):
            index = dict()
            lines.append(line)
        else:
            if index is not None:
                # index lines after heading "* results"
                parts = match_line(line)
                if parts:
                    year, key = get_key(parts)
                    if year not in index:
                        index[year] = dict()
                    index[year][key] = line
            else:
                # store lines before heading "* results"
                lines.append(line)
    return lines, index

# Read a TSV file with two columns into a dict.
# The first column is used as key and the second column as value.
# Lines starting with # are ignored.
def read_dict(flines, sep='\t', comment='#'):
    d = dict()
    for line in flines:
        if not line.startswith(comment):
            try:
                key, val = line.strip().split(sep, 1)
            except ValueError:
                pass
            else:
                d[key] = val
    return d

def gen_truefalse(candidates, true_positive, false_positive):
    for cand in candidates:
        if true_positive == false_positive or true_positive == cand["classification"] or false_positive != cand["classification"]:
            yield cand

# Enriches the Vossantos with additional information.
# The file should have two columns, the first being the article id, the
# second the data to be added for each Vossanto.
def gen_enrich(parts, key, f, sep='\t', missing=''):
    aid_to_val = read_dict(f, sep=sep)
    for part in parts:
        if part["aId"] in aid_to_val:
            part[key] = aid_to_val[part["aId"]]
        else:
            # always add the key, otherwise CSV columns get messed up
            part[key] = missing
        yield part


# Enriches the Vossantos with image information from Wikimedia commons.
# The file should have three columns, the first being the source id, the
# second the URL to the image page and the third the URL to the image itself.
def gen_enrich_images(parts, f, sep='\t', missing=''):
    images = read_dict(f, sep=sep)
    for part in parts:
        if part["sourceId"] in images:
            # further split value
            page_url, image_url, image_license = images[part["sourceId"]].split(sep)
            # https://commons.wikimedia.org/wiki/File:RodneyDangerfield1978.jpg       https://upload.wikimedia.org/wikipedia/commons/b/bf/RodneyDangerfield1978.jpgx
            # strip off common prefixes
            source_image_id = page_url[len("https://commons.wikimedia.org/wiki/File:"):]
            source_image_thumb = image_url[len("https://upload.wikimedia.org/wikipedia/commons/"):]
        else:
            # always add the key, otherwise CSV columns get messed up
            source_image_id = missing
            source_image_thumb = missing
            image_license = missing
        part["sourceImId"] = source_image_id
        part["sourceImThumb"] = source_image_thumb
        part["sourceImLicense"] = image_license
        yield part
        
# Skip all candidates whose source's id is contained in sourcefile.
# Sourcefile must contain one Wikidata id per line, followed by their name.
# Lines starting with # are ignored.
def gen_filter_sources(candidates, sourcefile):
    if sourcefile:
        sources = read_dict(sourcefile)
        for cand in candidates:
            if cand["sourceId"] not in sources:
                yield cand
    else:
        for cand in candidates:
            yield cand

def gen_candidates(lines):
    for line in lines:
        parts = match_line(line)
        if parts:
            yield parts

# remove control characters
def gen_rm_ctrl(parts):
    for part in parts:
        yield [re_ws.sub(' ', part[p]).strip() for p in part]

# generates a key for a Vossanto
def get_key(parts):
    return parts["year"], "|".join([parts["year"], parts["aId"], parts["sourcePhrase"], re_clean.sub('', parts["sentence"])])

def select_parts(parts, fields):
    if len(fields) > 0 and not "ALL" in fields:
        ids = Counter()
        for part in parts:
            result = OrderedDict()

            for key in fields:
                if key in part:
                    result[key] = part[key]
                elif key == "id":
                    # generate (hopefully unique) id
                    result["id"] = part["aId"] + "_" + str(ids[part["aId"]])
                    ids[part["aId"]] += 1
            yield result
    else:
        # when nothing has been selected, return everything
        for part in parts:
            yield part

# checks if the line is a Vossanto line
def match_line(line):
    # detect the Vossanto lines
    match = re_line.match(line.strip())
    if match:
        d = match.groupdict()

        # prepare some values
        trueVoss = d["truefalse"] != "+"
        sourcePhrase = extract_sourcephrase(d["sentence"], trueVoss)
        modifier = extract_modifier(d["sentence"], trueVoss)
        return {
            "year"           : d["year"],
            "date"           : d["year"] + "-" + d["month"] + "-" + d["day"],
            "aId"            : d["aid"],
            "fId"            : d["fid"],
            "sourceId"       : d["wdid"],
            "sourceLabel"    : d["wdlabel"],
            "sourcePhrase"   : sourcePhrase,
            "sourceUrl"      : "[[https://www.wikidata.org/wiki/" + d["wdid"] + "][" + d["wdlabel"] + "]]",
            "modifier"       : modifier,
            "text"           : d["sentence"],
            "aUrl"           : d["aurl"],
            "aUrlId"         : get_article_url_id(d["aurl"]),
            "classification" : trueVoss,
            "line"           : line.strip(),
            "newVoss"        : d["newmark"], # FIXME: where is this used?
            "status"         : d["status"] # FIXME: where is this used?
        }

    return None

# extract the modifier (enclosed in /.../) from the sentence
def extract_modifier(sentence, trueVoss):
    # ignore non-Vossantos
    if trueVoss:
        match = re_modifier.search(sentence)
        if match:
            return match.group(1)
    return ""

# extract the source phrase (enclosed in *the ... of*) from the sentence
def extract_sourcephrase(sentence, trueVoss):
    if trueVoss:
        match = re_sourcephrase.search(sentence)
        if match:
            return match.group(1)
    return ""

# check whether article URL is normalised ("http://query.nytimes.com/gst/fullpage.html?res=<HEXSTRING>")
# and if so, returns HEXSTRING
def get_article_url_id(aurl):
    match = re_aurlid.match(aurl)
    if match:
        return match.group(1)
    return None

# given a line, either adds the URL for the article or (if already existent), changes it
def set_article_url(line, urls):
    # detect Vossanto line
    match = re_line.match(line.strip())
    if match:
        d = match.groupdict()
        fid = d["fid"]
        if fid not in urls:
            print("WARN: URL for", fid, "not found", file=sys.stderr)
        else:
            url = urls[fid]
            # implement
            article = d["article"]
            return line.replace(article, "[[" + url + "][" + fid + "]]")
    else:
        print("WARN: line did not match", line[:50], file=sys.stderr)

# inserts a vossanto line into the index
def insert(index, line, string_new = '> '):
    # extract key for this line
    parts = match_line(line)
    if not parts:
        # print warning only if not a year heading
        if not re.match("^\*{2,3} [0-9]{4}$", line.strip()):
            print("WARN: line did not match", line[:50], file=sys.stderr)
        return
    # add new Vossanto
    year, key = get_key(parts)
    if key not in index[year]:
        index[year][key] = string_new + line

# convert value to string, taking care of None
def part_to_string(p):
    if p is None:
        return ""
    return str(p)

# print CSV/TSV lines
def print_csv(parts, sep):
    for part in parts:
        print(sep.join([part_to_string(part[p]) for p in part]))

# print JSON lines
def print_json(parts):
    print("[")
    first = True
    for part in parts:
        if first:
            first = False
        else:
            print(",")
        # FIXME: ignore keys with empty values
        print(json.dumps(part), end='')
    print("\n]")

# prints heading for each year
# must be called before select_parts, such that year information is available
# works by interleaving printing with the iteration through yield
def print_heading(parts):
    # to detect changing years (to print a heading)
    prev_year = None
    for part in parts:
        year = part["year"]
        if year != prev_year:
            print("\n**", year)
        prev_year = year
        # this enables us print the heading between the final print statements
        yield part

def parse_fields(s):
    return s.split(",")

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Manipulate Vossantos in and extracts them from org files.')
    parser.add_argument('file', type=argparse.FileType('r', encoding='utf-8'), nargs='?', default=sys.stdin, help='org mode file to process (default: STDIN)')

    # filtering options
    filtering = parser.add_argument_group('filter arguments')
    filtering.add_argument('-T', '--true', action="store_true", help="output only true Vossantos")
    filtering.add_argument('-F', '--false', action="store_true", help="output only false positives")
    filtering.add_argument('--ignore-source-ids', type=argparse.FileType('r', encoding='utf-8'), metavar="FILE", help='ignore candidates with a source id contained in FILE')
    # output format options
    output = parser.add_argument_group('output arguments')
    output.add_argument('-f', '--fields', type=parse_fields, metavar="FDS", default="ALL", help="fields to be included (default: '%(default)s')")
    parser.add_argument('-l', '--list-fields', action="store_true", help="list available fields for --fields")
    output.add_argument('-o', '--output', type=str, metavar="FMT", help="output format (default: '%(default)s')", default="csv", choices=["csv", "json"])
    output.add_argument('-s', '--sep', type=str, metavar="SEP", help="output separator for csv (default: '\\t')", default='\t')
    output.add_argument('-n', '--new', type=str, metavar="NEW", help="string to mark new entries (default: '%(default)s')", default='> ')
    output.add_argument('-c', '--clean', action="store_true", help="clean whitespace")
    output.add_argument('-H', '--heading', action="store_true", help="print year heading (only csv)")

    enrich = parser.add_argument_group('enrichment arguments', "Expect TSV files with article (or source) id in first column.")
    enrich.add_argument('-u', '--urls', type=argparse.FileType('r', encoding='utf-8'), metavar="F", help='add article URLs (prints org file!)')
    enrich.add_argument('-a', '--authors', type=argparse.FileType('r', encoding='utf-8'), metavar="F", help='add article authors')
    enrich.add_argument('-i', '--images', type=argparse.FileType('r', encoding='utf-8'), metavar="F", help='add source images')
    enrich.add_argument('-d', '--desks', type=argparse.FileType('r', encoding='utf-8'), metavar="F", help='add article desks')

    # special options
    special = parser.add_argument_group('special arguments')
    special.add_argument('-m', '--merge', type=argparse.FileType('r', encoding='utf-8'), metavar="F", help='file to merge')
    special.add_argument('-v', '--version', action="version", version="%(prog)s " + version)

    args = parser.parse_args()

    if args.merge:
        # read file into which the other file shall be merged
        lines, index = read_file(args.file)

        # read new file and insert Vossantos
        for line in args.merge:
            insert(index, line, args.new)
        # print first (unchanged) part of original file
        for line in lines:
            print(line, end='')

        # print Vossanto lines
        for year in sorted(index):
            print()
            print("**", year)
            for line in sorted(index[year]):
                print(index[year][line], end='')
    elif args.urls:
        # read URL file
        urls = read_dict(args.include_urls)
        # read file
        lines, index = read_file(args.file)
        # print first (unchanged) part of original file
        for line in lines:
            print(line, end='')
        # print Vossanto lines
        for year in sorted(index):
            print()
            print("**", year)
            for line in sorted(index[year]):
                # add URL to line
                print(set_article_url(index[year][line], urls), end='')
    elif args.list_fields:
        print("""
The following values are allowed for the --fields (-f) option:
  aId             article id in the Sandhaus corpus
  aUrl            article URL
  aUrlId          article id in the URL (for "fullpage.html" URLs only)
  author          author (requires --author)
  classification  'True' for true Vossantos, 'False' otherwise
  date            date in format YYYY-MM-DD
  desk            desk (requires --desk)
  fId             file id in the
  id              unique id (generated using the article id)
  line            original line from the input file
  modifier        modifier
  sourceId        Wikidata id of the source
  sourceLabel     Wikidata label of the source
  sourcePhrase    name of the source as it appears in the text
  sourceUrl       Wikidata URL of the source
  sourceImId      Wikimedia Commons id for source image (requires --images)
  sourceImThumb   Wikimedia Commons thumbnail path for source image (requires --images)
  sourceImLicense Wikimedia Commons license for image (requires --images)
  text            text (typically a sentence) containing the Vossanto
  year            publication year of the article

Several fields can be concatenated by ",", their order is taken into
account.

Special/obsolete keywords:
  ALL             print all available fields
  newVoss         whether the Vossanto has been marked as new
  status          additional information (D=duplicate, W=wrong detected)
""")
    else:
        # default: extract and print Vossantos
        parts = gen_candidates(args.file)
        parts = gen_truefalse(parts, args.true, args.false)
        parts = gen_filter_sources(parts, args.ignore_source_ids)
        if args.authors:
            parts = gen_enrich(parts, "author", args.authors)
        if args.desks:
            parts = gen_enrich(parts, "desk", args.desks)
        if args.images:
            parts = gen_enrich_images(parts, args.images)
        if args.heading:
            # interleaving the headings works by yielding the parts in a loop
            parts = print_heading(parts)
        parts = select_parts(parts, args.fields)
        if args.clean:
            parts = gen_rm_ctrl(parts)
        if args.output == "json":
            print_json(parts)
        else:
            print_csv(parts, args.sep)

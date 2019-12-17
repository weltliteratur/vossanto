#!/usr/bin/python
from __future__ import absolute_import, division, unicode_literals

import pywikibot

from urllib.request import unquote
from pywikibot import pagegenerators, textlib
from pywikibot.tools import deprecated
from pywikibot.site import DataSite, APISite
from pywikibot import pagegenerators as pg, textlib
import json
from pywikibot.exceptions import NoPage
timelineJSON = "../vossanto/timeline/vossantos.json"
with open(timelineJSON) as f:
    vossantoList = f.readlines()
    vossantoDicts = []
    for line in vossantoList[1:-2]:
        d = json.loads(line.rstrip()[0:-1])
        vossantoDicts.append(d)

sourceidListFromJson = list(set([d["sourceId"] for d in vossantoDicts]))
print(sourceidListFromJson.__len__())
#sourceidListFromJson  = ["Q18218128","Q5443"]

#sourceidList = ["Q9458","Q2685","Q5443","Q162629","Q235262","Q49481","Q381178","Q327071","Q25340127"]

#common_links = ["https://commons.wikimedia.org/wiki/File:Michael_Jordan.jpg",
#                "https://commons.wikimedia.org/wiki/File:Busterkeaton_edit.jpg",
#                "https://commons.wikimedia.org/wiki/File:Goethe_(Stieler_1828).jpg"
#                ]

wikidatapage = pywikibot.page.SiteLink('Q467658', DataSite("wikidata", "wikidata"))

wikidata_id_no_pic = []

import requests
def extract_image_license(image_name):

    start_of_end_point_str = 'https://commons.wikimedia.org' \
                         '/w/api.php?action=query&titles=File:'
    end_of_end_point_str = '&prop=imageinfo&iiprop=user' \
                       '|userid|canonicaltitle|url|extmetadata&format=json'
    result = requests.get(start_of_end_point_str + image_name+end_of_end_point_str)
    result = result.json()
    page_id = next(iter(result['query']['pages']))
    image_info = result['query']['pages'][page_id]['imageinfo']

    return image_info

def getCommon_Link(sourceId):
    site = pywikibot.Site("wikidata", "wikidata")
    repo = site.data_repository()
    item = pywikibot.ItemPage(repo, sourceId)
    t = item.get()
    imageprop = 'P18'
    if item.claims.keys().__contains__('P18'):
        source = item.claims[imageprop]
        s = source[0]
        commonSite = s.target
        common_url = "https://commons.wikimedia.org/wiki/" + commonSite.urlname()
        return unquote(common_url)
    else:
        wikidata_id_no_pic.append(sourceId)
        common_url = "https://www.wikidata.org/wiki/" + sourceId
        return common_url


def create_thumbnail_url(common_url):
    image_width_px = 180
    title = unquote(common_url).split(":")[-1]
    page = pywikibot.Page(pywikibot.Site(url=common_url),title=title)
    imagepage = pywikibot.FilePage(page.site, page.title())
    image_url_fitted = imagepage.get_file_url(image_width_px)
    return image_url_fitted


def getComment(common_url):
    #title = unquote(common_url).split(":")[-1]
    title = common_url.split(":")[-1]
    page = pywikibot.Page(pywikibot.Site(url=common_url), title=title)
    imagepage = pywikibot.FilePage(page.site, page.title())
    comment = imagepage.latest_file_info['comment']
    return comment


common_urls = []
thumbnail_urls = []
no_image_urls = []
no_data_sourceid = []
unknown_error_url = []
valid_source_id = []
permissions = []

for i,sourceId in list(enumerate(sourceidListFromJson)):
    try:
        common_url = getCommon_Link(sourceId)
    except:
        no_data_sourceid.append(sourceId)
        print("Bad sourceId: No information at https://www.wikidata.org/wiki/" + sourceId)
        continue
    if common_url.startswith("https://www.wikidata.org/wiki/"):
        no_image_urls.append("https://www.wikidata.org/wiki/" + sourceId)
        continue
    else:
        try:
            valid_source_id.append(sourceId)
            thumbnail_url = create_thumbnail_url(common_url)
            image_title = common_url.split("File:")[-1]
            image_info = extract_image_license(image_title)
            permissions.append(image_info[0]['extmetadata']['License']['value'])
            common_urls.append(common_url)
            thumbnail_urls.append(thumbnail_url)
            print(str(i), sourceId, common_url)
        except:
            unknown_error_url.append(common_url)
            continue

image_urls = ["\t".join(e) + "\n" for e in zip(valid_source_id,common_urls,thumbnail_urls,permissions)]
no_image_urls = "\n".join(no_image_urls)
no_data_sourceid="\n".join(no_data_sourceid)
unknown_error_url="\n".join(unknown_error_url)

with open("image_urls.tsv","w") as im:
    im.writelines(image_urls)

with open("no_image_urls.tsv","w") as nim:
    nim.writelines(no_image_urls)

with open("no_data_sourceId.tsv","w") as nds:
    nds.writelines(no_data_sourceid)

with open("unknown_error_urls.tsv","w") as ueu:
    ueu.writelines(unknown_error_url)

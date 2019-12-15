#!/usr/bin/python
from __future__ import absolute_import, division, unicode_literals

import pywikibot

from urllib.request import unquote
from pywikibot import pagegenerators, textlib
from pywikibot.tools import deprecated
from pywikibot.site import DataSite, APISite
from pywikibot import pagegenerators as pg, textlib

sourceidList = ["Q9458","Q2685","Q5443","Q162629","Q235262","Q49481","Q381178","Q327071","Q25340127"]

common_links = ["https://commons.wikimedia.org/wiki/File:Michael_Jordan.jpg",
                "https://commons.wikimedia.org/wiki/File:Busterkeaton_edit.jpg",
                "https://commons.wikimedia.org/wiki/File:Goethe_(Stieler_1828).jpg"
                ]

wikidatapage = pywikibot.page.SiteLink('Q467658', DataSite("wikidata", "wikidata"))

wikidata_id_no_pic = []

def getCommon_Link(wikidata_id):
    site = pywikibot.Site("wikidata", "wikidata")
    repo = site.data_repository()
    item = pywikibot.ItemPage(repo, wikidata_id)
    t = item.get()
    imageprop = 'P18'
    if item.claims.keys().__contains__('P18'):
        source = item.claims[imageprop]
        s = source[0]
        commonSite = s.target
        common_url = "https://commons.wikimedia.org/wiki/" + commonSite.urlname()
        return common_url
    else:
        wikidata_id_no_pic.append(wikidata_id)
        common_url = "noImage"
        return common_url


def create_thumbnail_url(common_url):
    image_width_px = 240
    title = unquote(common_url).split(":")[-1]
    page = pywikibot.Page(pywikibot.Site(url=common_url),title=title)
    imagepage = pywikibot.FilePage(page.site, page.title())
    image_url_fitted = imagepage.get_file_url(image_width_px)
    return image_url_fitted


def getComment(common_url):
    title = unquote(common_url).split(":")[-1]
    page = pywikibot.Page(pywikibot.Site(url=common_url), title=title)
    imagepage = pywikibot.FilePage(page.site, page.title())
    comment = imagepage.latest_file_info['comment']
    return comment


common_urls = []
thumbnail_urls = []
for wikidataid in sourceidList:
    common_url = getCommon_Link(wikidataid)
    if common_url == "noImage":
        break
    else:
        pass
    thumbnail_url = create_thumbnail_url(common_url)
    common_urls.append(common_url)
    thumbnail_urls.append(thumbnail_url)
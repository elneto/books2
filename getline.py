# -*- coding: utf-8 -*-
#! /usr/local/bin/python
# Este script toma una lista de libros y autores en un archivo csv
# y genera un archivo con la url correspondiente en goodreads
__author__ = "Ernesto Araiza"
__version__ = "0.1"
__email__ = "ernesto.araiza@gmail.com"
__status__ = "Development"

import argparse
import urllib2
from bs4 import BeautifulSoup

parser = argparse.ArgumentParser()
parser.add_argument("url", help="url to crawl")
args = parser.parse_args()

sopa = BeautifulSoup(urllib2.urlopen(args.url).read())
title = sopa.find("h1", {"id": "bookTitle"}).get_text().strip()
author = sopa.find("a", {"class": "authorName"}).span.get_text()
img = sopa.find("img", {"id": "coverImage"})['src']
rating = sopa.find("span", {"itemprop": "ratingValue"}).get_text()
ratings = sopa.find("span", {"itemprop": "ratingCount"})['title']
parts_url = args.url.split('/')
part_url = parts_url[len(parts_url)-1]
pages = sopa.find("span", {"itemprop": "numberOfPages"}).get_text()[:-6]

print title+','+author+','+rating+','+ratings+','+part_url+','+img+','+pages+','


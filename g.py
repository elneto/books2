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
import subprocess

def comillas(string):
	if string.find(',') != -1:
		return '"'+string+'"'
	else:
		return string

def setClipboardData(data):
	p = subprocess.Popen(['pbcopy'], stdin=subprocess.PIPE)
	p.stdin.write(data)
	p.stdin.close()
	retcode = p.wait()

parser = argparse.ArgumentParser()
parser.add_argument("url", help="url to crawl")
args = parser.parse_args()

sopa = BeautifulSoup(urllib2.urlopen(args.url).read())
title = sopa.find("h1", {"id": "bookTitle"}).get_text().strip()
title = comillas(title)
author = sopa.find("a", {"class": "authorName"}).span.get_text()
author = comillas(author)
img = sopa.find("img", {"id": "coverImage"})
if img is not None:
	img = img['src']
else:
	img = 'img/nopic.png'
rating = sopa.find("span", {"itemprop": "ratingValue"}).get_text()
ratings = sopa.find("span", {"itemprop": "ratingCount"})['title']
ratings = comillas(ratings)
parts_url = args.url.split('/')
part_url = parts_url[len(parts_url)-1]
pages = sopa.find("span", {"itemprop": "numberOfPages"})
if pages is not None:
	pages = pages.get_text()[:-6]
else:
	pages = "0"

line = title+','+author+','+rating+','+ratings+','+part_url+','+img+','+pages+','

print line.encode('utf-8')
setClipboardData(line.encode('utf-8'))


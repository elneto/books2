# -*- coding: utf-8 -*-
#! /usr/local/bin/python
# Este script toma una lista de libros y autores en un archivo csv
# y genera un archivo con la url correspondiente en goodreads
__author__ = "Ernesto Araiza"
__version__ = "0.1"
__email__ = "ernesto.araiza@gmail.com"
__status__ = "Development"

import csv
import argparse
import urllib2
from bs4 import BeautifulSoup

parser = argparse.ArgumentParser()
parser.add_argument("csvfile", help="El archivo csv")
args = parser.parse_args()

class GRReader:

		def __init__(self, csvfile):
			self.linereader = csv.DictReader(open(csvfile, 'rU'))

		def lee(self):
			for row in self.linereader:
				print row

		def busca(self):
			for row in self.linereader:
				base = 'https://www.goodreads.com/search?utf8=✓&q='
				title = row['title'].strip()
				title = title.replace(' ', '+')
				end = '&search_type=books&search%5Bfield%5D=title'
				url = base+title+end
				soup = BeautifulSoup(urllib2.urlopen(url).read())
				href = ""
				good_title = ""
				good_author = ""
				booklista = soup.findAll('a',{ "class" : "bookTitle" })
				for tag in booklista:
					href = tag['href'] 
					good_title = tag.span.get_text()
					#print good_title
					author_tag = tag.next_sibling.next_sibling.next_sibling.next_sibling.next_sibling.next_sibling
					good_author = author_tag.span.get_text()
					#print '**** Author' + ' ' + row['author'] + ' vs ' + good_author
					#print good_author
					if (row['author'].strip() in good_author):
						break
				print good_title + ' by ' + good_author + ' ' + href

gr = GRReader(args.csvfile)
#gr.lee()
gr.busca()
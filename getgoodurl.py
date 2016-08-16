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
			csvfile_write  = open('output.csv', 'wb')
			self.linewriter = csv.writer(csvfile_write, delimiter=',')
			self.linewriter.writerow(['id', 'title', 'author', 'avg_rating', 'ratings', 'url', 'img', 'pages', 'year'])

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
				avg_rating = ""
				ratings = ""

				booklista = soup.findAll('a',{ "class" : "bookTitle" })
				for tag in booklista:
					href = tag['href'][0:-17]
					good_title = tag.span.get_text()
					author_tag = tag.next_sibling.next_sibling.next_sibling.next_sibling.next_sibling.next_sibling
					good_author = author_tag.span.get_text()
					minirating = author_tag.next_sibling.next_sibling.next_sibling.next_sibling.span.get_text().strip()
					minirating_list = minirating.split(u' — ')
					avg_rating = minirating_list[0][0:-11]
					ratings = minirating_list[1][0:-8]
					if (row['author'].strip() in good_author):
						break

				url2 = 'https://www.goodreads.com' + href
				#print 'Visiting... ' + url2
				soup2 = BeautifulSoup(urllib2.urlopen(url2).read())
				img = soup2.find("img", {"id": "coverImage"})['src']
				pages = soup2.find("span", {"itemprop": "numberOfPages"}).get_text()[0:-6]

				self.linewriter.writerow([row['id'], good_title, good_author, avg_rating, ratings, href, img, pages, row['year']])
				print row['id'] + ' ' + good_title + ' by ' + good_author + ' ' + avg_rating + ' ' + ratings + ' ' +href + ' '+ img + ' ' + pages

gr = GRReader(args.csvfile)
#gr.lee()
gr.busca()
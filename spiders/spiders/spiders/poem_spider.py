# -*- coding:utf-8 -*- ''
# @author:zeng
# 
import scrapy
import os,sys
import re
from bs4 import BeautifulSoup
from spiders.items import PoemSpidersItem

class PoemSpider(scrapy.Spider):
	name = 'poem'
	#allowed_domains = ["poem.org"]
	start_urls = ["http://www.shicimingju.com"]

	def parse(self, response):
		soup = BeautifulSoup(response.body_as_unicode(),"lxml")
		dynasties = soup.find_all(class_="left_mark")[0].find_all('a')
		for dynasty in dynasties:
			url = dynasty.get('href')
			if 'http' not in url:
				url = 'http://www.shicimingju.com' + url
			yield scrapy.Request(url,callback=self.parse_dynasty)

	def parse_dynasty(self, response):
		soup = BeautifulSoup(response.body_as_unicode(),"lxml")
		poets = soup.find(class_="shirenlist").find_all('a')
		for poet in poets:
			url = poet.get('href')
			if 'http' not in url:
				url = 'http://www.shicimingju.com' + url
			yield scrapy.Request(url,callback=self.parse_poet)

		nextPage = soup.find(class_='pagenavi')
		if nextPage and len(nextPage.find_all('a')):
			nextPages = nextPage.find_all('a')
			nextUrl = nextPages[len(nextPages) - 1]
			if nextUrl.getText() == u'下一页':
				url = nextUrl.get('href')
				if 'http' not in url:
					url = 'http://www.shicimingju.com' + url
				yield scrapy.Request(url,callback=self.parse_dynasty)


	def parse_poet(self, response):
		soup = BeautifulSoup(response.body_as_unicode(),"lxml")
		poetries = soup.find(class_="shicilist").find_all('ul')
		for poetry in poetries:
			url = poetry.find_all('a')[0].get('href')
			if 'http' not in url:
				url = 'http://www.shicimingju.com' + url
			yield scrapy.Request(url,callback=self.parse_poem)

		nextPage = soup.find(class_='pagenavi')
		if nextPage and len(nextPage.find_all('a')):
			nextPages = nextPage.find_all('a')
			nextUrl = nextPages[len(nextPages) - 1]
			if nextUrl.getText() == u'下一页':
				url = nextUrl.get('href')
				if 'http' not in url:
					url = 'http://www.shicimingju.com' + url
				yield scrapy.Request(url,callback=self.parse_poet)

	def parse_poem(self, response):
		soup = BeautifulSoup(response.body_as_unicode(),"lxml")
		main = soup.find(id='middlediv')	
		jjzz = main.find(class_='jjzz').find_all('a')
		category = main.find(class_='listscmk')
		if category:
			categories = category.find_all('a')
			category = u''
			for cate in categories:
				category = category + cate.getText() + '_'
		else:
			category = u''
		content = main.find(class_='shicineirong')
		shangxi = main.find(class_='shangxi')
		if shangxi and shangxi.find('h3').getText() == u'作品赏析':
			shangxi = shangxi.getText().strip().replace('\xc2\xa0','')[4:-96]
		else:
			shangxi = u''

		item = PoemSpidersItem()
		item['name'] = main.find('h2').getText()[1:-1]
		item['dynasty'] = jjzz[0].getText()
		item['poet'] = jjzz[1].getText()
		item['category'] = category
		item['content'] = content.getText()
		item['shangxi'] = shangxi
		return item
		

		

		
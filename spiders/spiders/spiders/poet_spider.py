# -*- coding:utf-8 -*- 
import scrapy
import os,sys
import re
from bs4 import BeautifulSoup
# from spiders.items import PoetSpidersItem
f = open('E:\qihao\data\poetList.txt','w')
class PoetSpider(scrapy.Spider):
	name = 'poet'
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
			poetName = poet.getText().split('(')[0];
			f.write(poetName + '\n');

		nextPage = soup.find(class_='pagenavi')
		if nextPage and len(nextPage.find_all('a')):
			nextPages = nextPage.find_all('a')
			nextUrl = nextPages[len(nextPages) - 1]
			if nextUrl.getText() == u'下一页':
				url = nextUrl.get('href')
				if 'http' not in url:
					url = 'http://www.shicimingju.com' + url
				yield scrapy.Request(url,callback=self.parse_dynasty)
		

		

		
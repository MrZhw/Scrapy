# -*- coding:utf-8 -*-
import os,sys
import re
import scrapy
from bs4 import BeautifulSoup
import urllib
import string
reload(sys)
sys.setdefaultencoding('utf-8')
from spiders.items import ChengyuSpidersItem
class ChengyuSpider(scrapy.Spider):
	
	#name = "chengyu"
	start_urls = []
	for word in string.uppercase:
		start_urls.append('http://chengyu.t086.com/list/' + word + '_1.html')

	def parse(self, response):
		soup = BeautifulSoup(response.body_as_unicode(),"lxml")
		found = soup.find(class_='listw')
		words = found.find_all('a')
		for word in words:			
			url = "http://chengyu.t086.com" + word.get('href')
			print 'url = ', url, 'type = ', type(url)
			yield scrapy.Request(url,callback=self.parse_url)

		nextPage = soup.find(class_='mainbar3').find_all('a')
		nextUrl = nextPage[len(nextPage) - 1]
		if nextUrl.getText() == u'下一页':
			url = 'http://chengyu.t086.com/list/' + nextUrl.get('href')
			print 'url = ', url, 'type = ', type(url)
			yield scrapy.Request(url,callback=self.parse)


	def parse_url(self, response):
		soup = BeautifulSoup(response.body_as_unicode(),"lxml")
		card = soup.find(id='main')
		trs = card.find_all('tr')
		#print trs[0].find_all('td')[0].getText(), trs[0].find_all('td')[1].getText()
		item = ChengyuSpidersItem()
		item['lemma'] = trs[0].find_all('td')[1].getText()
		item['pronunciation'] = trs[1].find_all('td')[1].getText()
		item['semantic'] = trs[2].find_all('td')[1].getText()
		item['derivation'] = trs[3].find_all('td')[1].getText()
		item['example'] = trs[4].find_all('td')[1].getText()
		return item
# -*- coding:utf-8 -*-
import os,sys
import re
import scrapy
from bs4 import BeautifulSoup
from spiders.items import PoemSpidersItem

class TestSpider(scrapy.Spider):
	name = "test"

	start_urls = [
		"http://www.shicimingju.com/chaxun/list/20697.html"
	]
	def parse(self, response):
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

		# print 'title = ', main.find('h2').getText()[1:-1]
		# print 'dynasty = ', jjzz[0].getText()
		# print 'poet = ', jjzz[1].getText()
		# print 'category = ', category
		# print 'content = ', content.getText()
		# print 'shangxi = ', shangxi.getText()[:-97]
		



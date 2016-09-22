# -*- coding:utf-8 -*-
import os,sys
import re
import scrapy
from bs4 import BeautifulSoup
import urllib

domain = 'http://www.xiangsheng.org/'
download = u'E:/qihao/data/comic/相声文本/'
filename_withouts = [u'?', u'/', u'\\', u'"', u'<', u'>', u':', u'*', u'|']
class YuerSpider(scrapy.Spider):
	name = "crossTalk_text"
	#allowed_domains = ["dmoz.org"]
	
	start_urls = ["http://www.xiangsheng.org/portal.php?mod=list&catid=59"]
	def parse(self, response):
		soup = BeautifulSoup(response.body_as_unicode(),"lxml")
		founds = soup.find(class_='xld').find_all('dt')
		for found in founds[1:]:
			url = domain + found.find('a').get('href')
			#print url
			yield scrapy.Request(url,callback=self.parse_crossTalk)

		pageNav = soup.find(class_='nxt')
		if pageNav:
			url = pageNav.get('href')
			yield scrapy.Request(url,callback=self.parse)

	def parse_crossTalk(self, response):
		soup = BeautifulSoup(response.body_as_unicode(),"lxml")
		cnt = soup.find(id='article_content')
		title = soup.find('h1').getText().replace('\xc2\xa0','').replace('\n','').strip()
		author = soup.find(class_='h hm').find_all(class_='xg1')[0].getText()
		author = author.split(u'：')[1]
		#print title
		for filename_con in filename_withouts:
			if filename_con in title:
				title = title.replace(filename_con, '')
		if cnt.getText():
			f = open(download + title + '_' + author, 'w')
			f.write(cnt.getText().replace('\n','').replace('\xc2\xa0','').strip())



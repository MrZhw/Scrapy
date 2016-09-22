# -*- coding:utf-8 -*-
import os,sys
import re
import scrapy
from bs4 import BeautifulSoup
import urllib
reload(sys)
sys.setdefaultencoding('utf-8')
f = open("chinese_english.txt", 'a')
global cnt
cnt = 0
class YuerSpider(scrapy.Spider):
	name = "yuerEnZh"
	allowed_domains = ["yuer.hujiang.com"]
	start_urls = ["http://yuer.hujiang.com/yeyingyu/yygs/p320282/page2/"]
	def parse(self, response):
		global cnt
		soup = BeautifulSoup(response.body_as_unicode(),"lxml")
		article = soup.find(id='article')
		if article:
			lang_cns = article.find_all(class_='langs_cn')
			lang_ens = article.find_all(class_='langs_en')
			if len(lang_cns) != 0 and len(lang_cns) == len(lang_ens):
				for index, lang in enumerate(lang_cns):
					f.write("<cn count=\"" + str(cnt) + "\">\n" + lang_cns[index].getText() + "\n</cn>\n")
					f.write("<en count=\"" + str(cnt) + "\">\n" + lang_ens[index].getText() + "\n</en>\n")
					cnt += 1

		# founds = soup.find_all('a')
		# for found in founds:
		# 	url = found.get('href')
		# 	if url:
		# 		if "http" not in url:
		# 			url = "http://yuer.hujiang.com" + url
		# 		print 'url = ', url
		# 		yield scrapy.Request(url,callback=self.parse)

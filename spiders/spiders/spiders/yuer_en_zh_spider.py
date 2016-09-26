# -*- coding:utf-8 -*-
import os,sys
import re
import scrapy
from bs4 import BeautifulSoup
import urllib
import hashlib
reload(sys)
sys.setdefaultencoding('utf-8')
f = open("chinese_english.txt", 'a')
global cnt
cnt = 0
class YuerSpider(scrapy.Spider):
	name = "yuerPair"
	allowed_domains = ["yuer.hujiang.com"]
	start_urls = ["http://yuer.hujiang.com/yeyingyu/yygs/page1/"]

	finished_url = set()
	m = hashlib.md5()
	m.update("http://yuer.hujiang.com/yeyingyu/yygs/page1/")
	finished_url.add(m.hexdigest())

	def parse(self, response):
		global cnt
		soup = BeautifulSoup(response.body_as_unicode(),"lxml")
		article = soup.find(id='article')
		if article:
			lang_cns = article.find_all(class_='langs_cn')
			lang_ens = article.find_all(class_='langs_en')
			if len(lang_cns) != 0 and len(lang_cns) == len(lang_ens):
				for index, lang in enumerate(lang_cns):
					f.write("<pair count=\"" + str(cnt) + "\">\n")
					f.write("<cn>\n" + lang_cns[index].getText() + "\n</cn>\n")
					f.write("<en>\n" + lang_ens[index].getText() + "\n</en>\n")
					f.write("</pair>\n")
					cnt += 1

		founds = soup.find_all('a')
		for found in founds:
			url = found.get('href')
			if url:
				if "http" not in url:
					url = "http://yuer.hujiang.com" + url
				print 'url = ', url
				m2 = hashlib.md5()
				m2.update(url)
				if m2.hexdigest() not in self.finished_url:
					self.finished_url.add(m2.hexdigest())
					yield scrapy.Request(url,callback=self.parse)

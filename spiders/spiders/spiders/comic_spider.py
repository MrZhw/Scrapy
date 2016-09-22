# -*- coding:utf-8 -*-
import os,sys
import re
import scrapy
from bs4 import BeautifulSoup
import urllib

domain = 'http://www.xiangsheng.org/'
download = 'E:/qihao/data/comic/'
filename_withouts = [u'?', u'/', u'\\', u'"', u'<', u'>', u':', u'*', u'|']
class YuerSpider(scrapy.Spider):
	name = "comic"
	#allowed_domains = ["dmoz.org"]
	
	start_urls = ["http://www.xiangsheng.org/forum-4-1.html"]
	def parse(self, response):
		soup = BeautifulSoup(response.body_as_unicode(),"lxml")
		founds = soup.find(id='threadlist').find_all('tbody')
		for found in founds[1:]:
			url = domain + found.find(class_='s xst').get('href')
			yield scrapy.Request(url,callback=self.parse_comic)

		pageNav = soup.find(id='fd_page_top')
		if pageNav:
			url = domain + pageNav.find(class_='nxt').get('href')
			yield scrapy.Request(url,callback=self.parse)

	def parse_comic(self, response):
		soup = BeautifulSoup(response.body_as_unicode(),"lxml")
		cnt = soup.find_all(class_='t_f')
		title = soup.find('h1').getText().replace('\xc2\xa0','').replace('\n','').strip()
		print title
		for filename_con in filename_withouts:
			if filename_con in title:
				title = title.replace(filename_con, '')
		f = open(download + title, 'w')
		f.write(cnt[0].getText().replace('\n','').replace('\xc2\xa0','').strip())








# 下载音频
# 		soup = BeautifulSoup(response.body_as_unicode(),"lxml")
# 		found = soup.find(id='article_content')
# 		url = found.find('param').get('value')
# 		name = soup.find('h1').getText()
# 		suffix = url.split('.')[-1]
# 		urllib.urlretrieve(url,download + name + '.' + suffix)

# def auto_down(url, filename):
# 	try:
# 		urllib.urlretrieve(url,filename)
# 	except urllib.ContentTooShortError:
# 		print 'Network conditions is not good.Reloading.'
# 		auto_down(url,filename)
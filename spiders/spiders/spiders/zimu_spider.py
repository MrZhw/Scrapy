# -*- coding:utf-8 -*-
import os,sys
import re
import scrapy
from bs4 import BeautifulSoup
import urllib
reload(sys)
sys.setdefaultencoding('utf-8')
from spiders.items import ZimuSpidersItem
#t = open('test.txt','w')
download = 'E:/qihao/download/'
filename_withouts = ['?', '/', '\\', '"', '<', '>', ':', '*', '|']
class YuerSpider(scrapy.Spider):
	name = "zimu"
	#allowed_domains = ["dmoz.org"]
	
	start_urls = ['http://www.zimuzu.tv/esubtitle']	
	def parse(self, response):
		soup = BeautifulSoup(response.body_as_unicode(),"lxml")
		title_list = soup.find(class_='subtitle-list').find_all('a')
		for title in title_list:
			url = title.get('href')
			if 'http' not in url:
				url = 'http://www.zimuzu.tv' + url
			yield scrapy.Request(url, callback=self.parse_down)

		nextPage = soup.find(class_='pages')
		if nextPage and len(nextPage.find_all('a')):
			nextPages = nextPage.find_all('a')
			nextUrl = nextPages[len(nextPages) - 2]
			if nextUrl.getText().replace('\xc2\xa0','').replace(u'　','') == u'下一页':
				url = nextUrl.get('href')
				if 'http' not in url:
					url = "http://www.zimuzu.tv/esubtitle" + url
				yield scrapy.Request(url,callback=self.parse)

	def parse_down(self, response):
		soup = BeautifulSoup(response.body_as_unicode(),"lxml")
		srt_name = soup.find(class_='subtitle-links').find('a').getText()
		srt_url = soup.find(class_='subtitle-links').find('a').get('href')
		item = ZimuSpidersItem()
		file_urls = []
		file_names = []
		file_urls.append(srt_url)
		file_names.append(srt_name)
		item['file_names'] = file_names
		item['file_urls'] = file_urls
		return item

def auto_down(url, filename):
	try:
		urllib.urlretrieve(url,filename)
	except urllib.ContentTooShortError:
		print 'Network is not good.Reloading.'
		auto_down(url,filename)
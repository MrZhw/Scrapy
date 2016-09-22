# -*- coding:utf-8 -*-
import os,sys
import re
import scrapy
from bs4 import BeautifulSoup
import urlparse
reload(sys)
sys.setdefaultencoding('utf-8')

base = 'E:/qihao/data/61ertong/'
filename_withouts = ['?', '/', '\\', '"', '<', '>', ':', '*', '|']

class DmozSpider(scrapy.Spider):
	name = "61ertong"
	#allowed_domains = ["dmoz.org"]
	start_urls = [
		"http://www.61ertong.com/wenxue/tonghuagushi/list_177_1.html"
	]
	def parse(self, response):
		soup = BeautifulSoup(response.body_as_unicode(),"lxml")
		founds = soup.find(class_='wx-searchitem').find_all('a')
		for found in founds:
			link = found.get('href')
			yield scrapy.Request(link,callback=self.parse_url)

	def parse_url(self,response):
		soup = BeautifulSoup(response.body_as_unicode(),"lxml")
		links = soup.find(class_="list").find_all('li')
		mainUrl = response.url
		for link in links:
			url = link.find('h3').find('a').get('href')
			story = ''
			name = ''
			yield scrapy.Request(url, meta={'story':story, 'name':name}, callback=self.parse_story)

		nextPage = soup.find('div',class_='pagelist')
		#print 'pagelist = ', str(nextPage)
		if nextPage:
			nextPages = nextPage.find_all('a')
			if nextPages[len(nextPages) - 3].get('title') == u'下一页':
				url = 'http://www.61ertong.com/wenxue/' + mainUrl.split('/')[-2] + '/' + nextPages[len(nextPages) - 3].get('href')
				yield scrapy.Request(url, callback=self.parse_url)

	def parse_story(self,response):
		soup = BeautifulSoup(response.body_as_unicode(),"lxml")
		story = response.meta['story']
		name = response.meta['name']
		content = soup.find(class_='content')
		if content.find('p'):
			cnt = content.getText()
		else:
			cnt = str(content).split('<div class="dede_pages">')[0]
			cnt = re.sub('<p>|</p>|<br/>|<div class="content">|\n|　| ', '', cnt)
		story = story + cnt
		name = name if name != '' else soup.find('h1').getText()
		dede_pages = content.find(class_="dede_pages")
		nextPages = dede_pages.find_all('a')
		if nextPages and nextPages[len(nextPages) - 1].get('href') != '#':
			alUrl = response.url.split('/')
			alUrl[len(alUrl) - 1] = nextPages[len(nextPages) - 1].get('href')
			url = '/'.join(alUrl)
			yield scrapy.Request(url, meta={'story':story, 'name':name}, callback=self.parse_story)

		else:
			category = soup.find(class_='navigator').find_all('a')
			category = category[len(category) - 1].getText()
			for filename_con in filename_withouts:
				if filename_con in name:
					name = name.replace(filename_con, '_')
			
			path = base + category
			file = path + '/' + name
			if not os.path.exists(path):
				os.makedirs(path)		
			fw = open(file, 'wb')
			fw.write(story)


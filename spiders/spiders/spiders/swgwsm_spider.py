# -*- coding = utf-8 -*-
import os,sys
import re
import scrapy
from bs4 import BeautifulSoup

base = './why/'
filename_withouts = ['?', '/', '\\', '"', '<', '>', ':', '*', '|']
fw = open('urls.txt','wb')

class SwgwsmSpider(scrapy.Spider):
	name = "swgwsm"
	#allowed_domains = ["dmoz.org"]
	start_urls = [
		"http://www.tom61.com/shiwangeweishime/"
	]
	def parse(self, response):
		soup = BeautifulSoup(response.body_as_unicode(),"lxml")
		founds = soup.find(id='Mhead1_5')
		founds = founds.find_all('a')
		for found in founds:
			links = found.get('href')
			#print 'found = ', found, 'links = ', links
			yield scrapy.Request(links,callback=self.parse_url)

	def parse_url(self,response):
		#print 'res = ', response.body
		soup = BeautifulSoup(response.body_as_unicode(),"lxml")
		link = soup.find(id="Mhead2_0")
		_urls = link.find_all('a')
		#print 'title = ',soup.title.string, 'len = ', len(_urls)
		for _url in _urls:
			story = _url.get('href')
			if 'http' not in story:
				story = 'http://www.tom61.com' + story
			fw.write(story + '\n')
			#print 'story = ', story
			yield scrapy.Request(story,callback=self.parse_story)

		nextPage = soup.find_all('div',class_='t_fy')
		for np in nextPage:
			pages = np.find_all('a',class_='c_page')
			for page in pages:
				#if re.match('http',page) == None:
				_url = 'http://www.tom61.com' + page.get('href')
				#fw.write(story + '\n')
				#print '_url = ', _url
				yield scrapy.Request(_url,callback=self.parse_url_next)

	def parse_url_next(self,response):
		soup = BeautifulSoup(response.body_as_unicode(),"lxml")
		link = soup.find(id="Mhead2_0")
		_urls = link.find_all('a')
		for _url in _urls:
			story = _url.get('href')
			if 'http' not in story:
				story = 'http://www.tom61.com' + story
				#print "story = ", story
			fw.write(story + '\n')
			yield scrapy.Request(story,callback=self.parse_story)

	def parse_story(self,response):
		soup = BeautifulSoup(response.body_as_unicode(),"lxml")
		top = soup.title.string
		title = top.split('_')
		name = title[0]
		content = soup.find(class_='t_news_txt')
		story = ''
		_cnts = content.find_all('p')
		for _cnt in _cnts:
			temp = _cnt.get_text().encode('utf-8')
			story = story + temp.replace(' ','')
		story = story.strip().replace('\xc2\xa0','')
		for filename_con in filename_withouts:
			if filename_con in name:
				name = name.replace(filename_con, '')
		#print "name = ", name
		firstpath = base + title[2]
		secondpath = firstpath + '/' + title[1]
		filepath = base + name
		fw = open(filepath, 'w')
		fw.write(story)

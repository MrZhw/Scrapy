# -*- coding = utf-8 -*-
import os,sys
import re
import scrapy
from bs4 import BeautifulSoup
reload(sys)
sys.setdefaultencoding('utf-8')

base = r'./child_story/'
filename_withouts = ['?', '/', '\\', '"', '<', '>', ':', '*', '|']

class DmozSpider(scrapy.Spider):
	name = "tom"
	#allowed_domains = ["dmoz.org"]
	start_urls = [
		"http://www.tom61.com/shiwangeweishime/"
	]
	def parse(self, response):
		soup = BeautifulSoup(response.body_as_unicode(),"lxml")
		founds = soup.find_all('ul',class_='t_dh_tab')	
		for found in founds:
			links = found.find_all('a')
			for link in links:
				_url = link.get('href')
				#print 'url = ', _url
				yield scrapy.Request(_url,callback=self.parse_url)

	def parse_url(self,response):
		#print 'res = ', response.body
		soup = BeautifulSoup(response.body_as_unicode(),"lxml")
		link = soup.find(id="Mhead2_0")
		#for link in links:
		_urls = link.find_all('a')
		for _url in _urls:
			story = _url.get('href')
			if 'http' not in story:
				story = 'http://www.tom61.com' + story
			#print 'story = ', story
			yield scrapy.Request(story,callback=self.parse_story)

		nextPage = soup.find_all('div',class_='t_fy')
		for np in nextPage:
			pages = np.find_all('a',class_='c_page')
			for page in pages:
				_url = 'http://www.tom61.com' + page.get('href')
				yield scrapy.Request(_url,callback=self.parse_url_next)

	def parse_url_next(self,response):
		soup = BeautifulSoup(response.body_as_unicode(),"lxml")
		link = soup.find(id="Mhead2_0")
		#for link in links:
		_urls = link.find_all('a')
		for _url in _urls:
			story = _url.get('href')
			if 'http' not in story:
				story = 'http://www.tom61.com' + story
			#print 'story = ', story
			yield scrapy.Request(story,callback=self.parse_story)

	def parse_story(self,response):
		soup = BeautifulSoup(response.body_as_unicode(),"lxml")
		top = soup.title.string
		title = top.split('_')
		content = soup.find(class_='t_news_txt')
		story = ''
		_cnts = content.find_all('p')
		for _cnt in _cnts:
			temp = _cnt.get_text()
			story = story + temp

		name = title[0]
		for filename_con in filename_withouts:
			if filename_con in name:
				name = name.replace(filename_con, '_')

		firstpath = base + title[2]
		secondpath = firstpath + '/' + title[1]
		filepath = secondpath + '/' + name

		if not os.path.exists(firstpath):
			os.makedirs(firstpath)		
		if not os.path.exists(secondpath):
			os.makedirs(secondpath)		
		fw = open(filepath, 'wb')
		fw.write(story)


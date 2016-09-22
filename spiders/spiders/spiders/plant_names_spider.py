# -*- coding:utf-8 -*-
import scrapy
from bs4 import BeautifulSoup
import os,sys,re
from spiders.items import PlantNamesSpidersItem
import urlparse
class animalSpider(scrapy.Spider):
	name = 'plantNames'
	# allowed_domains = []
	# Subject Database of Chinese Plant, 中国植物主题数据库， http://www.plant.csdb.cn/names
	start_urls = ['http://www.plant.csdb.cn/names']

	def parse(self, response):
		soup = BeautifulSoup(response.body_as_unicode(),"lxml")
		founds = soup.find(class_='content-middle').find_all('tr')
		for found in founds[1:]:
			tds = found.find_all('td')
			
			latin_name = tds[0].find('a').getText().replace('\xc2\xa0',' ').replace(u'　',' ')
			nomenclator = tds[1].getText().replace('\xc2\xa0',' ').replace(u'　',' ')
			chinese_name = tds[2].getText().replace('\xc2\xa0',' ').replace(u'　',' ')
			location = tds[3].getText().replace('\xc2\xa0',' ').replace(u'　',' ')
			url = urlparse.urljoin('http://www.plant.csdb.cn/', tds[0].find('a').get('href'))
			yield scrapy.Request(url,
				meta={'url':url,'latin_name':latin_name,'nomenclator':nomenclator,
					  'chinese_name':chinese_name,'location':location}, 
				callback=self.parse_detail)

		nextPage = soup.find(class_='pager').find(class_='pager-next').find('a').get('href')
		nextUrl = urlparse.urljoin('http://www.plant.csdb.cn', nextPage)
		yield scrapy.Request(nextUrl, callback=self.parse)


	def parse_detail(self, response):
		item = PlantNamesSpidersItem()
		item['url'] = response.meta['url']
		item['latin_name'] = response.meta['latin_name']
		item['nomenclator'] = response.meta['nomenclator']
		item['chinese_name'] = response.meta['chinese_name']
		item['location'] = response.meta['location']
		item['description'] = u''
		soup = BeautifulSoup(response.body_as_unicode(),"lxml")
		content = soup.find_all(class_='quicktabs_tabpage')
		lines = str(content[0]).decode('utf-8').split('<br/>')
		description = lines[2].split('</b>')[1].replace(u'：','').replace('\xc2\xa0',' ').replace(u'　',' ').replace('\n',' ')
		description = re.sub(r' +', ' ', description)
		item["description"] = description
		return item
		# for line in lines:
		# 	if '<b>' in line:
		# 		temp = line.replace('<b>','').split('</b>')
		# 		#print 'line0 = ', temp[0], 'line1 = ', temp[1].replace(u'：','')
		# 		if temp[0] == u'形态描述':
		# 			print temp[1].replace(u'：','').replace('\xc2\xa0',' ').replace(u'　',' ')

		
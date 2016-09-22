# -*- coding:utf-8 -*-
import os,sys
import re,json
import scrapy
from bs4 import BeautifulSoup
from spiders.items import PlantSpidersItem
reload(sys)
sys.setdefaultencoding('utf-8')
class PlantSpider(scrapy.Spider):
	name = "plant_name"

	def start_requests(self):
		f = open('plants.txt','r')
		lines = f.readlines()		
		print "lines = ", len(lines)
		# return [
		# 	scrapy.FormRequest(
		# 		'https://sp0.baidu.com/8aQDcjqpAAV3otqbppnN2DJv/api.php',
		# 		formdata = {
		# 		'query':'常见植物大全',
		# 		'ie':'utf-8',
		# 		'oe':'utf-8',
		# 		'resource_id':'6839'
		# 		},
		# 		callback=self.parse_json
		# 	)
		# ]
		for line in lines:
			temp = line.strip().split(',')
			yield scrapy.FormRequest(
				 'http://baike.baidu.com/search/word',
				#'http://baike.baidu.com/item',
				meta = {'typeclass':temp[1],'name':temp[0]},
				formdata = {
					'word':temp[0]
				},
				callback=self.parse_baike
				)
		# return [
		# 	scrapy.FormRequest(
		# 		'http://baike.baidu.com/search/word',
		# 		meta = {'typeclass':line.strip.split(',')[1],'name':line.strip.split(',')[0]},
		# 		formdata = {
		# 			'word':line.strip().split(',')[0]
		# 		},
		# 		callback=self.parse_baike
		# 	) for line in lines
		# ]

	def parse_baike(self, response):
		if u'百度百科尚未收录词条' in response.body_as_unicode():
			return
		item = PlantSpidersItem()
		typeclass = response.meta['typeclass']
		name = response.meta['name']
		item['url'] = response.url
		item['category'] = typeclass
		soup = BeautifulSoup(response.body_as_unicode(),"lxml")
		summary = u''
		if soup.find(class_='lemma-summary'):
			summary = soup.find(class_='lemma-summary').getText()
		item['chinese_name'] = u'' 
		item['english_name'] = u'' 
		item['scientific_name'] = u'' 
		item['other_name'] = u'' 
		item['location'] = u'' 
		item['nomenclator'] = u'' 
		item['introduction'] = summary.strip()
		basic_info = soup.find(class_='basic-info')
		if basic_info:
			basic_names = basic_info.find_all(class_='name')
			basic_values = basic_info.find_all(class_='value')
			for index, basic_name in enumerate(basic_names):
				first = basic_name.getText().replace('\xc2\xa0','').replace(u'　','').replace(' ','')
				second = basic_values[index].getText().replace('\xc2\xa0','').strip()
				if first == u'中文学名':
					item['chinese_name'] = second
				if first == u'英文名称':
					item['english_name'] = second
				if first == u'拉丁学名':
					item['scientific_name'] = second
				if first == u'别称':
					item['other_name'] = second
				if first == u'分布区域':
					item['location'] = second
				if first == u'命名者' or first == u'命名者及年代':
					item['nomenclator'] = second
			item['chinese_name'] = item['chinese_name'] if item['chinese_name'] != u'' else name 
		return item



		
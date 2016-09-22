# -*- coding:utf-8 -*-
import os,sys
import re,json
import scrapy
from bs4 import BeautifulSoup
from spiders.items import PlantSpidersItem
reload(sys)
sys.setdefaultencoding('utf-8')
#plant_list = open('plants.txt','w')
class PlantSpider(scrapy.Spider):
	name = "plant"

	def start_requests(self):
		return [
			scrapy.FormRequest(
				'https://sp0.baidu.com/8aQDcjqpAAV3otqbppnN2DJv/api.php',
				formdata = {
				'query':'常见植物大全',
				'ie':'utf-8',
				'oe':'utf-8',
				'resource_id':'6839'
				},
				callback=self.parse_json
			)
		]

	def parse_json(self, response):
		js = json.loads(response.body)
		for category in js['data'][0]['result']:
			additional = int(category['additional'].replace(u'种',''))
			iterations = additional / 50
			iterations = iterations if  additional % 50 == 0 else iterations + 1
			for x in xrange(iterations):
				qn = str(50 * x)
				yield scrapy.FormRequest(
					'https://sp0.baidu.com/8aQDcjqpAAV3otqbppnN2DJv/api.php',
					formdata = {
						'query':category['ename'],
						'ie':'utf-8',
						'oe':'utf-8',
						'format':'json',
						'resource_id':'6829',
						'from_mid':'1',
						'rn':'50',
						'qn': qn
					},
					callback=self.parse_list
					)

	def parse_list(self, response):
		js = json.loads(response.body)
		typeclass = js['data'][0]['queryparser'][0]['pet_typeclass']
		#print 'typeclass = ', typeclass
		for data in js['data'][0]['disp_data']:
			name = data['name']
			#print name
			plant_list.write(name + ',' + typeclass + '\n')
			# yield scrapy.FormRequest(
			# 	'http://baike.baidu.com/search/word',
			# 	meta = {'typeclass':typeclass,'name':name},
			# 	formdata = {
			# 		'word':name
			# 	},
			# 	callback=self.parse_baike
			# 	)

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



		
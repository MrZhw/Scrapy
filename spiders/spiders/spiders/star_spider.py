# -*- coding:utf-8 -*- ''
# @author:zeng
# 
import scrapy
import os,sys
import re
from bs4 import BeautifulSoup
from spiders.items import StarSpidersItem
t = open('test.txt','w')
class PoemSpider(scrapy.Spider):
	name = 'star'
	#allowed_domains = ["http://www.ijq.tv/"]
	start_urls = ["http://www.ijq.tv/mingxing/list__1.html"]
	# start_urls = []
	# for x in xrange(1,186):
	# 	start_urls.append('http://www.ijq.tv/mingxing/list__' + str(x) + '.html')

	def parse(self, response):
		soup = BeautifulSoup(response.body_as_unicode(),"lxml")
		stars_list = soup.find(id='list_stars')
		stars = stars_list.find_all('li')
		for star in stars:
			url = star.find_all('a')[0].get('href')
			if 'http' not in url:
				url = "http://www.ijq.tv" + url
	 			#print url
			yield scrapy.Request(url,callback=self.parse_star)

		nextPage = soup.find(class_='pages')
		if nextPage and len(nextPage.find_all('a')):
			nextPages = nextPage.find_all('a')
			nextUrl = nextPages[len(nextPages) - 1]
			#t.write(nextUrl.getText().replace('\xc2\xa0','').replace(u'　','') + ',' + u'下一页') 
			if nextUrl.getText().replace('\xc2\xa0','').replace(u'　','') == u'下一页':
				url = nextUrl.get('href')
				if 'http' not in url:
					url = "http://www.ijq.tv" + url
				yield scrapy.Request(url,callback=self.parse)

	def parse_star(self, response):
		soup = BeautifulSoup(response.body_as_unicode(),"lxml")
		details = soup.find(id='v-details-list').find_all('p')
		item = StarSpidersItem()
		item['url'] = response.url
		item['microblog'] = u''
		for detail in details:
			pair =  detail.getText().split(u'：')
			first = pair[0].replace('\xc2\xa0','').replace(u'　','')
			second = pair[1]
			if u'《' in second:
				second = '_'.join(pair[1].replace(u'《',' ').replace(u'》',' ').split())
			if u'中文名' == first:
				item['chinese_name'] = second
				#print u'中文名'
			if u'英文名' == first:
				item['english_name'] = second
				#print u'英文名'
			if u'曾用名' == first:
				item['used_name'] = second
				#print u'曾用名'			
			if u'民族' == first:
				item['nation'] = second
				#print u'民族'
			if u'国家地区' == first:
				item['location'] = second
				#print u'国家地区'
			if u'出生日期' == first:
				item['birthday'] = second
				#print u'出生日期'
			if u'出生地' == first:
				item['birthplace'] = second
				#print u'出生地'
			if u'身高' == first:
				item['height'] = second
				#print u'身高'
			if u'体重' == first:
				item['weight'] = second
				#print u'体重'			
			if u'血型' == first:
				item['bloodType'] = second
				#print u'血型'
			if u'星座' == first:
				item['constellation'] = second
				#print u'星座'
			if u'毕业院校' == first:
				item['graduateSchool'] = second
				#print u'毕业院校'
			if u'职业' == first:
				item['profession'] = second
				#print u'职业'
			if u'经纪公司' == first:
				item['company'] = second
				#print u'经纪公司'
			if u'微博' == first:
				item['microblog'] = detail.find('a').get('href')
				#print u'微博'			
			if u'代表作' == first:
				item['representative'] = second
				#print u'代表作'
			if u'相关明星' == first:
				item['relatedStar'] = second
				#print u'相关明星'
		summary = soup.find(id='v-summary').find_all('div',id='hutia')
		item['personal'] = u''
		if summary:
			item['personal'] = summary[0].getText()
		return item



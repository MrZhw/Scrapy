# -*- coding:utf-8 -*-
import scrapy
from bs4 import BeautifulSoup
import os,sys,re
from spiders.items import AnimalSpidersItem
features = ['length','height','weight','life','feeding','breed','habit','location']
fenlei = ['jie','men','gang','mu','ke','shu','zhong']
class animalSpider(scrapy.Spider):
	name = 'animal'
	# allowed_domains = []
	start_urls = ['http://www.iltaw.com/animal/all']

	def parse(self, response):
		soup = BeautifulSoup(response.body_as_unicode(),"lxml")
		founds = soup.find(class_='nav').find_all('a')
		# item = AnimalSpidersItem()
		for x in xrange(6):
			category = re.split('M|B|F|A|R|I',founds[x].getText())
			#item['category'] = category[0]
			url = founds[x].get('href')
			yield scrapy.Request(url, meta={'cate':category}, callback=self.parse_animal)
			# request = scrapy.Request(url, callback=self.parse_animal)
			# request.meta['item'] = item
			# yield request

	def parse_animal(self, response):
		category = response.meta['cate']
		print category
		soup = BeautifulSoup(response.body_as_unicode(),"lxml")
		founds = soup.find(class_='info-list').find_all(class_='image-wrap')
		for found in founds:
			url = found.find('a').get('href')
			yield scrapy.Request(url, meta={'cate':category}, callback=self.parse_detail)
			# request = scrapy.Request(url, callback=self.parse_detail)
			# request.meta['item'] = item
			# yield request	
		nextPage = soup.find(class_='pager-v1')
		if nextPage and len(nextPage.find_all('a')):
			nextPages = nextPage.find_all('a')
			nextUrl = nextPages[len(nextPages) - 1]
			#t.write(nextUrl.getText().replace('\xc2\xa0','').replace(u'　','') + ',' + u'下一页') 
			if nextUrl.getText().replace('\xc2\xa0','').replace(u'　','') == u'>':
				url = nextUrl.get('href')
				if 'http' not in url:
					url = "" + url
				yield scrapy.Request(url, meta={'cate':category}, callback=self.parse_animal)

	def parse_detail(self, response):
		category = response.meta['cate']
		print category

		item = AnimalSpidersItem()
		item['category'] = category[0]
		# item = response.meta['item']
		item['url'] = response.url
		soup = BeautifulSoup(response.body_as_unicode(),"lxml")
		# inner_wrap = soup.find(class_='intro-inner-wrap')
		# left_wrap = inner_wrap.find(class_='left-wrap')
		# summary = re.split(u'；|。',left_wrap.getText())
		# item['chinese_name'] = re.split(u'：|（|）',summary[0])[1]
		# item['pingyin'] = re.split(u'：|（|）',summary[0])[3]
		# item['english_name'] = re.split(u'：|（|）',summary[1])[1]
		# item['scientific_name'] = re.split(u'：|（|）',summary[2])[1]
		# item['introduction'] = '。'.join(summary[3:])
		inner_wrap = soup.find(class_='intro-inner-wrap')
		left_wrap = inner_wrap.find(class_='left-wrap')
		lines = str(left_wrap).decode('utf-8').split('<br/>')
		line1 = lines[0].replace('<strong>','').replace('</strong>','').replace('<em>','').replace('</em>','').split(u'：')
		line2 = lines[1].replace('<strong>','').replace('</strong>','').replace('<em>','').replace('</em>','').split(u'：')
		line3 = lines[2].replace('<strong>','').replace('</strong>','').replace('<em>','').replace('</em>','').split(u'：')
		line4 = lines[3].replace('<strong>','').replace('</strong>','').replace('<em>','').replace('</em>','')
		item['chinese_name'] = line1[1].split(u'（')[0]
		#item['pingyin'] = line1[2].split(u'）')[0]
		item['english_name'] = line2[1]
		item['scientific_name'] = line3[1]
		item['introduction'] = line4

		right_wrap = inner_wrap.find(class_='right-wrap')
		details = right_wrap.find_all('p')
		for index,detail in enumerate(details):
			if detail.find('span'):
				item[features[index]] = detail.find('span').getText()
			else:
				item[features[index]] = u''

		# _property = str(soup.find(class_='property')).split('<br/>')
		# for x in xrange(7):
		# 	item[fenlei[x]] = _property[x].split(u'：')[1].split()[0]

		info = soup.find(class_='info-inner-wrap').find(class_='left-wrap')
		title = info.find_all('span')
		description = info.find_all(class_='description')

		item['description'] = u''
		item['ecologicalHabit'] = u''
		item['growthBreed'] = u''
		item['subspeciesTaxonomy'] = u''
		item['knowledge'] = u''
		item['distribution'] = u''
		item['livingCondition'] = u''
		item['englishIntroduction'] = u''
		item['information'] = u''
		for x in xrange(len(title)):
			if title[x].getText() == 'Description':
				item['description'] = description[x].getText()
			if title[x].getText() == 'Ecological Habit':
				item['ecologicalHabit'] = description[x].getText()
			if title[x].getText() == 'Growth and Breed':
				item['growthBreed'] = description[x].getText()
			if title[x].getText() == 'Subspecies and Taxonomy':
				item['subspeciesTaxonomy'] = description[x].getText()
			if title[x].getText() == 'Knowledge':
				item['knowledge'] = description[x].getText()
			if title[x].getText() == 'Distribution':
				item['distribution'] = description[x].getText()
			if title[x].getText() == 'Living Condition':
				item['livingCondition'] = description[x].getText()
			if title[x].getText() == 'Introduction':
				item['englishIntroduction'] = description[x].getText()
			if title[x].getText() == 'Information':
				item['information'] = description[x].getText()

		return item



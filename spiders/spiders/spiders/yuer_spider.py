# -*- coding:utf-8 -*-
import os,sys
import re
import scrapy
from bs4 import BeautifulSoup
import urllib
reload(sys)
sys.setdefaultencoding('utf-8')

down_video = r'./down/with_video/'
down_story = r'./down/without_video/'
down_other = r'./down/other'
filename_withouts = ['?', '/', '\\', '"', '<', '>', ':', '*', '|']
class YuerSpider(scrapy.Spider):
	name = "yuer"
	#allowed_domains = ["dmoz.org"]
	
	start_urls = []
	for x in xrange(1,50):
		start_urls.append("http://yuer.hujiang.com/yeyingyu/yygs/" + "page" + str(x))
	
	def parse(self, response):
		soup = BeautifulSoup(response.body_as_unicode(),"lxml")
		found = soup.find(class_='in_list_conent')
		links = found.find_all('a')
		for link in links:
			url = "http://yuer.hujiang.com" + link.get('href')
			#print 'url = ', url
			yield scrapy.Request(url,callback=self.parse_url)

	def parse_url(self, response):
		soup = BeautifulSoup(response.body_as_unicode(),"lxml")
		top = soup.title.string
		for without in filename_withouts:
			if without in top:
				top = top.replace(without, '')
		#print "top = ", top
		title = top.split('_')[0].replace(u'(中英)',u'').replace(u'（双语）',u'')
		#print 'title = ', title
		if title[0] == u'【':
			temp = title.split(u'】')
			category = temp[0][1:]
			category_path = down_video + category
			if not os.path.exists(category_path):
				os.makedirs(category_path)
			story = temp[1]
		elif title[len(title)-1] == u'】':
			temp = title.split(u'【')
			category = temp[1][:-1]
			category_path = down_video + category
			if not os.path.exists(category_path):
				os.makedirs(category_path)
			story = temp[0]
		elif u'）：' in title:
			temp = title.split(u'）：')
			category = temp[0][:-2]
			category_path = down_video + category
			if not os.path.exists(category_path):
				os.makedirs(category_path)
			story = temp[1]
		elif u'：' in title:
			temp = title.split(u'：')
			category = temp[0]
			category_path = down_video + category
			if not os.path.exists(category_path):
				os.makedirs(category_path)
			story = temp[1]
		elif u'-' in title:
			temp = title.split(u'-')
			category = temp[0]
			category_path = down_video + category
			if not os.path.exists(category_path):
				os.makedirs(category_path)
			story = temp[1]
		else:
			category_path = down_other
			story = title
		down_mp3 = category_path + '/' + story + '.mp3'
		down_p = category_path + '/' + story + '.p'
		down_cn = category_path + '/' + story + '.cn'
		down_en = category_path + '/' + story + '.en'

		article = soup.find(id='article')

		sonpath = re.search(r'son=(.+?)&',str(article))
		if sonpath != None:
			sonpath = sonpath.group(1)
			if not os.path.exists(down_mp3):
				auto_down(sonpath, down_mp3)

			contents = article.find_all('p')
			content = contents[len(contents) - 2].get_text().strip()
			#print 'content = ', content, 'type = ', type(content)
			fwp = open(down_p,'w')
			fwp.write(content)

		lang_cns = article.find_all(class_='langs_cn')
		lang_ens = article.find_all(class_='langs_en')
		if len(lang_cns) != 0:
			fwcn = open(down_cn,'w')
			for lang in lang_cns:
				p = lang.get_text()
				#print 'p = ', p, 'type = ', type(p)
				fwcn.write(p + '\n')

			fwen = open(down_en,'w')
			for lang in lang_ens:
				p = lang.get_text()
				#print 'p = ', p, 'type = ', type(p)
				fwen.write(p + '\n')
			
		# if len(lang_cns) != 0:
		# 	fwcn = open(down_cn,'w')
		# 	fwen = open(down_en,'w')
		# 	lang_write(lang_cns, fwcn)
		# 	lang_write(lang_ens, fwen)

		#yield scrapy.Request(url,callback=self.parse_url)
		
def lang_write(langs,fw):
	f = open(fw,'w')
	for lang in langs:
		p = lang_en.get_text().strip()
		f.write(p + '\n')

def auto_down(url, filename):
	try:
		urllib.urlretrieve(url,filename)
	except urllib.ContentTooShortError:
		print 'Network conditions is not good.Reloading.'
		auto_down(url,filename)
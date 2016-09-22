# -*- coding:utf-8 -*-
import os,sys
import re
import scrapy
from bs4 import BeautifulSoup
from scrapy.selector import Selector
reload(sys)
sys.setdefaultencoding('utf-8')

class Spider(scrapy.Spider):
	name = "sinaSpiderToLocal"
	host = "http://weibo.cn"
	start_urls = [
		1751675285, 5235640836, 5676304901, 5871897095, 2139359753, 5579672076, 2517436943, 5778999829, 5780802073, 
		2159807003,
		1756807885, 3378940452, 5762793904, 1885080105, 5778836010, 5722737202, 3105589817, 5882481217, 5831264835,
		2717354573, 3637185102, 1934363217, 5336500817, 1431308884, 5818747476, 5073111647, 5398825573, 2501511785,
	]
	scrawl_ID = set(start_urls)
	finish_ID = set()

	def start_requests(self):
		while True:
			ID = self.scrawl_ID.pop()
			self.finish_ID.add(ID)
			ID = str(ID)
			follows = []
			fans = []
			url_follows = "http://weibo.cn/%s/follow" % ID
			url_fans = "http://weibo.cn/%s/fans" % ID
			url_tweets = "http://weibo.cn/%s/profile?filter=1&page=1" % ID
			yield scrapy.Request(url=url_tweets, meta={"ID": ID}, callback=self.parse)
			yield scrapy.Request(url=url_follows, meta={"result": follows},callback=self.parse_connect)  # 去爬关注人
			yield scrapy.Request(url=url_fans, meta={"result": fans}, callback=self.parse_connect)  # 去爬粉丝
			

	def parse(self, response):
		ID = response.meta["ID"]
		soup = BeautifulSoup(response.body_as_unicode(),"lxml")
		tweets = soup.find_all(class_='c',id=True)
		for tweet in tweets:
			_id = tweet.get("id")
			content = tweet.find(class_='ctt')
			comment = re.findall(u'\u8bc4\u8bba\[(\d+)\]', tweet.getText())  # 评论数
			if content and comment and int(comment[0]) > 0:
				content = content.getText().strip(u"[\u7ec4\u56fe\u5171(\d+)\u5f20]")  # 去掉最后的"[组图共x张]"
				commentUrls = tweet.find_all(class_="cc")
				if commentUrls:
					for commentUrl in commentUrls:
						temp = response.meta["ID"] + "-" + _id
						f = open("./sina/" + temp, 'a')
						f.write("<Tweet>\n" + content + "\n")
						yield scrapy.Request(url=commentUrl.get('href'), meta={"file": f}, callback=self.parse_comment)

		urlPage = soup.find(id='pagelist')
		if urlPage:
			url_next = urlPage.find('a',text='\u4e0b\u9875')
			if url_next:
				yield scrapy.Request(url=self.host + url_next.get('href'), meta={"ID": response.meta["ID"]}, callback=self.parse)

	def parse_comment(self, response):
		soup = BeautifulSoup(response.body_as_unicode(),"lxml")
		comments = soup.find_all(class_='c', id=re.compile('C_(.*)'))
		f = response.meta["file"]
		for comment in comments:
			cnt = comment.find(class_='ctt')
			if cnt:
				cnt = re.compile(u'回复@(.*):').sub('', cnt.getText())
				f.write("<comment>\n" + cnt + "\n</comment>\n") 			# 评论内容

		nextPage = soup.find(id='pagelist')
		if nextPage:
			nextUrl = nextPage.find('a',text='\u4e0b\u9875')
			if nextUrl:
				yield scrapy.Request(url=self.host + nextUrl.get('href'), meta={"file": f}, callback=self.parse_comment)
		else:
			f.write("</Tweet>")

	def parse_connect(self, response):
		selector = Selector(response)
		text2 = selector.xpath(
			u'body//table/tr/td/a[text()="\u5173\u6ce8\u4ed6" or text()="\u5173\u6ce8\u5979"]/@href').extract()
		for elem in text2:
			elem = re.findall('uid=(\d+)', elem)
			if elem:
				response.meta["result"].append(elem[0])
				ID = int(elem[0])
				if ID not in self.finish_ID:  # 新的ID，如果未爬则加入待爬队列
					self.scrawl_ID.add(ID)
		url_next = selector.xpath(
			u'body//div[@class="pa" and @id="pagelist"]/form/div/a[text()="\u4e0b\u9875"]/@href').extract()
		if url_next:
			yield scrapy.Request(url=self.host + url_next[0], meta={"result": response.meta["result"]},callback=self.parse_connect)
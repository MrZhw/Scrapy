# -*- coding:utf-8 -*-
import os,sys
import re
import scrapy
from bs4 import BeautifulSoup
from SinaSpider.items import TweetsItem, CommentItem
reload(sys)
sys.setdefaultencoding('utf-8')

class Spider(scrapy.Spider):
	name = "sinaSpiderToDB"
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
			url_tweets = "http://weibo.cn/%s/profile?filter=1&page=1" % ID
			yield scrapy.Request(url=url_tweets, meta={"ID": ID}, callback=self.parse)

	def parse(self, response):
		ID = response.meta["ID"]
		soup = BeautifulSoup(response.body_as_unicode(),"lxml")
		tweets = soup.find_all(class_='c',id=True)
		for tweet in tweets:
			tweetsItems = TweetsItem()
			_id = tweet.get("id")
			content = tweet.find(class_='ctt')
			like = re.findall(u'\u8d5e\[(\d+)\]', tweet.getText())  # 点赞数
			transfer = re.findall(u'\u8f6c\u53d1\[(\d+)\]', tweet.getText())  # 转载数
			comment = re.findall(u'\u8bc4\u8bba\[(\d+)\]', tweet.getText())  # 评论数
			others = tweet.find(class_='ct')   # 求时间和使用工具（手机或平台）

			tweetsItems["ID"] = response.meta["ID"]
			tweetsItems["_id"] = response.meta["ID"] + "-" + _id
			if content:
				tweetsItems["Content"] = content.getText().strip(u"[\u7ec4\u56fe\u5171(\d+)\u5f20]")  # 去掉最后的"[组图共x张]"
			if like:
				tweetsItems["Like"] = int(like[0])
			if transfer:
				tweetsItems["Transfer"] = int(transfer[0])
			if comment:
				tweetsItems["Comment"] = int(comment[0])
			if others:
				others = others.getText().split(u"\u6765\u81ea")
				tweetsItems["PubTime"] = others[0]
				if len(others) == 2:
					tweetsItems["Tools"] = others[1]
			if content:
				yield tweetsItems

			if tweetsItems["Comment"] > 0:
				commentUrls = tweet.find_all(class_="cc")
				if commentUrls:
					for commentUrl in commentUrls:
						temp = response.meta["ID"] + "-" + _id
						yield scrapy.Request(url=commentUrl.get('href'), meta={"ID": temp }, callback=self.parse_comment)

		urlPage = soup.find(id='pagelist')
		if urlPage:
			url_next = urlPage.find('a',text='\u4e0b\u9875')
			if url_next:
				yield scrapy.Request(url=self.host + url_next.get('href'), meta={"ID": response.meta["ID"]}, callback=self.parse)

	def parse_comment(self, response):
		soup = BeautifulSoup(response.body_as_unicode(),"lxml")
		comments = soup.find_all(class_='c', id=re.compile('C_(.*)'))
		ID = response.meta["ID"]
		for comment in comments:
			commentItem = CommentItem()
			_id = comment.get('id')
			commentItem['ID'] = response.meta['ID']
			commentItem['_id'] = response.meta['ID'] + '-' + _id
			cnt = comment.find(class_='ctt')

			like = re.findall(u'\u8d5e\[(\d+)\]', comment.getText())  # 点赞数
			if like:
				commentItem["Like"] = int(like[0])
			if cnt:
				cnt = re.compile(u'回复@(.*):').sub('', cnt.getText())
				commentItem['Content'] = cnt 			# 评论内容
				yield commentItem

		nextPage = soup.find(id='pagelist')
		if nextPage:
			nextUrl = nextPage.find('a',text='\u4e0b\u9875')
			if nextUrl:
				yield scrapy.Request(url=self.host + nextUrl.get('href'), meta={"ID": response.meta['ID']}, callback=self.parse_comment)

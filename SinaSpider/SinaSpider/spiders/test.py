# -*- coding:utf-8 -*-
import os,sys
import re
import scrapy
from bs4 import BeautifulSoup
import codecs
from scrapy.selector import Selector
from scrapy.http import Request
import urllib
# from SinaSpider.items import TweetsItem, CommentItem
reload(sys)
sys.setdefaultencoding('utf-8')

def parse():
	soup = BeautifulSoup(codecs.open('../test.html','r','utf-8'),"lxml")
	# print soup.prettify()
	print soup.title
	# print soup.body()
	tweets = soup.find_all(class_='c',id=True)
	print len(tweets)
	for tweet in tweets:
		id = tweet.get("id")
		print id
		content = tweet.find(class_='ctt')
		like = re.findall(u'\u8d5e\[(\d+)\]', tweet.getText())  # 点赞数
		transfer = re.findall(u'\u8f6c\u53d1\[(\d+)\]', tweet.getText())  # 转载数
		comment = re.findall(u'\u8bc4\u8bba\[(\d+)\]', tweet.getText())  # 评论数
		others = tweet.find(class_='ct')  # 求时间和使用工具（手机或平台）

		if content:
			print 'yes'
			print content.getText()
		else:
			print "error"
		if like:
			print like[0]
		if transfer:
			print transfer[0]
		if comment:
			print comment[0]
		if others:
			others = others.getText().split(u"\u6765\u81ea")
			print others[0]
			if len(others) == 2:
				print others[1]

		if int(comment[0]) > 0:
			url_comment = tweet.find(class_='cc').get('href')
			urllib.urlopen(url_comment)
		# yield scrapy.Request(url_comment, callback=self.parse )

def testt():
	print 'error'
	soup = BeautifulSoup(codecs.open('../test2.html','r','utf-8'),"lxml")
	print soup.title
	comments = soup.find_all(class_='c', id=re.compile('C_(.*)'))
	# ID = response.meta["ID"]
	print len(comments)
	for comment in comments:
		# commentItem = CommentItem()
		id = comment.get("id")
		print id
		# commentItem['ID'] = response.meta['ID']
		# commentItem['_id'] = response.meta['ID'] + '-' + id
		cnt = comment.find(class_='ctt')
		if cnt:
			print cnt.getText()
			cnt = re.compile(u'回复@(.*):').sub('', cnt.getText())
			print len(cnt)
			print cnt
			# commentItem['Content'] = cnt

			# yield commentItem

	nextPage = soup.find(id='pagelist')
	if nextPage:
		nextUrl = nextPage.find('a',text='\u4e0b\u9875')
		if nextUrl:
			print "nextUrl = ", nextUrl
			# yield scrapy.Request(url=self.host + nextUrl, meta={"ID": response.meta['ID']}, callback=self.parse_comment)


if __name__ == '__main__':
	# parse()
	testt()
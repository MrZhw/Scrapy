# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html

from twisted.enterprise import adbapi
import MySQLdb
import MySQLdb.cursors
from SinaSpider.items import TweetsItem, CommentItem

import codecs
import logging
from scrapy.exceptions import DropItem
import socket,sys,os
from scrapy.http import Request

class MySQLPipeline(object):

	def __init__(self):
		self.dbpool = adbapi.ConnectionPool('MySQLdb',
			db='sina',
			user='root',
			passwd='mysql',
			cursorclass = MySQLdb.cursors.DictCursor,
			charset = 'utf8',
			use_unicode = True
		)

	def process_item(self, item, spider):
		query = self.dbpool.runInteraction(self._conditional_insert, item)
		query.addErrback(self.handle_error)
		return item

	def _conditional_insert(self, tx, item):

		if isinstance(item, TweetsItem):
			sql = "insert into `tweet`(`_id`,`ID`,`Content`,`PubTime`,`Tools`,`Like`,`Comment`,`Transfer`) values (%s, %s, %s, %s, %s, %s, %s, %s)"
			tx.execute(sql, (item['_id'],item['ID'],item['Content'],item['PubTime'],item['Tools'],item['Like'],item['Comment'],item['Transfer']))
			print 'insert tweetsItem'
		
		elif isinstance(item, CommentItem):
			sql = "insert into `comment`(`_id`,`ID`,`Content`,`Like`) values (%s, %s, %s, %s)"
			tx.execute(sql, (item['_id'],item['ID'],item['Content'],item['Like']))



	#异常处理
	def handle_error(self, failure):
		logging.error(failure)
# -*- coding:utf-8 -*-
import os,sys
import re
import scrapy
from bs4 import BeautifulSoup
import urlparse
reload(sys)
sys.setdefaultencoding('utf-8')
from twisted.enterprise import adbapi
import MySQLdb
import MySQLdb.cursors
from spiders.items import ZimuSpidersItem

class testPipeline(object):
	"""docstring for ChengyuPipeline"""
	def __init__(self):
		self.dbpool = adbapi.ConnectionPool('MySQLdb',
			db='knowledgebase',
			user='root',
			passwd='mysql',
			cursorclass = MySQLdb.cursors.DictCursor,
			charset = 'utf8',
			use_unicode = True
		)
	
	def process_item(self, item, spider):
	# 	query = self.dbpool.runInteraction(self._conditional_insert, item)
	# 	query.addErrback(self.handle_error)
	# 	return item

	# def _conditional_insert(self, tx, item):
	# 	sql = "insert into zimu(file_urls,files,file_paths) values (%s, %s, %s)"
	# 	tx.execute(sql, (item['file_urls'],item['files'],item['file_paths']))

	# #异常处理
	# def handle_error(self, failure):
	# 	logging.error(failure)

if __name__ == '__main__':
	item = ZimuSpidersItem()
	item['file_urls'] = '123456'
	item['files'] = '456789'
	item['file_paths'] = '987654'
	testPipeline(item)

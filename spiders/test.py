# -*- coding:utf-8 -*-
<<<<<<< HEAD
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

	# #寮傚父澶勭悊
	# def handle_error(self, failure):
	# 	logging.error(failure)

if __name__ == '__main__':
	item = ZimuSpidersItem()
	item['file_urls'] = '123456'
	item['files'] = '456789'
	item['file_paths'] = '987654'
	testPipeline(item)
=======
import os,re

s = '物种概述Summary中文名：扁体栉齿刺尾鱼（拼音：biǎn tǐ zhì chǐ cì wěi yú）；英文名：Spotted surgeonfish；学名：Ctenochaetus strigosus。扁体栉齿刺尾鱼，全长12-15厘米。分布于中东太平洋的夏威夷群岛及约翰斯顿岛海域，栖息深度1-113米，栖息在礁石区，单独活动。以藻类为食，与绿海龟存在共生关系，负责其清理。有雪卡鱼中毒的报告。世界自然保护联盟红色名录列为：未予评估'
print s
>>>>>>> 38d197371eb5b45637dd42c842bdbd9cdc731079

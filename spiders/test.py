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

	# #异常处理
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

s = '���ָ���Summary�������������γݴ�β�㣨ƴ����bi��n t�� zh�� ch�� c�� w��i y������Ӣ������Spotted surgeonfish��ѧ����Ctenochaetus strigosus�������γݴ�β�㣬ȫ��12-15���ס��ֲ����ж�̫ƽ���������Ⱥ����Լ��˹�ٵ�������Ϣ���1-113�ף���Ϣ�ڽ�ʯ�����������������Ϊʳ�����̺�����ڹ�����ϵ��������������ѩ�����ж��ı��档������Ȼ�������˺�ɫ��¼��Ϊ��δ������'
print s
>>>>>>> 38d197371eb5b45637dd42c842bdbd9cdc731079

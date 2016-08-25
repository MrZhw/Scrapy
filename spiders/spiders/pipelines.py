# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html
from twisted.enterprise import adbapi
import MySQLdb
import MySQLdb.cursors
import codecs
import logging
from scrapy .http import Request
from scrapy.pipelines.images import ImagesPipeline
from scrapy.exceptions import DropItem
import socket,sys,os
from items import ChengyuSpidersItem

class SpidersPipeline(object):
	def process_item(self, item, spider):
		return item 	

# class ChengyuPipeline(object):
# 	"""docstring for ChengyuPipeline"""
# 	def __init__(self):
		
		
class ChengyuPipeline(object):
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
		query = self.dbpool.runInteraction(self._conditional_insert, item)
		query.addErrback(self.handle_error)
		return item

	def _conditional_insert(self, tx, item):
		sql = "insert into chengyu(lemma, pronunciation, semantic, derivation, example) values (%s, %s, %s, %s, %s)"
		tx.execute(sql, (item['lemma'], item['pronunciation'], item['semantic'], item['derivation'], item['example']))

	#异常处理
	def handle_error(self, failure):
		log.err(failure)

class PoemPipeline(object):
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
		query = self.dbpool.runInteraction(self._conditional_insert, item)
		query.addErrback(self.handle_error)
		return item

	def _conditional_insert(self, tx, item):
		sql = "insert into poem(name, dynasty, poet, category, content, shangxi) values (%s, %s, %s, %s, %s, %s)"
		tx.execute(sql, (item['name'], item['dynasty'], item['poet'], item['category'], item['content'], item['shangxi']))

	#异常处理
	def handle_error(self, failure):
		logging.error(failure)

# class JsonWithEncodingCnblogsPipeline(object):
#     def __init__(self):
#         self.file = codecs.open('cnblogs.json', 'w', encoding='utf-8')
#     def process_item(self, item, spider):
#         line = json.dumps(dict(item), ensure_ascii=False) + "\n"
#         self.file.write(line)
#         return item
#     def spider_closed(self, spider):
#         self.file.close()

# class MySQLStoreChengyuPipeline(object):
#     def __init__(self, dbpool):
#         self.dbpool = dbpool
	
#     @classmethod
#     def from_settings(cls, settings):
#         dbargs = dict(
#             host=settings['MYSQL_HOST'],
#             db=settings['MYSQL_DBNAME'],
#             user=settings['MYSQL_USER'],
#             passwd=settings['MYSQL_PASSWD'],
#             charset='utf8',
#             cursorclass = MySQLdb.cursors.DictCursor,
#             use_unicode= True,
#         )
#         dbpool = adbapi.ConnectionPool('MySQLdb', **dbargs)
#         return cls(dbpool)

#     #pipeline默认调用
#     def process_item(self, item, spider):
#         d = self.dbpool.runInteraction(self._do_upinsert, item, spider)
#         d.addErrback(self._handle_error, item, spider)
#         d.addBoth(lambda _: item)
#         return d
#     #将每行更新或写入数据库中
#     def _do_upinsert(self, conn, item, spider):
#         linkmd5id = self._get_linkmd5id(item)
#         #print linkmd5id
#         now = datetime.utcnow().replace(microsecond=0).isoformat(' ')
#         conn.execute("""
#                 select 1 from cnblogsinfo where linkmd5id = %s
#         """, (linkmd5id, ))
#         ret = conn.fetchone()

#         if ret:
#             conn.execute("""
#                 update cnblogsinfo set title = %s, description = %s, link = %s, listUrl = %s, updated = %s where linkmd5id = %s
#             """, (item['title'], item['desc'], item['link'], item['listUrl'], now, linkmd5id))
#             #print """
#             #    update cnblogsinfo set title = %s, description = %s, link = %s, listUrl = %s, updated = %s where linkmd5id = %s
#             #""", (item['title'], item['desc'], item['link'], item['listUrl'], now, linkmd5id)
#         else:
#             conn.execute("""
#                 insert into cnblogsinfo(linkmd5id, title, description, link, listUrl, updated) 
#                 values(%s, %s, %s, %s, %s, %s)
#             """, (linkmd5id, item['title'], item['desc'], item['link'], item['listUrl'], now))
#             #print """
#             #    insert into cnblogsinfo(linkmd5id, title, description, link, listUrl, updated)
#             #    values(%s, %s, %s, %s, %s, %s)
#             #""", (linkmd5id, item['title'], item['desc'], item['link'], item['listUrl'], now)
#     #获取url的md5编码
#     def _get_linkmd5id(self, item):
#         #url进行md5处理，为避免重复采集设计
#         return md5(item['link']).hexdigest()
#     #异常处理
#     def _handle_error(self, failue, item, spider):
#         log.err(failure)
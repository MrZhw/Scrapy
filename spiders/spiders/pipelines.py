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
from scrapy.exceptions import DropItem
import socket,sys,os
from scrapy.http import Request
from scrapy.pipelines.images import ImagesPipeline
from scrapy.pipelines.files import FilesPipeline, FSFilesStore, S3FilesStore
class SpidersPipeline(object):
	def process_item(self, item, spider):
		return item 	

class ZimuFilesPipeline(FilesPipeline):
	# def file_path(self, request, response=None, info=None):
		# file_guid = request.url.split('/')[-1]
		# return 'full/%s' % (file_guid)
		# for file_name in item['file_names']:
		# 	return file_name
	
	def get_media_requests(self, item, info):
		for file_url in item['file_urls']:
			yield Request(file_url)

	def item_completed(self, results, item, info):
		file_paths = [x['path'] for ok, x in results if ok]
		if not file_paths:
			raise DropItem("Item contains no files")
		item['file_paths'] = file_paths
		return item
	
		
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

class StarPipeline(object):
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
		sql = "insert into star(url, chinese_name, english_name, used_name, nation, location, birthday, birthplace, height, weight, bloodType, constellation, graduateSchool, profession, company, representative, relatedStar, microblog, personal) values (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"
		tx.execute(sql, (item['url'], item['chinese_name'], item['english_name'], item['used_name'], item['nation'], item['location'], item['birthday'], item['birthplace'], item['height'], item['weight'], item['bloodType'], item['constellation'], item['graduateSchool'], item['profession'], item['company'], item['representative'], item['relatedStar'], item['microblog'], item['personal']))

	#异常处理
	def handle_error(self, failure):
		logging.error(failure)

class AnimalPipeline(object):
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
		# sql = "insert into star(url,category,chinese_name,pingyin,english_name,scientific_name,introduction,jie,men,gang,mu,ke,shu,zhong,length,height,weight,life,feeding,breed,habit,location,ecologicalHabit,growthBreed,subspeciesTaxonomy,knowledge,description,distribution,livingCondition,englishIntroduction,) values (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"
		# tx.execute(sql, (item['url'],item['category'],item['chinese_name'],item['pingyin'],item['english_name'],item['scientific_name'],item['introduction'],item['jie'],item['men'],item['gang'],item['mu'],item['ke'],item['shu'],item['zhong'],item['length'],item['height'],item['weight'],item['life'],item['feeding'],item['breed'],item['habit'],item['location'],item['ecologicalHabit'],item['growthBreed'],item['subspeciesTaxonomy'],item['knowledge'],item['description'],item['distribution'],item['livingCondition'],item['englishIntroduction']))
		sql = "insert into animal(url,category,chinese_name,english_name,scientific_name,introduction,length,height,weight,life,feeding,breed,habit,location,ecologicalHabit,growthBreed,subspeciesTaxonomy,knowledge,description,distribution,livingCondition,englishIntroduction,information) values (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"
		tx.execute(sql, (item['url'],item['category'],item['chinese_name'],item['english_name'],item['scientific_name'],item['introduction'],item['length'],item['height'],item['weight'],item['life'],item['feeding'],item['breed'],item['habit'],item['location'],item['ecologicalHabit'],item['growthBreed'],item['subspeciesTaxonomy'],item['knowledge'],item['description'],item['distribution'],item['livingCondition'],item['englishIntroduction'],item['information']))

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
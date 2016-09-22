# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy
from scrapy import Field, Item


class SinaspiderItem(scrapy.Item):
	# define the fields for your item here like:
	# name = scrapy.Field()
	pass

class TweetsItem(scrapy.Item):
	""" 微博信息 """
	_id = Field()  # 用户ID-微博ID
	ID = Field()  # 用户ID
	Content = Field()  # 微博内容
	PubTime = Field()  # 发表时间
	# Co_oridinates = Field()  # 定位坐标
	Tools = Field()  # 发表工具/平台
	Like = Field()  # 点赞数
	Comment = Field()  # 评论数
	Transfer = Field()  # 转载数

class CommentItem(scrapy.Item):
	"""评论信息"""
	_id = Field() 	# 用户ID-微博ID-评论ID
	ID = Field()   	# 用户ID-微博ID
	Content = Field()  # 评论内容
	Like = Field()	#点赞数



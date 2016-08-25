# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy
from scrapy.item import Item, Field


class SpidersItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    pass

class ChengyuSpidersItem(scrapy.Item):
	lemma = scrapy.Field()
	pronunciation = scrapy.Field()
	semantic = scrapy.Field()
	derivation = scrapy.Field()
	example = scrapy.Field()

class PoemSpidersItem(scrapy.Item):
	name = scrapy.Field()
	dynasty = scrapy.Field()
	poet = scrapy.Field()
	category = scrapy.Field()
	content = scrapy.Field()
	shangxi = scrapy.Field()


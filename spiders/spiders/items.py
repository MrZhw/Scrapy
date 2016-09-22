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

class StarSpidersItem(scrapy.Item):
	url = scrapy.Field()
	chinese_name = scrapy.Field()
	english_name = scrapy.Field()
	used_name = scrapy.Field()
	nation = scrapy.Field()
	location = scrapy.Field()
	birthday = scrapy.Field()
	birthplace = scrapy.Field()
	height = scrapy.Field()
	weight = scrapy.Field()
	bloodType = scrapy.Field()
	constellation = scrapy.Field()
	graduateSchool = scrapy.Field()
	profession = scrapy.Field()
	company = scrapy.Field()
	representative = scrapy.Field()
	microblog = scrapy.Field()
	relatedStar = scrapy.Field()
	personal = scrapy.Field()

class AnimalSpidersItem(scrapy.Item):
	url = scrapy.Field()
	category = scrapy.Field()
	chinese_name = scrapy.Field()
	#pingyin = scrapy.Field()
	english_name = scrapy.Field()
	scientific_name = scrapy.Field()
	introduction = scrapy.Field()
	# jie = scrapy.Field()
	# men = scrapy.Field()
	# gang = scrapy.Field()
	# mu = scrapy.Field()
	# ke = scrapy.Field()
	# shu = scrapy.Field()
	# zhong = scrapy.Field()
	length = scrapy.Field()
	height = scrapy.Field()
	weight = scrapy.Field()
	life = scrapy.Field()
	feeding = scrapy.Field()
	breed = scrapy.Field()
	habit = scrapy.Field()
	location = scrapy.Field()
	ecologicalHabit = scrapy.Field()
	growthBreed = scrapy.Field()
	subspeciesTaxonomy = scrapy.Field()
	knowledge = scrapy.Field()
	description = scrapy.Field()
	distribution = scrapy.Field()
	livingCondition = scrapy.Field()
	englishIntroduction = scrapy.Field()
	information = scrapy.Field()

class PlantSpidersItem(scrapy.Item):
	url = scrapy.Field()
	category = scrapy.Field()
	chinese_name = scrapy.Field()
	english_name = scrapy.Field()
	scientific_name = scrapy.Field()
	other_name = scrapy.Field()
	location = scrapy.Field()
	nomenclator = scrapy.Field()
	introduction = scrapy.Field()

class PlantNamesSpidersItem(scrapy.Item):
	url = scrapy.Field()
	chinese_name = scrapy.Field()
	latin_name = scrapy.Field()
	location = scrapy.Field()
	nomenclator = scrapy.Field()
	description = scrapy.Field()
		

class ZimuSpidersItem(scrapy.Item):
	file_urls = scrapy.Field()
	files = scrapy.Field()
	file_paths = scrapy.Field()

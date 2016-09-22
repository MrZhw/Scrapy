# -*- coding: utf-8 -*-

BOT_NAME = 'SinaSpider'

SPIDER_MODULES = ['SinaSpider.spiders']
NEWSPIDER_MODULE = 'SinaSpider.spiders'

DOWNLOAD_DELAY = 2

#COOKIES_ENABLED = False

DOWNLOADER_MIDDLEWARES = {
	'SinaSpider.middleware.UserAgentMiddleware': 401,
	'SinaSpider.middleware.CookiesMiddleware': 402,
}

ITEM_PIPELINES = {
	'SinaSpider.pipelines.MySQLPipeline': 300,
}

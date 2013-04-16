#encoding:utf8
'''
Created on 2013-4-15
@author: Administrator
'''

BOT_NAME = 'ChannelOneListSpider'
#SPIDER_MODULES = ['crawler.shc.fe.spiders_picture']
SPIDER_MODULES = ['spiders']
LOG_LEVEL = 'DEBUG'
DOWNLOAD_DELAY = 0.3
LOG_ENCODING = u'UTF-8'
LOG_FILE = u'fetch.log'
ITEM_PIPELINES = [
    'pipeline.CSVPipeline',
]

DOWNLOADER_MIDDLEWARES = {
    'middlewares.ProxyRetryMiddleWare':450,
    'scrapy.contrib.downloadermiddleware.retry.RetryMiddleware':None
}

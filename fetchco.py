# encoding=utf8
'''
Created on 2013-3-20
@author: corleone
'''
from scrapy.cmdline import execute
from scrapy.settings import CrawlerSettings

if __name__ == '__main__':
    import_modules = __import__('settings', globals={}
                                , locals={}, fromlist=['', ])
    settings = CrawlerSettings(import_modules)
    execute(['scrapy', 'crawl', 'ChannelOneListSpider', ], settings=settings)

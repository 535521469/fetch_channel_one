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
    
    proxies = []
    
    with open(u'proxy.txt', u'r') as f:
        proxies = map(str.strip, f.readlines())
    
    settings = CrawlerSettings(import_modules, values={u'proxies':proxies})
    execute(['scrapy', 'crawl', 'ChannelOneTVListSpider', ], settings=settings)
#    execute(['scrapy', 'crawl', 'ChannelOneMoiveListSpider', ], settings=settings)

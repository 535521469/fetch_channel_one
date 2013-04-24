# encoding=utf8
'''
Created on 2013-4-15
@author: corleone
'''
from scrapy import log
from scrapy.contrib.downloadermiddleware.retry import RetryMiddleware

class ProxyRetryMiddleWare(RetryMiddleware):

    def __init__(self, settings):
        RetryMiddleware.__init__(self, settings)

    def _retry(self, request, reason, spider):
        retries = request.meta.get('retry_times', 0)
        proxy = request.meta.get(u'proxy')
        if retries <= self.max_retry_times - 1:
            try:
                next_proxy = spider.get_next_proxy(request.cookies)
            except Exception:
                msg = (u'there is no proxy list in cookies %s ,please check')
                spider.log(msg, log.WARNING)
                return RetryMiddleware._retry(self, request, reason, spider)
            if proxy:
                msg = (u'proxy %s fail, use %s for the %srd time '
                       'retry') % (proxy, next_proxy, retries)
            else:
                msg = (u'request without proxy , use %s for the %srd time '
                       'retry') % (next_proxy, retries)
            spider.log(msg, log.INFO)
            request.meta[u'proxy'] = next_proxy 
            
        return RetryMiddleware._retry(self, request, reason, spider)
        
        
        
            

    
    

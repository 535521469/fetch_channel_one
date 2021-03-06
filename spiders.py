# encoding:utf8
'''
Created on 2013-4-15
@author: Administrator
'''
from items import MovieItem, ItemConst
from scrapy import log
from scrapy.http.request import Request
from scrapy.selector import HtmlXPathSelector
from scrapy.spider import BaseSpider
import itertools

class ChannelOneSpider(BaseSpider):
    
    name = u'ChannelOneSpider'
    
    home_page = u"http://www.1channel.ch"
    index_page = u'%s/index.php' % home_page

    def get_next_proxy(self, cookies):
        return cookies[u'proxies'].next()

class ChannelOneListSpider(ChannelOneSpider):

    name = u'ChannelOneListSpider'

    def parse(self, response):
        
        hxs = HtmlXPathSelector(response)
        block_a_tags = hxs.select('//div[@class="index_container"]//div[@class="index_item index_item_ie"]/a')
        
        cookies = response.request.cookies
        
        try:
            with open(u'fetched.txt', u'r') as f:
                fetched_urls = map(str.strip, f.readlines())
        except Exception:
            fetched_urls = []
        
        for idx, a_tag in enumerate(block_a_tags):
            
            href = a_tag.select('@href')
            
            with open(u'detail.txt', u'a') as f:
                f.write('%s@@@@@%s\n' % (response.url, self.home_page + href.extract()[0],))
            
            if self.home_page + href.extract()[0] in fetched_urls:
                continue
                
            yield Request(self.home_page + href.extract()[0],
                          ChannelOneDetailSpider().parse,
                          dont_filter=True,)
#                          meta={u'proxy':cookies[u'proxies'].next()},
#                          cookies=cookies
#                          )
        with open(u'text.html', u'w') as f:
            f.write(response.body)
        page_div_tag = hxs.select('//div[@class="pagination"]')
        try:
            current_page = page_div_tag.select('span[@class="current"]/text()').extract()[0]
        except Exception as e:
            current_page = 1
            with open(u'page.html', u'w') as f:
                f.write(response.body)
            print response.url
        next_page = '%s?page=%s' % (self.index_page, int(current_page) + 1)
        
        self.log(u"add next page %s " % next_page, log.INFO)
        
        yield Request(next_page, self.parse,
#                      meta={u'proxy':cookies[u'proxies'].next()},
                      cookies=cookies
                      )

class ChannelOneMoiveListSpider(ChannelOneListSpider):
    
    name = u'ChannelOneMoiveListSpider'
    
    def start_requests(self):
        cookies = build_cookies(self)
        page_no = 1721
        for i in range(1, page_no):
            yield Request('%s?page=%s' % (self.index_page, i),
                          self.parse, cookies=cookies,
                          meta={u'proxy':cookies[u'proxies'].next()},
                          )
        
class ChannelOneTVListSpider(ChannelOneListSpider):
    
    name = u"ChannelOneTVListSpider"
    
    def start_requests(self):
        cookies = build_cookies(self)
        page_no = 281
        yield Request(u'%s?tv=&page=1' % (self.index_page,), self.parse,
                      cookies=cookies,
                      )
        
    def parse(self, response):
        
        for req in ChannelOneListSpider().parse(response):
            if isinstance(req, Request):
                req.replace(url=u'%s%s' % (req.url, u'&tv='))

class ChannelOneDetailSpider(ChannelOneSpider):
    
    name = u'ChannelOneDetailSpider'
    
    def parse(self, response):
        
        with open(u'fetched.txt', u'a') as f:
            f.write(response.url + u'\n')
        
        hxs = HtmlXPathSelector(response)
        mi = MovieItem()
        
        url = response.url
        mi[ItemConst.url] = url
        
        title = hxs.select('//div[@class="stage_navigation movie_navigation"]//a/text()').extract()[0]
        mi[ItemConst.title] = title
        
        main_div_tag = hxs.select('//div[@class="movie_info"]')
        tr_tags = main_div_tag.select('//table/tr')
        try:
            desc = main_div_tag.select('//table/tr[1]//p/text()').extract()[0].strip().replace(u'\n', u'').replace(u'\r', u'')
            mi[ItemConst.desc] = desc
        except Exception:
            self.log(u'desc wrong %s' % url, log.CRITICAL)
        
        try:
            img = main_div_tag.select('//div[@class="movie_thumb"]/img/@src').extract()[0]
            mi[ItemConst.img] = img
        except Exception :
            self.log(u'img wrong %s' % url, log.CRITICAL)

        try:
            imdb = main_div_tag.select('//div[@class="mlink_imdb"]/a/@href').extract()[0]
            mi[ItemConst.imdb] = imdb
        except Exception :
            pass
        
        for strong_tag in tr_tags.select('//strong'):
            try:
                strong_val = strong_tag.select('text()').extract()[0]
            except Exception:
                continue
            if strong_val == u'Released:':
                td_val = strong_tag.select(u'parent::td/parent::tr/td[2]/text()').extract()[0]
                mi[ItemConst.released_date] = td_val
            elif strong_val == u'Runtime:':
                td_val = strong_tag.select(u'parent::td/parent::tr/td[2]/text()').extract()[0]
                mi[ItemConst.runtime] = td_val
            elif strong_val == u'Genres:':
                td_val = strong_tag.select(u'parent::td/parent::tr/td[2]//a/text()').extract()
                if len(td_val):
                    mi[ItemConst.category1] = td_val[0]
                if len(td_val) > 1:
                    mi[ItemConst.category2] = td_val[1]
                mi[ItemConst.genres] = u','.join(td_val)
            elif strong_val == u'Countries:':
                td_val = strong_tag.select(u'parent::td/parent::tr/td[2]//a/text()').extract()
                mi[ItemConst.conuntries] = u','.join(td_val)
            elif strong_val == u'Director:':
                td_val = strong_tag.select(u'parent::td/parent::tr/td[2]//a/text()').extract()
                mi[ItemConst.director] = u','.join(td_val)
            elif strong_val == u'Actors:':
                td_val = strong_tag.select(u'parent::td/parent::tr/td[2]//a/text()').extract()
                mi[ItemConst.actors] = u','.join(td_val)
        
        self.log(u"add %s" % url, log.INFO)
        yield mi
        
def build_cookies(self):
    ipproxies = self.settings[u'proxies']
    ipproxy_generator = itertools.cycle(ipproxies)
    cookies = {
               u'proxies':ipproxy_generator
               }
    return cookies

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

class ChannelOneSpider(BaseSpider):
    
    name = u'ChannelOneSpider'
    
    home_page = u"http://www.1channel.ch"
    index_page = u'%s/index.php' % home_page

class ChannelOneListSpider(ChannelOneSpider):
    
    name = u'ChannelOneListSpider'
    DOWNLOAD_DELAY = 1
    
    def start_requests(self):
        page_no = 1
        yield self.make_requests_from_url('%s?page=%s' % (self.index_page, page_no))

    def parse(self, response):
        
        hxs = HtmlXPathSelector(response)
        block_a_tags = hxs.select('//div[@class="index_container"]//div[@class="index_item index_item_ie"]/a')
        
        for a_tag in block_a_tags:
            href = a_tag.select('@href')
            yield Request(self.home_page + href.extract()[0],
                          ChannelOneDetailSpider().parse, dont_filter=True)
            
        page_div_tag = hxs.select('//div[@class="pagination"]')
        current_page = page_div_tag.select('span[@class="current"]/text()').extract()[0]
        
        next_page = '%s?page=%s' % (self.index_page, int(current_page) + 1)
        
        self.log(u"add next page %s " % next_page, log.INFO)
        
        yield Request(next_page, self.parse)
        

class ChannelOneDetailSpider(ChannelOneSpider):
    
    DOWNLOAD_DELAY = 2
    
    def parse(self, response):
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
            
                
                
                
        

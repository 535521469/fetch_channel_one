# encoding:utf8
'''
Created on 2013-4-15
@author: Administrator
'''
from scrapy.item import Item, Field

class MovieItem(Item):
    
    title = Field()
    released_date = Field()
    runtime = Field()
    genres = Field()
    conuntry = Field()
    director = Field()
    actors = Field()
    description = Field()
    category1 = Field()
    category2 = Field()
    img = Field()
    imdb = Field()
    url = Field()

class ItemConst(object):
    title = u'title'
    released_date = u'released_date'
    runtime = u'runtime'
    genres = u'genres'
    conuntries = u'conuntry'
    director = u'director'
    actors = u'actors'
    desc = u'description'
    category1 = u'category1'
    category2 = u'category2'
    img = u'img'
    imdb = u'imdb'
    url = u'url'
    

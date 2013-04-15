# encoding:utf8
'''
Created on 2013-4-15
@author: Administrator
'''
from items import ItemConst
from scrapy.contrib.exporter import CsvItemExporter

class CSVPipeline(object):

    def process_item(self, item, spider):
        self.csv_exporter.export_item(item)

    def open_spider(self, spider):
        filed_list = [ItemConst.title,
                        ItemConst.released_date,
                        ItemConst.runtime,
#                        ItemConst.genres,
                        ItemConst.conuntries,
                        ItemConst.director,
                        ItemConst.actors,
                        ItemConst.desc,
                        ItemConst.category1,
                        ItemConst.category2,
                        ItemConst.img,
                        ItemConst.imdb,
                        ItemConst.url,
                        ]
        
        with open(u'output.csv', u'w') :
            pass
        
        self.csv_exporter = CsvItemExporter(file(u'output.csv', u'a'),
                                            fields_to_export=filed_list,
                                            lineterminator=u'\n')

    def close_spider(self, spider):
        pass
        
        

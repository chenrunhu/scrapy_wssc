# -*- coding: utf-8 -*-
import scrapy

class BookItem(scrapy.Item):
    id = scrapy.Field()
    cateId = scrapy.Field()
    name = scrapy.Field()
    author = scrapy.Field()
    create_date = scrapy.Field()  ###
    isHot = scrapy.Field()  ###
    isSerial = scrapy.Field()  # "哈弗H5"
    status = scrapy.Field()  # "哈弗H5"
    lastUpdate = scrapy.Field()  # "经典版 2.0T 手动 两驱 精英型",
    describe = scrapy.Field()
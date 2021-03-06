# -*- coding: utf-8 -*-
import scrapy

class BookSubContentItem(scrapy.Item):
    id = scrapy.Field()
    bookId = scrapy.Field()
    title = scrapy.Field()
    content = scrapy.Field()
    createDate = scrapy.Field()
    linkUrl = scrapy.Field()
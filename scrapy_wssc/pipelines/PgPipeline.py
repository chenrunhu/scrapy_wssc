# -*- coding: utf-8 -*-

from scrapy_wssc.Item.BookContentItem import BookContentItem
from scrapy_wssc.Item.BookItem import BookItem
from scrapy_wssc.service.impl.BookServiceImpl import BookServiceImpl


class PgPipeline(object):
    def __init__(self):

        bookService = BookServiceImpl()
        self.bookService = bookService
        print u'=====初始化服务类完成====='


    def process_item(self, item, spider):
        if isinstance(item, BookItem):
            self.bookService.addBook(item)
        elif (item, BookContentItem):
            self.bookService.addBookContent(item)

        return item
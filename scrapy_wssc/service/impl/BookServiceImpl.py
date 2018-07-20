# -*- coding: utf-8 -*-

import psycopg2

from scrapy.utils.project import get_project_settings
from scrapy_wssc.service.BookService import BookService


class BookServiceImpl(BookService):

    def __init__(self):
        settings = get_project_settings()
        self.connection = psycopg2.connect(
            # database=settings.get('POSTGRES_DB'),
            # user=settings.get('POSTGRES_USER'),
            # password=settings.get('POSTGRES_PW'),
            # host=settings.get('POSTGRES_SERVER'),
            # port=settings.get('POSTGRES_PORT'),
            database='wsscdb',
            user='postgres',
            password='postgres',
            host='10.0.0.19',
            port='5432',
        )
        self.cursor = self.connection.cursor()

    def addBook(self,item):
        _sql = """INSERT INTO t_book(id,cate_id,name,author,create_date,is_hot,is_serial,status,last_update,describe,book_url)
                          VALUES ('%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s');""" % (
            item['id'], item['cateId'], item['name'], item['author'], item['create_date'], item['isHot'],
            item['isSerial'], item['status'], item['lastUpdate'], item['describe'], item['bookUrl'])
        try:
            self.cursor.execute(self.cursor.mogrify(_sql))
            self.connection.commit()

        except Exception, e:
            self.connection.rollback()
            print "Error: %s" % e


    def addBookContent(self,item):
        _sql = """INSERT INTO t_book_content(id,book_id,title,content,create_date,link_url)
                                      VALUES ('%s','%s','%s','%s','%s','%s');""" % (
            item['id'], item['bookId'], item['title'], item['content'], item['createDate'], item['linkUrl'])
        try:
            self.cursor.execute(self.cursor.mogrify(_sql))
            self.connection.commit()
        except Exception, e:
            self.connection.rollback()
            print "Error: %s" % e

    def addBookSubContent(self, item):
        _sql = """INSERT INTO t_book_sub_content(id,book_id,title,content,create_date,link_url)
                                              VALUES ('%s','%s','%s','%s','%s','%s');""" % (
            item['id'], item['bookId'], item['title'], item['content'], item['createDate'], item['linkUrl'])
        try:
            self.cursor.execute(self.cursor.mogrify(_sql))
            self.connection.commit()
        except Exception, e:
            self.connection.rollback()
            print "Error: %s" % e

    def isExistBookInfo(self,bookId):
        print('')

    def getLastUpdatechapter(self,bookId):
        _sql = """  SELECT id,link_url from t_book_content WHERE book_id = '%s' order by id limit 1;
        """ % (bookId)
        try:
            self.cursor.execute(self.cursor.mogrify(_sql))
            rows = self.cursor.fetchall()
            for row in rows:
                #print('id=' + str(row[0]) + ' link_url=' + str(row[1]))
                return row

        except Exception, e:
            self.connection.rollback()
            print "Error: %s" % e


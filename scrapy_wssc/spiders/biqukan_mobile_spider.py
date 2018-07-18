# -*- coding: utf-8 -*-
import re
import datetime

import bs4
import scrapy

from scrapy_wssc.Item.BookContentItem import BookContentItem
from scrapy_wssc.Item.BookItem import BookItem


class biqukan_mobile_spider(scrapy.Spider):
    name = 'biqukan_mobile_spider'

    def __init__(self, bid=None):

        super(biqukan_mobile_spider, self).__init__()
        self.start_urls = ['http://m.biqukan.com/sort/1_1/'] #玄幻小说  2
        self.allowed_domain = 'm.biqukan.com'


    def parse(self, response):
        soup = bs4.BeautifulSoup(response.text, 'lxml')

        book_list = soup.select('ul[class="lis"] li')
        for li in book_list:
            book_href = li.select('span[class="s2"] a')[0].get('href')

            yield scrapy.Request(url=u'http://m.biqukan.com'+book_href,callback=self.get_book_info, meta={"cateId":2,"book_href":book_href})

    def get_book_info(self, response):
        pattern = re.compile(r'(\/\d+\/)(\d+)')  # 用于匹配书的id
        soup = bs4.BeautifulSoup(response.text, 'lxml')

        bookItem = BookItem();
        bookItem['id'] = pattern.search(response.meta['book_href']).group(2)
        bookItem['cateId'] = response.meta['cateId']
        bookItem['name'] = soup.select('div[class="book_info"] div[class="book_box"] dl dt[class="name"]')[0].string
        bookItem['author'] = soup.select('div[class="book_info"] div[class="book_box"] dl dd[class="dd_box"] span')[0].string.split(u'：' )[1]
        bookItem['isHot'] = True
        bookItem['isSerial'] = True
        bookItem['status'] = 1
        bookItem['lastUpdate'] = soup.select('div[class="book_info"] div[class="book_box"] dl dd')[2].span.string.split(u'：' )[1]
        bookItem['describe'] = soup.select('div[class="book_about"] dl dd')[0].get_text() #使用get_text可以提取该标签里包含的标签
        bookItem['bookUrl'] = response.request.url
        bookItem['create_date'] = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')

        yield bookItem

        book_content_list = response.xpath('//div[@id="list"]/dl/dd')
        for con_li in book_content_list:
            con_url =  con_li.xpath('a/attribute::href').extract()[0]
            if con_url.startswith('/book/'):
                yield scrapy.Request(url='https://www.qu.la' + con_url, callback=self.get_book_content,
                                     meta={'url': 'https://www.qu.la' + con_url, "bookId": bookItem["id"]})


    def get_book_content(self,response):
        pattern = re.compile(r'^(https://www.qu.la/.*?)(\d+)(.html)$')

        soup = bs4.BeautifulSoup(response.text, 'lxml')
        bookContentItem = BookContentItem();
        bookContentItem['id'] = pattern.search(response.meta['url']).group(2)
        bookContentItem['bookId'] =  response.meta['bookId']
        bookContentItem['title'] =  soup.find('div',attrs={"class":"bookname"}).h1.get_text()
        bookContentItem['content'] = soup.find('div',id="content").get_text()
        bookContentItem['linkUrl'] = response.meta['url']
        bookContentItem['createDate'] = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        yield bookContentItem



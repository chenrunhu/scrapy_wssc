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

        first_book_content = soup.select('div[class="books"] div[class="book_last"]')[1].dl.find_all('dd')[0]
        book_content_href = first_book_content.select('a')[0].get('href')
        yield scrapy.Request(url=u'http://m.biqukan.com' + book_content_href, callback=self.get_book_content,
                             meta={ "bookId": bookItem["id"],"book_content_href":book_content_href,"book_href":response.meta['book_href']})


    def get_book_content(self,response):
        pattern1 = re.compile(r'^\/(\d+)\/(\d+)\/(\d+).html$') #没有子页
        pattern2 = re.compile(r'^\/(\d+)\/(\d+)\/(\d+_?\d+).html$')#有子页

        soup = bs4.BeautifulSoup(response.text, 'lxml')
        bookContentItem = BookContentItem();

        book_content_href = response.meta['book_content_href']
        if re.match(pattern1, book_content_href, flags=0):
            bookContentItem['id'] = pattern1.search(book_content_href).group(3)
            bookContentItem['title'] = soup.select('div[class="header"] span[class="title"]')[0].string.split(u'_')[0].strip()
        elif re.match(pattern2, book_content_href, flags=0):
            bookContentItem['id'] = pattern2.search(book_content_href).group(3).split("_")[0]
            bookContentItem['title'] = soup.select('div[class="header"] span[class="title"]')[0].string.split(u'_')[0].strip()+u'（第'+ pattern2.search(book_content_href).group(3).split("_")[1] +u'页）'

        bookContentItem['bookId'] =  response.meta['bookId']
        bookContentItem['content'] = soup.find('div',id="chaptercontent").get_text()
        bookContentItem['linkUrl'] = response.request.url
        bookContentItem['createDate'] = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        yield bookContentItem

        next_content_href = soup.select('p[class="Readpage"] a[id="pb_next"]')[0].get('href')
        if next_content_href != response.meta['book_href']:
            yield scrapy.Request(url=u'http://m.biqukan.com' + next_content_href, callback=self.get_book_content,
                             meta={"bookId":response.meta['bookId'], "book_content_href": next_content_href,"book_href":response.meta['book_href']})



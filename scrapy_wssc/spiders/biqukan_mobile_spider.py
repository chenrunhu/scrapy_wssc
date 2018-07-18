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

            #爬取章节
            yield scrapy.Request(url=u'http://m.biqukan.com'+book_href,callback=self.get_book_info, meta={"cateId":2,"book_href":book_href})

    def get_book_info(self, response):
        pattern = re.compile(r'(\/\d+\/)(\d+)')  # 用于匹配书的id
        soup = bs4.BeautifulSoup(response.text, 'lxml')

        bookItem = BookItem();
        bookItem['id'] = pattern.search(soup.find('div',id="info").find('a',{"style":"color:red;"}).attrs['href']).group()
        bookItem['cateId'] = response.meta['cateId']
        bookItem['name'] = soup.find('div',id="info").h1.get_text()
        bookItem['author'] = soup.find('div',id="info").p.get_text().split(u'：' )[1]
        bookItem['isHot'] = True
        bookItem['isSerial'] = True
        bookItem['status'] = 1
        bookItem['lastUpdate'] = soup.find('div',id="info").find_all('p')[2].get_text().split(u'：' )[1]
        bookItem['describe'] = soup.find('div',id="intro").get_text().replace(" ", "")
        bookItem['bookUrl'] = response.request.url
        bookItem['create_date'] = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')

        # LastUpdatechapter = self.bookService.getLastUpdatechapter(bookItem["id"])
        # if(LastUpdatechapter == None):
        #     #print '本书还未采集！！！'
        #     #bookContentUrl = response.xpath('//div[@id="list"]/dl/dt')[1].xpath('dd')[0].xpath('a/attribute::href').extract()[0]
        #     bookContentUrl = soup.find('div', id="list").dl.find_all('dt')[1].next_sibling.next_sibling.a.attrs['href']
        #     if bookContentPatten.search(bookContentUrl) :
        #         bookContentUrl = response.request.url + bookContentPatten.search(bookContentUrl).group()
        #     else:
        #         bookContentUrl = 'https://www.qu.la' + bookContentUrl
        #     firstChapterUrl = bookContentUrl
        #     print u'书名：'+ bookItem['name']+ u',第一章地址：'+firstChapterUrl
        # else:
        #     print '本编号：'+str(LastUpdatechapter[0]) + ',章节地址：'+str(LastUpdatechapter[1])
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



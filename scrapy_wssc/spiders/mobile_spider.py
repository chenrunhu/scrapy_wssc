# -*- coding: utf-8 -*-
import re
import datetime

import bs4
import scrapy

from scrapy_wssc.Item.BookContentItem import BookContentItem
from scrapy_wssc.Item.BookItem import BookItem


class mobile_spider(scrapy.Spider):
    name = 'mobile_spider'

    def __init__(self, bid=None):
        """初始化起始页面和游戏bid
        """
        super(mobile_spider, self).__init__()
        self.bid = bid  # 参数bid由此传入
        self.start_urls = ['https://m.qu.la/wapsort/4_1.html'] #历史小说  1
                           #'https://www.qu.la/xuanhuanxiaoshuo/',#玄幻小说  2
                          # 'https://www.qu.la/dushixiaoshuo/'] #都市小说  3
        self.allowed_domain = 'm.qu.la'
        #self.driver = webdriver.Chrome(
         #   executable_path="C:/Program Files (x86)/Google/Chrome/Application/chromedriver.exe")
        #self.driver.set_page_load_timeout(10)  # throw a TimeoutException when thepage load time is more than 5 seconds.

        #self.bookService = BookServiceImpl()

    def parse(self, response):
        pattern = re.compile(r'\d+')

        book_list = response.xpath('//div[@class="recommend"]/div[@id="main"]/div')
        for li in book_list:
            bookItem = BookItem();
            bookItem['id'] = pattern.search(li.xpath('a/@href').extract()[0]).group()
            bookItem['cateId'] = 1
            bookItem['name'] = li.xpath('a/p[@class="title"]/text()').extract()[0].strip()
            bookItem['author'] = li.xpath('a/p[@class="author"]/text()').extract()[0].split(u'：')[1]
            bookItem['isHot'] = True
            bookItem['isSerial'] = True
            bookItem['status'] = 1
            bookItem['lastUpdate'] = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            bookItem['describe'] = li.xpath('p[@class="review"]/text()').extract()[1].split(u'：')[1].strip()
            bookItem['bookUrl'] = 'https://m.qu.la'+li.xpath('a/@href').extract()[0]
            bookItem['create_date'] = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            yield bookItem

            #爬取章节
            yield scrapy.Request(url='https://m.qu.la/booklist/'+bookItem['id']+'.html',callback=self.get_book_chapter_list, meta={"cateId":1})

    def get_book_chapter_list(self,response):
        soup = bs4.BeautifulSoup(response.text, 'lxml')
        chapterList = soup.find('div',id="chapterlist").p
        for chapter in chapterList:
            pass

    def get_book_info(self, response):
        pattern = re.compile(r'\d+')
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



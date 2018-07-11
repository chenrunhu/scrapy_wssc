# -*- coding: utf-8 -*-
import re
import datetime

import requests
import bs4
import scrapy
from scrapy.spider import BaseSpider
import scrapy
from scrapy.http import Request
from scrapy_wssc.BookItem import BookItem
import time
import base64
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait

class ls_wb_spider(scrapy.Spider):
    name = 'ls_wb_spider'

    def __init__(self, bid=None):
        """初始化起始页面和游戏bid
        """
        super(ls_wb_spider, self).__init__()
        self.bid = bid  # 参数bid由此传入
        self.start_urls = ['https://www.qu.la/lishixiaoshuo/']
        self.allowed_domain = 'www.qu.la'
        #self.driver = webdriver.Chrome(
         #   executable_path="C:/Program Files (x86)/Google/Chrome/Application/chromedriver.exe")
        #self.driver.set_page_load_timeout(10)  # throw a TimeoutException when thepage load time is more than 5 seconds.

    def parse(self, response):
        """模拟浏览器实现翻页，并解析每一个话题列表页的url_list
        """
        # url_set = set()  # 话题url的集合
        # self.driver.get(response.url)
        #
        # wait = WebDriverWait(self.driver, 10)
        # wait.until(
        #     #  等价于 def getA(x) {  return  x.find_element_by_xpath('//ul[@class="post-list"]/li[@class]/a')) }
        #     lambda x: x.find_element_by_xpath('//div[@id="newscontent"]/div[@class="l"]/ul'))  # VIP，内容加载完成后爬取
        sel_list = response.xpath('//div[@id="newscontent"]/div[@class="l"]/ul/li')
        for li in sel_list:
            #book_desc_html = self.get_book_desc('https://www.qu.la'+li.xpath('span[@class="s2"]/a/attribute::href').extract()[0])
            #soup = bs4.BeautifulSoup(book_desc_html, 'lxml')
            yield  scrapy.Request(url='https://www.qu.la'+li.xpath('span[@class="s2"]/a/attribute::href').extract()[0],callback=self.get_book_info)

    def get_book_info(self, response):
        pattern = re.compile(r'\d+')
        soup = bs4.BeautifulSoup(response.text, 'lxml')

        bookItem = BookItem();
        bookItem['id'] = pattern.search(soup.find('div',id="info").find('a',{"style":"color:red;"}).attrs['href']).group()
        bookItem['cateId'] = 1
        # bookItem['name'] = li.find_element_by_xpath('//li/span[@class="s4"]').text
        # bookItem['author'] = li.find_element_by_xpath('//li/span[@class="s4"]').text
        bookItem['name'] = li.xpath('span[@class="s2"]/a/text()').extract()[0]
        bookItem['author'] = li.xpath('span[@class="s4"]/text()').extract()[0]
        bookItem['isHot'] = True
        bookItem['isSerial'] = True
        bookItem['status'] = 1
        bookItem['lastUpdate'] = datetime.datetime.now().strftime('%Y-') + \
                                 li.xpath('span[@class="s5"]/text()').extract()[0]
        # bookItem['describe'] = soup.find(name='div', attrs={'id': 'intro'}).string
        bookItem['describe'] = ''
        bookItem['bookUrl'] = 'https://www.qu.la' + li.xpath('span[@class="s2"]/a/attribute::href').extract()[0]
        bookItem['create_date'] = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        try:
            r = requests.get(url, timeout=30)
            r.raise_for_status
            r.encoding = r.apparent_encoding
            # r.encoding = 'utf-8'
            return r.text
        except:
            print("Open Error!!!")


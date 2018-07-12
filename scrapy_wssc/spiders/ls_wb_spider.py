# -*- coding: utf-8 -*-
import re
import datetime

import bs4
import scrapy

from scrapy_wssc.Item.BookContentItem import BookContentItem
from scrapy_wssc.Item.BookItem import BookItem


class ls_wb_spider(scrapy.Spider):
    name = 'ls_wb_spider'

    def __init__(self, bid=None):
        """初始化起始页面和游戏bid
        """
        super(ls_wb_spider, self).__init__()
        self.bid = bid  # 参数bid由此传入
        self.start_urls = ['https://www.qu.la/lishixiaoshuo/'] #历史小说  1
                           #'https://www.qu.la/xuanhuanxiaoshuo/',#玄幻小说  2
                          # 'https://www.qu.la/dushixiaoshuo/'] #都市小说  3
        self.allowed_domain = 'www.qu.la'
        #self.driver = webdriver.Chrome(
         #   executable_path="C:/Program Files (x86)/Google/Chrome/Application/chromedriver.exe")
        #self.driver.set_page_load_timeout(10)  # throw a TimeoutException when thepage load time is more than 5 seconds.

        #self.bookService = BookServiceImpl()

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
        book_list = response.xpath('//div[@id="newscontent"]/div[@class="l"]/ul/li')
        for li in book_list:
            #book_desc_html = self.get_book_desc('https://www.qu.la'+li.xpath('span[@class="s2"]/a/attribute::href').extract()[0])
            #soup = bs4.BeautifulSoup(book_desc_html, 'lxml')
            cateName = li.xpath('span[@class="s1"]/text()').extract()[0]
            cateId = 2
            if cmp(cateName,u'[历史军事]') == 0 :
                cateId = 1
            elif cmp(cateName,u'[玄幻奇幻]') == 0:
                cateId = 2
            elif cmp(cateName, u'[都市言情]') == 0:
                cateId = 3
            yield scrapy.Request(url='https://www.qu.la'+li.xpath('span[@class="s2"]/a/attribute::href').extract()[0],callback=self.get_book_info, meta={"cateId":cateId})

    def get_book_info(self, response):
        pattern = re.compile(r'\d+')
        #bookContentPatten = re.compile(r'^\d+.html')

       # print response.text
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



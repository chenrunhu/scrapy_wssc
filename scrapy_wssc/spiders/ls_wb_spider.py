# -*- coding: utf-8 -*-
import scrapy
from scrapy.spider import BaseSpider
import scrapy
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
        self.driver = webdriver.Chrome(
            executable_path="C:/Program Files (x86)/Google/Chrome/Application/chromedriver.exe")
        self.driver.set_page_load_timeout(10)  # throw a TimeoutException when thepage load time is more than 5 seconds.

    def parse(self, response):
        """模拟浏览器实现翻页，并解析每一个话题列表页的url_list
        """
        url_set = set()  # 话题url的集合
        self.driver.get(response.url)
        while True:
            wait = WebDriverWait(self.driver, 5)
            wait.until(
                #  等价于 def getA(x) {  return  x.find_element_by_xpath('//ul[@class="post-list"]/li[@class]/a')) }
                lambda x: x.find_element_by_xpath('//ul[@class="post-list"]/li[@class]/a'))  # VIP，内容加载完成后爬取
            sel_list = self.driver.find_elements_by_xpath('//ul[@class="post-list"]/li[@class]/a')
            url_list = [sel.get_attribute("href") for sel in sel_list]
            url_set |= set(url_list)
            try:
                wait = WebDriverWait(self.driver, 10)
                wait.until(lambda driver: driver.find_element_by_xpath(
                    '//ul[@class="pg1"]/li[@class="pg_next"]'))  # VIP，内容加载完成后爬取
                next_page = self.driver.find_element_by_xpath('//ul[@class="pg1"]/li[@class="pg_next"]')
                next_page.click()  # 模拟点击下一页
            except:
                print "#####Arrive thelast page.#####"
                break

# coding:utf-8
from selenium import webdriver
from selenium.webdriver.support.wait import WebDriverWait

driver = webdriver.Chrome(
            executable_path="C:/Program Files (x86)/Google/Chrome/Application/chromedriver.exe")
driver.get("http://www.baidu.com")
# 等待时长10秒，默认0.5秒询问一次
WebDriverWait(driver, 10).until(lambda x: x.find_element_by_id("kw")).send_keys("yoyo")
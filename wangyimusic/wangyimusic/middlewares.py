# -*- coding: utf-8 -*-
import random
import time
from selenium import webdriver
from scrapy.http import HtmlResponse

class UserAgentMiddleware(object):
    """ 换User-Agent """
    def process_request(self, request, spider):
        agents = [
    "Mozilla/5.0 (Linux; U; Android 2.3.6; en-us; Nexus S Build/GRK39F) AppleWebKit/533.1 (KHTML, like Gecko) Version/4.0 Mobile Safari/533.1",
    "Avant Browser/1.2.789rel1 (http://www.avantbrowser.com)",
    "Mozilla/5.0 (Windows; U; Windows NT 6.1; en-US) AppleWebKit/532.5 (KHTML, like Gecko) Chrome/4.0.249.0 Safari/532.5",
    "Mozilla/5.0 (Windows; U; Windows NT 5.2; en-US) AppleWebKit/532.9 (KHTML, like Gecko) Chrome/5.0.310.0 Safari/532.9",
    "Mozilla/5.0 (Windows NT 6.1; Win64; x64; rv:2.0.1) Gecko/20100101 Firefox/4.0.1",
    "Mozilla/5.0 (Windows NT 5.1; rv:5.0) Gecko/20100101 Firefox/5.0",
    "Mozilla/5.0 (Windows NT 6.1; WOW64; rv:6.0a2) Gecko/20110622 Firefox/6.0a2",
    "Mozilla/5.0 (Windows NT 6.1; WOW64; rv:7.0.1) Gecko/20100101 Firefox/7.0.1",
    "Mozilla/5.0 (Windows NT 6.1; WOW64; rv:2.0b4pre) Gecko/20100815 Minefield/4.0b4pre",
    "Mozilla/4.0 (compatible; MSIE 5.5; Windows NT 5.0 )",
    "Mozilla/4.0 (compatible; MSIE 5.5; Windows 98; Win 9x 4.90)",
    "Mozilla/5.0 (Windows; U; Windows XP) Gecko MultiZilla/1.6.1.0a",
    "Mozilla/2.02E (Win95; U)"]
        agent = random.choice(agents)
        request.headers["User-Agent"] = agent
        
class JavaScriptMiddleware(object):
    """使用PhantomJS"""
    def process_request(self, request, spider):
        print("spider.name",spider.name)
        #if spider.name[-2:] == "JS":
        print(">>>PhantomJS is starting...")
        driver = webdriver.PhantomJS()
        driver.set_window_size(1120, 550)
        driver.get(request.url)
        time.sleep(3)
        driver.switch_to.frame(0)
        #driver.switch_to.frame(driver.find_element_by_xpath("//iframe"))
        body = driver.page_source.replace(u'\xa9',u'') #去除版权符号
        #print(">>>",body)
        current_url = driver.current_url
        driver.close()
        return HtmlResponse(current_url, body=body, encoding="utf-8", request=request)
# -*- coding: utf-8 -*-
import time
import re
import datetime
from scrapy.spider import CrawlSpider
from scrapy.selector import Selector
from scrapy.http import Request
from wangyimusic.items import SongsItem
from selenium import webdriver

class Spider(CrawlSpider):
    name = "wangyi"
    host = "http://music.163.com/#/discover/artist"
    start_urls = [
        "http://music.163.com/#/discover/artist",
    ]
    scrawl_url = set()  # 记录待爬的歌手ID
    songs_url = set() #记录待爬歌曲
    
    def __init__(self):
        self.driver = webdriver.PhantomJS()
        self.driver.set_window_size(1120, 550)
    def parse(self, response):
        """获取热门歌手"""
        #print(">>>正在打开网页")
        self.driver.get("http://music.163.com/#/discover/artist")
        self.driver.switch_to.frame(self.driver.find_element_by_xpath("//iframe"))
        #print(">>>网页已打开")
        Singers = SongsItem()
        singer_item = self.driver.find_element_by_xpath('//*[@id="m-artist-box"]').find_elements_by_xpath(".//a[1]")
        for singer in singer_item[:20]:
            if len(singer.text) > 0:
                Singers['Singer'] = singer.text
                Singers["SingerHref"] = singer.get_attribute("href")
                self.scrawl_url.add(singer.get_attribute("href"))
                print(">>>",Singers['Singer'])
                yield Singers
        print(self.scrawl_url)
        url = self.scrawl_url.pop()
        yield Request(url=url,callback=self.parse1)  #爬取个人歌曲
    
    def parse1(self, response):
        """ 抓取歌手歌曲 """
        print(">>>歌曲",len(self.scrawl_url))
        #print(">>>正在打开网页:%s" % response.url)
        self.driver.get(response.url)
        time.sleep(15)
        self.driver.switch_to.frame(self.driver.find_element_by_xpath("//iframe"))
        Songs = SongsItem()
        song_datas = self.driver.find_elements_by_xpath("//span[@class='txt']")
        num = 1 #记录歌曲数目，验证是否爬取完整
        for data in song_datas:
            song_url = data.find_element_by_xpath(".//a").get_attribute("href")
            song_name = data.find_element_by_xpath(".//b").text
            print(">>>",num)
            num += 1
            self.songs_url.add(song_url)
            yield Songs
        if len(self.scrawl_url) > 0:
            url = self.scrawl_url.pop()
            yield Request(url=url,callback=self.parse1)
        elif len(self.songs_url) > 0:
            song_url = self.songs_url.pop()
            yield Request(url=song_url,callback=self.parse2)
    def parse2(self, response):
        """抓取评论数"""
        #print(">>>评论",len(self.scrawl_url))
        self.driver.get(response.url)
        time.sleep(5)
        self.driver.switch_to.frame(self.driver.find_element_by_xpath("//iframe"))
        flag_datas = self.driver.find_element_by_xpath("//span[@class='j-flag']").text
        flag_song = self.driver.find_element_by_xpath("//em[@class='f-ff2']").text
        print(len(self.songs_url),">>>",flag_datas,response.url)
        if len(self.songs_url) > 0:
            song_url = self.songs_url.pop()
            yield Request(url=song_url,callback=self.parse2)
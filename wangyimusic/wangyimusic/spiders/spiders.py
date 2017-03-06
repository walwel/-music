# -*- coding: utf-8 -*-

import re
import datetime
import scrapy
from scrapy.selector import Selector
from wangyimusic.items import SongsItem

class MySpider(scrapy.spiders.Spider):
    name = "wangyiJS"
    host = "http://music.163.com/#/discover/artist"
    start_urls = [
        "http://music.163.com/#/discover/artist",
    ]

    def parse(self, response):
        """获取热门歌手"""
        Singers = SongsItem()
        selector = Selector(response)
        singer_items = selector.xpath('//*[@id="m-artist-box"]').extract()
        #print(">>>",singer_items[0].replace(u"\xa0",u""))
        if len(singer_items) > 0:
            singer_item = Selector(text=singer_items[0]).xpath("//a[1]").extract()
            #print(">>>",singer_item)
            for singer in singer_item:
                text = re.match(r"<a .*?>(.*?)</a>",singer)
                if len(text.groups()[0]) > 0:
                    Singers['Singer'] = text.groups()[0]
                    Singers["SingerHref"] = re.match(r'<a href="(.*?)" class=.*?</a>',singer).groups()[0]
                    print(">>>歌手&主页",Singers['Singer'],Singers["SingerHref"])
                    #yield Singers
                    yield scrapy.Request(url="http://music.163.com/#" + Singers["SingerHref"], meta={'item':Singers}, callback=self.parse1)  #爬取个人歌曲
    def parse1(self, response):
        """获取歌手主页歌曲"""
        Songs = response.meta["item"]
        selector = Selector(response)
        song_items = selector.xpath('//span[@class="txt"]').extract()
        print("song_items",len(song_items))
        #if len(song_items) > 0:
        for song in song_items:
            song = song.replace(u"\xa0",u"")
            Songs["SongHref"], Songs["SongName"] = re.match(r'<span .*?><a href="(.*?)"><b .*?>(.*?)</b></a>',song).groups()
            print(">>>歌曲&主页",Songs["SongHref"], Songs["SongName"])
            url="http://music.163.com/#" + Songs["SongHref"]
            print(">>>url",url)
            yield scrapy.Request(url=url, meta={'items':Songs}, callback=self.parse2)
    def parse2(self, response):
        """获取歌曲信息"""
        print("parse2")
        Songs = response.meta["items"]
        selector = Selector(response)
        flag = selector.xpath('//span[@class="j-flag"]/text()').extract()
        if len(flag) > 0:
            Songs["SongFlag"] = flag[0]
            print(">>>评论",Songs["SongFlag"])
            yield Songs
            print("<<<parse2")
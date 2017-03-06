# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

from scrapy import Field, Item

class SongsItem(Item):
    '''获取歌曲信息'''
    Singer = Field() #歌手
    SingerHref = Field() #歌手主页地址
    SongName = Field() #歌曲名称
    SongHref = Field() #歌曲主页
    SongFlag = Field() #歌曲评论数
    
    

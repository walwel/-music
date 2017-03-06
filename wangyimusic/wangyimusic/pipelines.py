# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html

from items import SongsItem
import pymysql

class WangyimusicPipeline(object):
    def __init__(self):
        self.conn = pymysql.connect(host="127.0.0.1", 
                                    user="root", 
                                    passwd="",                                    
                                    port=3306,
                                    db="WangYiMusic",
                                    charset="utf8")
    def process_item(self, item, spider):
        try:
            if isinstance(item, SongsItem):
                print(">>>","歌手："+item["Singer"]+"主页：" + item["SingerHref"] + "歌曲：" + item["SongName"] + "ID:" + item["SongHref"] + "评论数：" +item["SongFlag"])
            return item
        except Exception as err:
            print(">>>",err)
    def close_spider(self):
        self.conn.close()

# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html
from huanqiuwang.settings import mongodb_sheet,mongodb_name,mongodb_port,mongodb_host
import pymongo

class HuanqiuwangPipeline(object):
    def __init__(self):
        host = mongodb_host
        port = mongodb_port
        dbname = mongodb_name
        sheetname = mongodb_sheet
        cur = pymongo.MongoClient(host=host, port=port)
        mydb = cur[dbname]
        self.post = mydb[sheetname]

    def process_item(self, item, spider):
        data = dict(item)
        self.post.insert(data)
        return item

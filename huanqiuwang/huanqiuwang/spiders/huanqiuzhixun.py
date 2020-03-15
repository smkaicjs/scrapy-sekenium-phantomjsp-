# -*- coding: utf-8 -*-
from scrapy import Spider,Request

from huanqiuwang.items import HuanqiuwangItem

class HuanqiuzhixunSpider(Spider):
    name = 'huanqiuzhixun'
    allowed_domains = ['world.huanqiu.com']



    start_urls = ['http://world.huanqiu.com/']

    def parse(self, response):

        url = response.xpath("//div[@class='all-con']//div[@class='m-recommend-con']//ul/li/a/@href").extract()
        start_list = []
        headers = {'Accept': 'image/webp,image/apng,image/*,*/*;q=0.8',
                   'Accept-Encoding': 'gzip, deflate, br',
                   'Accept-Language': 'zh-CN,zh;q=0.9',
                   'Connection': 'keep-alive',
                   'Cookie': 'BIDUPSID=88AFE2D4DB89CEBF7161EA3C4F3A414A; PSTM=1583734446; BAIDUID=88AFE2D4DB89CEBF14DDD7474A084F6A:FG=1; BDORZ=B490B5EBF6F3CD402E515D22BCDA1598; H_PS_PSSID=30963_1442_21083_30824_30717; delPer=0; PSINO=6',
                   'Host': 'eclick.baidu.com',
                   'Referer': 'https://world.huanqiu.com/',
                   }

        for ll in url:
            urls_list = 'http://world.huanqiu.com/'+ll
            start_list.append(urls_list)
            for ss in start_list:
                yield Request(ss,headers=headers,callback=self.start_parse)

    def start_parse(self,response):
        item = HuanqiuwangItem()
        item['title'] = response.xpath("//div[@class='t-container-title']//text()").extract()
        item['content'] = response.xpath("//section//p//text()").extract()
        print("*"*66)
        print("蜘蛛一完成下载")
        print("*" * 66)
        yield item



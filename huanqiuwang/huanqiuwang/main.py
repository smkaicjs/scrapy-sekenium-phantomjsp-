import os
import time
while True:
    os.system('scrapy crawl huanqiuzhixun')
    os.system('scrapy crawl chainzhixun')
    time.sleep(3600)
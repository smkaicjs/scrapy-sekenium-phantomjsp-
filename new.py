from multiprocessing import Pool
import os
import time
import csv
from lxml import etree
import requests
from urllib import parse
from selenium import webdriver
from multiprocessing import Manager
#从首页获取分栏urls
def first_url_page_all(url,url_funtion_list):

    response = requests.get(url)
    response.encoding='utf-8'

    ele_list = etree.HTML(response.content)
    ele_list_page=ele_list.xpath("//div[@class='rTxt']/a/@href")
    for urls in ele_list_page:
        urls = parse.urljoin('http://',urls)
        url_funtion_list.put((urls,second_page))

    #print(start_urls)

#分栏页动态信息urls
def second_page(url,url_funtion_list):
    path = os.getcwd()

    driver = webdriver.PhantomJS(executable_path=path+'\phantomjs.exe')
    driver.get(url)
    driver.page_source.encode('utf-8')
    #second_page_list = []

    for res in driver.find_elements_by_xpath("//ul[@id='recommend']/li/a"):
        responses = res.get_attribute('href')
        url_funtion_list.put((responses,deta_page))


    driver.close()
    #return second_page_list
#详情页解析
def deta_page(url, url_funtion_list):
    try:
        response = requests.get(url)
        response.encoding = 'utf-8'
        responses = etree.HTML(response.content)

        title = responses.xpath("//div[@class='t-container-title']//text()")
        titles = ''.join(title)
        titles.replace(' ', '')
        content = responses.xpath("//section/p/text()")
        contents = ''.join(content)
        contents.replace('/n', '').replace(' ', '')
        sore = responses.xpath("//div[@class='metadata-info']/p//text()")
        sores = ''.join(sore).replace('/n', '').replace(' ', '')
        print('已经连接到数据，请等待几分钟完成爬取，然后在桌面会生成资讯.csv文件，请转化为utf-8-bom编码')
        list_all = []
        list_all.append([titles, sores, contents])
        with open('C:\\Users\\Administrator\\Desktop\\资讯.csv资讯.csv', 'a', encoding='utf-8') as csvfile:
            writer = csv.writer(csvfile)
            writer.writerows(list_all)
    except:
        print('出错的URL是：',url)



    #with open('环球网资讯（now）.csv','utf-8','wb') as f:
        #f.write()


if __name__ == '__main__':
    queue = Manager().Queue()
    url = 'https://www.huanqiu.com/'
    #first_url_page_all(url)
    #url_funtion_list = [(url,first_url_page_all)]
    queue.put((url,first_url_page_all))
    with open('C:\\Users\\Administrator\\Desktop\\资讯.csv', 'w',encoding='utf-8') as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(["标题","来源","内容"])
#解耦合，添加进程池
    #一般进程个数小于等于cpu数量*2
    pool = Pool(6)
    res_list = []
    while True:
        try:
            url,funct = queue.get(timeout=30)
            res = pool.apply_async(func=funct,args=(url,queue))
        #funct(url,url_funtion_list)
        ## list
            res_list.append(res)
        except:
            print('爬取完成')
            quit()

    pool.close
    pool.join()

''' while True:
       # for second_page_urls in first_url_page_all(url):
            second_page(second_page_urls)
            for deta_page_url in second_page(second_page_urls):
                deta_page(deta_page_url)
    time.sleep(3600)'''

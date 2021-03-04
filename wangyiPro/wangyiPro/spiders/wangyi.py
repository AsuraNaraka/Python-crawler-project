# -*- coding: utf-8 -*-
import scrapy
from selenium import webdriver
from wangyiPro.items import WangyiproItem


class WangyiSpider(scrapy.Spider):
    name = 'wangyi'
    # allowed_domains = ['https://news.163.com/']
    start_urls = ['https://news.163.com/']
    modules_urls = []  # 存储五个板块对应详情页的 url

    # 解析五大板块对应详情页的url
    # 实例化一个浏览器对象
    def __init__(self):
        self.bro = webdriver.Chrome()

    def parse(self, response):
        li_list = response.xpath('//*[@id="js_festival_wrap"]/div[3]/div[2]/div[2]/div[2]/div/ul/li')
        alist = [3, 4, 6, 7, 8]
        for index in alist:
            module_url = li_list[index].xpath('./a/@href').extract_first()
            self.modules_urls.append(module_url)  # 对每一个板块的 url 进行请求发送

        # 依次对每一个板块对应的页面进行请求
        for url in self.modules_urls:  # 对每一个板块的 url 进行请求发送
            yield scrapy.Request(url, callback=self.parse_module)

    # 每一个板块对应的新闻标题相关的内容都是动态加载
    def parse_module(self, response):  # 解析每一个板块页面中对应新闻的标题和新闻详情页的url
        # response.xpath()
        div_list = response.xpath('/html/body/div/div[3]/div[4]/div[1]/div/div/ul/li/div/div')
        for div in div_list:
            title = div.xpath('./div/div[1]/h3/a/text()').extract_first()
            new_detail_url = div.xpath('./div/div[1]/h3/a/@href').extract_first()

            # 进行请求传参，传给 WangyiproItem
            item = WangyiproItem()
            item['title'] = title

            # 对新闻详情页的 url 发起请求S
            yield scrapy.Request(url=new_detail_url, callback=self.parse_detail, meta={'item': item})

    def parse_detail(self, response):  # 解析新闻内容
        content = response.xpath(
            '//*[@id="content"]/div[2]/div/p/text() | //*[@id="content"]/div[2]/p/text()').extract()
        content = ''.join(content)
        item = response.meta['item']
        item['content'] = content

        yield item

    def closed(self, spider):
        self.bro.quit()

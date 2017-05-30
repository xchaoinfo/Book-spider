# -*- coding: utf-8 -*-

import scrapy
from BookSpider.items import AmazonSpiderItem
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import CrawlSpider, Rule
import re


class AmazonSpider(CrawlSpider):
    name = 'amazon'
    allowed_domains = ['amazon.cn']
    start_urls = ["https://www.amazon.cn/b/ref=sr_aj?node=658394051&ajr=0"]
    url_xpath = '//a[contains(@class, "s-color-twister-title-link")]'
    author_xpath = '//div[@id="refinementList"]'
    nextPage_xpath = '//a[@id="pagnNextLink"]'
    book_class_xpath = '//div[contains(@class, "browseBox")]/ul[2]'
    rules = (
        # Rule(LinkExtractor(restrict_xpaths=(author_xpath,)), follow=True),
        # Rule(LinkExtractor(restrict_xpaths=(book_class_xpath,)), follow=True),
        # Rule(LinkExtractor(allow=("b/ref.*",), restrict_xpaths=(book_class_xpath,)), follow=True),
        # Rule(LinkExtractor(restrict_xpaths=(nextPage_xpath,)), follow=True),
        Rule(LinkExtractor(deny=("b/ref.*",), restrict_xpaths=(url_xpath,)), callback="parse_item"),
    )

    # def start_requests(self):
    #     for url in self.start_urls:
    #         yield scrapy.Request(url=url, callback=self.parse_starturls)

    def parse_starturls(self, response):
        url_list = response.xpath('//div[contains(@class, "browseBox")]/ul[2]/li/a/@href').extract()
        home_url = "https://www.amazon.cn"
        url_list = [home_url + u for u in url_list]
        for url in url_list:
            yield scrapy.Request(url)

    def parse_item(self, response):
        """[summary]
        解析图书页面的信息
        [description]
        获取URL,书名，装帧方式，评论数，价格
        Arguments:
            url -- [书籍的商品的 URL]
            name -- [书名]
            packed -- [装帧方式]
            comments_num -- [评论数]
            price -- [价格]
        """
        # 获取商品页面的 URL
        url = response.url

        name = response.xpath('//span[contains(@id, "roductTitle")]/text()').extract()[0]

        packed = response.xpath('//h1[@id="title"]/span[contains(@class,"a-color-secondary")]/text()').extract()[0]
        packed = packed.strip()

        comments_list = response.xpath('//span[@id="acrCustomerReviewText"]/text()').re(r'\d+')
        comments_num = ''.join(comments_list)
        if comments_num:
            comments_num = int(comments_num)
        else:
            comments_num = 0

        pattern = r'￥(.*?)\n'
        price_selector_text = response.xpath('//li[@class="swatchElement selected"]').extract()[0]
        res = re.findall(pattern, price_selector_text)
        price = res[0]
        if price:
            price = float(price)
        else:
            price = 0.0
        # price = price_selector.css('span.a-size-base::text').extract()[0]
        # price = price.replace("￥", '').strip()

        AmazonItem = AmazonSpiderItem()
        AmazonItem['url'] = url
        AmazonItem['name'] = name
        AmazonItem['packed'] = packed
        AmazonItem['comments_num'] = comments_num
        AmazonItem['price'] = price
        # # 提取 IBSN 确定图书的唯一性
        # html_content = response.body.decode(response.encoding)
        # pattern = r"<li><b>条形码:</b>(\d+)</li>"
        # ISBN_list = re.findall(pattern, html_content, re.S)
        # if ISBN_list:
        #     ISBN = int(ISBN_list[0])
        # else:
        #     ISBN = 0
        yield AmazonItem

        # 使用 ItemLoader 来处理数据
        # item_loader = AmazonSpiderItemLoader(item=AmazonSpiderItem(), response=response)
        # item_loader.add_value('url', url)
        # item_loader.add_value('name', name)
        # item_loader.add_value('packed', packed)
        # item_loader.add_value('comments_num', comments_num)
        # item_loader.add_value('price', price)

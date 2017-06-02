# -*- coding: utf-8 -*-
import scrapy
from BookSpider.tools.connect_mysql import ConnectMySQL
from urllib.parse import urlencode
from BookSpider.items import JdSpiderItem


class JdSpider(scrapy.Spider):
    name = "jd"
    allowed_domains = ["jd.com"]
    start_urls = list()
    jd_search_host = "http://search.jd.com/Search?"
    conSQL = ConnectMySQL()
    conSQL.execute_sql("select name from amazon_book")
    book_name_packed = conSQL.cursor.fetchall()
    params = {
        "keyword": "",
        "enc": "utf-8"
    }
    for name_packed in book_name_packed:
        params["keyword"] = " ".join(name_packed)
        url = jd_search_host + urlencode(params)
        start_urls.append(url)

    def parse(self, response):
        book_info = response.xpath('//div[@class="gl-i-wrap"]')[0]
        url = "http:" + book_info.xpath('div[@class="p-name"]/a/@href').extract()[0]
        name = book_info.xpath('div[@class="p-name"]/a/em/font/text()').extract()[0]
        packed = book_info.xpath('div[@class="p-name"]/a/em/text()').extract()[0]
        price = book_info.xpath('div[@class="p-price"]/strong/i/text()').extract()[0]
        if price:
            price = float(price)
        else:
            price = 0
        comments_num = book_info.xpath('div[@class="p-commit"]/strong/a/text()').extract()
        if comments_num:
            comments_num = "".join(comments_num)
        else:
            comments_num = "0"
        JdItem = JdSpiderItem()
        JdItem['url'] = url
        JdItem['name'] = name
        JdItem['packed'] = packed
        JdItem['comments_num'] = comments_num
        JdItem['price'] = price
        yield JdItem

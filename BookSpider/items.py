# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy
from scrapy.loader import ItemLoader
from scrapy.loader.processors import TakeFirst


class AmazonSpiderItemLoader(ItemLoader):
    # 自定义itemloader
    default_output_processor = TakeFirst()


class AmazonSpiderItem(scrapy.Item):
    # define the fields for your item here like:
    # IBSN = scrapy.Field()
    url = scrapy.Field()
    name = scrapy.Field()
    packed = scrapy.Field()  # 装帧 == 精装-平装-Kindle电子书
    comments_num = scrapy.Field()
    price = scrapy.Field()

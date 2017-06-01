# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html
import hashlib
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

    def get_insert_sql(self):
        insert_sql = """
            INSERT INTO amazon_book (id, url, name, packed, comments_num, price)
            VALUES (%s, %s, %s, %s, %s, %s)
        """

        book_id = self.hash_book_id(self["name"] + self["packed"])
        url = self["url"]
        name = self["name"]
        packed = self["packed"]
        comments_num = self["comments_num"]
        price = self["price"]
        params = (book_id, url, name, packed, comments_num, price)

        return insert_sql, params

    def hash_book_id(self, book_id):
        md5 = hashlib.md5()
        md5.update(book_id.encode('utf-8'))
        return md5.hexdigest()


class JdSpiderItem(scrapy.Item):
    # define the fields for your item here like:
    # IBSN = scrapy.Field()
    url = scrapy.Field()
    name = scrapy.Field()
    packed = scrapy.Field()  # 装帧 == 精装-平装-Kindle电子书
    comments_num = scrapy.Field()
    price = scrapy.Field()

    def get_insert_sql(self):
        insert_sql = """
            INSERT INTO jd_book (id, url, name, packed, comments_num, price)
            VALUES (%s, %s, %s, %s, %s, %s)
        """

        book_id = self.hash_book_id(self["name"] + self["packed"])
        url = self["url"]
        name = self["name"]
        packed = self["packed"]
        comments_num = self["comments_num"]
        price = self["price"]
        params = (book_id, url, name, packed, comments_num, price)

        return insert_sql, params

    def hash_book_id(self, book_id):
        md5 = hashlib.md5()
        md5.update(book_id.encode('utf-8'))
        return md5.hexdigest()

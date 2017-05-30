# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html
import mysql.connector as my
import hashlib
from twisted.enterprise import adbapi
import BookSpider.settings as settings


class BookspiderPipeline(object):
    def process_item(self, item, spider):
        return item


class MySQLPipeline(object):
    # 书籍的相关信息写入mysql
    def __init__(self):
        host = settings.MYSQL_HOST
        db = settings.MYSQL_DBNAME
        user = settings.MYSQL_USER
        passwd = settings.MYSQL_PASSWORD
        self.conn = my.connect(user=user, password=passwd, host=host, database=db)
        self.cursor = self.conn.cursor()

    def process_item(self, item, spider):
        # print(item)
        book_id = self.hash_book_id(item["name"] + item["packed"])
        url = item["url"]
        name = item["name"]
        packed = item["packed"]
        comments_num = item["comments_num"]
        price = item["price"]
        book_data = (book_id, url, name, packed, comments_num, price)

        insert_sql = """
            INSERT INTO amazon_book (id, url, name, packed, comments_num, price)
            VALUES (%s, %s, %s, %s, %s, %s)
        """
        self.cursor.execute(insert_sql, book_data)
        self.conn.commit()

    def hash_book_id(self, book_id):
        md5 = hashlib.md5()
        md5.update(book_id.encode('utf-8'))
        return md5.hexdigest()



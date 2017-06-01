# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html
import mysql.connector as my
from twisted.enterprise import adbapi
import BookSpider.settings as settings
import hashlib


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
        # 对 书名 和 书籍的装帧方式进行 MD5 加密, 保证数据写入到 MySQL 的唯一性
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


class MysqlTwistedPipline(object):
    def __init__(self, dbpool):
        self.dbpool = dbpool

    @classmethod
    def from_settings(cls, settings):
        dbparms = dict(
            host=settings["MYSQL_HOST"],
            db=settings["MYSQL_DBNAME"],
            user=settings["MYSQL_USER"],
            password=settings["MYSQL_PASSWORD"],
            charset='utf8',
            use_unicode=True,
        )
        dbpool = adbapi.ConnectionPool("mysql.connector", **dbparms)

        return cls(dbpool)

    def process_item(self, item, spider):
        # 使用twisted将mysql插入变成异步执行
        query = self.dbpool.runInteraction(self.do_insert, item)
        query.addErrback(self.handle_error, item, spider)  # 处理异常

    def handle_error(self, failure, item, spider):
        # 处理异步插入的异常
        print(failure)

    def do_insert(self, cursor, item):

        insert_sql, params = item.get_insert_sql()
        cursor.execute(insert_sql, params)

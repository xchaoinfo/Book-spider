#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import mysql.connector as my
import BookSpider.settings as settings


class ConnectMySQL(object):
    """docstring for ConnectMySQL"""

    def __init__(self):
        super(ConnectMySQL, self).__init__()
        host = settings.MYSQL_HOST
        db = settings.MYSQL_DBNAME
        user = settings.MYSQL_USER
        passwd = settings.MYSQL_PASSWORD
        self.conn = my.connect(user=user, password=passwd, host=host, database=db)
        self.cursor = self.conn.cursor()

    def execute_sql(self, sql):
        self.cursor.execute(sql)

    def __del__(self):
        self.conn.close()

# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html
import traceback

import pymysql
import logging
import six

from dog_project.items import DogInfoItem

logger = logging.getLogger('dog_pipeline')

MYSQL_HOST = 'localhost'
MYSQL_DBNAME = 'dog'
MYSQL_USER = 'root'
MYSQL_PASSWD = 'root'

table_name_dict = {
    DogInfoItem: 'dog_info'
}

def get_table_name(item):
    if type(item) in table_name_dict.keys():
        return table_name_dict[type(item)]
    return None


class DogProjectPipeline(object):

    def open_spider(self, spider):
        self.connect = pymysql.connect(
            host=MYSQL_HOST,
            db=MYSQL_DBNAME,
            user=MYSQL_USER,
            passwd=MYSQL_PASSWD,
            charset='utf8mb4',
            use_unicode=True)
        self.cursor = self.connect.cursor()
        # logger.info('每次一个spider开启的时候，重启对应的pipleline_sql')

    def process_item(self, item, spider):
        table_name = get_table_name(item)
        if table_name is None:
            return
        sql = ''
        try:
            # logger.info(str(item))
            sql = self.insert_or_update_sql(item, table_name=table_name)
            self.cursor.execute(sql)
            self.connect.commit()
        except Exception as error:
            logger.debug(sql)
            traceback.print_exc()

    def insert_or_update_sql(self, item, table_name):

        col_str = ''
        row_str = ''
        for key in item.keys():
            col_str = col_str + " `" + key + "`,"
            row_str = "{}{},".format(row_str, self.sql_quote(item[key]))
        sql = "INSERT INTO {} ({}) VALUES ({}) ON DUPLICATE KEY UPDATE ".format(table_name, col_str[1:-1], row_str[:-1])
        for (key, value) in six.iteritems(item):
            if value is not None:
                sql += "`{}` = {}, ".format(key, self.sql_quote(value))
        sql = sql[:-2]

        sql.replace("'None'", 'null')
        return sql

    @staticmethod
    def sql_quote(value):
        if value is None:
            return 'NULL'
        return "'{}'".format(str(value).replace("'", "''"))


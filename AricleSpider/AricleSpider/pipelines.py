# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html
import json

from scrapy.pipelines.images import ImagesPipeline
#避免文件编码问题
import codecs
import MySQLdb
import MySQLdb.cursors
from twisted.enterprise import adbapi


class AriclespiderPipeline(object):
    def process_item(self, item, spider):
        return item


class JsonWithEncodingPipeline(object):
    # 自定义json文件的导出
    def __init__(self):
        # 完成文件的打开和写入
        self.file = codecs.open('article.json','w',encoding='utf-8',)

    def process_item(self,item,spider):
        #ensure_ascii编码问题，如果不设置的话，其他编码容易出错
        print('item',item)
        lines = json.dumps(dict(item),ensure_ascii=False)+"\n"
        print(lines)
        self.file.write(lines)
        print('&'*30)
        # 一定要return出去，下一个需要接收
        return item
    #关闭文件
    def spider_closed(self,spider):
        self.file.close()




# class MysqlPipline(object):
#     def __init__(self):
#         self.conn = MySQLdb.connect('localhost','root','123456','article_spider',charset='utf8',use_unicode=True)
#         self.cursor = self.conn.cursor()
#
#     def process_item(self,item,spider):
#         insert_sql = """
#         insert into jobbole_article(title,url,create_date,fav_nums) VALUES (%s,%s,%s,%s)
#         """
#         self.cursor.execute(insert_sql,(item['title'],item['url'],item['create_date'],item['fav_nums']))
#         self.conn.commit()


# 异步化
class MysqlTwistedPipline(object):
    def __init__(self,dbpool):
        self.dbpool = dbpool
    @classmethod
    def from_settings(cls,settings):
        # 参数名称是固定的，和Python代码连接数据库的参数名称一致
        dbparms = dict( host = settings['MYSQL_HOST'],
        user = settings['MYSQL_USER'],
        db = settings['MYSQL_DBNAME'],
        passwd = settings['MYSQL_PASSWORD'],
              charset='utf8',
              cursorclass=MySQLdb.cursors.DictCursor,
              use_unicode=True)
        dbpool = adbapi.ConnectionPool('MySQLdb',**dbparms)
        return cls(dbpool)

    def process_item(self,item,spider):
        # 使用twisted将mysql插入变为异步执行
        query = self.dbpool.runInteraction(self.do_insert,item)
        # 错误的处理
        query.addErrback(self.handle_error,item,spider)# 处理异常

    def handle_error(self,failure,item,spider):
        #处理异步插入的异常
        print(failure)

    def do_insert(self,cursor,item):
        # 执行具体的插入
        insert_sql = """
                insert into jobbole_article(title,url,create_date,fav_nums) VALUES (%s,%s,%s,%s)
                """
        cursor.execute(insert_sql, (item['title'], item['url'], item['create_date'], item['fav_nums']))
        print('插入成功******************8')


class ArticleImagePipeline(ImagesPipeline):
    def item_completed(self, results, item, info):
        print(results)
        if 'front_image_url' in item:
            for ok,value in results:
                image_file_path = value['path']
            item['front_image_path'] = image_file_path
        return item











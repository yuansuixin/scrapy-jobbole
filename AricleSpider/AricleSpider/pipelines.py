# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html
import json

from scrapy.pipelines.images import ImagesPipeline
#避免文件编码问题
import codecs


class AriclespiderPipeline(object):
    def process_item(self, item, spider):
        return item

class JsonWithEncodingPipeline(object):
    def __init__(self):
        # 完成文件的打开和写入
        self.file = codecs.open('article.json','w',encoding='utf-8')

    def process_item(self,item,spider):
        #ensure_ascii编码问题，如果不设置的话，其他编码容易出错
        print('item',item)
        lines = json.dumps(dict(item),ensure_ascii=False)+'/n'
        print(lines)
        self.file.write(lines)
        # 一定要return出去，下一个需要接收
        return item
    #关闭文件
    def spider_closed(self,spider):
        self.file.close()


class ArticleImagePipeline(ImagesPipeline):
    def item_completed(self, results, item, info):
        print(results)
        for ok,value in results:
            image_file_path = value['path']
        item['front_image_path'] = image_file_path
        return item











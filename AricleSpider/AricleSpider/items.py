# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html
import datetime

import re
import scrapy
from scrapy.loader import ItemLoader
from scrapy.loader.processors import MapCompose, TakeFirst, Join


class AriclespiderItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    pass


def add_jobbole(value):
    return value+'-kerry'


def date_convert(value):
    try:
        create_date = datetime.datetime.strptime(value, '%Y%m/%d').date()
    except Exception as e:
        create_date = datetime.datetime.now()
    return create_date

class ArticleItemLoader(ItemLoader):
    # 自定义itemloader
    default_output_processor = TakeFirst()

def get_nums(value):
    match_re = re.match('.*?(\d+).*', value)
    if match_re:
        nums = int(match_re.group(1))
    else:
        nums = 0
    return nums

def return_value(value):
    return value
def remove_comment_tags(value):
    #去掉tag中提取的评论
    if "评论" in value:
        return ""
    else:
        return value

class JobBoleArticleItem(scrapy.Item):
    # 有参数，可以对字段做预处理,参数是函数，这里也可以添加两个函数
    title = scrapy.Field(
        # input_processor = MapCompose(lambda x:x+"-jobbole",add_jobbole)# 实际上是将title的值传给add_jobbole（）这个方法，作为这个方法的参数
    )
    create_date = scrapy.Field(
        input_processor = MapCompose(date_convert),
    )
    url = scrapy.Field()
    #对url进行摘要
    url_object_id = scrapy.Field()
    # 封面图,必须要保持原有的值，并且是list类型
    front_image_url = scrapy.Field(
        # 一定要注意，重要
        # 写一个函数，这样的话既没有改变url中值，也可以覆盖掉default_output_processor，保持list类型
        output_processor=MapCompose(return_value)
    )
    front_image_path = scrapy.Field()
    # 点赞数
    praise_nums = scrapy.Field(
        input_processor = MapCompose(get_nums)
    )
    #评论数
    comment_nums = scrapy.Field(
        input_processor=MapCompose(get_nums)
    )
    fav_nums = scrapy.Field(
        input_processor=MapCompose(get_nums)
    )
    tags = scrapy.Field(
        input_processor=MapCompose(remove_comment_tags),
        output_processor = Join(',')
    )
    content = scrapy.Field()














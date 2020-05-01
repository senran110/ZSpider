# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html


import scrapy


class QuestionItem(scrapy.Item):
    # define the fields for your item here like:
    # table = "question"
    question_title = scrapy.Field()
    question_id = scrapy.Field()
    answer_num = scrapy.Field()


class UserItem(scrapy.Item):
    # table = "user"
    username = scrapy.Field()
    userid = scrapy.Field()
    headline = scrapy.Field()
    vote_num = scrapy.Field()


class DangdangItem(scrapy.Item):
    # Field字段名和数据库字段名相同,拷贝这段SQL拼接脚本
    table_name = "dd_GoodInfo"

    goods_id = scrapy.Field()  # 商品id
    category = scrapy.Field()  # 商品类别
    title = scrapy.Field()  # 商品名称
    link = scrapy.Field()  # 商品链接
    price = scrapy.Field()  # 商品价格
    comments_num = scrapy.Field()  # 商品评论数
    praise_num = scrapy.Field()  # 商品好评数
    negative_num = scrapy.Field()  # 商品差评数
    praise_rate = scrapy.Field()  # 商品的好评率
    source = scrapy.Field()  # 商品的来源地
    detail = scrapy.Field()  # 商品详情
    img_link = scrapy.Field()  # 商品图片链接
    author = scrapy.Field()
    pub = scrapy.Field()




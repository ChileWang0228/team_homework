# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class PoemSpiderItem(scrapy.Item):
    # define the fields for your item here like:
    # 第一题
    author_name = scrapy.Field()
    author_info = scrapy.Field()  # 作家基本信息
    author_article_set_title = scrapy.Field()  # 作家作品全集名称
    author_article_set = scrapy.Field()  # 作家作品全集
    author_famous_poem_set_title = scrapy.Field()  # 作者名词诗句的总名称
    author_famous_poem_set = scrapy.Field()  # 名句集

    # 第二题
    poem_file_name = scrapy.Field()  # 存放古诗的文件名
    file_name = scrapy.Field()  # 存放诗人的文件名
    poem_content = scrapy.Field()  # 古诗内容

    # 第三题
    search_source_code = scrapy.Field()  # 搜索作家网页的源码
    search_index = scrapy.Field()  # 搜索页码

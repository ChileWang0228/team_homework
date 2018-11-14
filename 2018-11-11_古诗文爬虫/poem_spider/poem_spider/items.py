# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class PoemSpiderItem(scrapy.Item):
    # define the fields for your item here like:
    name = scrapy.Field()
    author_url = scrapy.Field()
    source_code = scrapy.Field()
    file_name = scrapy.Field()
    f_type = scrapy.Field()  # 写入的文件夹
    search_url = scrapy.Field()
    search_source_code = scrapy.Field()  # 搜索作家的源码
    search_index = scrapy.Field()  # 搜索页码
    # author_summary = scrapy.Field()
    # author_popluar_poem_word_set = scrapy.Field()
    # author_poem_word_set = scrapy.Field()

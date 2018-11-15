# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html

from scrapy.exceptions import DropItem
import os
import logging
logger = logging.getLogger(__name__)


class PoemSpiderPipeline(object):
    def __init__(self):
        folder = os.path.exists('author')
        currend_path = os.getcwd()
        self.author_path = currend_path + '/author/'
        if not folder:
            os.mkdir(self.author_path)

        folder = os.path.exists('poesy')
        self.poesy_path = currend_path + '/poesy/'
        if not folder:
            os.mkdir(self.poesy_path)

        folder = os.path.exists('search')
        self.search_path = currend_path + '/search/'
        if not folder:
            os.mkdir(self.search_path)

    def process_item(self, item, spider):
        logger.warning(item)  # 写入日志

        if item:
            try:
                file_name = str(self.author_path + item['file_name'].split('.')[0] + '.txt')  # 写入诗人文件夹
                # 写入诗人文件夹
                with open(file_name, 'w') as fw:
                    fw.write(item['author_info'])
                    fw.write('\n')
                    fw.write('\n')
                    fw.write(item['author_article_set_title'] + '\n')
                    fw.write('\n')
                    fw.write(item['author_article_set'])
                    fw.write('\n')
                    fw.write(item['author_famous_poem_set_title'])
                    fw.write('\n')
                    fw.write(item['author_famous_poem_set'])

                #  写入搜索文件夹
                file_name = str(self.search_path + item['author_name'] + '_' + item['search_index'] + '.html')
                with open(file_name, 'w') as fw:
                    fw.write(item['search_source_code'][0])
                return item
            except Exception as e:
                del e
                # 写入古诗文件夹
                file_name = str(self.poesy_path + item['poem_file_name'] + '.txt')
                with open(file_name, 'w') as fw:
                    fw.write(item['poem_content'])
                return item
        else:
            raise DropItem("Missing item in %s" % item)


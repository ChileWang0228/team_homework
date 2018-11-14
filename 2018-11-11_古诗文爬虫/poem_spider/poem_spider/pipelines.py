# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html

from scrapy.exceptions import DropItem
import os


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
        if item:
            # print('item：', item)
            if item['f_type'] == 'shiren':
                file_name = str(self.author_path + item['file_name'])  # 写入诗人文件夹
                with open(file_name, 'w') as fw:
                    fw.write(item['source_code'][0])

            else:
                file_name = str(self.poesy_path + item['file_name'])
                with open(file_name, 'w') as fw:
                    fw.write(item['source_code'][0])
                return item

            #  写入搜索文件夹
            try:
                file_name = str(self.search_path + item['name'] + '_' + item['search_index'] + '.html')
                with open(file_name, 'w') as fw:
                    fw.write(item['search_source_code'][0])
                return item
            except Exception as e:
                pass
        else:
            raise DropItem("Missing item in %s" % item)


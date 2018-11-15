#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
@Operating system: KALI LINUX
@编译器：python3.7
@Created on 2018-11-12 12:13
@Author:ChileWang
@algorithm：古诗文爬虫
"""

import scrapy
from poem_spider.items import PoemSpiderItem
from scrapy import Selector
from scrapy.crawler import CrawlerProcess


class PoemSpider(scrapy.Spider):
    name = 'poem'  # 爬虫的名称
    allow_domains = ['gushimi.org']  # 允许的域名
    # start_urls = ['https://www.gushimi.org/shiren/']
    start_urls = ['https://www.gushimi.org/shiren/', 'https://www.gushimi.org/gushi/']
    for i in range(1, 20):  # 总共20页古诗
        url = 'https://www.gushimi.org/gushi/index_%s.html' % str(i + 1)
        start_urls.append(url)

    def format_author_info(self, author_name, author_article_num, author_dynasty,
                           author_article_summary, author_title_set):
        """
        格式化作家信息
            作者名
            作品数目
            朝代
            作者简历
            作者作品
        :return:
        """
        author_info = '诗人:%s\n作品数目：%s\n朝代：%s\n%s\n' % (author_name, author_article_num,
                                                author_dynasty, author_article_summary)
        i = 0
        for title in author_title_set:
            i += 1
            author_info += ('<<' + title + '>> ')
            if i == 4:
                author_info += '\n'
                i = 0
        return author_info

    def format_poem(self, author_article, author_article_info, author_name):
        """
        格式化作品：
            作品题目
            作者
            作品内容
        :param author_article:诗词内容集合
        :param author_article_info:诗词题目等信息集合
        :param author_name:
        :return:
        """
        author_poem_title = []  # 诗词题目（作品信息格式化）
        author_poem = []  # 诗词（诗词内容格式化）
        for i in range(len(author_article)):
            if len(author_article[i]) > 6:
                author_poem.append(author_article[i].replace(' - - ', ''))
        temp = ''
        for info in author_article_info:
            temp += (info + '\n')
            if info == author_name:
                author_poem_title.append(temp)
                temp = ''
        fina_poem = ''
        for i in range(len(author_poem_title)):
            fina_poem += (author_poem_title[i] + author_poem[i]) + '\n'
        return fina_poem

    def format_famous_poem(self, author_famous_poem, author_name):
        """
        格式化后的名句集
        :param author_famous_poem: 名句集合
        :param author_name:
        :return:
        """
        author_famous_poem_set = []
        temp = ''
        for i in range(len(author_famous_poem)):
            temp += author_famous_poem[i] + '。 '
            if author_famous_poem[i] == author_name:
                i += 1
                temp += (' <<' + author_famous_poem[i] + '>> \n')
                author_famous_poem_set.append(temp)
                temp = ''

        fina_famous_poem_set = ''
        for i in range(len(author_famous_poem_set)):
            fina_famous_poem_set += (author_famous_poem_set[i] + '\n')

        return fina_famous_poem_set

    def parse(self, response):
        """
        网页解析
        :return:item[author_info]
        """
        authors = response.xpath(".//*[@class='news_box']")  # 抽取所有作家
        for author in authors:
            # 判断是否为诗人网址
            url_type = str(author.xpath(".//*[@class='news_title']/a/@href").extract()[0]).split('/')[1]
            poem_file_name = (str(author.xpath(".//*[@class='news_title']/a/@href")  # 古诗存放文件名
                                  .extract()[0]).split('/')[-1]).split('.')[0]
            if url_type == 'shiren':  # 诗人网址
                url = 'https://www.gushimi.org' + author.xpath(".//*[@class='news_title']/a/@href").extract()[0]
                author_name = author.xpath(".//*[@class='news_title']/a/text()").extract()[0]

                author_article_num = author.xpath(".//*[@class='news_summy']/text()").extract()[1].split(':')[1]  # 诗人作品数
                author_dynasty = author.xpath(".//*[@class='news_summy']/a/text()").extract()[0]  # 诗人朝代
                author_article_summary = author.xpath(".//*[@class='news_text']/p/text()").extract()[0]  # 诗人简介
                author_title_set = author.xpath(".//*[@class='news_text']/p/a/text()").extract()  # 诗人作品题目大全
                # 格式化作者信息
                author_info = self.format_author_info(author_name, author_article_num, author_dynasty,
                                   author_article_summary, author_title_set)
                item = PoemSpiderItem(author_name=author_name, author_info=author_info, file_name=str(url).split('/')[-1])
                request = scrapy.Request(url=url, callback=self.parse_body)  # 解析诗人网页以提取作品
                request.meta['item'] = item  # 暂存item
                yield request
            next_page = Selector(response).re(u'<a href="(\S*)">下一页</a>')
            if next_page:
                yield scrapy.Request(url='https://www.gushimi.org' + next_page[0], callback=self.parse)

            else:  # 古诗网址
                print(poem_file_name)
                poem_title = author.xpath(".//*[@class='news_title']/a/text()").extract()  # 所有诗词题目
                poem_author = author.xpath(".//*[@class='news_summy']/a/text()").extract()  # 所有诗词作者
                poem_summary = author.xpath(".//*[@class='news_summy']/text()").extract()  # 所有诗词简介
                poem_content = author.xpath(".//*[@class='news_text']/p/text()").extract()  # 所有诗词简介
                # 格式化古诗内容
                fina_poem = '%s\n%s%s%s\n%s\n' % (poem_title[0], poem_summary[0], poem_author[0],
                                                  poem_summary[1], poem_content[0])

                print(fina_poem)
                print('----------------------')

                # url = 'https://www.gushimi.org' + author.xpath(".//*[@class='news_title']/a/@href").extract()[0]
                item = PoemSpiderItem(poem_file_name=poem_file_name, poem_content=fina_poem)
                yield item

    def parse_body(self, response):
        """
        提取诗人作品全集
        :param response:
        :return:fina_poem author_article_set_title
        """
        item = response.meta['item']
        aritcles = response.xpath(".//*[@class='content_box']")[3]  # 抽取所有作家作品全集
        author_article_set_title = aritcles.xpath(".//*/h3/text()").extract()[0]  # 作者所有诗词集的总名称
        author_article_info = aritcles.xpath(".//*/li/a/text()").extract()  # 作品具体信息(作品名和作者名)
        author_article = aritcles.xpath(".//*/li/text()").extract()  # 诗词内容

        #  格式化诗词内容
        fina_poem = self.format_poem(author_article, author_article_info, item['author_name'])
        item['author_article_set_title'] = author_article_set_title
        item['author_article_set'] = fina_poem

        #  格式化名句集合
        aritcles = response.xpath(".//*[@class='content_box']")[2]  # 抽取所有作家名句
        author_famous_poem_set_title = aritcles.xpath(".//*/h3/text()").extract()[0]  # 作者名词诗句的总名称
        author_famous_poem = aritcles.xpath(".//*/li/a/text()").extract()  # 名句

        fina_famous_poem_set = self.format_famous_poem(author_famous_poem, item['author_name'])
        item['author_famous_poem_set_title'] = author_famous_poem_set_title
        item['author_famous_poem_set'] = fina_famous_poem_set

        # yield item

        # 搜索该作者
        search_url = 'https://www.gushimi.org/e/sch/index.php?keyboard=%s&Submit=' % item['author_name']
        request2 = scrapy.Request(url=search_url, callback=self.parse_search)
        request2.meta['item'] = item  # 暂存item
        yield request2

    def parse_search(self, response):
        """
        解析搜索
        :param response:
        :return:item
        """
        try:
            item = response.meta['item']
            item['search_source_code'] = response.xpath('/html').extract()  # 搜索结果的网页源码
            if response.xpath(".//*[@class='list_page']/.//*/b/text()").extract():  # 网页页码不为空
                item['search_index'] = response.xpath(".//*[@class='list_page']/.//*/b/text()").extract()[1]

            else:
                item['search_index'] = str(0)
            yield item
            next_page = Selector(response).re(u'<a href="(\S*)">下一页</a>')
            if next_page:
                yield scrapy.Request(url='https://www.gushimi.org' + next_page[0].replace('amp;', ''), callback=self.parse_search)
        except Exception as e:
            del e

    def parse_poem(self, response):
        """
        解析古诗网址全集
        :param response:
        :return:
        """

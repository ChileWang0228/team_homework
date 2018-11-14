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
# from items import PoemSpiderItem
from scrapy import Selector

from scrapy.crawler import CrawlerProcess


class PoemSpider(scrapy.Spider):
    name = 'poem'  # 爬虫的名称
    allow_domains = ['gushimi.org']  # 允许的域名
    start_urls = ['https://www.gushimi.org/shiren/', 'https://www.gushimi.org/gushi/']
    for i in range(1, 20):
        url = 'https://www.gushimi.org/gushi/index_%s.html' % str(i + 1)
        start_urls.append(url)

    def parse(self, response):
        """
        网页解析
        :return:
        """
        authors = response.xpath(".//*[@class='news_box']")  # 抽取所有作家
        file_type = ''
        for author in authors:
            url = 'https://www.gushimi.org' + author.xpath(".//*[@class='news_title']/a/@href").extract()[0]
            author_name = author.xpath(".//*[@class='news_title']/a/text()").extract()[0]
            file_type = str(url).split('/')[-2]
            item = PoemSpiderItem(author_url=url, name=author_name, file_name=str(url).split('/')[-1], f_type=file_type)
            request = scrapy.Request(url=url, callback=self.parse_body)
            request.meta['item'] = item  # 暂存item
            yield request

        if file_type == 'shiren':  # 诗人
            next_page = Selector(response).re(u'<a href="(\S*)">下一页</a>')
            if next_page:
                yield scrapy.Request(url='https://www.gushimi.org' + next_page[0], callback=self.parse)

    def parse_body(self, response):
        """
        解析诗人或诗句的网页
        :param response:
        :return:request
        """
        item = response.meta['item']
        item['source_code'] = response.xpath('/html').extract()
        search_url = 'https://www.gushimi.org/e/sch/index.php?keyboard=%s&Submit=' % item['name']
        request2 = scrapy.Request(url=search_url, callback=self.parse_search)
        request2.meta['item'] = item  # 暂存item
        yield request2

        yield item

    def parse_search(self, response):
        """
        解析搜索
        :param response:
        :return:item
        """
        try:
            item = response.meta['item']
            item['search_source_code'] = response.xpath('/html').extract()
            if response.xpath(".//*[@class='list_page']/.//*/b/text()").extract():  # 网页页码不为空
                item['search_index'] = response.xpath(".//*[@class='list_page']/.//*/b/text()").extract()[1]

            else:
                item['search_index'] = str(1)
            yield item
            next_page = Selector(response).re(u'<a href="(\S*)">下一页</a>')
            if next_page:
                yield scrapy.Request(url='https://www.gushimi.org' + next_page[0].replace('amp;', ''), callback=self.parse_search)
        except Exception as e:
            del e


if __name__ == '__main__':
    process = CrawlerProcess(
        {
            'USER_AGENT': 'Mozilla / 5.0(X11;Linux86_64) AppleWebKit / 537.36(KHTML, likeGecko) Chrome / 70.0.3538.77Safari / 537.36'
        }
    )
    process.crawl('poem')
    process.start()

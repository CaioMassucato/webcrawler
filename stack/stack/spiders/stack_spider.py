from scrapy import Spider, Selector
from stack.items import StackItem
from scrapy.spiders import CrawlSpider, Rule
from scrapy.linkextractors import LinkExtractor
from scrapy.selector import Selector
import sys
import getopt

class PageCrawlSpider(CrawlSpider):
    name = "stackcrawler"
    allowed_domains = ["stackoverflow.com"]
    start_urls = [
        "http://stackoverflow.com/questions?sort=newest",
    ]
    rules = (
        Rule(
            LinkExtractor(allow=(r'&page=\d')),
            callback='parse_item',
            follow=True
        ),
    )

    def parse_item(self, response):
        keyword = str(self.keyword);
        hxs = Selector(response)
        questions = hxs.xpath('//div[@class="summary"]/h3[contains(., "' + keyword + '")]')
        for question in questions:
            item = StackItem()
            item['title'] = question.xpath(
                'a[@class="question-hyperlink"]/text()').extract()[0]
            item['url'] = question.xpath(
                'a[@class="question-hyperlink"]/@href').extract()[0]
            yield item
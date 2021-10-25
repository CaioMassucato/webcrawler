from time import clock_settime
from scrapy import Spider, Selector
from stack.items import StackItem
from scrapy.spiders import CrawlSpider, Rule
from scrapy.linkextractors import LinkExtractor
from scrapy.selector import Selector
from scrapy.exceptions import CloseSpider

class PageCrawlSpider(CrawlSpider):
    name = "stackcrawler"
    max_pages = 10000
    count = 0
    allowed_domains = ["stackoverflow.com"]
    start_urls = [
        "http://stackoverflow.com/questions?tab=Votes",
    ]
    rules = (
        Rule(
            LinkExtractor(allow=(r'&page=\d')),
            callback='parse_item',
            follow=True,
        ),
    )

    def parse_item(self, response):
        if self.count >= self.max_pages:
            raise CloseSpider("Maximum number of requests reached!")
        hxs = Selector(response)
        questions = hxs.xpath('//div[@class="summary"]')
        for question in questions:
            item = StackItem()
            item['title'] = question.xpath(
                'h3/a[@class="question-hyperlink"]/text()').extract()[0]
            item['url'] = question.xpath(
                'h3/a[@class="question-hyperlink"]/@href').extract()[0]   
            item['body'] = question.xpath(
                'div[@class="excerpt"]/text()').extract()[0]  
            yield item
        self.count += 1
from scrapy import Item, Field

class StackItem(Item):
    title = Field()
    url = Field()
    body = Field()


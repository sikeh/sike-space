from scrapy.item import Item, Field
from scrapy.contrib.spiders.crawl import CrawlSpider

class Offer(Item):
    city = Field()
    price = Field()
    url = Field()

class KlmSpider(CrawlSpider):
    pass






import scrapy
from toyspider.items import ToyspiderItem


class BasicSpider(scrapy.Spider):
    name = 'basic'
    allowed_domains = ['google']
    start_urls = ['http://google/']

    def parse(self, response):
        item = ToyspiderItem()
        self.log(f"""url:
            {response.xpath('//*[@itemprop="url"][1]/text()').extract()}""")
        item['url'] = \
            response.xpath('//*[@itemprop="url"][1]/text()').extract()

        return item

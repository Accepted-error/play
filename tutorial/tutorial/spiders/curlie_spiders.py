import scrapy

from tutorial.items import CurlieItem

class Curliespider(scrapy.Spider):
    name = "curlie"
    allowed_domains = ['curlie.org']
    start_urls = [
        'http://curlie.org/en/Computers/Programming/Languages/Python/Resources/',
        'http://curlie.org/en/Computers/Programming/Languages/Ruby/Books/'
    ]

    def parse(self,response):
        sel = scrapy.selector.Selector(response)
        site = sel.xpath('//*[@class="site-sort-by-date"]/div/div[3]')
        items = []
        for i in site:
            item = CurlieItem()
            item['title'] = i.xpath('a/div/text()').extract()
            item['link'] = i.xpath('a/@href').extract()
            item['des'] = i.xpath('div/text()').extract()
            items.append(item)

        return items
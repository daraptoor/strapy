# -*- coding: utf-8 -*-
import scrapy


class QuotesallSpider(scrapy.Spider):
    name = 'quotesall'
    allowed_domains = ['toscrape.com']
    start_urls = ['http://quotes.toscrape.com']

    def parse(self, response):
        self.log('hello world'+ response.url)
        for quote in response.css('div.quote'):
            item = {
                'author_name': quote.css('small.author::text').extract_first(),
                'text': quote.css('span.text::text').extract_first(),
                'tags': quote.css('a.tag::text').extract(),
            }
            yield item
        # following all pages in pagination
        next_page_url = response.css('li.next > a::attr(href)').extract_first()
        if next_page_url:
            next_page_url = response.urljoin(next_page_url)
            yield scrapy.Request(url=next_page_url, callback=self.parse)

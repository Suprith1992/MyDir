# -*- coding: utf-8 -*-
#from scrapy.spiders import CrawlSpider,Rule
#from scrapy.linkextractors import LinkExtractor 
from scrapy import Spider
from scrapy.http import Request


class BooksSpider(Spider):
    name = 'books'
    allowed_domains = ['books.toscrape.com']
    start_urls = ('http://books.toscrape.com/',)

    #rules = (Rule(LinkExtractor(deny_domains=('google.com'),allow=('fantasy','music')),callback='parse_page',follow=False),)

    #def parse_page(self, response):
        #pass

    def parse(self,response):
    	books = response.xpath('//h3/a/@href').extract()
    	for book in books:
    		absolute_url = response.urljoin(book)
    		yield Request(absolute_url,callback=self.parse_book)

    	#process next page
    	next_page_url = response.xpath('//li[@class="next"]/a/@href').extract_first()
    	absolute_next_page_url = response.urljoin(next_page_url)
    	yield Request(absolute_next_page_url)

	def parse_book(self, response):
		title = response.xpath('//*[@class="price_color"]/text()').extract()

		price = response.xpath('//*[@class="price_color"]/text()').extract()
		image_url = response.xpath('//img/@src').extract_first()
		image_url = image_url.replace('../../','http://books.toscrape.com/')
		rating = response.xpath('//*[contains(@class,"star-rating")]/@class').extract_first()
		rating=rating.replace('star-rating','')
		description = response.xpath('//*[@id="product_description"]/following-sibling::text()').extract_first()

		yield {
			    'title': title,
				'image_url':image_url,
				'rating':rating,
				'description':description

		}


import re
import scrapy
from scrapy.loader import ItemLoader
from ..items import NewzItem
from itemloaders.processors import TakeFirst

pattern = r'(\xa0)?'

class NewzSpider(scrapy.Spider):
	name = 'newz'
	start_urls = ['https://news.anz.com/new-zealand']

	def parse(self, response):
		post_links = response.xpath('//h2/a/@href').getall()
		yield from response.follow_all(post_links, self.parse_post)

	def parse_post(self, response):
		date = response.xpath('//div[@class="component article-date"]/@aria-label | //div[@class="component article-date"]/span/text()').get()
		title = response.xpath('//h1/text()').get()
		content = response.xpath('//div[@class="text__content"]//text()').getall()
		content = [p.strip() for p in content if p.strip()]
		content = re.sub(pattern, "",' '.join(content))

		item = ItemLoader(item=NewzItem(), response=response)
		item.default_output_processor = TakeFirst()

		item.add_value('title', title)
		item.add_value('link', response.url)
		item.add_value('content', content)
		item.add_value('date', date)

		yield item.load_item()

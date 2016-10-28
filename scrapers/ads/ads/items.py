import scrapy


class AdItem(scrapy.Item):
    title = scrapy.Field()
    description = scrapy.Field()
    price = scrapy.Field()
    structured_data = scrapy.Field()

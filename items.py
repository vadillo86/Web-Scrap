import scrapy


class BggItem(scrapy.Item):
    ranking = scrapy.Field()
    name = scrapy.Field()
    year = scrapy.Field()
    rating_geek = scrapy.Field()
    rating_avg = scrapy.Field()
    num_voters = scrapy.Field()

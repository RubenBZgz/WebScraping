# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class MydomainItem(scrapy.Item):
    filename = scrapy.Field()
    content = scrapy.Field()
    pass


class Videogames2(scrapy.Item):
    title = scrapy.Field()
    image = scrapy.Field()
    releaseDate = scrapy.Field()
    genres = scrapy.Field()
    officialPrice = scrapy.Field()
    keyPrice = scrapy.Field()
    pass


class Videogames(scrapy.Item):
    filename = scrapy.Field()
    id = scrapy.Field()
    pass

import scrapy
from ..items import MydomainItem

# Esto es un clave valor para el nombre del archivo
DICT = {
    'https://quotes.toscrape.com/page/1/': 'domain1.json',
    'https://quotes.toscrape.com/page/2/': 'domain2.json',
}

class MydomainSpider(scrapy.Spider):
    name = "MydomainSpider"
    allowed_domains = ["quotes.toscrape.com"]
    start_urls = [
        'https://quotes.toscrape.com/page/1/',
        'https://quotes.toscrape.com/page/2/',
    ]

    def parse(self, response):
        item = MydomainItem()
        item["filename"] = DICT[response.url]
        item["content"] = response.body.decode("utf-8")
        contenido = response.body.decode("utf-8")
        print(f"CONTENIDO {contenido}")
        yield item
    
    #scrapy crawl MydomainSpider
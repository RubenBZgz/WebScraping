import scrapy
from ..items import MydomainItem

class GgdealsSpider(scrapy.Spider):
    name = "ggdeals"
    allowed_domains = ["gg.deals"]
    start_urls = ["https://gg.deals/games/?type=1&page=1"]
    i = 0
    json = "["

    #def parse_games(self, response, **kwargs):

    def parse(self, response):
        titles = response.xpath(
            "//a[contains(@class, 'game-info-title')]/text()"
        ).getall()
        releaseDate = response.xpath(
            "//div[contains(@class, 'tag-release-date')]//span[contains(@class, 'value')]/text()"
        ).getall()
        genres = response.xpath(
            "//div[contains(@class, 'tag-genres')]//span[contains(@class, 'value')]//span/text()"
        ).getall()
        officialPrice = response.xpath(
            "//div[contains(@class, 'shop-price-retail')]//div//span//span/text()"
        ).getall()
        keyPrice = response.xpath(
            "//div[contains(@class, 'shop-price-keyshops')]//div//span//span/text()"
        ).getall()

        print(f"titles {titles}")
        
        
        

        i = GgdealsSpider.i
        while i < titles.lenght:
            json = ""
            if i==0:
                json += '{"titles": {titles[i]}, "releaseDate": {releaseDate[i]}, "genres": {genres[i]}, "officialPrice" : {officialPrice[i]}, "keyPrice" : {keyPrice[i]}}'
                GgdealsSpider.i+=1
            else: 
                json += ',{"titles": {titles[i]}, "releaseDate": {releaseDate[i]}, "genres": {genres[i]}, "officialPrice" : {officialPrice[i]}, "keyPrice" : {keyPrice[i]}}'
            yield {"titles": titles[i], "releaseDate": releaseDate[i], "genres": genres[i], "officialPrice": officialPrice[i], "keyPrice": keyPrice[i]}
        
        print(f"JSON {json}")

        #for title in titles:
        #    yield response.follow(
        #        f"https://gg.deals/game/{title}", callback=self.parse_games
        #    )

        paginas = response.xpath(
             "//a[contains(@class, 'endless_page_link page-link')]/text()"
        ).getall()
        #ultima_pagina = max([*map(int, paginas)])
        ultima_pagina = 2
        current_url = response.url
        index = response.url.index("=") + 1
        base_url = current_url[:index]
        current_page = int(current_url[index:])

        #item = MydomainItem()
        #item["filename"] = "prueba"
        #item["content"] = response.body.decode("utf-8")

        #if current_page < ultima_pagina:
        #    print(f"PAGINA ACTUAL {current_page}")
        #    yield response.follow(f"{base_url}{current_page+1}")


        

        pass

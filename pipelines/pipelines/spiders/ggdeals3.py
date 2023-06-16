import json

import scrapy

from ..items import MydomainItem, Videogames


class Ggdeals3Spider(scrapy.Spider):
    name = "ggdeals3"
    allowed_domains = ["gg.deals"]
    start_urls = ["https://gg.deals/games/?type=1&page=1"]
    i = 0
    CustomJson = "["
    global jsonFile
    jsonFile = []
    global jsonData
    jsonData = {}

    def parse(self, response):
        titles = response.xpath(
            "//a[contains(@class, 'game-info-title')]/text()"
        ).getall()
        response.xpath(
            "//a[contains(@class, 'game-info-title')]/text()"
        ).extract_first()
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

        results = response.xpath("//div[contains(@class, 'game-item')]")
        response.xpath(".//picture//img/@src")

        # jsonFile = Ggdeals2Spider.jsonFile
        # jsonFile = []

        for game in results:
            title = "".join(
                game.xpath(".//a[contains(@class, 'game-info-title')]/text()").getall()
            )
            image = "".join(game.xpath(".//picture//img/@src").getall())
            releaseDate = "".join(
                game.xpath(
                    ".//div[contains(@class, 'tag-release-date')]//span[contains(@class, 'value')]/text()"
                ).getall()
            )
            genres = "".join(
                game.xpath(
                    ".//div[contains(@class, 'tag-genres')]//span[contains(@class, 'value')]//span/@title"
                ).getall()
            )
            officialPrice = "".join(
                game.xpath(
                    ".//div[contains(@class, 'shop-price-retail')]//div//span//span/text()"
                ).getall()
            )
            officialPrice = officialPrice[0 : len(officialPrice) - 1]
            keyPrice = "".join(
                game.xpath(
                    ".//div[contains(@class, 'shop-price-keyshops')]//div//span//span/text()"
                ).getall()
            )
            keyPrice = keyPrice[0 : len(keyPrice) - 1]
            data = {}
            data["title"] = title
            json_data_title = json.dumps(data["title"])
            data["image"] = image
            json_data_image = json.dumps(data["image"])
            data["releaseDate"] = releaseDate
            json_data_date = json.dumps(data["releaseDate"])
            data["genres"] = genres
            json_data_genres = json.dumps(data["genres"])
            # HAY QUE HACER QUE DA IGUAL SI ESTÁ VACÍO
            data["officialPrice"] = officialPrice
            json_data_oPrice = json.dumps(data["officialPrice"])
            data["keyPrice"] = keyPrice
            json_data_kPrice = json.dumps(data["keyPrice"])
            # Guardo todos los datos en jsonFile
            jsonData["title"] = json_data_title
            jsonData["image"] = json_data_image
            jsonData["releaseDate"] = json_data_date
            jsonData["genres"] = json_data_genres
            jsonData["officialPrice"] = json_data_oPrice
            jsonData["keyPrice"] = json_data_kPrice
            # jsonFile[0].append(json_data_title)
            # jsonFile[1].append(json_data_image)
            # jsonFile[2].append(json_data_date)
            # jsonFile[3].append(json_data_genres)
            # jsonFile[4].append(json_data_oPrice)
            # jsonFile[5].append(json_data_kPrice)

        paginas = response.xpath(
            "//a[contains(@aria-label, 'Last page')]/text()"
        ).getall()
        # ultima_pagina = max([*map(int, paginas)])
        ultima_pagina = 1
        current_url = response.url
        indexType = response.url.index("=") + 1
        indexPage = response.url.index("=", indexType) + 1
        base_url = current_url[:indexPage]
        current_page = int(current_url[indexPage:])

        if current_page < ultima_pagina:
            print(f"PAGINA ACTUAL {current_page}")
            yield response.follow(f"{base_url}{current_page+1}")

        print("JSON: ", jsonData["title"])
        # item = Videogames()
        # item["filename"] = "prueba2.json"
        # item["title"] = json_data_title
        # print("JSON FILE:  ", jsonFile)
        # yield item

        # scrapy shell "https://gg.deals/games/?type=1&page=1"
        # scrapy crawl ggdeals2

        pass

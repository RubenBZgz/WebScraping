import json

import scrapy

from ..items import MydomainItem


class Ggdeals2Spider(scrapy.Spider):
    name = "ggdeals2"
    allowed_domains = ["gg.deals"]
    start_urls = ["https://gg.deals/games/?type=1&page=1"]
    i = 0
    CustomJson = "["
    global jsonFile
    jsonFile = []

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
            data["titles"] = title
            data["image"] = image
            data["releaseDate"] = releaseDate
            data["genres"] = genres
            # HAY QUE HACER QUE DA IGUAL SI ESTÁ VACÍO
            data["officialPrice"] = officialPrice
            data["keyPrice"] = keyPrice
            json_data = json.dumps(data)
            jsonFile.append(json_data)
            print("JSON: ", json_data)
            print("")
            print("")

        paginas = response.xpath(
            "//a[contains(@aria-label, 'Last page')]/text()"
        ).getall()
        # ultima_pagina = max([*map(int, paginas)])
        ultima_pagina = 4
        current_url = response.url
        indexType = response.url.index("=") + 1
        indexPage = response.url.index("=", indexType) + 1
        base_url = current_url[:indexPage]
        current_page = int(current_url[indexPage:])

        if current_page < ultima_pagina:
            print(f"PAGINA ACTUAL {current_page}")
            yield response.follow(f"{base_url}{current_page+1}")

        item = MydomainItem()
        item["filename"] = "ggdeals2.json"
        item["content"] = jsonFile
        print("JSON FILE:  ", jsonFile)
        yield item

        # scrapy shell "https://gg.deals/games/?type=1&page=1"
        # scrapy crawl ggdeals2

        # while i < len(titles):
        #     json = ""
        #     if i==0:
        #         data = {}
        #         data['titles'] = titles[i]
        #         data['releaseDate'] = releaseDate[i]
        #         data['genres'] = genres[i]
        #         data['officialPrice'] = officialPrice[i]
        #         data['keyPrice'] = keyPrice[i]
        #         json_data = json.dumps(data)
        #         print ('JSON: ', json_data)
        #         Ggdeals2Spider.i+=1
        #     else:
        #         data = {}
        #         data['titles'] = titles[i]
        #         data['releaseDate'] = releaseDate[i]
        #         data['genres'] = genres[i]
        #         data['officialPrice'] = officialPrice[i]
        #         data['keyPrice'] = keyPrice[i]
        #         json_data = json.dumps(data)
        #         print ('JSON: ', json_data)
        #     #yield {"titles": titles[i], "releaseDate": releaseDate[i], "genres": genres[i], "officialPrice": officialPrice[i], "keyPrice": keyPrice[i]}

        pass

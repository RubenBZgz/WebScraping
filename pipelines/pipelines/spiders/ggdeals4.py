import json

# import jsonpickle
import scrapy

# from ..items import MydomainItem, Videogames, Videogames2

# from json import JSONEncoder


# class MyEncoder(JSONEncoder):
#     def default(self, o):
#         return o.__dict__


class Ggdeals4Spider(scrapy.Spider):
    name = "ggdeals4"
    allowed_domains = ["gg.deals"]
    start_urls = ["https://gg.deals/games/?type=1&page=1"]
    global i
    i = 0
    CustomJson = "["
    global jsonFile
    jsonFile = []
    global providerData
    providerData = []
    # global idGame
    idGame = 0

    def parsePrice(price):
        officialPrice = price[0 : len(price) - 1]
        if officialPrice == "":
            officialPrice = "0"
        officialPrice = officialPrice.replace("Fre", "0")
        officialPrice = officialPrice.replace("~", "")
        officialPrice = officialPrice.replace(",", ".")
        return officialPrice

    def parse_games(self, response, **kwargs):
        providerResults = response.xpath("//div[contains(@class, 'game-deals-item')]")
        for game in providerResults:
            providerTitle = "".join(
                game.xpath(
                    ".//div[contains(@class, 'game-info-wrapper')]//a[contains(@class, 'game-info-title')]/text()"
                ).getall()
            )
            providerImage = "".join(
                game.xpath(".//a[contains(@class, 'shop-link')]//img/@src").get()
            )
            providerPrice = "".join(
                game.xpath(
                    ".//div[contains(@class, 'game-info-wrapper')]//span[contains(@class, 'game-price-current')]/text()"
                ).getall()
            )
            providerPrice = Ggdeals4Spider.parsePrice(providerPrice)
            providerLink = "".join(
                game.xpath(".//a[contains(@class, 'shop-link')]/@href").getall()
            )
            providerLink = "gg.deals" + providerLink
            print(providerTitle)

            data = {}
            data["title"] = providerTitle
            data["image"] = providerImage
            data["price"] = providerPrice
            data["link"] = providerLink
            json_data = json.dumps(data)
            indexStart = json_data.find("price")
            indexStart = json_data.find(":", indexStart)
            indexStart = json_data.find('"', indexStart)
            json_data = (
                json_data[:indexStart]
                + providerPrice
                + ", "
                + '"link": "'
                + providerLink
                + '"}'
            )
            # DATOS = []
            providerData.append(json_data)
            # print("HOLAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA")
        # print("===============================")
        # print("PROVIDER DATA")
        # print(providerData)

        # game-info-title-wrapper

    def parse(self, response):
        # titles = response.xpath(
        #     "//a[contains(@class, 'game-info-title')]/text()"
        # ).getall()

        results = response.xpath("//div[contains(@class, 'game-item')]")

        for game in results:
            title = "".join(
                game.xpath(".//a[contains(@class, 'game-info-title')]/text()").getall()
            )
            # image = "".join(game.xpath(".//picture//img/@src").getall())
            image = "".join(
                game.xpath(
                    ".//picture//source[contains(@height, '143')]/@srcset"
                ).getall()
            )
            indexStart = image.find(",")
            indexEnd = image.find(" 2x")
            image = image[indexStart:indexEnd]
            # print(image[indexStart:indexEnd])
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
            keyPrice = "".join(
                game.xpath(
                    ".//div[contains(@class, 'shop-price-keyshops')]//div//span//span/text()"
                ).getall()
            )
            data = {}
            # id = idGame
            # data["id"] = self.idGame
            data["title"] = title
            data["image"] = image
            data["releaseDate"] = releaseDate
            # data["genres"] = genres
            # if officialPrice == "":
            #     officialPrice = "NULL"

            officialPrice = Ggdeals4Spider.parsePrice(officialPrice)
            data["officialPrice"] = officialPrice
            # if keyPrice == "":
            #     keyPrice = "NULL"

            keyPrice = Ggdeals4Spider.parsePrice(keyPrice)
            data["keyPrice"] = keyPrice
            json_data = json.dumps(data)

            # QUITO LAS " DE LOS APARTADOS NÚMERICOS Y QUITO LAS "
            # INDEX DE OFFICIAL PRICE
            indexStart = json_data.find("officialPrice")
            indexStart = json_data.find(":", indexStart)
            indexStart = json_data.find('"', indexStart)
            indexEnd = json_data.find(",", indexStart)

            # INDEX DE KEY PRICE
            indexStart2 = json_data.find("keyPrice")
            indexStart2 = json_data.find(":", indexStart2)
            indexStart2 = json_data.find('"', indexStart2)
            indexEnd2 = json_data.find(",", indexStart2)

            prueba = (
                json_data[:indexStart]
                + json_data[indexStart + 1 : indexEnd - 1]
                + json_data[indexEnd:indexStart2]
                + json_data[indexStart2 + 1 : indexEnd2 - 1]
                + json_data[indexEnd2:]
            )
            prueba2 = (
                json_data[:indexStart]
                + officialPrice
                + ", "
                + '"keyPrice": '
                + keyPrice
                + "}"
            )
            # print("====================")
            # print("PRUEBA2")
            # print(prueba2)
            # print("====================")
            # print("PRUEBA")
            # print(prueba)
            # {"title": "Diablo IV", "image": "https://img.gg.deals/9b/75/151098779ccb080d94ee39feeb25e83d1d2d_249xr143.jpg", "releaseDate": "", "officialPrice": 69.99, "keyPrice": 68.29},
            jsonFile.append(prueba)
            self.idGame = self.idGame + 1

        paginas = response.xpath(
            "//a[contains(@aria-label, 'Last page')]/text()"
        ).getall()
        # ultima_pagina = max([*map(int, paginas)])
        ultima_pagina = 2
        current_url = response.url
        indexType = response.url.index("=") + 1
        indexPage = response.url.index("=", indexType) + 1
        base_url = current_url[:indexPage]
        current_page = int(current_url[indexPage:])

        links = response.xpath(
            "//div[contains(@class, 'game-item-with-sidebar')]//a[contains(@class, 'full-link')]/@href"
        ).getall()
        # print("====================================")
        # print(links)

        # BUCLE PARA ENTRAR A CADA JUEGO
        y = 0
        # print(links)
        # print(len(links))
        for game in links:
            # print(f"gg.deals{game}")

            # print(f"{game}")
            # yield response.follow(f"{game}", callback=self.parse_games)
            y = y + 1
            yield response.follow(f"{game}", callback=self.parse_games)
            # if y == 0:
            #     y = y + 1
            #     yield response.follow(f"{game}", callback=self.parse_games)
            # else:
            #     break
        if current_page < ultima_pagina:
            print(f"PAGINA ACTUAL {current_page}")
            yield response.follow(f"{base_url}{current_page+1}")

        # # Quito las comillas simples ', no son necesarias
        # json_data = str(jsonFile)
        # json_data = json_data.replace("'{", " {")
        # json_data = json_data.replace("}'", "}")
        # json_data = json_data.replace("\\", "")

        # with open("VideogamesJSON.json", "w") as outfile:
        #     outfile.write(json_data)

        # # print("==========================")
        # # print("PROVIDER DATA 2")
        # # print(providerData)

        # json_data = str(providerData)
        # json_data = json_data.replace("'{", " {")
        # json_data = json_data.replace("}'", "}")
        # json_data = json_data.replace("\\", "")

        # with open("ProvidersJSON.json", "w") as outfile:
        #     outfile.write(json_data)

        # scrapy shell "https://gg.deals/games/?type=1&page=1"
        # scrapy crawl ggdeals2

        pass

    def closed(self, reason):
        # will be called when the crawler process ends
        # any code
        # do something with collected data
        # Quito las comillas simples ', no son necesarias
        json_data = str(jsonFile)
        json_data = json_data.replace("'{", " {")
        json_data = json_data.replace("}'", "}")
        json_data = json_data.replace("\\", "")

        with open("VideogamesJSON.json", "w") as outfile:
            outfile.write(json_data)

        json_data = str(providerData)
        json_data = json_data.replace("'{", " {")
        json_data = json_data.replace("}'", "}")
        json_data = json_data.replace("\\", "")

        with open("ProvidersJSON.json", "w") as outfile:
            outfile.write(json_data)

from typing import Any, Iterable, Optional
import scrapy
from scrapy.http import Request
from scrapy.http.request import NO_CALLBACK


class FilmSpider(scrapy.Spider):
    name = "film"
    allowed_domains = ["ru.wikipedia.org"]
    start_urls = ["https://ru.wikipedia.org/wiki/%D0%9A%D0%B0%D1%82%D0%B5%D0%B3%D0%BE%D1%80%D0%B8%D1%8F:%D0%A4%D0%B8%D0%BB%D1%8C%D0%BC%D1%8B_%D0%BF%D0%BE_%D0%B0%D0%BB%D1%84%D0%B0%D0%B2%D0%B8%D1%82%D1%83"]

    def parse(self, response):
        DOMAIN = "https://ru.wikipedia.org"
        films = films = response.xpath(
            "//*[@class='mw-category-group']//a/@href"
        ).getall()
        for film in films:
            film_url = DOMAIN + film
            yield response.follow(url=film_url, callback=self.parse_film_page)
        next_page = response.xpath("//div[@id='mw-pages']//a/@href")[-1].extract()
        if next_page:
            next_page_url = DOMAIN + next_page
            yield response.follow(url=next_page_url, callback=self.parse)

    def parse_imdb(self, response):
        pass

    def parse_film_page(self, response):
        film_dict = {
            "title": None,
            "genre": None,
            "director": None,
            "country": None,
            "year": None
        }
        headings = response.xpath("/html/body/div[3]/h1/span/text()").get()
        film_dict["title"] = headings
        table_rows = response.css("table tr")
        for r in table_rows:
            r_text = r.xpath("th/text()").get()
            if r_text and "Режиссёр" in r_text:
                if director := r.xpath('td/span/a/text()').get():
                    film_dict["director"] = director
                else:
                    film_dict["director"] = r.xpath('td//span/text()').get()
            elif r_text == "Страна":
                if country := r.xpath('td//span/a/text()').get():
                    film_dict["country"] = country
                else:
                    film_dict["country"] = r.xpath(
                        'td//span/a/span/text()'
                    ).get()
            elif r_text == "Год" or r_text == "Дата выхода":
                if year := r.xpath('td/a/span/text()').get():
                    film_dict["year"] = year
                elif year := r.xpath('td//span/a/text()').get():
                    film_dict["year"] = year
                else:
                    film_dict["year"] = r.xpath('td/span/text()').get()
            elif (r.xpath("th/a/text()").get()
                  and "Жанр" in r.xpath("th/a/text()").get()):
                if genre := r.xpath('td//span/a/text()').getall():
                    film_dict["genre"] = genre
                else:
                    film_dict["genre"] = r.xpath(
                        'td/div/ul/li/a/text()'
                    ).getall()
        yield film_dict

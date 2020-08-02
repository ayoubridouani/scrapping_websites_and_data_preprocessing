import math
import scrapy
from ..items import HespressItem


class Hespress(scrapy.Spider):
    name = "hespress"
    path_root = "https://www.hespress.com"
    current_page = 1.0

    def start_requests(self):
        urls = [
            'https://www.hespress.com/archive/2019/9',
            'https://www.hespress.com/archive/2019/8'
        ]
        for url in urls:
            yield scrapy.Request(url=url, callback=self.parse)

    def parse(self, response):
        description_link = response.css("p a::attr(href)").getall()
        for i in range(10):
            yield scrapy.Request(url=self.path_root + description_link[i], callback=self.getdesc)

        # next page automatically not working in the website
        # next_page = response.css(".page_groups::attr(href)").getall()[-2]
        # if next_page is not None:
        #     print(next_page)
        #     yield response.follow(url=next_page, callback=self.parse)

        next_page = self.path_root + "/archive/2019/" + str(response.url.split("/")[5]) + "/index." + str(
            int(math.floor(self.current_page))) + ".html"
        if self.current_page <= 272:  # max pages that will scrap: 272
            print(next_page)
            self.current_page += 0.5
            yield response.follow(url=next_page, callback=self.parse)

    def getdesc(self, response):
        url = response.url
        title = response.css(".page_title::text").get()
        comments = response.css(".comment_text::text").getall()

        items = HespressItem()

        items["url"] = url
        items["title"] = title
        items["comments"] = comments

        yield items

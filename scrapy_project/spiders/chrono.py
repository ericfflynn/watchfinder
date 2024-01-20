import scrapy


class ChronoSpider(scrapy.Spider):
    name = "chrono"
    allowed_domains = ["chrono24.com"]
    start_urls = ["https://chrono24.com"]

    def parse(self, response):
        pass

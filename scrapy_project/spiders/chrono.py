import scrapy
from bs4 import BeautifulSoup
import re
import json

class ChronoSpider(scrapy.Spider):
    name = "chrono"
    allowed_domains = ["chrono24.com"]
    start_urls = ["https://chrono24.com"]

    def parse(self, response):
        rows = response.xpath("//html/body/div[2]/main/div/section[6]/div/div/ul/li[1]") #[1] only will get most popular watch
        for row in rows:
            link = row.xpath(".//@href").get()
            yield response.follow(url=link, callback=self.get_watch_results)

    def get_watch_results(self, response):
        results = response.xpath("//div[@class='article-item-container wt-search-result article-image-carousel']/a/@href").extract()
        for result in results:
            link = result
            yield response.follow(url=link, callback=self.extract_watch_results)

    def extract_watch_results(self, response):
        maintable = response.xpath('//table[1]')
        t = BeautifulSoup(maintable[0].extract(),features='lxml').get_text().strip()
        rt = re.sub('\\n+', '_', t)
        split = rt.split("Condition_")
        n1 = split[0]
        n2 = split[1].replace("_"," ", 1)
        final = n1+"Condition_"+n2
        rtf = final.replace("Basic Info_","").replace("Caliber_","").replace("Case_","").replace("Bracelet/strap_","").replace("Functions_","").replace("Try it on_","").replace("Size guide_", "").split("_")
        a = iter(rtf)
        output_dict = dict(zip(a, a))
        yield output_dict
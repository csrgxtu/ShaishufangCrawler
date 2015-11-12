import scrapy

class ShaishufangSpider(scrapy.Spider):
    name = "Shaishufang"
    allowed_domains = ["shaishufang.com"]
    start_urls = [
        "http://shaishufang.com/index.php/site/detail/uid/74557/ubid/10490038/status//category/D/friend/false",
    ]

    def parse(self, response):
        filename = '74557.html'
        with open(filename, 'wb') as f:
            f.write(response.body)

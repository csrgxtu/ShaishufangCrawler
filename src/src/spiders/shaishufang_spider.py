import scrapy

class ShaishufangSpider(scrapy.Spider):
    name = "Shaishufang"
    allowed_domains = ["shaishufang.com"]
    start_urls = [
        'http://shaishufang.com/index.php/site/main/uid/1/status//category//friend/false',
        'http://shaishufang.com/index.php/site/main/uid/74557/status//category//friend/false',
    ]

    def start_requests(self):
        for i in range(len(self.start_urls)):
            yield scrapy.Request(self.start_urls[i], cookies={'shaishufang': 'Mjc5MTYwfGZmY2VmYzIyYmMxZjhlZThjNzgzYjFlOGIxOWUwODg2'})

    def parse(self, response):
        filename = '74557.html'
        with open(filename, 'wb') as f:
            f.write(response.body)

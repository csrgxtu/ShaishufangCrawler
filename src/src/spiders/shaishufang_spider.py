import scrapy

class ShaishufangSpider(scrapy.Spider):
    name = "Shaishufang"
    allowed_domains = ["shaishufang.com"]
    start_urls = []

    # build start_urls list first
    def __init__(self):
        urlPrefix = 'http://shaishufang.com/index.php/site/main/uid/'
        urlPostfix = '/status//category//friend/false'
        for i in range(1, 2):
            self.start_urls.append(urlPrefix + str(i) + urlPostfix)

    def start_requests(self):
        for i in range(len(self.start_urls)):
            yield scrapy.Request(self.start_urls[i], cookies={'shaishufang': 'Mjc5MTYwfGZmY2VmYzIyYmMxZjhlZThjNzgzYjFlOGIxOWUwODg2'})

    def parse(self, response):
        filename = '74557.html'
        with open(filename, 'wb') as f:
            f.write(response.body)

# -*- coding: utf-8 -*-

BOT_NAME = 'src'

SPIDER_MODULES = ['src.spiders']
NEWSPIDER_MODULE = 'src.spiders'

## SETTING FOR CRAWLERA

# Retry many times since proxies often fail
# RETRY_TIMES = 10
DOWNLOAD_DELAY = 0
# Retry on most error codes since proxies fail for different reasons
# RETRY_HTTP_CODES = [500, 503, 504, 400, 403, 404, 408]
# HTTP Proxy enabled

#CRAWLERA_ENABLED = True
#CRAWLERA_USER = '04ec6cb7fd744be28ce4973a962b146d'
#CRAWLERA_PASS = ''
#DEFAULT_REQUEST_HEADERS = {
  # 'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
  # 'Accept-Language': 'zh-CN,zh;q=0.8',
#  'X-Crawlera-Cookies': 'disable'
#}
#AUTOTHROTTLE_ENABLED= False
#CONCURRENT_REQUESTS = 16
#CONCURRENT_REQUESTS_PER_DOMAIN = 16
#AUTOTHROTTLE_ENABLED = False
# DOWNLOAD_TIMEOUT = 600

DOWNLOADER_MIDDLEWARES = {
    # 'scrapy.contrib.downloadermiddleware.retry.RetryMiddleware': 90,
    # 'scrapy.downloadermiddlewares.retry.RetryMiddleware': 90,
#    'scrapy_crawlera.CrawleraMiddleware': 600,
    'src.randomproxy.RandomProxy': 100,
    'scrapy.contrib.downloadermiddleware.httpproxy.HttpProxyMiddleware': 110,
}

# LOG_LEVEL = 'INFO'
CONCURRENT_REQUESTS=8

API_HOST = 'http://192.168.100.3:5000/'
COOKIE = 'Mjc5MTYwfGZmY2VmYzIyYmMxZjhlZThjNzgzYjFlOGIxOWUwODg2'

# PROXY_LIST = '/path/to/proxy/list.txt'

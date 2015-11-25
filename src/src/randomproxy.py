import re
import random
import base64
import logging

from urllib2 import urlopen

url  = "http://svip.kuaidaili.com/api/getproxy/?orderid=983980639044193&num=5&browser=1&protocol=1&method=1&sp1=1&quality=0&sort=0&format=json&sep=1"

def updateIPs(url):

    dictproxies = {}

    req  = urlopen(url)
    page = req.read()

    idx  = page.find('proxy_list') + len('proxy_list') + 4
    s    = page[idx:-3]

    for ul in s.split(','):
        proxy = 'http://' + ul[2:-1]
        dictproxies[proxy] = ''

    return dictproxies


class RandomProxy(object):

    @classmethod
    def process_request(self, request, spider):

        proxies = updateIPs(url)

        proxy_address = random.choice(proxies.keys()) # "http://YOUR_PROXY_IP:PORT"
        proxy_user_pass = proxies[proxy_address]      # "USERNAME:PASSWORD"
        request.meta['proxy'] = proxy_address         # "http://YOUR_PROXY_IP:PORT"
        logging.info(proxy_address)

        # Use the following lines if your proxy requires authentication
        if proxy_user_pass:
            basic_auth = 'Basic ' + base64.encodestring(proxy_user_pass)
            request.headers['Proxy-Authorization'] = basic_auth

import json
import os
import requests
from scrapy.crawler import CrawlerProcess
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import CrawlSpider, Rule, Request
import scrapy_useragents
from win10toast import ToastNotifier

from config import config
QUINTA_CHAT_IDs = config['QUINTA_CHAT_IDs']

PRODUCTS_VILLA_DIANA = []

def inform_bot(message, store, chat_id, send_telegram):
    text = '{store}:\n'.format(store=store)
    for item in message:
        text += item[0] + ': ' + item[1]
        text += '\n'

    toaster = ToastNotifier()
    toaster.show_toast("Tiendas Virtuales", store)

    payload = {
        'chat_id': chat_id,
        'text': text,
    }

    session = requests.Session()  # ignore proxy in requests
    session.trust_env = False
    session.proxy = False

    if send_telegram == True:
        response = session.post('https://api.telegram.org/bot{bot_token}/sendMessage'.format(bot_token=BOT_TOKEN),
                                data=payload)
        print(response.content)


def update_info():

    if PRODUCTS_VILLA_DIANA:
        for chat_id in QUINTA_CHAT_IDs:
            inform_bot(PRODUCTS_VILLA_DIANA, 'Villa Diana', chat_id, True)

class villadianaSpider(CrawlSpider):
    name = 'villadiana_spider'
    allowed_domains = ['tuenvio.cu']
    start_urls = ['https://www.tuenvio.cu/caribehabana/Products?depPid=46087']
    handle_httpstatus_list = [301, 302]

    custom_settings = {
        'HTTPPROXY_ENABLED': False,
        'COOKIES_ENABLED': False,
        'REDIRECT_ENABLE': False,
        'DOWNLOADER_MIDDLEWARES': {
            'scrapy.downloadermiddlewares.useragent.UserAgentMiddleware': None,
            'scrapy_useragents.downloadermiddlewares.useragents.UserAgentsMiddleware': 500,
        },
        'USER_AGENTS': [
            ('Mozilla/5.0 (X11; Linux x86_64) '
             'AppleWebKit/537.36 (KHTML, like Gecko) '
             'Chrome/57.0.2987.110 '
             'Safari/537.36'),  # chrome
            ('Mozilla/5.0 (X11; Linux x86_64) '
             'AppleWebKit/537.36 (KHTML, like Gecko) '
             'Chrome/61.0.3163.79 '
             'Safari/537.36'),  # chrome
            ('Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:55.0) '
             'Gecko/20100101 '
             'Firefox/55.0'),  # firefox
            ('Mozilla/5.0 (X11; Linux x86_64) '
             'AppleWebKit/537.36 (KHTML, like Gecko) '
             'Chrome/61.0.3163.91 '
             'Safari/537.36'),  # chrome
            ('Mozilla/5.0 (X11; Linux x86_64) '
             'AppleWebKit/537.36 (KHTML, like Gecko) '
             'Chrome/62.0.3202.89 '
             'Safari/537.36'),  # chrome
            ('Mozilla/5.0 (X11; Linux x86_64) '
             'AppleWebKit/537.36 (KHTML, like Gecko) '
             'Chrome/63.0.3239.108 '
             'Safari/537.36'),  # chrome
        ],
    }

    rules = (
        # Extract links matching 'category.php' (but not matching 'subsection.php')
        # and follow links from them (since no callback means follow=True by default).
        Rule(LinkExtractor(deny=('/.js'))),
        Rule(LinkExtractor(deny=('/.css'))),
        Rule(LinkExtractor(deny=('/.jpg'))),
        Rule(LinkExtractor(deny=('/.png')))

    )

    def start_requests(self):
        for url in self.start_urls:
            yield Request(url)

    def parse(self, response):
        items = []
        global PRODUCTS_AVAILABLE_IN_VILLA_DIANA

        if response.status == 200:
            items = response.css(".hProductItems div.thumbTitle a::text").extract()
            links = response.css(".hProductItems div.thumbTitle a::attr(href)").extract()
            prices = response.css(".hProductItems div.thumbPrice span::text").extract()


            global PRODUCTS_VILLA_DIANA


            [ PRODUCTS_VILLA_DIANA.append((items[i] + ' ' + prices[i],'https://www.tuenvio.cu/caribehabana/' + links[i])) for i in range(len(items))]

        return {'items': items}


crawler = CrawlerProcess()
crawler.crawl(villadianaSpider)
print('start')

result = crawler.start()
update_info()
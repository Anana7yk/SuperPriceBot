import requests
from bs4 import BeautifulSoup
from urllib.parse import urlparse
class PriceFetcher:
    def fetch_html(self, url):
        response = requests.get(url)
        if response.status_code != 200:
            raise Exception(f'Ошибка загрузки страницы: {url}')
        return response.text

    def get_price_selector(self, url):
        domain = urlparse(url).netloc.lower()

        selectors = {
            'foxfishing.ru': 'price',
            'sunduk-ribaka.ru': 'v-product-prices__general price nowrap',
            'chitai-gorod.ru': 'product-offer-price__current',
            'labirint.ru' : 'buying-priceold-val-number',
            'my-shop.ru' : 'price',
            'biblio-globus.ru': 'price_new price_with_discount',
            'libroroom.ru': 'price_value',
            'mdk-arbat.ru': 'itempage-price_inet',
            'fmagazin.ru' : 'currency rub from',
            'fizmatkniga.org': 'inframe bg'
        }

        for key, value in selectors.items():
            if key in domain:
                return value

        raise ValueError("Неизвестный магазин или неверный URL")

    def extract_price(self, html, url):
        soup = BeautifulSoup(html, 'html.parser')
        selector = self.get_price_selector(url)
        price_tag = soup.find('span', class_=selector)
        if price_tag:
            return self._parse_price(price_tag.text)
        raise ValueError('Цена не найдена на странице', price_tag)


    def _parse_price(self, price_text):
        return float(price_text.replace('₽', '').replace('ðóá.', '').replace(' ', '').strip())


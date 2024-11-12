from pricefetcher import PriceFetcher

class PriceScraper:
    def __init__(self):
        self.fetcher = PriceFetcher()

    def get_price(self, url):
        if not self.is_valid_url(url):
            raise ValueError('Неверный URL')
        html = self.fetcher.fetch_html(url)
        return self.fetcher.extract_price(html, url)

    def is_valid_url(self, url):
        return url.startswith("http")

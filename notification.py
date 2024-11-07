import time
from telegram import Bot

from typing import Optional


class NotificationManager:
    def __init__(self, db, scraper, bot_token: str):
        self.db = db
        self.scraper = scraper
        self.bot: Optional[Bot] = Bot(token=bot_token)

    def check_prices(self):
        while True:
            items = self.db.get_items()
            for item in items:
                current_price = self.scraper.get_price(item['url'])
                if current_price < item['price']:
                    self.db.update_price(item['item_id'], current_price)

                    self.send_notification(item['user_id'], item['url'], current_price)

                    print(f'Цена на товар {item["url"]} снизилась! Новая цена: {current_price} руб.')
            time.sleep(3600)

    def send_notification(self, user_id, url, new_price):
        message = f'Цена на товар {url} снизилась! Новая цена: {new_price} руб.'
        self.bot.send_message(chat_id=user_id, text=message)

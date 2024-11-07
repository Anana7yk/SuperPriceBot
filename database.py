import sqlite3
import json

class DatabaseManager:
    def __init__(self, db_name="prices.db"):
        self.conn = sqlite3.connect(db_name)
        self.cursor = self.conn.cursor()
        self._create_tables()

    def _create_tables(self):
        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS users (
                user_id INTEGER PRIMARY KEY,
                name TEXT
            )
        ''')
        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS items (
                item_id INTEGER PRIMARY KEY AUTOINCREMENT,
                user_id INTEGER,
                url TEXT,
                price REAL,
                price_history TEXT,
                FOREIGN KEY (user_id) REFERENCES users(user_id)
            )
        ''')
        self.conn.commit()

    def add_item(self, user_id, url, price):
        price_history = json.dumps([price])
        self.cursor.execute('''
            INSERT INTO items (user_id, url, price, price_history)
            VALUES (?, ?, ?, ?)
        ''', (user_id, url, price, price_history))
        self.conn.commit()

    def remove_item(self, item_id):
        self.cursor.execute('DELETE FROM items WHERE item_id = ?', (item_id,))
        self.conn.commit()

    def get_items(self, user_id):
        self.cursor.execute('SELECT item_id, url, price FROM items WHERE user_id = ?', (user_id,))
        return self.cursor.fetchall()

    def update_price(self, item_id, new_price):
        self.cursor.execute('SELECT price_history FROM items WHERE item_id = ?', (item_id,))
        price_history = self.cursor.fetchone()[0]
        price_history = json.loads(price_history)
        price_history.append(new_price)
        self.cursor.execute('''
            UPDATE items SET price = ?, price_history = ? WHERE item_id = ?
        ''', (new_price, json.dumps(price_history), item_id))
        self.conn.commit()

    def get_price_history(self, item_id):
        self.cursor.execute('SELECT price_history FROM items WHERE item_id = ?', (item_id,))
        return json.loads(self.cursor.fetchone()[0])

from telegram import Update
from telegram.ext import ContextTypes
from database import DatabaseManager
from scraper import PriceScraper
from notification import NotificationManager
from plotter import PlotManager
from config import bot_token
db = DatabaseManager()
scraper = PriceScraper()
notifier = NotificationManager(db, scraper, bot_token)
plotter = PlotManager(db)

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "Добро пожаловать в Price Tracker Bot! Используйте /add <URL> для добавления товара."
    )

async def add_item(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if len(context.args) != 1:
        await update.message.reply_text('Пожалуйста, отправьте URL товара.')
        return

    url = context.args[0]
    user_id = update.message.from_user.id
    price = scraper.get_price(url)

    if price:
        db.add_item(user_id, url, price)
        await update.message.reply_text(f'Товар добавлен для отслеживания. Начальная цена: {price} руб.')
    else:
        await update.message.reply_text("Не удалось получить цену с указанного URL.")

async def remove_item(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if len(context.args) != 1:
        await update.message.reply_text('Пожалуйста, укажите ID товара для удаления.')
        return

    item_id = int(context.args[0])
    db.remove_item(item_id)
    await update.message.reply_text(f'Товар с ID {item_id} удалён из списка отслеживаемых.')

async def list_items(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.message.from_user.id
    items = db.get_items(user_id)

    if not items:
        await update.message.reply_text('У вас нет отслеживаемых товаров.')
        return

    response = 'Ваши отслеживаемые товары:\n'
    for item_id, url, price in items:
        response += f"{item_id}. {url} - {price} руб.\n"

    await update.message.reply_text(response)

async def show_stats(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if len(context.args) != 1:
        await update.message.reply_text('Пожалуйста, укажите ID товара для статистики.')
        return

    item_id = int(context.args[0])
    graph = plotter.generate_price_graph(item_id)

    await update.message.reply_photo(photo=graph)

async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        'Используйте команды /add, /remove, /list, /stats для взаимодействия с ботом.'
    )

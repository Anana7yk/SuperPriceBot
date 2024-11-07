from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, filters, ContextTypes
from database import DatabaseManager
from scraper import PriceScraper
from notification import NotificationManager
from plotter import PlotManager

bot_token = '8001944130:AAFXs6fgTpW4egjOdBakgwf-CfTDOzSc78c'
db = DatabaseManager()
scraper = PriceScraper()
notifier = NotificationManager(db, scraper, bot_token)
plotter = PlotManager(db)


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "Добро пожаловать в Price Tracker Bot! Используйте /add <URL> для добавления товара.")


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
    for item in items:
        # Используем индексы для обращения к элементам кортежа
        item_id, url, price = item
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
    await update.message.reply_text('Используйте команды /add, /remove, /list, /stats для взаимодействия с ботом.')


def main():
    app = ApplicationBuilder().token(bot_token).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("add", add_item))
    app.add_handler(CommandHandler("remove", remove_item))
    app.add_handler(CommandHandler("list", list_items))
    app.add_handler(CommandHandler("stats", show_stats))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))

    app.run_polling()


if __name__ == "__main__":
    main()
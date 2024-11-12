from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, filters
from handlers import start, add_item, remove_item, list_items, show_stats, handle_message
from config import bot_token
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

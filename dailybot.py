from telegram.ext import Updater, MessageHandler, CommandHandler, Filters
from telegram import ParseMode
import logging
from quotesScraper import quotes_main
import random, secrets
import os

__allQuotes, __taggedQuotes = quotes_main()
choose_random = secrets.SystemRandom()

TOKEN = os.environ.get('DAILYBOT_TOKEN')

def start(update, context):
    welcome_text = "Hey! Watcha doin? Want to hear something exciting?"
    context.bot.send_message(
        chat_id = update.effective_chat.id, text = welcome_text
    )

def quote(update, context):
    category = update.message.text.replace("/quote", "").split()
    if not len(category) == 0 and category[0] in __taggedQuotes:
        try:
            text, author = secrets.choice(__taggedQuotes[category[0]])
        except:
            text = secrets.choice(__taggedQuotes[category[0]])[0]
            author = "Anonymous"
        reply = f"<b><i>{text}</i></b>\nby <i>{author}</i>"
        context.bot.send_message(
            chat_id = update.effective_chat.id, text = reply, parse_mode = ParseMode.HTML
        )
    else:
        try:
            text, author = secrets.choice(__allQuotes)
        except:
            text = secrets.choice(__allQuotes)
            author = "Anonymous"
        reply = f"Here's something:\n<b><i>{text}</i></b>\nby <i>{author}</i>"
        context.bot.send_message(
            chat_id = update.effective_chat.id, text = reply, parse_mode = ParseMode.HTML
        )

def echo(update, context):
    echo_back = update.message.text 
    context.bot.send_message(
        chat_id = update.effective_chat.id, text= echo_back
    )

if __name__ == "__main__":
    updater = Updater(token = TOKEN, use_context=True)
    dispatcher = updater.dispatcher
    logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)

    # intialise handlers
    start_handler = CommandHandler('start', start)
    dispatcher.add_handler(start_handler)

    quote_handler = CommandHandler('quote', quote)
    dispatcher.add_handler(quote_handler)

    echo_handler = MessageHandler( Filters.text & (~Filters.command), echo)
    dispatcher.add_handler(echo_handler)

    updater.start_polling()
    updater.idle()
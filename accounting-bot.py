from settings import TOKEN

from typing import Dict

from telegram import ReplyKeyboardMarkup, Update
from telegram.ext import (
    Updater,
    CommandHandler,
    Filters,
    ConversationHandler,
    CallbackContext,
)

def start(update: Update, context: CallbackContext):
    name = update.message.from_user.username
    saludo = f"""
    Hola {name}! Esto es un digitador contable
    """
    update.message.reply_text(saludo)


def main():
    updater = Updater(TOKEN, use_context=True)

    updater.dispatcher.add_handler(
        CommandHandler("start", start)
    )

    #start
    updater.start_polling()
    print('arranco...')

    #esperando
    updater.idle()


if __name__ == "__main__":
    main()

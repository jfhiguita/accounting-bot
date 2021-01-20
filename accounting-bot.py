"""
Este es un bot que muestra las preguntas en botones para elegir,
pero las respuestas deben ser digitadas
"""

#libreria propia
from settings import TOKEN


#librerias externas
import logging

from telegram import ReplyKeyboardMarkup, Update
from telegram.ext import (
    Updater,
    CommandHandler,
    MessageHandler,
    Filters,
    ConversationHandler,
    CallbackContext,
)

# enable logging
logging.basicConfig(
    format = '%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO
)

logger = logging.getLogger(__name__)

CHOOSING, TYPING_REPLY, TYPING_CHOICE = range(3)

reply_keyboard = [
    ['Fecha', 'Detalle'],
    ['Cantidad', 'Medida'],
    ['Valor', 'Entrega Factura'],
    ['Listo'],
]
markup = ReplyKeyboardMarkup(reply_keyboard, one_time_keyboard=True)


def data_sheet(user_data:dict()):
    data_typing = []

    for key, value in user_data.items():
        data_typing.append(f'{key} - {value}')

    return "\n".join(data_typing).join(["\n","\n"])


def start(update: Update, context: CallbackContext):
    name = update.message.from_user.username
    saludo = f"""
    Hola {name}! Soy un digitador automatico.\n
    Escoja cada uno de los items y digite su valor
    """
    update.message.reply_text(saludo, reply_markup=markup,)

    return CHOOSING


def regular_choice(update: Update, context: CallbackContext):
    pass


def done(update: Update, context: CallbackContext):
    pass


def main():
    updater = Updater(TOKEN, use_context=True)
    dispatcher = updater.dispatcher

    #add conversation handler with the states
    conv_handler = ConversationHandler(
        entry_points = [CommandHandler('start', start)],
        states = {
            CHOOSING: [
                MessageHandler(
                    Filters.regex('^(Fecha|Detalle|Cantidad|Medida|Valor|Entrega Factura)$'), regular_choice
                ),
            ],
        },
        fallbacks = [MessageHandler(Filters.regex('^Listo$'), done)],
    )

    dispatcher.add_handler(conv_handler)

    #start
    updater.start_polling()
    print('arranco...')

    #esperando
    updater.idle()


if __name__ == "__main__":
    main()

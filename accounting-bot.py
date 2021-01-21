"""
Este es un bot que muestra las preguntas en botones para elegir,
pero las respuestas deben ser digitadas
"""

#libreria propia
from settings import TOKEN


#librerias externas
import datetime
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
    Hola {name}! Soy un digitador automatico.
    Escoja cada uno de los items y digite su valor
    """
    update.message.reply_text(saludo, reply_markup=markup,)

    return CHOOSING


def regular_choice(update: Update, context: CallbackContext):
    choosen_answer = update.message.text
    context.user_data['choice'] = choosen_answer
    notice = f'Tu elegiste {choosen_answer.lower()} Dime cual?'
    update.message.reply_text(notice)

    return TYPING_REPLY



def done(update: Update, context: CallbackContext):
    user_data = context.user_data
    if 'choice' in user_data:
        del user_data['choice']

    notice = f'Esta es la informacion a guardar:\n{(user_data)}\nBye!'
    update.message.reply_text(notice)
    #queda pendiente la funcion de guardar la info

    user_data.clear()
    return ConversationHandler.END


def received_information(update: Update, context: CallbackContext):
    user_data = context.user_data
    typed_answer = update.message.text
    #typed_answer = update.message.date.strftime('%Y-%m-%d')
    category = user_data['choice']
    user_data[category] = typed_answer
    del user_data['choice']

    notice = f'esto me has dicho:\n{data_sheet(user_data)}, Dime que mas?'
    update.message.reply_text(notice, reply_markup=markup)
    
    return CHOOSING


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
            TYPING_REPLY: [
                MessageHandler(
                    Filters.text & ~(Filters.command | Filters.regex('^Listo$')),
                    received_information,
                )
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

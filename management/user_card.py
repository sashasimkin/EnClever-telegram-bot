from telegram.ext import Updater
from mongoengine import *

import logging
from telegram.ext import MessageHandler, Filters
from telegram import InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Updater, CommandHandler, CallbackQueryHandler

connect('testbd1')


class FlashCard(Document):
    """
    FlashCard
    """
    term = StringField(required=True)
    term_native = StringField(required=True)  # In russian
    description = StringField(required=True)
    pic = StringField(required=True)  # URL/path to the image

    meta = {'allow_inheritance': True}

for c in FlashCard.objects:
    print(c.term + c.term_native + c.description, c.pic)


updater = Updater(token='349763703:AAEJJVColK86rVmlaXxzh-tGU4XYN3YQWi4')
dispatcher = updater.dispatcher
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                     level=logging.INFO)


def start(bot, update):
    bot.send_message(chat_id=update.message.chat_id, text="Hello")

start_handler = CommandHandler('start', start)
dispatcher.add_handler(start_handler)


def user_card(bot, update):
    keyboard = [[InlineKeyboardButton("1 - Add card", callback_data='1'),
                 InlineKeyboardButton("2 - Change card", callback_data='2')],
                 [InlineKeyboardButton("4 - All cards", callback_data='4'),
                 InlineKeyboardButton("3 - Delete card", callback_data='3')]]
    reply_markup = InlineKeyboardMarkup(keyboard)
    update.message.reply_text('Please choose:', reply_markup=reply_markup)


def button(bot, update):
    query = update.callback_query
    bot.edit_message_text(text="Selected option: %s" % query.data,
                          chat_id=query.message.chat_id,
                          message_id=query.message.message_id)


def all_user_card(bot, update, args):
    all = []
    for c in FlashCard.objects:
        print(c.term + c.term_native + c.description, c.pic)
        # all = c.term + c.term_native + c.description, c.pic
        all_in_card = []
        all_in_card.append(c.term)
        all_in_card.append(c.term_native)
        all_in_card.append(c.description)
        all_in_card.append(c.pic)
        str_in_card = " ".join(all_in_card)

        all.append(str_in_card)
        bot.send_message(chat_id=update.message.chat_id, text=str_in_card)

all_handler = CommandHandler('all_user_card', all_user_card, pass_args=True)
dispatcher.add_handler(all_handler)


# add new user card
def add(user_term, user_term_native, user_description, user_pic):
    FlashCard(term=user_term, term_native=user_term_native, description=user_description, pic=user_pic).save()


# delete user card
def delete(id):
    obj = FlashCard.objects(term=id)
    obj.delete()
    #FlashCard.remove({'term':id})#.update(unset__sensordict__S=id)



updater.dispatcher.add_handler(CommandHandler('start', start))
updater.dispatcher.add_handler(CommandHandler('user_card', user_card))
updater.dispatcher.add_handler(CallbackQueryHandler(button))

# Start the Bot
updater.start_polling()
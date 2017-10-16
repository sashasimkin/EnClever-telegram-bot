from telegram.ext import Updater
from telegram.ext import CommandHandler, CallbackQueryHandler
from telegram import InlineKeyboardButton, InlineKeyboardMarkup


class UserCommandHandler(object):

    def __init__(self, dispatcher):
        self.dispatcher = dispatcher

    def add_handlers(self):
        self.dispatcher.add_handler(CommandHandler('hello', self.hello))
        self.dispatcher.add_handler(CommandHandler('stop', self.stop))
        self.dispatcher.add_handler(CommandHandler('start', self.start))
        self.dispatcher.add_handler(CallbackQueryHandler(self.button))

    
    def hello(self, bot, update):
        bot.send_message(chat_id=update.message.chat_id, text="Hi there! I'm your personal demon, which will hunt you 24/7.\
                                                                     I'm gonna teach you some english you never forget")

    def start(self, bot, update):
        keyboard = [[InlineKeyboardButton("Beginner", callback_data='Beginner')],
                 [InlineKeyboardButton("Intermediate", callback_data='Intermediate')],
                [InlineKeyboardButton("Fluent", callback_data='Fluent')]]

        reply_markup = InlineKeyboardMarkup(keyboard)

        update.message.reply_text('Please choose your target english level:', reply_markup=reply_markup)

    def button(self, bot, update):
        query = update.callback_query


        bot.edit_message_text(text="Selected level: %s" % query.data,
                              chat_id=query.message.chat_id,
                              message_id=query.message.message_id)

class EnCleverBot(object):

    def __init__(self, token):
        self.updater = Updater(token=token)
        self.dispatcher = self.updater.dispatcher
        self.handler = UserCommandHandler(self.dispatcher)

    def run(self):
        print('Less go')
        self.handler.add_handlers()
        self.updater.start_polling()
        self.updater.idle()

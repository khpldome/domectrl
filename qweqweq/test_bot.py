

import logging

import test_json


logging.basicConfig(filename='telegram_bot.log',
                    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    level=logging.INFO)
# logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.DEBUG)
logger = logging.getLogger()
logger.setLevel(logging.INFO)
# logger.setLevel(logging.DEBUG)

TOKEN = '345369460:AAGgeEcjoDtS2YCk9f8_N03rBUxjItk_vco'

# bot = telegram.Bot(token=TOKEN)
# print(bot.get_me())
# logging.debug(bot.get_me())
#
# updates = bot.get_updates()
# print([u.message.text for u in updates])
#
# chat_id = bot.get_updates()[-1].message.chat_id
# print("chat_id=", chat_id)
#
# bot.send_message(chat_id=chat_id, text="I'm sorry Dave I'm afraid I can't do that.")
# logging.info("I'm sorry Dave I'm afraid I can't do that.")



from telegram.ext import Updater
from telegram.ext import CommandHandler
from telegram.ext import MessageHandler, Filters

updater = Updater(token=TOKEN)
dispatcher = updater.dispatcher


def start(bot, update):
    bot.send_message(chat_id=update.message.chat_id, text="I'm a bot, please talk to me!")


start_handler = CommandHandler('start', start)
dispatcher.add_handler(start_handler)


def echo(bot, update):
    val = 'units_per_em'
    output = str(update.message.text) + ': ' + str(val)
    bot.send_message(chat_id=update.message.chat_id, text=output)
    logging.info("bot.send_message:" + output)


echo_handler = MessageHandler(Filters.text, echo)
dispatcher.add_handler(echo_handler)


def caps(bot, update, args):
    text_caps = ' '.join(args).upper()
    bot.send_message(chat_id=update.message.chat_id, text=text_caps)


caps_handler = CommandHandler('caps', caps, pass_args=True)
dispatcher.add_handler(caps_handler)


def put(bot, update, args):
    lst = args
    output = test_json.write_dict_content(lst)
    bot.send_message(chat_id=update.message.chat_id, text=output)


put_handler = CommandHandler('put', put, pass_args=True)
dispatcher.add_handler(put_handler)


def get(bot, update, args):
    lst = args
    output = test_json.read_dict_content(lst)
    bot.send_message(chat_id=update.message.chat_id, text=output)


get_handler = CommandHandler('get', get, pass_args=True)
dispatcher.add_handler(get_handler)


updater.start_polling()


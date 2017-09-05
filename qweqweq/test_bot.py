
import telegram
from telegram.ext import Updater
from telegram.ext import CommandHandler
import logging

logging.basicConfig(filename='telegram_bot.log',
                    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    level=logging.INFO)
# logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.DEBUG)
logger = logging.getLogger()
logger.setLevel(logging.INFO)
# logger.setLevel(logging.DEBUG)

TOKEN = '345369460:AAGgeEcjoDtS2YCk9f8_N03rBUxjItk_vco'

bot = telegram.Bot(token=TOKEN)
print(bot.get_me())
logging.debug(bot.get_me())

updates = bot.get_updates()
print([u.message.text for u in updates])

chat_id = bot.get_updates()[-1].message.chat_id
print("chat_id=", chat_id)

bot.send_message(chat_id=chat_id, text="I'm sorry Dave I'm afraid I can't do that.")
logging.info("I'm sorry Dave I'm afraid I can't do that.")

# updater = Updater(token=TOKEN)
# dispatcher = updater.dispatcher
#
#
# def start(bot, update):
#     bot.send_message(chat_id=update.message.chat_id, text="I'm a bot, please talk to me!")
#
# start_handler = CommandHandler('start', start)
# dispatcher.add_handler(start_handler)
#
# updater.start_polling()





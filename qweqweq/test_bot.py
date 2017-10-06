

import logging

import test_json


from telegram.ext import Updater
from telegram.ext import CommandHandler
from telegram.ext import MessageHandler, Filters


def start(bot, update):
    bot.send_message(chat_id=update.message.chat_id, text="I'm a bot, please talk to me!")


def echo(bot, update):
    import socket
    name = socket.gethostname().encode('utf-8')
    text = (": " + update.message.text).encode('utf-8')
    output = name + text
    bot.send_message(chat_id=update.message.chat_id, text=output.decode())
    logging.info("bot.send_message: " + output.decode())
    print("/echo: " + output.decode())


def caps(bot, update, args):
    output = ' '.join(args).upper()
    bot.send_message(chat_id=update.message.chat_id, text=output)
    print("/caps: " + output)


def put(bot, update, args):
    lst = args
    output = test_json.write_dict_content(lst)
    bot.send_message(chat_id=update.message.chat_id, text=output)
    print("/put: " + output)


def get(bot, update, args):
    lst = args
    print("get:", str(lst))
    output = test_json.read_dict_content(lst)
    bot.send_message(chat_id=update.message.chat_id, text=output)
    print("/get: " + output)


def dlt(bot, update, args):  # delete
    lst = args
    print("dlt:", str(lst))
    output = test_json.delete_dict_content(lst)
    bot.send_message(chat_id=update.message.chat_id, text=output)
    print("/dlt: " + output)


def pull(bot, update, args):
    lst = args
    output = test_json.copy_gdrive_2_localFile()
    bot.send_message(chat_id=update.message.chat_id, text=output)


def push(bot, update, args):
    lst = args
    output = test_json.copy_localFile_2_gdrive()
    bot.send_message(chat_id=update.message.chat_id, text=output)


def error(bot, update, error):
    logger.warning('Update "%s" caused error "%s"' % (update, error))


# This handler must be added last!!!
def unknown(bot, update):
    bot.send_message(chat_id=update.message.chat_id, text="Unknown command!")


def main_bot():

    # Enable logging
    logging.basicConfig(filename='telegram_bot.log',
                        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                        level=logging.INFO)
    logger = logging.getLogger(__name__)
    # print("logger:", logger)

    TOKEN = '345369460:AAGgeEcjoDtS2YCk9f8_N03rBUxjItk_vco'
    updater = Updater(token=TOKEN)
    dispatcher = updater.dispatcher

    start_handler = CommandHandler('start', start)
    dispatcher.add_handler(start_handler)
    dispatcher.add_handler(MessageHandler(Filters.text, echo))
    dispatcher.add_handler(CommandHandler('caps', caps, pass_args=True))
    dispatcher.add_handler(CommandHandler('put', put, pass_args=True))
    dispatcher.add_handler(CommandHandler('get', get, pass_args=True))
    dispatcher.add_handler(CommandHandler('dlt', dlt, pass_args=True))
    dispatcher.add_handler(CommandHandler('pull', pull, pass_args=True))
    dispatcher.add_handler(CommandHandler('push', push, pass_args=True))

    # log all errors
    dispatcher.add_error_handler(error)
    dispatcher.add_handler(MessageHandler(Filters.command, unknown))

    updater.start_polling()
    updater.idle()


def parse_args(cmd, list_args):
    '''

                                                /help
                                                /info
    get(x, '/a/b/43')                           /get a b 43
    search(x, "a/b/[cd]")                       /srch a b [cd]
    search(x, "a/b/[cd]", yielded=True)         /srch a b [cd] -y
    search(x, '**', afilter=afilter)            /srch ** -f
    set(x, 'a/b/[cd]', 'Waffles')               /set a b [cd] Waffles
    new(x, 'a/b/e/f/g', "Roffle")               /new a b e f g Roffle
    new(x, 'a/b/e/f/h', [])                     /new a b e f h -l
    new(x, 'a/b/e/f/h/13', 'big array')         /new a b e f h 13 big_sarray

    dlt(x, '/a/b/43')                           /dlt a b 43
    '''

    glob = ''
    val = 'val'
    flag = None
    if list_args:
        pass

    return glob, val, flag


if __name__ == '__main__':

    # main_bot()

    res = parse_args("get", ['dfsdfs' '11212'])
    print(res)


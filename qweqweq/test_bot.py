

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


def set(bot, update, args):

    glob, val, flag = parse_args(args)
    output = test_json.set_dict_content(glob, val, flag)
    bot.send_message(chat_id=update.message.chat_id, text=output)
    print("/set: " + output)


def get(bot, update, args):

    glob, val, flag = parse_args(args)
    output = test_json.get_dict_content(glob, val, flag)
    bot.send_message(chat_id=update.message.chat_id, text=output)
    print("/get: " + output)


def srch(bot, update, args):

    glob, val, flag = parse_args(args)
    output = test_json.search_dict_content(glob, val, flag)
    bot.send_message(chat_id=update.message.chat_id, text=output)
    print("/srch: " + output)


def dlt(bot, update, args):  # delete

    glob, val, flag = parse_args(args)
    output = test_json.delete_dict_content(glob, val, flag)
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
    dispatcher.add_handler(CommandHandler('set', set, pass_args=True))
    dispatcher.add_handler(CommandHandler('get', get, pass_args=True))
    dispatcher.add_handler(CommandHandler('srch', srch, pass_args=True))
    dispatcher.add_handler(CommandHandler('dlt', dlt, pass_args=True))
    dispatcher.add_handler(CommandHandler('pull', pull, pass_args=True))
    dispatcher.add_handler(CommandHandler('push', push, pass_args=True))

    # log all errors
    dispatcher.add_error_handler(error)
    dispatcher.add_handler(MessageHandler(Filters.command, unknown))

    updater.start_polling()
    updater.idle()


def parse_args(list_args):
    '''
    Может быть либо value, либо flag. Одновременно оба быть не могут!
                                                /help
                                                /info
    get(x, '/a/b/43')                           /get a b 43
    search(x, "a/b/[cd]")                       /srch a b [cd]
    search(x, "a/b/[cd]", yielded=True)         /srch a b [cd] -y
    search(x, '**', afilter=afilter)            /srch ** -f
    set(x, 'a/b', 'Waffles', afilter=afilter)   /set a b [cd] Waffles -fRafff
    delete(x, 'a/b/e/f/g')                      /dlt a b e f g
    new(x, 'a/b/e/f/g', "Roffle")               /new a b e f g Roffle
    new(x, 'a/b/e/f/h', [])                     /new a b e f h -l
    new(x, 'a/b/e/f/h/13', 'big array')         /new a b e f h 13 big_sarray
    delete(x, '/a/b/43')                        /dlt a b 43
    '''

    glob = ''
    val = ''
    flag = None
    if len(list_args) > 1:

        glob = "/".join(list_args[:-1])
        last = list_args[-1]    # take last item

        # Проверяем последний (если он из флагов)
        if last[:2] in ['-y', '-f', '-l']:
            # Handle flags
            flag = last
        else:
            val = last
    else:
        print('Short command!')
        glob = "/".join(list_args)

    return glob, val, flag


if __name__ == '__main__':

    main_bot()

    # lst_1 = ['a', 'b', 'c', '[df]', 'sssssdddds', '-y']
    # lst_2 = ['a', 'b', 'c', '[df]', 'sssssdddds']
    # lst_3 = ['a', 'b', 'c', '[df]']
    # lst_4 = ['a', 'b']
    # lst_5 = ['a', ]
    # lst_6 = ['a', '-l']
    # lst_6 = ['a', 'ss', 'q', '-fhjkl']
    #
    # print(lst_1, parse_args(lst_1))
    # print(lst_2, parse_args(lst_2))
    # print(lst_3, parse_args(lst_3))
    # print(lst_4, parse_args(lst_4))
    # print(lst_5, parse_args(lst_5))
    # print(lst_6, parse_args(lst_6))











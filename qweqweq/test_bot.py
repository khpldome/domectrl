#!/usr/bin/env python
# -*- coding: utf-8 -*-

import logging

import test_json
import test_conversation as tc

from telegram.ext import (Updater, CommandHandler, MessageHandler, Filters, RegexHandler,
                          ConversationHandler)
from telegram.ext import CallbackQueryHandler
from telegram import InlineKeyboardButton, InlineKeyboardMarkup
from telegram import (ReplyKeyboardMarkup, ReplyKeyboardRemove)


GENDER, PHOTO, LOCATION, BIO = range(4)


# Enable logging
logging.basicConfig(filename='telegram_bot.log',
                    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    level=logging.INFO)
logger = logging.getLogger(__name__)


def start(bot, update):
    # bot.send_message(chat_id=update.message.chat_id, text="I'm a bot, please talk to me!")
    keyboard = [[InlineKeyboardButton("/get", callback_data='/get'),
                 InlineKeyboardButton("Option 2", callback_data='2')],
                [InlineKeyboardButton("Option 3", callback_data='3')]]

    reply_markup = InlineKeyboardMarkup(keyboard)

    update.message.reply_text('Please choose:', reply_markup=reply_markup)


def button(bot, update):
    query = update.callback_query

    bot.edit_message_text(text="Typed: %s" % query.data,
                          chat_id=query.message.chat_id,
                          message_id=query.message.message_id)

###############################################################################


def info(bot, update):
    reply_keyboard = [['Boy', 'Girl', '/get'], ]

    update.message.reply_text(
        'Send /cancel to stop talking to me.\n\n',
        reply_markup=ReplyKeyboardMarkup(reply_keyboard, one_time_keyboard=True))


def cancel(bot, update):
    user = update.message.from_user
    logger.info("User %s canceled the conversation." % user.first_name)
    update.message.reply_text('Bye! I hope we can talk again some day.',
                              reply_markup=ReplyKeyboardRemove())


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

    keyboard = [[InlineKeyboardButton("/caps", callback_data='/caps'),
                 InlineKeyboardButton("/echo", callback_data='/echo')],

                [InlineKeyboardButton("/get", callback_data=output)]]

    update.message.reply_text(reply_markup=InlineKeyboardMarkup(keyboard))


def get(bot, update, args):

    glob, val, flag = parse_args('get', args)
    output, list_keys = test_json.get_dict_content(glob, val, flag)
    # bot.send_message(chat_id=update.message.chat_id, text=output)
    # print("->/get " + args + '/n<-' + output)

    user = update.message.from_user
    output = user.first_name + ' ' + user.last_name + ':\n' + output
    # {'id': 442763659, 'first_name': 'Serhii', 'is_bot': False, 'last_name': 'Surmylo', 'username': 'Serhii_Surmylo',
    #  'language_code': 'ru'}
    if user.id == 442763659:
        if len(list_keys) > 0:
            line = []
            for i in list_keys:
                # reply_keyboard = [['/get '+list_keys[0], '/get '+list_keys[1], '/get '+list_keys[2], ],
                #                   ['/get ', '/info'], ]
                line.append('/get ' + glob + ' ' + i)
                reply_keyboard = [line, ['/get ', '/info'], ]
        else:
            reply_keyboard = [['/get', ]]

        update.message.reply_text(
            output,
            reply_markup=ReplyKeyboardMarkup(reply_keyboard, one_time_keyboard=True))
    else:
        update.message.reply_text('Unaccepted action!')


def srch(bot, update, args):

    glob, val, flag = parse_args('srch', args)
    output = test_json.search_dict_content(glob, val, flag)
    bot.send_message(chat_id=update.message.chat_id, text=output)
    print("->/srch " + str(args) + '/n<-' + str(output))


def set(bot, update, args):

    glob, val, flag = parse_args('set', args)
    output = test_json.set_dict_content(glob, val, flag)
    bot.send_message(chat_id=update.message.chat_id, text=output)
    print("/set: " + output)


def new(bot, update, args):

    glob, val, flag = parse_args('new', args)
    output = test_json.new_dict_content(glob, val, flag)
    bot.send_message(chat_id=update.message.chat_id, text=output)
    print("->/new " + str(args) + '/n<-' + output)


def dlt(bot, update, args):  # delete

    glob, val, flag = parse_args('dlt', args)
    output = test_json.delete_dict_content(glob, val, flag)
    bot.send_message(chat_id=update.message.chat_id, text=output)
    print("->/dlt " + str(args) + '/n<-' + output)


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

    TOKEN = '345369460:AAGgeEcjoDtS2YCk9f8_N03rBUxjItk_vco'
    updater = Updater(token=TOKEN)
    dispatcher = updater.dispatcher

    dispatcher.add_handler(CommandHandler('start', start))
    # dispatcher.add_handler(CallbackQueryHandler(button))

    dispatcher.add_handler(CommandHandler('info', info))
    dispatcher.add_handler(CommandHandler('cancel', cancel))

    # dispatcher.add_handler(MessageHandler(Filters.text, echo))
    dispatcher.add_handler(CommandHandler('caps', caps, pass_args=True))
    dispatcher.add_handler(CommandHandler('get', get, pass_args=True))
    dispatcher.add_handler(CommandHandler('srch', srch, pass_args=True))
    dispatcher.add_handler(CommandHandler('set', set, pass_args=True))
    dispatcher.add_handler(CommandHandler('new', new, pass_args=True))
    dispatcher.add_handler(CommandHandler('dlt', dlt, pass_args=True))
    dispatcher.add_handler(CommandHandler('pull', pull, pass_args=True))
    dispatcher.add_handler(CommandHandler('push', push, pass_args=True))

    # Add conversation handler with the states GENDER, PHOTO, LOCATION and BIO
    conv_handler = ConversationHandler(
        entry_points=[CommandHandler('start2', tc.start2)],

        states={
            GENDER: [RegexHandler('^(Boy|Girl|Other)$', tc.gender)],

            PHOTO: [MessageHandler(Filters.photo, tc.photo),
                    CommandHandler('skip', tc.skip_photo)],

            LOCATION: [MessageHandler(Filters.location, tc.location),
                       CommandHandler('skip', tc.skip_location)],

            BIO: [MessageHandler(Filters.text, tc.bio)]
        },

        fallbacks=[CommandHandler('cancel', tc.cancel2)]
    )

    dispatcher.add_handler(conv_handler)

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
    set(x, 'a/b', 'Waffles', afilter=afilter)   /set a b [cd] Waffles -fRafff
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

        # Check last for flag or value
        if last[:2] in ['-y', '-f', '-l']:
            # Handle flags
            flag = last
        elif cmd in ['set', 'new']:
            val = last
        else:
            glob += '/' + last
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











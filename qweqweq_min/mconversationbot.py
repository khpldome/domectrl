#!/usr/bin/env python
# -*- coding: utf-8 -*-
𞹗=range
ڿ=True
from telegram import(ReplyKeyboardMarkup,ReplyKeyboardRemove)
from telegram.ext import(Updater,CommandHandler,MessageHandler,Filters,RegexHandler,ConversationHandler)
ݺ=ConversationHandler.END
𥁱=Filters.text
ܙ=Filters.location
ٺ=Filters.photo
import logging
𐰠=logging.getLogger
𞠅=logging.INFO
𞺅=logging.basicConfig
𞺅(filename='conversbot.log',format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',level=𞠅)
𥖑=𐰠(__name__)
𞢑,㘉,熏,𧟍=𞹗(4)
def 𪄓(bot,뫲):
 ﷆ=[['Boy','Girl','Other'],]
 뫲.message.reply_text('Hi! My name is Professor Bot. I will hold a conversation with you. ' 'Send /cancel to stop talking to me.\n\n' 'Are you a boy or a girl?',reply_markup=ReplyKeyboardMarkup(ﷆ,one_time_keyboard=ڿ))
 return 𞢑
def 덻(bot,뫲):
 𫷆=뫲.message.from_user
 𥖑.info("Gender of %s: %s"%(𫷆.first_name,뫲.message.text))
 뫲.message.reply_text('I see! Please send me a photo of yourself, ' 'so I know what you look like, or send /skip if you don\'t want to.',reply_markup=ReplyKeyboardRemove())
 return 㘉
def 𐬥(bot,뫲):
 𫷆=뫲.message.from_user
 𧛚=bot.get_file(뫲.message.photo[-1].file_id)
 𧛚.download('user_photo.jpg')
 𥖑.info("Photo of %s: %s"%(𫷆.first_name,'user_photo.jpg'))
 뫲.message.reply_text('Gorgeous! Now, send me your location please, ' 'or send /skip if you don\'t want to.')
 return 熏
def 𢵡(bot,뫲):
 𫷆=뫲.message.from_user
 𥖑.info("User %s did not send a photo."%𫷆.first_name)
 뫲.message.reply_text('I bet you look great! Now, send me your location please, ' 'or send /skip.')
 return 熏
def 蚎(bot,뫲):
 𫷆=뫲.message.from_user
 𐫛=뫲.message.location
 𥖑.info("Location of %s: %f / %f"%(𫷆.first_name,𐫛.latitude,𐫛.longitude))
 뫲.message.reply_text('Maybe I can visit you sometime! ' 'At last, tell me something about yourself.')
 return 𧟍
def ﲫ(bot,뫲):
 𫷆=뫲.message.from_user
 𥖑.info("User %s did not send a location."%𫷆.first_name)
 뫲.message.reply_text('You seem a bit paranoid! ' 'At last, tell me something about yourself.')
 return 𧟍
def څ(bot,뫲):
 𫷆=뫲.message.from_user
 𥖑.info("Bio of %s: %s"%(𫷆.first_name,뫲.message.text))
 뫲.message.reply_text('Thank you! I hope we can talk again some day.')
 return ݺ
def 𤛘(bot,뫲):
 𫷆=뫲.message.from_user
 𥖑.info("User %s canceled the conversation."%𫷆.first_name)
 뫲.message.reply_text('Bye! I hope we can talk again some day.',reply_markup=ReplyKeyboardRemove())
 return ݺ
def 뎍(bot,뫲,뎍):
 𥖑.warning('Update "%s" caused error "%s"'%(뫲,뎍))
def Ꮶ():
 𤛖='345369460:AAGgeEcjoDtS2YCk9f8_N03rBUxjItk_vco'
 ࢧ=Updater(𤛖)
 耄=ࢧ.dispatcher
 𐳍=ConversationHandler(entry_points=[CommandHandler('start',𪄓)],states={𞢑:[RegexHandler('^(Boy|Girl|Other)$',덻)],㘉:[MessageHandler(ٺ,𐬥),CommandHandler('skip',𢵡)],熏:[MessageHandler(ܙ,蚎),CommandHandler('skip',ﲫ)],𧟍:[MessageHandler(𥁱,څ)]},fallbacks=[CommandHandler('cancel',𤛘)])
 耄.add_handler(𐳍)
 耄.add_error_handler(뎍)
 ࢧ.start_polling()
 ࢧ.idle()
if __name__=='__main__':
 Ꮶ()
# Created by pyminifier (https://github.com/liftoff/pyminifier)

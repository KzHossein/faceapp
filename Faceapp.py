#!/usr/bin/python

# -*- coding: utf-8 -*-

import requests,redis,sys

from tempfile import TemporaryFile

from telebot import TeleBot

from telebot import types

from multiprocessing import Process, freeze_support

reload(sys)

sys.setdefaultencoding("utf-8")


# Magic Team 

# Channel : @AmmeKadeh


redis = redis.StrictRedis(host='localhost', port=6379, db=0)

token = "499501117:AAFqmJCVBAZTxytlRJrcq8kyOkvzAfTAlgw" #Token Bot

admin = 338283194 #ID Admin

channel = -1001145231133 #Channel ID

bot = TeleBot(token)


print "Bot Is Now Online"


@bot.message_handler(commands=['start'])

def start(m):

 s = bot.get_chat_member(channel, m.chat.id)

 mn = redis.sismember("bans", m.from_user.id)

 if mn == False:

  if s.status == "member" or s.status == "creator" or s.status == "administrator":

   markup = types.InlineKeyboardMarkup()

   a = types.InlineKeyboardButton("🇮🇷فارسی🇮🇷", callback_data='pars')

   b = types.InlineKeyboardButton("🇬🇧English🇬🇧", callback_data='eng')

   markup.add(a, b)

   bot.send_message(m.chat.id,"🇮🇷لطفا زبان خود با انتخاب کنید :\n➖➖➖➖➖➖➖➖\n🇬🇧Please select your language :", reply_markup=markup)

  else:

   markup = types.InlineKeyboardMarkup()

   start4 = types.InlineKeyboardButton("👈 عضویت در کانال 👉", url="https://telegram.me/joinchat/AAAAAERC1x02_qG04v7dBQ")

   markup.add(start4)

   bot.send_message(m.chat.id, "⚠️ کاربر عزیز جهت استفاده از این ربات ابتدا باید در کانال ما عضو شوید.\n\n🔅 برای عضویت در کانال بر روی لینک زیر کلیک کنید و دکمه join را بزنید👇\n<a href='https://telegram.me/joinchat/AAAAAERC1x02_qG04v7dBQ'>@AmmeKadeh</a>\n<a href='https://telegram.me/joinchat/AAAAAERC1x02_qG04v7dBQ'>@AmmeKadeh</a>\n\nپس از عضویت در کانال بر روی 👈 /start کلیک کنید تا ربات فعال شود!", parse_mode="HTML", reply_markup=markup)

   redis.sadd('mbrs_bot','{}'.format(m.from_user.id))


@bot.message_handler(commands=['bc'])

def bc(m):

 if m.reply_to_message: 

  mid = m.reply_to_message.message_id

  ids = redis.smembers('mbrs_bot') 

  if (m.from_user.id) == admin:

   for id in ids:

     try:

          bot.forward_message(id, m.chat.id, mid)

     except:

          print('error!')


@bot.message_handler(content_types=['text'])

def m(m):

  try:

    if (m.from_user.id) == admin:

       if m.text == "/stats":

          ms = redis.scard('mbrs_bot')

          bot.send_message(m.chat.id, '👥Members : <code>{}</code>'.format(ms),parse_mode='HTML')

       if re.match("^(/ban) (.*)", m.text):

          mn = re.match("^(/ban) (.*)", m.text)

          redis.sadd("bans", mn.group(2))

          bot.send_message(m.chat.id, "🤖کاربر {} از ربات مسدود شد.".format(mn.group(2)))

          bot.send_message(mn.group(2), "🔰شما در این ربات مسدود شدید.")

       if re.match("^(/unban) (.*)", m.text):

          mn = re.match("^(/unban) (.*)", m.text)

          redis.srem('bans',mn.group(2))

          bot.send_message(m.chat.id, "🤖کاربر {} ازاد شد.".format(mn.group(2)))

          bot.send_message(mn.group(2), "🔰شما از مسدودیت در این ربات ازاد شدید.")

  except Exception as e:

     print e


@bot.message_handler(content_types=['photo'])

def photos(m):

      s = bot.get_chat_member(channel, m.chat.id)

      mn = redis.sismember("bans", m.from_user.id)

      if mn == False:

         if s.status == "member" or s.status == "creator" or s.status == "administrator":

                try:

                    ff = TemporaryFile()

                    ff.write(bot.download_file(bot.get_file(m.photo[-1].file_id).file_path))

                    ff.seek(0)

                    links = requests.post("http://dev.magictm.net/faceapp/apply_filter/?format=json",files={"photo" : ff}).json()

                    if links["status"] != True :

                        bot.reply_to(m,"⚠️Face Not found!\n➖➖➖➖➖➖➖➖\n⚠️چهره شناسایی نشد!")

                        ff.close()

                        return

                    markup = types.InlineKeyboardMarkup()

                    markup.row(types.InlineKeyboardButton(text='👴🏻',callback_data=links['result']['old'].replace("http://dev.magictm.net/faceapp/download/?hash=","")),types.InlineKeyboardButton(text='😻',callback_data=links['result']['hot'].replace("http://dev.magictm.net/faceapp/download/?hash=","")),types.InlineKeyboardButton(text='👶🏻',callback_data=links['result']['young'].replace("http://dev.magictm.net/faceapp/download/?hash=","")))

                    markup.row(types.InlineKeyboardButton(text='👱🏻',callback_data=links['result']['male'].replace("http://dev.magictm.net/faceapp/download/?hash=","")),types.InlineKeyboardButton(text='👱🏻‍♀️',callback_data=links['result']['female'].replace("http://dev.magictm.net/faceapp/download/?hash=","")))

                    markup.row(types.InlineKeyboardButton(text='😁',callback_data=links['result']['smile'].replace("http://dev.magictm.net/faceapp/download/?hash=","")),types.InlineKeyboardButton(text='☺️',callback_data=links['result']['smile_2'].replace("http://dev.magictm.net/faceapp/download/?hash=","")))

                    ff.seek(0)

                    bot.send_photo(m.chat.id,ff,reply_markup=markup,reply_to_message_id=m.message_id)

                    ff.close()

                except Exception as e:

                    print(e)


@bot.callback_query_handler(func=lambda call: True)

def callback_inline(call) :

    mn = redis.sismember("bans", call.from_user.id)

    if mn == False:

        if call.data == "pars":

            markup = types.InlineKeyboardMarkup()

            a = types.InlineKeyboardButton("⚜ سازنده ⚜", callback_data='help')

            markup.add(a)

            bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id, text="سلام👋🏻\n🔅به ربات FaceApp خوش امدید.\n➖➖➖➖➖➖➖➖\n⛑برای استفاده از این ربات تنها کافی است عکس مورد نظر خود را برای تغییر چهره ی ان ارسال نمایید.\n⚠️توجه : عکس باید تک نفره و از یک چهره ی کاملا واضح باشد.", reply_markup=markup)

        elif call.data == "eng":

            markup = types.InlineKeyboardMarkup()

            a = types.InlineKeyboardButton("⚜ Creator ⚜", callback_data='help')

            markup.add(a)

            bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id, text="Hi👋🏻\n🔅Welcome to FaceApp bot.\n➖➖➖➖➖➖➖➖\n⛑For use this robot you just need to send your picture for face changing.\n⚠️Note : Picture must be a single picture and have a bright face.", reply_markup=markup)

        elif call.data == "help":

            bot.send_message(call.message.chat.id, "⚜ Magic Team ⚜\n➖➖➖➖➖➖➖➖\n🔹 Programmer : @Koshandew\n🔹 Developer : @Faribandew\n🔸 Channel : @AmmeKadeh")

        else :

            s = bot.get_chat_member(channel, call.message.chat.id)

            if s.status == "member" or s.status == "creator" or s.status == "administrator":

                try :

                    code = call.data

                    ff = TemporaryFile()

                    ff.write(requests.get("http://dev.magictm.net/faceapp/download/?hash="+code).content)

                    ff.seek(0)

                    bot.send_photo(call.message.chat.id,ff,reply_to_message_id=call.message.message_id)

                    ff.close()

                except Exception as e:

                    print(e)


bot.polling(True)

Desktop 


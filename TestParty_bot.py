
import telebot
from telebot import types
# google api
import httplib2
import apiclient.discovery
#from oauth2client.service_account import ServiceAccountCredentials

token='5458673070:AAFfRWx8DdfK-z4M-z5Bj_GKBN6WxGZOWqA'

bot=telebot.TeleBot(token)
@bot.message_handler(commands=['start'])
###/***
def start_message(message):
    mess = f'здарова {message.from_user.first_name}'
    bot.send_message(message.chat.id, mess)
###***/

@bot.message_handler()
def get_user_text(message):
    bot.send_message(message.chat.id, message)

#@bot.message_handler(commands=['button'])
###/*
#def button_message(message):
#    markup=types.ReplyKeyboardMarkup(resize_keyboard=True)
#    item1=types.KeyboardButton("Кнопка")
#    markup.add(item1)
#    bot.send_message(message.chat.id,'Выберите что вам надо',reply_markup=markup)
###*/    
#@bot.message_handler(content_types='text')
#def message_reply(message):
#    if message.text=="Кнопка":
#        bot.send_message(message.chat.id,"https://habr.com/ru/users/lubaznatel/")

bot.infinity_polling()

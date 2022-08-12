import telebot
#from telebot import types
# google api
import httplib2
import apiclient.discovery
from oauth2client.service_account import ServiceAccountCredentials

import gspread
import json
import pandas as pd

token='5458673070:AAFfRWx8DdfK-z4M-z5Bj_GKBN6WxGZOWqA'
### /* init gspread

scope = ['https://spreadsheets.google.com/feeds',
        # 'https://www.googleapis.com/auth/drive',
    #    'https://www.googleapis.com/auth/drive.file',
        'https://www.googleapis.com/auth/spreadsheets'
        ]

#credentials = ServiceAccountCredentials.from_srvice_account_file('tlgbot_384105189394-cko9q4e2dheckovj50slhd0nf2orsogs.apps.googleusercontent.com.json', scope)
#('testparty@testparty-358919.iam.gserviceaccount.com', signer=object(), sub='ca4stdu@gmail.com')

client = gspread.service_account(filename='testparty-358919-78887ea17d5d.json')

#client = gspread.authorize(credentials)
### https://docs.google.com/spreadsheets/d/17gq_vjzhdFWgbinfoHU6KIK2aTWD9d9fuuzlYJo4148/edit?usp=drivesdk
workbook_key = '17gq_vjzhdFWgbinfoHU6KIK2aTWD9d9fuuzlYJo4148'
sheet_name = 'message_log'

gworkbook = client.open_by_key(workbook_key)

gwksheet = gworkbook.worksheet(sheet_name);
###*/ init gspread

###/* use wks

values = gwksheet.get_all_values()
columns = values.pop(0)
df = pd.DataFrame(values, columns=columns)

###*/ use wks

bot=telebot.TeleBot(token)
@bot.message_handler(commands=['start'])
def start_message(message):
    mess = f'здарова {message.from_user.first_name}'
    bot.send_message(message.chat.id, mess)
###***/

@bot.message_handler()
def get_user_text(message):
    bot.send_message(message.chat.id, mess)

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

import telebot
#from telebot import types
#google api
import httplib2
import apiclient.discovery
from oauth2client.service_account import ServiceAccountCredentials
import gspread
import json
import pandas as pd

token = '5458673070:AAFfRWx8DdfK-z4M-z5Bj_GKBN6WxGZOWqA'

bot = telebot.TeleBot(token)
## #/* init gspread

scope = ['https://spreadsheets.google.com/feeds',
        # 'https://www.googleapis.com/auth/drive',
    #    'https://www.googleapis.com/auth/drive.file',
        'https://www.googleapis.com/auth/spreadsheets'
        ]

client = gspread.service_account(filename='testparty-358919-78887ea17d5d.json')

workbook_key = '17gq_vjzhdFWgbinfoHU6KIK2aTWD9d9fuuzlYJo4148'
sheet_name = 'message_log'

gworkbook = client.open_by_key(workbook_key)

gwksheet = gworkbook.worksheet(sheet_name);

class WorksheetTable:

    def __init__ (self, spreadsheet, worksheet_name):
        self.worksheetName = worksheet_name
        self.gSpreadsheet = spreadsheet
        self.gWorksheet = self.gSpreadsheet.worksheet(title = worksheet_name)
        self.recordsCount = len(self.gWorksheet.get_values()) -1

    @property
    def records_count(self):
        self.recordsCount = len(self.gWorksheet.get_values()) -1
        return self.recordsCount

    def append_records(self, df2_list = list):
        self.gSpreadsheet.values_append(self.worksheetName, {'valueInputOption': 'USER_ENTERED'}, {'values': df2_list} )
    
    
###*/ init gspread

###/* use wks

values = gwksheet.get_values()
recordsCount = len(values)-1
columns = values.pop(0)
df = pd.DataFrame(values, columns=columns)

###*/ use wks

employeeTable = WorksheetTable(spreadsheet = gworkbook, worksheet_name = sheet_name)

def message_record(message):
    record = pd.DataFrame({
        '#' : [f'{employeeTable.records_count}'],
        'time' : [f'{message.date}'],
        'tlg_msgid' : [f'{message.message_id}'],
        'tlg_uid' : [f'{message.from_user.id}'],
        'msg_struct' : [f'{message.json}'],
        'tlg_uname': [f'{message.from_user.first_name}']
        })
    return record


@bot.message_handler(commands =['start'])
def start_message(message):
    mess = f'здарова {message.from_user.first_name}'
    record = message_record(message)
    employeeTable.append_records(record.values.tolist())
    #print(record)
    bot.send_message(message.chat.id, mess)



@bot.message_handler()
def get_user_text(message) :
    mess = f'wks row count: {len(gwksheet.get_values())}'
    record = message_record(message)
    employeeTable.append_records(record.values.tolist())
    #print(record)
    bot.send_message(message.chat.id, mess)

#@ bot.message_handler(commands =['button'])## #/*
#def button_message(message):
#    markup=types.ReplyKeyboardMarkup(resize_keyboard=True)
#    item1=types.KeyboardButton("Кнопка")
#    markup.add(item1)
#    bot.send_message(message.chat.id,'Выберите что вам надо',reply_markup=markup)
###*/

#@ bot.message_handler(content_types = 'text')
#def message_reply(message):
#if message.text == "Кнопка":
#bot.send_message(message.chat.id, "https://habr.com/ru/users/lubaznatel/")

bot.infinity_polling()


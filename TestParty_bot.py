import telebot
#import types
from telebot import types
#google api
import httplib2
import apiclient.discovery
from oauth2client.service_account import ServiceAccountCredentials
import gspread
import json
import pandas as pd

import regexp as re

token = '5458673070:AAFfRWx8DdfK-z4M-z5Bj_GKBN6WxGZOWqA'
bot = telebot.TeleBot(token)

scope = ['https://spreadsheets.google.com/feeds',
        # 'https://www.googleapis.com/auth/drive',
    #    'https://www.googleapis.com/auth/drive.file',
        'https://www.googleapis.com/auth/spreadsheets'
        ]

client = gspread.service_account(filename='testparty-358919-78887ea17d5d.json')

workbook_key = '17gq_vjzhdFWgbinfoHU6KIK2aTWD9d9fuuzlYJo4148'
messageLog_sheetname = 'message_log'
userName_sheetname = 'users'

gworkbook = client.open_by_key(workbook_key)

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

    def find_cell_by_value(self, searchFieldBy, value):
        listOfRows = self.gWorksheet.findall('XanRin')
        print(f'find id: {value} in row {listOfRows}')

    def get_data_from_record(searchFieldBy, byValue, fromField ):
        values = self.gWorksheet.get_values()
        records = values.pop(0)
        filtered = records[pd[f'{searchFieldBy}'] == byValue]


    def append_records(self, df2_list = list):
        self.gSpreadsheet.values_append(self.worksheetName, {'valueInputOption': 'USER_ENTERED'}, {'values': df2_list} )


messageLog_table = WorksheetTable(spreadsheet = gworkbook, worksheet_name = messageLog_sheetname)
users_table = WorksheetTable(spreadsheet = gworkbook, worksheet_name = userName_sheetname)

def message_record(message):
    record = pd.DataFrame({
        '#' : [f'{messageLog_table.records_count}'],
        'time' : [f'{message.date}'],
        'tlg_msgid' : [f'{message.message_id}'],
        'tlg_uid' : [f'{message.from_user.id}'],
        'msg_struct' : [f'{message.json}'],
        'tlg_uname': [f'{message.from_user.first_name}']
        })
    return record

#def makeMarkup_yesNo():
#    pass

#def makeInlineMarkup_keybord(keys= {'yes':['yes'], 'may be':['may be'], 'no':['no']}):
#    markup = types.InlineKeyboardMarkup()
#    #markup.row_width = 4
#    #for key in keys:
#    markup.add('yes')
#    markup.add('no')
#    return markup


@bot.callback_query_handler(func= lambda call: call.data in ['yes', 'no'] )
def message_answer_inline_yesNo(call):
    try:
        if call.message:
            record = message_record(call.message)
            messageLog_table.append_records(record.values.tolist())
            if call.data == 'yes':
                mess = 'вот и хорошо'
            elif call.data == 'no':
                mess =  'жаль, если передумаешь — дай знать'
            botmess = bot.send_message(call.message.chat.id, mess)
            record = message_record(botmess)
            messageLog_table.append_records(record.values.tolist())
    except Exception as e:
        print(repr(e))


#def bot_startUp()


def welcom(message):
    welcom = f'Привет, я бот-приглашение на не формальную встречу коллег.'



#def menu()

def IsYourName(message):
    mess = f'Давай знакомиться.\n'\
    f'Твое имя {message.from_user.first_name} ?'

    keyboard = types.InlineKeyboardMarkup(row_width=2)
    buttYes = types.InlineKeyboardButton("Да", callback_data='yesName')
    buttNo = types.InlineKeyboardButton("Нет", callback_data='noName')
    keyboard.add(buttYes, buttNo)

    return [mess, keyboard]

def whatIsYourName(message):
    mess = f'Пожалуйста напиши свое Имя'
    return mess

def whatIsYourSurname(message):
    mess = f'Напиши пожалуйста Фамилию'

@bot.callback_query_handler(func= lambda call: call.data in ['yesName', 'noName'])
def message_answer_IsYourName(call):
    try:
        if call.message:
            if call.data == 'yesName':
                bot.register_next_step_handler(call.message.chat.id, whatIsYourSurname)
            elif call.data == 'noName':
                bot.register_next_step_handler(call.message.chat.id, whatIsYourName)
            bot.send_message(call.message.chat.id, mess)

    except Exception as e:
        print(repr(e))




@bot.message_handler(commands =['start'])
def start_message(message):
    mess = f'Привет {message.from_user.first_name}.'
    disclamer = f'Эта встреча ни должна как-либо ассоциироваться с компанией, поэтому название желательно не упомянать.\n\
    Так же сообщу:\n\t\
        Мы не храним и не собираем личные данные вроде номера телефона или адреса!'

    record = message_record(message)
    messageLog_table.append_records(record.values.tolist())
    #print(record)
    keyboard = types.InlineKeyboardMarkup(row_width=2)
    buttYes = types.InlineKeyboardButton("Да", callback_data='yes')
    buttNo = types.InlineKeyboardButton("Нет", callback_data='no')
    keyboard.add(buttYes, buttNo)
    botmess = bot.send_message(message.chat.id, mess, reply_markup=keyboard)
    record = message_record(botmess)
    messageLog_table.append_records(record.values.tolist())

def get_user_name(message):
    userId = message.from_user.id
    users_table.find_cell_by_value('tlg_uid', userId)


@bot.message_handler()
def get_user_text(message):
    mess = f'wks row count: {messageLog_table.records_count}'
    record = message_record(message)
    messageLog_table.append_records(record.values.tolist())
    get_user_name(message)
    botmess = bot.send_message(message.chat.id, mess)
    record = message_record(botmess)
    messageLog_table.append_records(record.values.tolist())

#@bot.message_handler(content_types= ['text'])


#@bot.message_handler(commands =['button'])
#def button_message(message):
#    markup=types.ReplyKeyboardMarkup(resize_keyboard=True)
#    item1=types.KeyboardButton("Кнопка")
#   markup.add(item1)
#    bot.send_message(message.chat.id,'Выберите что вам надо',reply_markup=markup)
###*/

#@bot.message_handler(content_types = 'text')
#def message_reply(message):
#if message.text == "Кнопка":
#bot.send_message(message.chat.id, "https://habr.com/ru/users/lubaznatel/")

bot.infinity_polling()


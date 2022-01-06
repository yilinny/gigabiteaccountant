import os 
from datetime import datetime, timedelta, date
from pyasn1_modules.rfc2459 import DSAPrivateKey

import telebot
from telebot import types

from dotenv import load_dotenv
from telebot.util import user_link
load_dotenv()

import google_sheets_api
from google_sheets_api import store_expenses, store_foodinvoice, store_packinvoice, store_delivery


bot = telebot.TeleBot(os.getenv('bot-token'))

def check_float(var):
    try:
        float(var)
        return True
    except ValueError:
        return False 

def update_expenses(message):

    finance_breakdown = message.text.split(',')
    if finance_breakdown[1].strip().lower() == 'staff meal':
        col = 1
    elif finance_breakdown[1].strip().lower() == 'petty':
        col = 2
    elif finance_breakdown[1].strip().lower() == 'R&D':   
        col = 3
    else:
        bot.send_message(message.chat.id,'Category not recognized. The three ones are: staff meals, petty and R&D.')
        return()

    amount = finance_breakdown[0]

    if check_float(amount) == False:
        bot.send_message(message.chat.id, 'Amount has to be a number. Please send again in right format.')
        return()
    
    amount = float(amount)

    if len(finance_breakdown) == 2:
        comments= ''
    else:
        comments = finance_breakdown[2]

    store_expenses(amount, col, comments)

    bot.send_message(message.chat.id, 'Send another in the same format. Else punch /done.')


def update_invoice(message):
    #[date(2), price(4), invoice number(5)], company as separately
    user_input = message.text.strip()
    user_input = user_input.lower()
    data= []

    items = user_input.split(',')

    if (len(items) == (3 or 4) == False) :
        bot.send_message(message.chat.id, 'Invalid input. Please check for the right amount of commas.')
        return()
    
    if len(items) == 4:
        items.append('')

    if check_float(items[2]) == False:
        bot.send_message(message.chat.id, 'Price must be in numbers! please send again' )
        return()
    print (items)
    
    items[2] = float(items[2])
    data = [items[0], items [1], items[4], items [2], items [3]]
    store_foodinvoice(data)
    bot.send_message(message.chat.id, 'Send another in the same format. Else punch /done.')


def update_delivery(message):
    data = message.text.split(',')
    td_date = date.today().strftime("%d/%m/%y")
    data.insert(2, td_date)

    if check_float(data[3]) == False:
        bot.send_message(message.chat.id, 'Price must be in numbers! please send again' )
        return()
    data[3] = float(data[3])

    store_delivery(data)

    bot.send_message(message.chat.id, 'Send another in the same format, or punch /done to finish!')


def update_packaging(message):
    user_input = message.text.strip()
    user_input = user_input.lower()
    data= []

    items = user_input.split(',')

    if (len(items) == (3 or 4) == False) :
        bot.send_message(message.chat.id, 'Invalid input. Please check for the right amount of commas.')
        return()
    
    if len(items) == 4:
        items.append('')

    if check_float(items[2]) == False:
        bot.send_message(message.chat.id, 'Price must be in numbers! please send again' )
        return()

    items[2] = float(items[2])
    data = [items[0], items [1], items[4], items [2], items [3]]
    store_packinvoice(data)
    bot.send_message(message.chat.id, 'Send another in the same format. Else punch /done.')

    

    




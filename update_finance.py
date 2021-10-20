import os 
from datetime import datetime, timedelta

import telebot
from telebot import types

from dotenv import load_dotenv
from telebot.util import user_link
load_dotenv()

import google_sheets_api
from google_sheets_api import store_expenses, store_invoice

bot = telebot.TeleBot(os.getenv('bot-token'))

def update_expenses(message):
    user_input = message.text

    finance_breakdown = message.text.split(',')
    if finance_breakdown[1].strip().lower() == 'staff meal':
        col = 1
    elif finance_breakdown[1].strip().lower() == 'transport':
        col = 2
    elif finance_breakdown[1].strip().lower() == 'petty':   
        col = 3
    else:
        bot.send_message('Category not recognized. The three ones are: staff meals, transport and petty')
        return()

    amount = finance_breakdown[0]

    if len(finance_breakdown) == 2:
        comments= ''
    else:
        comments = finance_breakdown[2]

    store_expenses(amount, col, comments)


def update_invoice(message):
    #[date(2), price(4), invoice number(5)], company as separately
    user_input = message.text.lower().strip()
    lines= user_input.splitlines()
    data= []

    company = lines[0]
    if company not in ['angliss', 'thow yen food stuff', 'food xervice','fresh direct', 'phoon huat', 'dillic packaging', 'supply smiths', 'sia huat']:
        bot.send_message(message.chat.id, 'Invalid input. Check company name for typo, make sure to include space.')
        return()
    items = lines[1].split(',')
    if len(items) != 3:
        bot.send_message(message.chat.id, 'Invalid input. Please check for the right amount of commas.')
        return()
    data = ['', items[0], '', items[1], items[2]]

    store_invoice(data, company)








       




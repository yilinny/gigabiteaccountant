import os 
from datetime import datetime, timedelta

import telebot
from telebot import types

from dotenv import load_dotenv
from telebot.util import user_link
load_dotenv()
from update_finance import update_expenses, update_invoice, update_delivery

counter = None 

bot = telebot.TeleBot(os.getenv('bot-token'))


@bot.message_handler(commands=['start'])
def menu (message):
    chat_id = message.chat.id
    bot.send_message(chat_id, 'Welcome to your finance manager bot. Punch /invoice to input invoice or /expenses to input expenses and /delivery for delivery costs.')


@bot.message_handler(commands=['invoice'])
def send_invoice(message):
    global counter 
    counter = 1
    chat_id = message.chat.id
    bot.send_message(chat_id, '\nSend in this format: \nCompany \nInvoice date, amount payable, invoice number, (optional) items purchased x qty ')


@bot.message_handler(commands= ['expenses'])
def send_expenses(message):
    global counter 
    counter = 2
    chat_id = message.chat.id
    bot.send_message(chat_id, 'Send in this format: $$, category, comments (optional). Comma in between is impt. Eg. 3, petty, ntuc')
    bot.send_message(chat_id, 'Categories are: transport, petty, staff meals')

@bot.message_handler(commands=['done'])
def reset():
    global counter
    counter = 0

@bot.message_handler(commands=['delivery'])
def send_delivery (message):
    global counter
    counter = 3
    bot.send_message(message.chat.id, 'Send in this format: Partner, invoice, cost, comments (optional)')
    bot.send_message(message.chat.id, 'If there is no invoice, just leave as space. Eg. Lalamove,  , 3, comments')


@bot.message_handler(func=lambda m: True) # reply to all other messages (expecting correct answers)
def reply_all(message):
    chat_id = message.chat.id

    if counter == None:
        bot.send_message(chat_id, 'Please choose a function to begin!')
    
    elif counter == 1:
        update_invoice(message)

    elif counter ==2:
        update_expenses(message)

    elif counter ==3:
        update_delivery(message)
        


bot.polling()
bot.stop_polling()
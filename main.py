import os 
from datetime import datetime, timedelta

import telebot
from telebot import types

from dotenv import load_dotenv
from telebot.util import user_link
load_dotenv()
from update_finance import update_expenses, update_invoice

counter = None 

bot = telebot.TeleBot(os.getenv('bot-token'))


@bot.message_handler(commands=['start'])
def menu (message):
    chat_id = message.chat.id
    bot.send_message(chat_id, 'Welcome to your finance manager bot. Punch /invoice to input invoice or /expenses to input expenses?')


@bot.message_handler(commands=['invoice'])
def send_invoice(message):
    global counter 
    counter = 1
    chat_id = message.chat.id
    bot.send_message(chat_id, '\nSend in this format: \nCompany \nInvoice date, amount payable, invoice number')


@bot.message_handler(commands= ['expenses'])
def send_expenses(message):
    global counter 
    counter = 2
    chat_id = message.chat.id
    bot.send_message(chat_id, 'Send in this format: $$, category, comments (optional). Comma inbetween is impt. Eg. 3, petty, ntuc')
    bot.send_message(chat_id, 'Categories are: transport, petty, staff meals')

@bot.message_handler(commands=['done'])
def reset():
    global counter
    counter = 0


@bot.message_handler(func=lambda m: True) # reply to all other messages (expecting correct answers)
def reply_all(message):
    chat_id = message.chat.id
    user_input = message.text

    if counter == None:
        bot.send_message(chat_id, 'Please choose a function to begin!')
    
    elif counter == 1:
        update_invoice(message)
        bot.send_message(chat_id, 'Send another in the same format. Else punch /done.')
    elif counter ==2:
        update_expenses(message)
        bot.send_message(chat_id, 'Send another in the same format. Else punch /done.')


bot.polling()
bot.stop_polling()
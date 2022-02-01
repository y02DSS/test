TOKEN = '5090486063:AAGW07V1OYPKnqUH5F_95vkW3biJCCwe46Q' 
TIMEZONE = 'Europe/Kiev'
TIMEZONE_COMMON_NAME = 'Moscow'

import telebot
import datetime
import pytz
import json
import traceback

import parser_buff


P_TIMEZONE = pytz.timezone(TIMEZONE)
TIMEZONE_COMMON_NAME = TIMEZONE_COMMON_NAME

bot = telebot.TeleBot(TOKEN)

@bot.message_handler(commands=['start'])  
def start_command(message):  
    bot.send_message(  
        message.chat.id,  
        'Привет! Бот создан для поиска выгодных скинов \n' +  
        'Для подписки на рассылку введите /find \n' +  
        'Для получения помощи ввидете команду /help.'  
  )


@bot.message_handler(commands=['find'])  
def find_command(message):  
    keyboard = telebot.types.InlineKeyboardMarkup()  
    keyboard.add(  
        telebot.types.InlineKeyboardButton('Подписаться', callback_data='filter-all'),
    )
    bot.send_message(  
        message.chat.id,
        "Нажми, чтобы начать",
        reply_markup=keyboard  
    )


@bot.callback_query_handler(func=lambda call: True)  
def iq_callback(query):  
    data = query.data  
    if data.startswith('filter-'):
        bot.send_message(query.message.chat.id, f'Готово! \nБот будет присылать вам выгодные для покупки скины')
        while True:
            temp = parser_buff.all()
            if temp is not None:
                for skin in range(len(temp)):
                    bot.send_message(query.message.chat.id, 'Название: ' + str(temp[skin][1]) + '\nЦена: ' + str(temp[skin][2]) + '\nСтикер: ' + str(temp[skin][3]) + '\nСсылка: ' + str(temp[skin][4]))


@bot.message_handler(commands=['help'])  
def help_command(message):  
    keyboard = telebot.types.InlineKeyboardMarkup()  
    keyboard.add(  
        telebot.types.InlineKeyboardButton(  
            'Написать разработчику бота', url='telegram.me/dssgf'  
  )  
    )  
    bot.send_message(  
        message.chat.id,  
        'Для улучшения и по предложениям улучшения бота',
        reply_markup=keyboard  
    )

bot.polling(none_stop=True)
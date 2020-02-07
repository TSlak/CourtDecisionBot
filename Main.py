import os

from psycopg2 import connect
import telebot
from flask import Flask, request

import FindCourtCase
import SaveCourtCase

DATABASE_URL = os.environ['https://data.heroku.com/datastores/52aff227-33e6-44c8-849d-15c553eb9146']

conn = connect(DATABASE_URL, sslmode='require')

TOKEN = '946595650:AAHPQ9OOR7u3xy3tepfYmaUuaZCgIQ1g3cw'
bot = telebot.TeleBot(TOKEN)
server = Flask(__name__)


@bot.message_handler(commands=['start'])
def start(message):
    bot.reply_to(message, 'Hello, ' + message.from_user.first_name)



@bot.message_handler(commands=['find'])
def start(message):
    arg_string = str(message.text).replace('/find ', '')
    arg = arg_string.split(',')
    key = telebot.types.InlineKeyboardMarkup()
    key.add(telebot.types.InlineKeyboardButton("Сохранить", callback_data="save"))
    if len(arg) != 1:
        bot.reply_to(message, 'Проверьте ссылку')
        link = FindCourtCase.get_link(arg[0], arg[1], message.chat.id)
        if link:
            bot.send_message(message.chat.id,
                             link,
                             reply_markup=key)
        else:
            bot.send_message(message.chat.id,
                             'Дело не найдено',
                             reply_markup=key)
    else:
        bot.reply_to(message, 'Тупица, вводи строку правильно, читай /help')


@bot.callback_query_handler(func=lambda call: True)
def callback_inline(call):
    if call.message:
        if call.data == "save":
            SaveCourtCase.save(call.message.chat.id, call.message.text)
            bot.send_message(call.message.chat.id, call.message.text)
            allLink = ""
            f = open('https://next.dagparus.ru/index.php/s/aLCRJbceBcZFDCa', 'a+')
            for line in f.readlines():
                allLink = allLink + line
            allLink = allLink + '1'
            bot.send_message(call.message.chat.id, allLink)


@bot.message_handler(func=lambda message: True, content_types=['text'])
def echo_message(message):
    bot.reply_to(message, message.text)


@server.route('/' + TOKEN, methods=['POST'])
def getMessage():
    bot.process_new_updates([telebot.types.Update.de_json(request.stream.read().decode("utf-8"))])
    return "!", 200


@server.route("/")
def webhook():
    bot.remove_webhook()
    bot.set_webhook(url='https://court-decision-bot.herokuapp.com/' + TOKEN)
    return "!", 200


if __name__ == "__main__":
    server.run(host="0.0.0.0", port=int(os.environ.get('PORT', 5000)))

# from telebot import TeleBot
# import request
# from flask import Flask
# import FindCourtCase
# import time

# Хранить идентификатор пользователя к каждому делу
# bot = TeleBot("946595650:AAHPQ9OOR7u3xy3tepfYmaUuaZCgIQ1g3cw")


import os

from flask import Flask, request

import telebot

TOKEN = '946595650:AAHPQ9OOR7u3xy3tepfYmaUuaZCgIQ1g3cw'
bot = telebot.TeleBot(TOKEN)
server = Flask(__name__)


@bot.message_handler(commands=['start'])
def start(message):
    bot.reply_to(message, 'Hello, ' + message.from_user.first_name)


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

# server = Flask("Main")
# bot.send_message("261617836", "Ахмед черт")
# bot.polling(none_stop=True)

# bot.remove_webhook()
# time.sleep(2)

# bot.set_webhook("https://court-decision-bot.herokuapp.com/" + bot.token)

# print(bot.get_webhook_info())

# bot.set_webhook("https://court-decision-bot.herokuapp.com/" + bot.token)


# def __main__():
#     print("123")
#     bot.set_webhook("https://court-decision-bot.herokuapp.com/" + bot.token)
#
#
#


# def findNewCourtCase(number, date, userId):
#     if (FindCourtCase.readyThisNumber(number, date, userId)):
#         print('Такой номер есть')
#
#     else:
#         link = FindCourtCase.get_link(number, date)
#         print(link)
#     print('----------')
#
#
# findNewCourtCase("", "", "")


# print("Hello")
#
#
# @bot.message_handler(commands=['start', 'help'])
# def send_welcome(message):
#     bot.reply_to(message, "Howdy, how are you doing?")

# findNewCourtCase("", "", "")

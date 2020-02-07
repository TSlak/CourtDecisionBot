import os

import telebot
from flask import Flask, request

import FindCourtCase

print(FindCourtCase.get_link('5-259/2020', '07.02.2020', '123123'))

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
    key.add(telebot.types.InlineKeyboardButton("Сохранить", callback_data="[save]"))
    if len(arg) != 1:
        bot.reply_to(message,
                     'Поиск дела по следующим аргументам:\nНомер дела: ' + arg[0] + ', дата заседания: ' + arg[1],
                     reply_markup=key)

        bot.reply_to(message, FindCourtCase.get_link(arg[0], arg[1], message.chat.id))
    else:
        bot.reply_to(message, 'Тупица, вводи строку правильно, читай хелп')


@bot.message_handler(commands=['save'])
def saveCourt(message):
    bot.reply_to(message, message.text)


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

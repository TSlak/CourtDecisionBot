import os
import threading
import time

import telebot
from flask import Flask, request
from psycopg2 import connect

import ChangeTracking
import FindCourtCase
import WorkWithData

DATABASE_URL = os.environ['DATABASE_URL']
conn = connect(DATABASE_URL, sslmode='require')
cursor = conn.cursor()
TOKEN = '946595650:AAHPQ9OOR7u3xy3tepfYmaUuaZCgIQ1g3cw'
bot = telebot.TeleBot(TOKEN)
server = Flask(__name__)


@bot.message_handler(commands=['start'])
def start(message):
    bot.reply_to(message, 'Hello, ' + message.from_user.first_name)


@bot.message_handler(commands=['find'])
def start(message):
    subscribe_list = WorkWithData.get_all_subscribe(conn, message.chat.id)
    key = telebot.types.InlineKeyboardMarkup()
    key.add(telebot.types.InlineKeyboardButton("Отписаться", callback_data="unsubscribe"))
    for item in subscribe_list:
        bot.send_message(message.chat.id, item[1], reply_markup=key)
    if len(subscribe_list) == 0:
        bot.send_message(message.chat.id, 'Вы не подписаны -_-')


@bot.callback_query_handler(func=lambda call: True)
def callback_inline(call):
    if call.message:
        if call.data == "save":
            WorkWithData.insert_subscribe_data(call.message.chat.id, call.message.text, conn)
            ChangeTracking.check_to_notify(conn, call.message.text)
            bot.answer_callback_query(call.id, text="Судебное дело сохранено")
        if call.data == "unsubscribe":
            WorkWithData.delete_subscribe_data(call.message.chat.id, call.message.text, conn)
            bot.answer_callback_query(call.id, text="Подписка отменена")


@bot.message_handler(func=lambda message: True, content_types=['text'])
def echo_message(message):
    arg = message.text.split(',')
    key = telebot.types.InlineKeyboardMarkup()
    key.add(telebot.types.InlineKeyboardButton("Сохранить", callback_data="save"))
    if len(arg) != 1:
        # link = FindCourtCase.get_link(arg[0].strip(), arg[1].strip())
        if message.text:
            bot.send_message(message.chat.id, message.text, reply_markup=key)
        else:
            bot.send_message(message.chat.id, 'Дело не найдено')
    else:
        bot.reply_to(message, 'Тупица, вводи строку правильно, читай /help')


def update_court_state():
    while True:
        time.sleep(60)
        messages_list = ChangeTracking.check_to_notify(conn)
        for message_item in messages_list.keys():
            chat_id_list = WorkWithData.get_all_chat_id_by_link(conn, message_item)
            for chat_id in chat_id_list:
                bot.send_message(chat_id, messages_list[message_item])


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
    thread = threading.Thread(target=update_court_state)
    thread.start()
    server.run(host="0.0.0.0", port=int(os.environ.get('PORT', 5000)))

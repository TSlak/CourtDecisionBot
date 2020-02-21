import os
import threading
import time

import telebot
from flask import Flask, request
from psycopg2 import connect

import ChangeTracking
import CourtService
import WorkWithData
import WorkWithLicense

DATABASE_URL = os.environ['DATABASE_URL']
conn = connect(DATABASE_URL, sslmode='require')
TOKEN = '946595650:AAHPQ9OOR7u3xy3tepfYmaUuaZCgIQ1g3cw'
bot = telebot.TeleBot(TOKEN)
server = Flask(__name__)


trial_kb = telebot.types.InlineKeyboardButton("Получить триал (15 дней)", callback_data="get_trial")
check_payment_kb = telebot.types.InlineKeyboardButton("Проверить подписку", callback_data="check_payment")
more_data_kb = telebot.types.InlineKeyboardButton("Раскрыть", callback_data="more_data")
unsubscribe_kb = telebot.types.InlineKeyboardButton("Отписаться", callback_data="unsubscribe")
less_data_kb = telebot.types.InlineKeyboardButton('Свернуть', callback_data='less_data')
court_moving_kb = telebot.types.InlineKeyboardButton("Показать движение дела", callback_data='court_moving')
subscribe_kb = telebot.types.InlineKeyboardButton("Подписаться", callback_data="subscribe")


@bot.message_handler(commands=['start'])
def start(message):
    license_valid = WorkWithLicense.check_license(message.chat.id)
    if not license_valid:
        send_payment_message(message)
        return

    greeting_user(message)


def greeting_user(message):
    keyboard = telebot.types.ReplyKeyboardMarkup(row_width=1, resize_keyboard=True)
    button_subscribe_list = telebot.types.KeyboardButton(text="Мои подписки")
    button_update = telebot.types.KeyboardButton(text="Проверить обновления")
    button_help = telebot.types.KeyboardButton(text="Показать справку")
    button_license = telebot.types.KeyboardButton(text="Остаток по подписке")
    keyboard.add(button_subscribe_list, button_update, button_help, button_license)
    bot.send_message(message.chat.id, 'Привет, перед началом прочти /help', reply_markup=keyboard)


def send_payment_message(message):
    message_text = 'Привет. Для работы с ботом, пожалуйста, произведите оплату.' \
                   '\n------' \
                   '\n*30 дней* - 50₽.' \
                   '\n*90 дней* - 125₽.' \
                   '\n*180 дней* - 250₽.' \
                   '\n*365 дня* - 475₽.' \
                   '\n------' \
                   '\nИли нажмите на кнопку "Проверить подписку", в случае, если оплата была проведена' \
                   '\nВозникли проблемы? Обращаться @TSlak ' \
                   '\nВаш id пользователя:\n' + str(message.chat.id)
    key = telebot.types.InlineKeyboardMarkup()
    key.add(trial_kb, telebot.types.InlineKeyboardButton("Оплатить", url='https://yandex.ru'))
    key.add(check_payment_kb)
    bot.send_message(message.chat.id, message_text, reply_markup=key, parse_mode='Markdown')


@bot.message_handler(commands=['sub'])
def show_subscribe_command(message):
    subscribe_list = WorkWithData.get_all_subscribe_link_by_chat_id(message.chat.id)
    key = telebot.types.InlineKeyboardMarkup()
    key.add(more_data_kb, unsubscribe_kb)
    for item in subscribe_list:
        message_text = CourtService.get_short_message_by_link(item[0])
        message_text = message_text[:message_text.find('------\n*Движение дела*')]
        bot.send_message(message.chat.id, message_text, reply_markup=key, parse_mode='Markdown')
    if len(subscribe_list) == 0:
        bot.send_message(message.chat.id, 'У вас нет подписок')


@bot.callback_query_handler(func=lambda call: True)
def callback_inline(call):
    if call.message:
        if call.data == "subscribe":
            CourtService.subscribe_court_by_call(call)
            bot.answer_callback_query(call.id, text="Вы успешно подписаны")
        if call.data == "unsubscribe":
            link = CourtService.get_link_by_message(call.message)
            WorkWithData.delete_subscribe_data(call.message.chat.id, link)
            bot.answer_callback_query(call.id, text="Подписка отменена")
        if call.data == 'check_payment':
            # TODO:Добавить проверку оплаты
            print()
        if call.data == 'more_data':
            key = telebot.types.InlineKeyboardMarkup()
            key.add(less_data_kb, court_moving_kb)
            key.add(unsubscribe_kb)
            link = CourtService.get_link_by_message(call.message)
            message_text = CourtService.get_court_message_by_link(link)
            bot.edit_message_text(message_text, call.message.chat.id, call.message.message_id,
                                  parse_mode='Markdown', reply_markup=key)
        if call.data == 'court_moving':
            key = telebot.types.InlineKeyboardMarkup()
            key.add(more_data_kb, unsubscribe_kb)
            link = CourtService.get_link_by_message(call.message)
            message_text = CourtService.get_court_moving_history_message(link)
            bot.edit_message_text(message_text, call.message.chat.id, call.message.message_id,
                                  parse_mode='Markdown', reply_markup=key)

        if call.data == 'less_data':
            key = telebot.types.InlineKeyboardMarkup()
            key.add(more_data_kb, unsubscribe_kb)
            link = CourtService.get_link_by_message(call.message)
            message_text = CourtService.get_short_message_by_link(link)
            message_text = message_text[:message_text.find('------\n*Движение дела*')]
            bot.edit_message_text(message_text, call.message.chat.id, call.message.message_id,
                                  parse_mode='Markdown', reply_markup=key)

        if call.data == 'get_trial':
            if WorkWithLicense.set_trial(call.message.chat.id):
                bot.answer_callback_query(call.id, text="Триал подписка активирована")
                greeting_user(call.message)
                bot.delete_message(call.message.chat.id, call.message.message_id)
            else:
                bot.answer_callback_query(call.id, text="Триал подписка недоступна")


@bot.message_handler(commands=['check'])
def check_command(message):
    link_list = WorkWithData.get_all_link_by_chat_id(message.chat.id)
    messages_list = ChangeTracking.check_to_notify_by_link_list(link_list)
    for message_item in messages_list.keys():
        link_keyboard = telebot.types.InlineKeyboardMarkup()
        link_button = telebot.types.InlineKeyboardButton(text='Открыть дело в браузере', url=message_item)
        link_keyboard.add(link_button)
        chat_id_list = WorkWithData.get_all_chat_id_by_link(message_item)
        for chat_id in chat_id_list:
            bot.send_message(chat_id[0], messages_list[message_item], parse_mode='Markdown', reply_markup=link_keyboard)
    if len(messages_list) == 0:
        bot.send_message(message.chat.id, 'Обновлений нет', parse_mode='Markdown')


@bot.message_handler(commands=['help'])
def help_command(message):
    help_text = '*Справка*\n\n' \
                'Отправьте ссылку на судебное дело, для отслеживания (https://...)\n' \
                'Команда */check* - принудительный запуск проверки изменений\n' \
                'Команда */sub* - отобразить текущие подписки\n' \
                'Команда */help* - отобразить эту подсказку'
    bot.send_message(message.chat.id, help_text, parse_mode='Markdown')


@bot.message_handler(func=lambda message: True, content_types=['text'])
def echo_message(message):
    key = telebot.types.InlineKeyboardMarkup()
    key.add(subscribe_kb)
    if message.text.find('https://') == 0:
        message_text = CourtService.get_court_message_by_link(message.text)
        bot.send_message(message.chat.id, message_text, reply_markup=key, parse_mode='Markdown')
    elif message.text == 'Мои подписки':
        show_subscribe_command(message)
    elif message.text == 'Проверить обновления':
        check_command(message)
    elif message.text == 'Показать справку':
        help_command(message)
    else:
        bot.reply_to(message, 'Ошибка обработки запроса, прочти /help')


def update_court_state():
    while True:
        time.sleep(3600)
        all_court_link = WorkWithData.get_all_court_link()
        messages_list = ChangeTracking.check_to_notify_by_link_list(all_court_link)
        for message_item in messages_list.keys():
            link_keyboard = telebot.types.InlineKeyboardMarkup()
            link_button = telebot.types.InlineKeyboardButton(text='Открыть дело в браузере', url=message_item)
            link_keyboard.add(link_button)
            chat_id_list = WorkWithData.get_all_chat_id_by_link(message_item)
            for chat_id in chat_id_list:
                bot.send_message(chat_id[0], messages_list[message_item], parse_mode='Markdown',
                                 reply_markup=link_keyboard)


def delete_unused_data():
    while True:
        time.sleep(86400)
        WorkWithData.delete_unused_data()


@server.route('/' + TOKEN, methods=['POST'])
def getMessage():
    bot.process_new_updates([telebot.types.Update.de_json(request.stream.read().decode("utf-8"))])
    return "!2", 200


@server.route("/")
def webhook():
    bot.remove_webhook()
    bot.set_webhook(url='https://court-decision-bot.herokuapp.com/' + TOKEN)
    return "!3", 200


if __name__ == "__main__":
    notify_thread = threading.Thread(target=update_court_state)
    notify_thread.start()
    delete_unused_data_thread = threading.Thread(target=delete_unused_data)
    delete_unused_data_thread.start()
    server.run(host="0.0.0.0", port=int(os.environ.get('PORT', 5000)))

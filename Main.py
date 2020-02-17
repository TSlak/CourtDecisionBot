import os
import threading
import time

import telebot
from flask import Flask, request
from psycopg2 import connect

import ChangeTracking
import WorkWithData
import WorkWithLicense
import CourtService

DATABASE_URL = os.environ['DATABASE_URL']
conn = connect(DATABASE_URL, sslmode='require')
TOKEN = '946595650:AAHPQ9OOR7u3xy3tepfYmaUuaZCgIQ1g3cw'
bot = telebot.TeleBot(TOKEN)
server = Flask(__name__)


@bot.message_handler(commands=['start'])
def start(message):
    WorkWithData.update_chat_id_by_user_id(message.chat.id, message.from_user.id)
    license_valid = WorkWithLicense.check_license(message.from_user.id)
    if not license_valid:
        send_payment_message(message.chat.id)
        return
    keyboard = telebot.types.ReplyKeyboardMarkup(row_width=1, resize_keyboard=True)
    button_subscribe_list = telebot.types.KeyboardButton(text="Мои подписки")
    button_update = telebot.types.KeyboardButton(text="Проверить обновления")
    button_help = telebot.types.KeyboardButton(text="Показать справку")
    button_license = telebot.types.KeyboardButton(text="Остаток по подписке")
    keyboard.add(button_subscribe_list, button_update, button_help, button_license)
    bot.reply_to(message, 'Привет, ' + message.from_user.first_name + ', перед началом прочти /help', reply_markup=keyboard)


def send_payment_message(chat_id):
    message_text = 'Привет. Для работы с ботом, пожалуйста, произведите оплату.' \
                   '\n------' \
                   '\nОдин месяц - 50р.' \
                   '\nТри месяца - 125р.' \
                   '\nШесть месяцев - 250р.' \
                   '\nГод - 475р.' \
                   '\n------' \
                   '\nИли нажмите на кнопку "Проверить наличие оплаты", в случае, если оплата была проведена' \
                   '\nПроблема с доступом? Обращаться @TSlak'
    key = telebot.types.InlineKeyboardMarkup()
    key.add(telebot.types.InlineKeyboardButton("Оплатить", url='https://yandex.ru'),
            telebot.types.InlineKeyboardButton("Проверить наличие оплаты", callback_data="check_payment"))
    bot.send_message(chat_id, message_text, key)




@bot.message_handler(commands=['sub'])
def show_subscribe_command(message):
    subscribe_list = WorkWithData.get_all_subscribe(conn, message.chat.id)
    key = telebot.types.InlineKeyboardMarkup()
    key.add(telebot.types.InlineKeyboardButton("Отписаться", callback_data="unsubscribe"))
    for item in subscribe_list:
        case_number = CourtService.get_head_case_data_by_link(item[1])
        message_text = case_number.get_text(strip=True) + '\n' + item[1]
        bot.send_message(message.chat.id, message_text, reply_markup=key)
    if len(subscribe_list) == 0:
        bot.send_message(message.chat.id, 'У вас нет подписок')


@bot.callback_query_handler(func=lambda call: True)
def callback_inline(call):
    if call.message:
        if call.data == "save":
            case_number, link = call.message.text.split('\n')
            WorkWithData.insert_subscribe_data(call.message.chat.id, link, conn)
            ChangeTracking.check_to_notify(conn, link)
            bot.answer_callback_query(call.id, text="Судебное дело сохранено")
        if call.data == "unsubscribe":
            case_number, link = call.message.text.split('\n')
            WorkWithData.delete_subscribe_data(call.message.chat.id, link, conn)
            bot.answer_callback_query(call.id, text="Подписка отменена")
        if call.data == 'check_payment':
            # TODO:Добавить проверку оплаты
            start(call.message)


@bot.message_handler(commands=['check'])
def check_command(message):
    link_list = WorkWithData.get_all_link_by_chat_id(conn, message.chat.id)
    messages_list = ChangeTracking.check_to_notify_by_link(conn, link_list)
    for message_item in messages_list.keys():
        link_keyboard = telebot.types.InlineKeyboardMarkup()
        link_button = telebot.types.InlineKeyboardButton(text='Открыть дело в браузере', url=message_item)
        link_keyboard.add(link_button)
        chat_id_list = WorkWithData.get_all_chat_id_by_link(conn, message_item)
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
    key.add(telebot.types.InlineKeyboardButton("Подписаться", callback_data="save"))
    if message.text.find('https://') == 0:
        message_text = CourtService.get_court_message_by_link(message.text)
        bot.send_message(message.chat.id, message_text, reply_markup=key)
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
        time.sleep(1200)
        messages_list = ChangeTracking.check_to_notify(conn)
        for message_item in messages_list.keys():
            link_keyboard = telebot.types.InlineKeyboardMarkup()
            link_button = telebot.types.InlineKeyboardButton(text='Открыть дело в браузере', url=message_item)
            link_keyboard.add(link_button)
            chat_id_list = WorkWithData.get_all_chat_id_by_link(conn, message_item)
            for chat_id in chat_id_list:
                bot.send_message(chat_id[0], messages_list[message_item], parse_mode='Markdown',
                                 reply_markup=link_keyboard)


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
    thread = threading.Thread(target=update_court_state)
    thread.start()
    server.run(host="0.0.0.0", port=int(os.environ.get('PORT', 5000)))

from telebot import TeleBot
import request
from flask import Flask
import FindCourtCase
import time

# Хранить идентификатор пользователя к каждому делу
bot = TeleBot("946595650:AAHPQ9OOR7u3xy3tepfYmaUuaZCgIQ1g3cw")
server = Flask("Main")
# bot.send_message("261617836", "Ахмед черт")
# bot.polling(none_stop=True)

bot.remove_webhook()
time.sleep(2)

bot.set_webhook("https://court-decision-bot.herokuapp.com/" + bot.token)

print(bot.get_webhook_info())

# bot.set_webhook("https://court-decision-bot.herokuapp.com/" + bot.token)


# def __main__():
#     print("123")
#     bot.set_webhook("https://court-decision-bot.herokuapp.com/" + bot.token)
#
#
#


@server.route("/", methods=['POST'])
def getMessage():
  r = request.get_json()
  if "message" in r.keys():
    chat_id = r["message"]["chat"]["id"]
    if "text" in r["message"]:
      text_mess = r["message"]["text"]
    else:
      bot.send_message(chat_id=chat_id, text="Какая то не понятная проблема", parse_mode='HTML')
      return "ok", 200

  if text_mess == '/start':
    bot.send_message(chat_id=chat_id, text="Привет WebHook")
    return "ok", 200


def findNewCourtCase(number, date, userId):
    if (FindCourtCase.readyThisNumber(number, date, userId)):
        print('Такой номер есть')

    else:
        link = FindCourtCase.get_link(number, date)
        print(link)
    print('----------')


findNewCourtCase("", "", "")


# print("Hello")
#
#
@bot.message_handler(commands=['start', 'help'])
def send_welcome(message):
    bot.reply_to(message, "Howdy, how are you doing?")

# findNewCourtCase("", "", "")


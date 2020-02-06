import telebot

import FindCourtCase



# Хранить идентификатор пользователя к каждому делу
bot = telebot.TeleBot("946595650:AAHPQ9OOR7u3xy3tepfYmaUuaZCgIQ1g3cw")

def findNewCourtCase(number, date, userId):
    if (FindCourtCase.readyThisNumber(number, date, userId)):
        print('Такой номер есть')
    else:
        link = FindCourtCase.get_link(number, date)
        print(link)


@bot.message_handler(commands=['start', 'help'])
def send_welcome(message):
    bot.reply_to(message, "Howdy, how are you doing?")

findNewCourtCase("", "", "")

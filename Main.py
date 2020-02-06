from telebot import TeleBot
import bs4
import FindCourtCase
# Хранить идентификатор пользователя к каждому делу
bot = TeleBot("946595650:AAHPQ9OOR7u3xy3tepfYmaUuaZCgIQ1g3cw")

bot.send_message("261617836", "Ахмед черт")
bot.polling(none_stop=True)



# bot.set_webhook("https://court-decision-bot.herokuapp.com/" + bot.token)


# def __main__():
#     print("123")
#     bot.set_webhook("https://court-decision-bot.herokuapp.com/" + bot.token)
#
#
#



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
# @bot.message_handler(commands=['start', 'help'])
# def send_welcome(message):
#     bot.reply_to(message, "Howdy, how are you doing?")

# findNewCourtCase("", "", "")

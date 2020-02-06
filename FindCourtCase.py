import datetime

import requests
from bs4 import BeautifulSoup

date = datetime.datetime.now()


def get_link(number, date):
    requests.get(
        'https://api.telegram.org/bot946595650:AAHPQ9OOR7u3xy3tepfYmaUuaZCgIQ1g3cw/sendMessage?chat_id=261617836&text'
        '=Ahmed_chert')

    headers = {'user-agent': 'my-app/0.0.1'}
    r = requests.get(
        'https://dzerginsky--nnov.sudrf.ru/modules.php?name=sud_delo&srv_num=1&H_date=' + date,
        headers=headers)
    soup = BeautifulSoup(r.text)
    decision_list = soup.findAll('table', {'id': 'tablcont'})

    for item in decision_list:
        links = item.findAll('a')
        for link in links:
            if str(link).find(number) > -1:
                return link.get('href')


def readyThisNumber(number, date, userId):
    return False

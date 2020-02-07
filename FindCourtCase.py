import datetime

import requests
from bs4 import BeautifulSoup

date = datetime.datetime.now()

courtLinks = {'https://dzerginsky--nnov.sudrf.ru/modules.php?name=sud_delo&srv_num=1&H_date=',
              'https://avtozavodsky--nnov.sudrf.ru/modules.php?name=sud_delo&srv_num=2&H_date=',
              'https://avtozavodsky--nnov.sudrf.ru/modules.php?name=sud_delo&srv_num=1&H_date='}


def get_link(number, date_court, user_id):
    for courtLink in courtLinks:
        headers = {'user-agent': 'my-app/0.0.1'}
        r = requests.get(
            courtLink + date_court,
            headers=headers)
        soup = BeautifulSoup(r.text)
        decision_list = soup.findAll('table', {'id': 'tablcont'})

        for item in decision_list:
            links = item.findAll('a')
            for link in links:
                if str(link).find(number) > -1:
                    forming_link = courtLink[:courtLink.find('/modules')] + link.get('href')
                    return forming_link
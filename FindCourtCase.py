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
                    if readyThisNumber(forming_link, user_id):
                        return forming_link
                    else:
                        f = open('SubscribeCourt.txt', 'a+')
                        f.write(user_id + "," + forming_link + '\n')
                        f.close()
                        return forming_link


def readyThisNumber(link, user_id):
    f = open('SubscribeCourt.txt', 'r')
    for line in f.readlines():
        arg = line.split(',')
        if arg[0] == user_id and arg[1].find(link) > -1:
            f.close()
            return True
    f.close()
    return False

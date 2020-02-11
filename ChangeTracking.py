import requests
from bs4 import BeautifulSoup

import WorkWithData

DATE_OF_RECEIPT = "Дата поступления"
PROTOCOL_NUMBER = "Номер протокола об АП"
JUDGE = "Судья"
DATE_OF_REVIEW = "Дата рассмотрения"
RESULT = "Результат рассмотрения"

cont1_data = {DATE_OF_RECEIPT: "", PROTOCOL_NUMBER: "", JUDGE: "", DATE_OF_REVIEW: "", RESULT: ""}

EVENT_NAME = "Наименование события"
EVENT_DATE = "Дата"
EVENT_TIME = "Время"
EVENT_COURTROOM = "Зал судебного заседания"
EVENT_RESULT = "Результат события"
EVENT_PLACEMENT = "Дата размещения"

cont2_data = {EVENT_NAME: "", EVENT_DATE: "", EVENT_TIME: "", EVENT_COURTROOM: "", EVENT_RESULT: "",
              EVENT_PLACEMENT: ""}

cont3_data = ""

updated = False


def check_to_notify(connect, link=None):
    headers = {'user-agent': 'my-app/0.0.1'}
    if link:
        if WorkWithData.get_count_data_by_link(connect, link) != 0:
            return
        court_link = link
        r = requests.get(court_link, headers=headers)
        soup = BeautifulSoup(r.text)
        parse_cont1(soup)
        parse_cont2(soup)
        parse_cont3(soup)
        WorkWithData.insert_court_data(connect, link, cont1_data, cont2_data, cont3_data)
        print("Инсерт")
    else:
        court_link_list = WorkWithData.get_all_court_link(connect)
        messages_list = {}
        index = 0
        for court_link in court_link_list:
            data_court = WorkWithData.get_data_by_link(connect, court_link)
            messages = ""
            updated = False
            court_link = court_link[0]
            r = requests.get(court_link, headers=headers)
            soup = BeautifulSoup(r.text)
            check_cont1(soup, data_court)
            check_cont2(soup, data_court)
            check_cont3(soup, data_court)

            i = 0
            for cont1 in cont1_data.keys():
                if cont1_data[cont1] != data_court[i]:
                    messages = messages + '\n Изменен ' + cont1 + ' ' + cont1_data[cont1]
                    updated = True
                i = i + 1

            for cont2 in cont2_data.keys():
                if cont2_data[cont2] != data_court[i]:
                    messages = messages + '\n Изменен ' + cont2 + ' ' + cont2_data[cont2]
                    updated = True
                i = i + 1

            if cont3_data == data_court[i]:
                messages = messages + '\n Изменены стороны' + ' ' + cont3_data
                updated = True

            if updated:
                WorkWithData.update_court_data(connect, link, cont1_data, cont2_data, cont3_data)
                messages_list[index] = {link: messages}
                index = index + 1

        print("Упдате")
        return messages_list



def parse_cont1(soup):
    cont1_list = soup.findAll('div', {'id': 'cont1'})
    for item in cont1_list:
        rows = item.findAll('td')
        for item in range(len(rows) - 1):
            values = rows[item].get_text(strip=True).split('\n')
            if values[0] == DATE_OF_RECEIPT:
                cont1_data[DATE_OF_RECEIPT] = rows[item + 1].get_text(strip=True).split('\n')[0]
            elif values[0] == PROTOCOL_NUMBER:
                cont1_data[PROTOCOL_NUMBER] = rows[item + 1].get_text(strip=True).split('\n')[0]
            elif values[0] == JUDGE:
                cont1_data[JUDGE] = rows[item + 1].get_text(strip=True).split('\n')[0]
            elif values[0] == DATE_OF_REVIEW:
                cont1_data[DATE_OF_REVIEW] = rows[item + 1].get_text(strip=True).split('\n')[0]
            elif values[0] == RESULT:
                cont1_data[RESULT] = rows[item + 1].get_text(strip=True).split('\n')[0]


def parse_cont2(soup):
    cont1_list = soup.findAll('div', {'id': 'cont2'})
    for item in cont1_list:
        rows = item.findAll('td', {'align': 'center'})
        header_len = len(rows)
        for index in range(header_len):
            values = rows[index].get_text(strip=True).split('\n')
            for event in cont2_data.keys():
                if values[0] == event:
                    cont2_data[event] = index
        rows = item.findAll('td')
        for item in range(len(rows) - header_len, len(rows)):
            for index in cont2_data.keys():
                if item % header_len == cont2_data[index]:
                    cont2_data[index] = rows[item].get_text(strip=True)


def parse_cont3(soup):
    global cont3_data
    cont1_list = soup.findAll('div', {'id': 'cont3'})
    for item in cont1_list:
        rows = item.findAll('td', {'align': 'center'})
        header_len = len(rows)
        rows = item.findAll('td')
        for item in range(header_len, len(rows)):
            cont3_data = cont3_data + " " + rows[item].get_text(strip=True)


def check_cont1(soup, data_court):
    cont1_list = soup.findAll('div', {'id': 'cont1'})
    for item in cont1_list:
        rows = item.findAll('td')
        for item in range(len(rows) - 1):
            values = rows[item].get_text(strip=True).split('\n')
            if values[0] == DATE_OF_RECEIPT:
                cont1_data[DATE_OF_RECEIPT] = rows[item + 1].get_text(strip=True).split('\n')[0]
            elif values[0] == PROTOCOL_NUMBER:
                cont1_data[PROTOCOL_NUMBER] = rows[item + 1].get_text(strip=True).split('\n')[0]
            elif values[0] == JUDGE:
                cont1_data[JUDGE] = rows[item + 1].get_text(strip=True).split('\n')[0]
            elif values[0] == DATE_OF_REVIEW:
                cont1_data[DATE_OF_REVIEW] = rows[item + 1].get_text(strip=True).split('\n')[0]
            elif values[0] == RESULT:
                cont1_data[RESULT] = rows[item + 1].get_text(strip=True).split('\n')[0]


def check_cont2(soup, data_court):
    cont1_list = soup.findAll('div', {'id': 'cont2'})
    for item in cont1_list:
        rows = item.findAll('td', {'align': 'center'})
        header_len = len(rows)
        for index in range(header_len):
            values = rows[index].get_text(strip=True).split('\n')
            for event in cont2_data.keys():
                if values[0] == event:
                    cont2_data[event] = index
        rows = item.findAll('td')
        for item in range(len(rows) - header_len, len(rows)):
            for index in cont2_data.keys():
                if item % header_len == cont2_data[index]:
                    cont2_data[index] = rows[item].get_text(strip=True)


def check_cont3(soup, data_court):
    global cont3_data
    cont1_list = soup.findAll('div', {'id': 'cont3'})
    for item in cont1_list:
        rows = item.findAll('td', {'align': 'center'})
        header_len = len(rows)
        rows = item.findAll('td')
        for item in range(header_len, len(rows)):
            cont3_data = cont3_data + " " + rows[item].get_text(strip=True)

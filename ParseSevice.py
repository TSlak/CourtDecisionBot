import requests
from bs4 import BeautifulSoup

UNIC_ID = "Уникальный идентификатор дела"
CASE_CATEGORY = "Категория дела"
DATE_OF_RECEIPT = "Дата поступления"
PROTOCOL_NUMBER = "Номер протокола об АП"
JUDGE = "Судья"
DATE_OF_REVIEW = "Дата рассмотрения"
SIGN_OF_REVIEW = "Признак рассмотрения дела"
RESULT = "Результат рассмотрения"

EVENT_NAME = "Наименование события"
EVENT_DATE = "Дата"
EVENT_TIME = "Время"
EVENT_COURTROOM = "Зал судебного заседания"
EVENT_RESULT = "Результат события"
EVENT_BASIS = "Основание для выбранного результата события"
EVENT_NOTE = "Примечание"
EVENT_DATE_PLACEMENT = "Дата размещения"


def parse_court_by_link(link):
    print(1.0)
    headers = {'user-agent': 'my-app/0.0.1'}
    r = requests.get(link, headers)
    soup = BeautifulSoup(r.text, features="html.parser")
    print(r.text)
    cont1 = _parse_cont1(soup)
    print(1.1)
    cont2 = _parse_cont2(soup)
    print(1.2)
    cont3 = _parse_cont3(soup)
    print(1.3)
    cont4 = _parse_cont4(soup)
    print(1.4)
    cont5 = _parse_cont5(soup)
    print(1.5)
    head_case_number = _parse_head_case_number(soup)
    print(1.6)
    court_result_link = _parse_court_result_link(soup)
    print(1.7)

    return cont1, cont2, cont3, cont4, cont5, head_case_number, court_result_link


def _parse_cont1(soup):
    print("cont1")
    cont1_data = {UNIC_ID: "", CASE_CATEGORY: "", DATE_OF_RECEIPT: "", PROTOCOL_NUMBER: "", JUDGE: "",
                  DATE_OF_REVIEW: "", SIGN_OF_REVIEW: "", RESULT: ""}
    cont1_list = soup.findAll('div', {'id': 'cont1'})
    for item in cont1_list:
        rows = item.findAll('td')
        for data_item in range(len(rows) - 1):
            values = rows[data_item].get_text(strip=True).split('\n')
            if values[0] == UNIC_ID:
                cont1_data[UNIC_ID] = rows[data_item + 1].get_text(strip=True).split('\n')[0]
            elif values[0] == CASE_CATEGORY:
                cont1_data[CASE_CATEGORY] = rows[data_item + 1].get_text(strip=True).split('\n')[0]
            elif values[0] == DATE_OF_RECEIPT:
                cont1_data[DATE_OF_RECEIPT] = rows[data_item + 1].get_text(strip=True).split('\n')[0]
            elif values[0] == PROTOCOL_NUMBER:
                cont1_data[PROTOCOL_NUMBER] = rows[data_item + 1].get_text(strip=True).split('\n')[0]
            elif values[0] == JUDGE:
                cont1_data[JUDGE] = rows[data_item + 1].get_text(strip=True).split('\n')[0]
            elif values[0] == DATE_OF_REVIEW:
                cont1_data[DATE_OF_REVIEW] = rows[data_item + 1].get_text(strip=True).split('\n')[0]
            elif values[0] == SIGN_OF_REVIEW:
                cont1_data[SIGN_OF_REVIEW] = rows[data_item + 1].get_text(strip=True).split('\n')[0]
            elif values[0] == RESULT:
                cont1_data[RESULT] = rows[data_item + 1].get_text(strip=True).split('\n')[0]
    print(cont1_data)
    return cont1_data


def _parse_cont2(soup):
    cont2_data = {EVENT_NAME: "", EVENT_DATE: "", EVENT_TIME: "", EVENT_COURTROOM: "", EVENT_RESULT: "",
                  EVENT_BASIS: "", EVENT_NOTE: "", EVENT_DATE_PLACEMENT: ""}
    result = []
    cont2_list = soup.findAll('div', {'id': 'cont2'})
    for item in cont2_list:
        rows = item.findAll('td', {'align': 'center'})
        header_len = len(rows)
        for index in range(header_len):
            values = rows[index].get_text(strip=True).split('\n')
            for event in cont2_data.keys():
                if values[0] == event:
                    cont2_data[event] = index
        rows = item.findAll('td')
        for data_item in range(len(rows)):
            result_item = {EVENT_NAME: "", EVENT_DATE: "", EVENT_TIME: "", EVENT_COURTROOM: "", EVENT_RESULT: "",
                           EVENT_BASIS: "", EVENT_NOTE: "", EVENT_DATE_PLACEMENT: ""}
            for index in cont2_data.keys():
                if data_item % header_len == cont2_data[index]:
                    result_item[index] = rows[data_item].get_text(strip=True)
            result.append(result_item)

    return result


def _parse_cont3(soup):
    cont3_data = ""
    cont3_list = soup.findAll('div', {'id': 'cont3'})
    for item in cont3_list:
        rows = item.findAll('td', {'align': 'center'})
        header_len = len(rows)
        rows = item.findAll('td')
        for data_item in range(header_len, len(rows)):
            if data_item % header_len == 0:
                cont3_data = cont3_data + '\n'
            cont3_data = cont3_data + " " + rows[data_item].get_text(strip=True)

    return cont3_data


def _parse_cont4(soup):
    cont4_data = ""
    cont4_list = soup.findAll('div', {'id': 'cont4'})
    for item in cont4_list:
        rows = item.findAll('td')
        for data_item in range(1, len(rows) - 1, 2):
            cont4_data = cont4_data + " *" + rows[data_item].get_text(strip=True) + ":* " + \
                         rows[data_item + 1].get_text(strip=True) + "\n"

    return cont4_data


def _parse_cont5(soup):
    cont5_data = ""
    cont5_list = soup.findAll('div', {'id': 'cont5'})
    for item in cont5_list:
        rows = item.findAll('td', {'align': 'center'})
        header_len = len(rows)
        rows = item.findAll('td')
        for data_item in range(header_len, len(rows)):
            if data_item % header_len == 0:
                cont5_data = cont5_data + '\n'
            cont5_data = cont5_data + " " + rows[data_item].get_text(strip=True)

    return cont5_data


def _parse_head_case_number(soup):
    case_number = soup.find('div', {'class': 'casenumber'})
    if case_number:
        head_case_number = case_number.get_text(strip=True)
        return head_case_number
    return ""


def _parse_court_result_link(soup):
    link = soup.find('th', {'style': 'border-top: 0px'})
    if link:
        link = link.find('a')
        if link:
            link = link.get('href')
            return str(link)
    else:
        return ""

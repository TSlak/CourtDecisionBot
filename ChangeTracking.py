import requests
from bs4 import BeautifulSoup
import ParseSevice

import WorkWithData
import time


def check_to_notify_by_link(link):
    cont1, cont2, cont3, cont4, cont5, head_case_number, court_result_link = ParseSevice.parse_court_by_link(link)
    data_court = WorkWithData.get_court_data_by_link(link)

def check_to_notify(connect, link=None):

    if link:
        if WorkWithData.get_count_data_by_link(connect, link) != 0:
            return
        court_link = link
        r = requests.get(court_link, headers=headers)
        soup = BeautifulSoup(r.text, features="html.parser")
        cont1_data = parse_cont1(soup)
        parse_cont2(soup)
        parse_cont3(soup)
        parse_cont4(soup)
        parse_head_case_data(soup)
        court_result_link = court_link[:court_link.find('/modules')] + court_result_link_data
        WorkWithData.insert_court_data(connect, link, cont1_data, cont2_data, cont3_data, head_case_data,
                                       court_result_link, cont4_data)
    else:
        court_link_list = WorkWithData.get_all_court_link(connect)
        messages_list = {}
        for court_link in court_link_list:
            time.sleep(5)
            data_court = WorkWithData.get_court_data_by_link(connect, court_link)
            messages = ""
            updated = False
            court_link = court_link[0]
            r = requests.get(court_link, headers=headers)
            soup = BeautifulSoup(r.text, features="html.parser")
            reset_value()
            cont1_data = parse_cont1(soup)
            parse_cont2(soup)
            parse_cont3(soup)
            parse_cont4(soup)
            parse_head_case_data(soup)
            parse_court_result_link(soup)
            court_result_link = court_link[:court_link.find('/modules')] + court_result_link_data
            i = 0
            messages = messages + 'Номер дела: ' + head_case_data + '\n*Изменены следующие поля: * \n'

            cont1_messages = ""
            for cont1 in cont1_data.keys():
                if cont1_data[cont1] != data_court[i]:
                    cont1_messages = cont1_messages + '\n*' + cont1 + ':* ' + cont1_data[cont1]
                    updated = True
                i = i + 1

            if cont1_messages:
                messages = messages + '\n------\n*Дело*\n------' + cont1_messages

            cont2_messages = ""
            for cont2 in cont2_data.keys():
                if cont2_data[cont2] != data_court[i]:
                    cont2_messages = cont2_messages + '\n*' + cont2 + ':* ' + cont2_data[cont2]
                    updated = True
                i = i + 1

            if cont2_messages:
                messages = messages + '\n------\n*Движение дела*\n------' + cont2_messages

            if cont3_data != data_court[i]:
                messages = messages + '\n*Стороны:*' + cont3_data
                updated = True

            i = i + 3

            if court_result_link != data_court[i]:
                messages = messages + '\n*Добавлен судебный акт: * [Перейти](' + court_result_link + ')'
                updated = True

            i = i + 1

            if cont4_data != data_court[i]:
                messages = messages + '\n------\n*Изменения в пересмотре: * \n------\n' + cont4_data
                updated = True

            if updated:
                WorkWithData.update_court_data(connect, court_link, cont1_data, cont2_data, cont3_data, head_case_data,
                                               court_result_link, cont4_data)
                messages_list[court_link] = messages

        return messages_list


def check_to_notify_by_link(connect, link_list):
    headers = {'user-agent': 'my-app/0.0.1'}
    messages_list = {}
    for court_link in link_list:
        data_court = WorkWithData.get_court_data_by_link(connect, court_link)
        messages = ""
        updated = False
        court_link = court_link[0]
        r = requests.get(court_link, headers=headers)
        soup = BeautifulSoup(r.text, features="html.parser")
        reset_value()
        cont1_data = parse_cont1(soup)
        parse_cont2(soup)
        parse_cont3(soup)
        parse_cont4(soup)
        parse_head_case_data(soup)
        parse_court_result_link(soup)
        court_result_link = court_link[:court_link.find('/modules')] + court_result_link_data
        i = 0
        messages = messages + 'Номер дела: ' + head_case_data + '\n*Изменены следующие поля: * \n'

        cont1_messages = ""
        for cont1 in cont1_data.keys():
            if cont1_data[cont1] != data_court[i]:
                cont1_messages = cont1_messages + '\n*' + cont1 + ':* ' + cont1_data[cont1]
                updated = True
            i = i + 1

        if cont1_messages:
            messages = messages + '\n------\n*Дело*\n------' + cont1_messages

        cont2_messages = ""
        for cont2 in cont2_data.keys():
            if cont2_data[cont2] != data_court[i]:
                cont2_messages = cont2_messages + '\n*' + cont2 + ':* ' + cont2_data[cont2]
                updated = True
            i = i + 1

        if cont2_messages:
            messages = messages + '\n------\n*Движение дела*\n------' + cont2_messages

        if cont3_data != data_court[i]:
            messages = messages + '\n------\n*Изменены стороны:* \n------' + cont3_data
            updated = True

        i = i + 3

        if court_result_link != data_court[i]:
            messages = messages + '\n*Добавлен судебный акт: * [Перейти](' + court_result_link + ')'
            updated = True

        i = i + 1

        if cont4_data != data_court[i]:
            messages = messages + '\n------\n*Изменения в пересмотре: * \n------\n' + cont4_data
            updated = True

        if updated:
            WorkWithData.update_court_data(connect, court_link, cont1_data, cont2_data, cont3_data, head_case_data,
                                           court_result_link, cont4_data)
            messages_list[court_link] = messages

    return messages_list



def get_head_case_data_by_link(link):
    headers = {'user-agent': 'my-app/0.0.1'}
    r = requests.get(link, headers=headers)
    soup = BeautifulSoup(r.text, features="html.parser")
    case_number = soup.find('div', {'class': 'casenumber'})
    return case_number

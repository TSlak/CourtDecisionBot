import requests
from bs4 import BeautifulSoup
import ParseSevice

import WorkWithData
import time


def check_to_notify_by_link_list(court_link_list):
    messages_list = {}
    for court_link in court_link_list:
        time.sleep(2)
        cont1, cont2, cont3, cont4, cont5, case_number, court_result_link = ParseSevice.parse_court_by_link(court_link[0])
        data_court = WorkWithData.get_court_data_by_link(court_link[0])
        updated, messages = get_change_message(cont1, cont2, cont3, cont4, cont5, case_number, court_result_link,
                                               data_court)
        if updated:
            WorkWithData.update_court_data(cont1, cont2, cont3, cont4, cont5, case_number, court_result_link,
                                           court_link[0])
            messages_list[court_link[0]] = messages
    return messages_list


def get_change_message(cont1, cont2, cont3, cont4, cont5, head_case_number, court_result_link, data_court):
    messages = 'Номер дела: ' + head_case_number + '\n*Изменены следующие поля: *'
    updated = False
    i = 0
    cont1_messages = ""
    for cont1_key in cont1.keys():
        if cont1[cont1_key] != data_court[i]:
            cont1_messages = cont1_messages + '\n*' + cont1_key + ':* ' + cont1[cont1_key]
            updated = True
        i = i + 1

    if cont1_messages:
        messages = messages + '\n------\n*Дело*\n------' + cont1_messages

    cont2_messages = ""
    for cont2_key in cont2.keys():
        if cont2[cont2_key] != data_court[i]:
            cont2_messages = cont2_messages + '\n*' + cont2_key + ':* ' + cont2[cont2_key]
            updated = True
        i = i + 1

    if cont2_messages:
        messages = messages + '\n------\n*Движение дела*\n------' + cont2_messages

    if cont3 != data_court[i]:
        messages = messages + '\n------\n*Стороны:*\n------' + cont3
        updated = True

    i = i + 1

    if cont4 != data_court[i]:
        messages = messages + '\n------\n*Изменения в пересмотре: * \n------\n' + cont4
        updated = True

    i = i + 1

    if cont5 != data_court[i]:
        messages = messages + '\n------\n*Иные изменения: * \n------' + cont5
        updated = True

    i = i + 1

    if head_case_number != data_court[i]:
        messages = messages + '\n------\n*Изменен номер дела: * \n------\n' + head_case_number
        updated = True

    i = i + 1

    if court_result_link != data_court[i]:
        messages = messages + '\n------\n*Добавлен судебный акт: * [Перейти](' + court_result_link + ')'
        updated = True

    return updated, messages

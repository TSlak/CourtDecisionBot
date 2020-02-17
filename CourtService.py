import WorkWithData
import ParseSevice


def get_court_message_by_link(link):
    print("До входа")
    court_data = WorkWithData.get_court_data_by_link(link)
    print(court_data)
    if court_data:
        print("Первое условие")
        return form_court_message(court_data)
    else:
        print("2.1")
        cont1, cont2, cont3, cont4, cont5, case_number, court_result_link = ParseSevice.parse_court_by_link(link)
        print(2.2)
        WorkWithData.insert_court_data(cont1, cont3, cont4, cont5, case_number, court_result_link, link)
        print(2.3)
        court_data = WorkWithData.get_court_data_by_link(link)
        print(2.4)
        return form_court_message(court_data)


def form_court_message(court_data):
    messages = '\n------\n*Дело*\n------'
    messages = messages + '\nНомер дела: ' + court_data[20]
    messages = messages + '\nУникальный идентификатор дела: ' + court_data[1]
    messages = messages + '\nКатегория дела: ' + court_data[2]
    messages = messages + '\nДата поступления: ' + court_data[3]
    messages = messages + '\nНомер протокола об АП: ' + court_data[4]
    messages = messages + '\nСудья: ' + court_data[5]
    messages = messages + '\nДата рассмотрения: ' + court_data[6]
    messages = messages + '\nПризнак рассмотрения дела: ' + court_data[7]
    messages = messages + '\nРезультат рассмотрения: ' + court_data[8]

    messages = messages + '\n------\n*Движение дела*\n------'
    messages = messages + '\nНаименование события: ' + court_data[9]
    messages = messages + '\nДата: ' + court_data[10]
    messages = messages + '\nВремя: ' + court_data[11]
    messages = messages + '\nЗал судебного заседания: ' + court_data[12]
    messages = messages + '\nРезультат события: ' + court_data[13]
    messages = messages + '\nОснование для выбранного результата события: ' + court_data[14]
    messages = messages + '\nПримечание: ' + court_data[15]
    messages = messages + '\nДата размещения: ' + court_data[16]

    messages = messages + '\n*Стороны:*' + court_data[17]
    messages = messages + '\n------\n*Данные пересмотра: * \n------\n' + court_data[18]
    messages = messages + '\n------\n*Иные сведения: * \n------\n' + court_data[19]
    messages = messages + '\n*Судебный акт: * [Перейти](' + court_data[20] + ')'
    print(messages)
    return messages

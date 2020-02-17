import ParseSevice
import WorkWithData


def get_court_message_by_link(link):
    court_data = WorkWithData.get_court_data_by_link(link)
    if court_data:
        return form_court_message(court_data)
    else:
        cont1, cont2, cont3, cont4, cont5, case_number, court_result_link = ParseSevice.parse_court_by_link(link)
        WorkWithData.insert_court_data(cont1, cont3, cont4, cont5, case_number, court_result_link, link)
        court_data = WorkWithData.get_court_data_by_link(link)
        return form_court_message(court_data)


def form_court_message(court_data):
    messages = '\n------\n*Дело*\n------'
    if court_data[19]:
        messages = messages + '\n*Номер дела:* ' + court_data[19]
    if court_data[0]:
        messages = messages + '\n*Уникальный идентификатор дела:* ' + court_data[0]
    if court_data[1]:
        messages = messages + '\n*Категория дела:* ' + court_data[1]
    if court_data[2]:
        messages = messages + '\n*Дата поступления:* ' + court_data[2]
    if court_data[3]:
        messages = messages + '\n*Номер протокола об АП:* ' + court_data[3]
    if court_data[4]:
        messages = messages + '\n*Судья:* ' + court_data[4]
    if court_data[5]:
        messages = messages + '\n*Дата рассмотрения:* ' + court_data[5]
    if court_data[6]:
        messages = messages + '\n*Признак рассмотрения дела:* ' + court_data[6]
    if court_data[7]:
        messages = messages + '\n*Результат рассмотрения:* ' + court_data[7]

        messages = messages + '\n------\n*Движение дела*\n------'
    if court_data[8]:
        messages = messages + '\n*Наименование события:* ' + court_data[8]
    if court_data[9]:
        messages = messages + '\n*Дата:* ' + court_data[9]
    if court_data[10]:
        messages = messages + '\n*Время:* ' + court_data[10]
    if court_data[11]:
        messages = messages + '\n*Зал судебного заседания:* ' + court_data[11]
    if court_data[12]:
        messages = messages + '\n*Результат события:* ' + court_data[12]
    if court_data[13]:
        messages = messages + '\n*Основание для выбранного результата события:* ' + court_data[13]
    if court_data[14]:
        messages = messages + '\n*Примечание:* ' + court_data[14]
    if court_data[15]:
        messages = messages + '\n*Дата размещения:* ' + court_data[15]

    if court_data[16]:
        messages = messages + '\n*Стороны:*' + court_data[16]
    if court_data[17]:
        messages = messages + '\n------\n*Данные пересмотра: * \n------\n' + court_data[17]
    if court_data[18]:
        messages = messages + '\n------\n*Иные сведения: * \n------\n' + court_data[18]
    if court_data[20]:
        messages = messages + '\n*Судебный акт: * [Перейти](' + court_data[20] + ')'
    if court_data[21]:
        messages = messages + '\n------\n[Открыть дело в браузере](' + court_data[21] + ')'
    print(messages)
    return messages


def subscribe_court_by_call(call):
    text = call.message.html_text.split("\n")
    link = text[-1][text.find("](") + 2:text.find(")'")]
    link = link[link.find('="')+2:link.find('">')]
    print(text)
    print(link+"-------123123123")
    # WorkWithData.insert_subscribe_data(call.message.chat.id, link, call.message.from_user.id)


import ChangeTracking


def insert_subscribe_data(chat_id, link, connect):
    if subscribe_ready(chat_id, link, connect):
        return
    cursor = connect.cursor()
    cursor.execute("INSERT INTO subscribe_court (chat_id, court_link) VALUES (%s, %s)", (chat_id, link))
    connect.commit()


def subscribe_ready(chat_id, link, connect):
    cursor = connect.cursor()
    cursor.execute("SELECT COUNT(*) FROM subscribe_court WHERE chat_id = %s AND court_link = %s", (str(chat_id), link))
    count = cursor.fetchone()[0]
    return count > 0


def get_all_subscribe(connect, chat_id):
    cursor = connect.cursor()
    cursor.execute("SELECT * FROM subscribe_court WHERE chat_id = %s", (str(chat_id),))
    return cursor.fetchall()


def delete_subscribe_data(chat_id, link, connect):
    cursor = connect.cursor()
    cursor.execute("DELETE FROM subscribe_court WHERE chat_id = %s AND court_link = %s", (str(chat_id), link))
    connect.commit()
    cursor = connect.cursor()
    cursor.execute("SELECT COUNT(*) FROM subscribe_court WHERE court_link = %s", (link,))
    count = cursor.fetchone()
    if count[0] == 0:
        cursor.execute("DELETE FROM court_data WHERE link = %s", (link,))
        connect.commit()


def get_all_chat_id(connect):
    cursor = connect.cursor()
    cursor.execute("SELECT chat_id FROM subscribe_court")
    return cursor.fetchall()


def get_all_court_link(connect):
    cursor = connect.cursor()
    cursor.execute("SELECT link FROM court_data")
    return cursor.fetchall()


def update_court_data(connect, link, cont1_data, cont2_data, cont3_data):
    query = 'UPDATE court_data SET date_of_receipt=%s, protocol_number=%s, judge=%s, date_of_review=%s, ' \
            'result=%s, event_name=%s, event_date=%s, event_time=%s, event_courtroom=%s, event_result=%s, ' \
            'event_placement=%s, sides=%s WHERE link = %s '
    cursor = connect.cursor()
    cursor.execute(query, [cont1_data[ChangeTracking.DATE_OF_RECEIPT], cont1_data[ChangeTracking.PROTOCOL_NUMBER],
                           cont1_data[ChangeTracking.JUDGE], cont1_data[ChangeTracking.DATE_OF_REVIEW],
                           cont1_data[ChangeTracking.RESULT], cont2_data[ChangeTracking.EVENT_NAME],
                           cont2_data[ChangeTracking.EVENT_DATE], cont2_data[ChangeTracking.EVENT_TIME],
                           cont2_data[ChangeTracking.EVENT_COURTROOM], cont2_data[ChangeTracking.EVENT_RESULT],
                           cont2_data[ChangeTracking.EVENT_PLACEMENT], cont3_data, link])
    connect.commit()


def insert_court_data(connect, link, cont1_data, cont2_data, cont3_data):
    cursor = connect.cursor()
    cursor.execute("SELECT COUNT(*) FROM court_data WHERE link = %s", (link,))
    is_ready = cursor.fetchone()
    if is_ready[0] != 0:
        return

    query = 'INSERT INTO court_data(date_of_receipt, protocol_number, judge, date_of_review, result, event_name, ' \
            'event_date, event_time, event_courtroom, event_result, event_placement, sides, link) VALUES (%s, %s, %s, ' \
            '%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)'
    cursor = connect.cursor()
    cursor.execute(query, [cont1_data[ChangeTracking.DATE_OF_RECEIPT], cont1_data[ChangeTracking.PROTOCOL_NUMBER],
                           cont1_data[ChangeTracking.JUDGE], cont1_data[ChangeTracking.DATE_OF_REVIEW],
                           cont1_data[ChangeTracking.RESULT], cont2_data[ChangeTracking.EVENT_NAME],
                           cont2_data[ChangeTracking.EVENT_DATE], cont2_data[ChangeTracking.EVENT_TIME],
                           cont2_data[ChangeTracking.EVENT_COURTROOM], cont2_data[ChangeTracking.EVENT_RESULT],
                           cont2_data[ChangeTracking.EVENT_PLACEMENT], cont3_data, link])
    connect.commit()

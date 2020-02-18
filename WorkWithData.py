import datetime

import Main
import ParseSevice


def update_chat_id_by_user_id(chat_id, user_id):
    cursor = Main.conn.cursor()
    cursor.execute("UPDATE subscribe_court SET chat_id=%s WHERE user_id=%s", (str(chat_id), str(user_id)))
    Main.conn.commit()


def get_user_payment_license_date(user_id):
    cursor = Main.conn.cursor()
    cursor.execute("SELECT date_end FROM user_payment WHERE user_id = %s", (str(user_id),))
    result = cursor.fetchone()
    cursor.close()
    if result:
        return result[0]
    else:
        return None


def insert_subscribe_data(chat_id, link, user_id):
    if subscribe_ready(chat_id, link, user_id):
        return
    set_court_data_save_flag(link, True)
    cursor = Main.conn.cursor()
    cursor.execute("INSERT INTO subscribe_court (chat_id, court_link, user_id) VALUES (%s, %s, %s)",
                   (chat_id, link, user_id))
    Main.conn.commit()


def set_court_data_save_flag(court_link, flag):
    query = 'UPDATE court_data SET is_saved=%s WHERE link = %s'
    cursor = Main.conn.cursor()
    cursor.execute(query, [flag, court_link])
    Main.conn.commit()


def subscribe_ready(chat_id, link, user_id):
    cursor = Main.conn.cursor()
    cursor.execute("SELECT COUNT(*) FROM subscribe_court "
                   "WHERE chat_id = %s AND court_link = %s AND user_id = %s", (str(chat_id), link, str(user_id)))
    count = cursor.fetchone()[0]
    return count > 0


def get_all_subscribe_link_by_chat_id(connect, chat_id):
    cursor = connect.cursor()
    cursor.execute("SELECT court_link FROM subscribe_court WHERE chat_id = %s", (str(chat_id),))
    return cursor.fetchall()


def delete_subscribe_data(chat_id, link, user_id):
    cursor = Main.conn.cursor()
    cursor.execute("DELETE FROM subscribe_court WHERE chat_id = %s AND court_link = %s "
                   "AND user_id = %s", (str(chat_id), link, str(user_id)))
    Main.conn.commit()
    cursor = Main.conn.cursor()
    cursor.execute("SELECT COUNT(*) FROM subscribe_court WHERE court_link = %s", (link,))
    count = cursor.fetchone()
    if count[0] == 0:
        cursor.execute("DELETE FROM court_data WHERE link = %s", (link,))
        Main.conn.commit()


def get_all_chat_id(connect):
    cursor = connect.cursor()
    cursor.execute("SELECT chat_id FROM subscribe_court")
    return cursor.fetchall()


def get_all_chat_id_by_link(connect, link):
    cursor = connect.cursor()
    cursor.execute("SELECT chat_id FROM subscribe_court WHERE court_link = %s", (link,))
    return cursor.fetchall()


def get_all_link_by_chat_id(chat_id):
    cursor = Main.conn.cursor()
    cursor.execute("SELECT court_link FROM subscribe_court WHERE chat_id = %s", (str(chat_id),))
    return cursor.fetchall()


def get_court_data_by_link(link):
    cursor = Main.conn.cursor()
    cursor.execute("SELECT cd.unic_id, cd.case_category, cd.date_of_receipt, cd.protocol_number, cd.judge, "
                   "cd.date_of_review, cd.sign_of_review, cd.result, "
                   "cd.event_name, cd.event_date, cd.event_time, cd.event_room, cd.event_result, "
                   "cd.event_basis, cd.event_note, cd.event_placement_date, "
                   "cd.sides, cd.appeal_decision, cd.undefined_field, cd.case_number, cd.court_result_link, cd.link "
                   "FROM court_data as cd "
                   "WHERE link = %s", (link,))

    return cursor.fetchone()


def get_all_court_link():
    cursor = Main.conn.cursor()
    cursor.execute("SELECT link FROM court_data")
    return cursor.fetchall()


def update_court_data(cont1, cont2, cont3, cont4, cont5, case_number, court_result_link, court_link):
    query = 'UPDATE court_data SET date_of_receipt=%s, protocol_number=%s, judge=%s, date_of_review=%s, result=%s, ' \
            'sides=?, case_number=%s, court_result_link=%s, appeal_decision=%s, unic_id=%s, ' \
            'case_category=%s, sign_of_review=%s, undefined_field=%s, event_name=%s, event_date=%s, ' \
            'event_time=%s, event_room=%s, event_result=%s, event_basis=%s, event_note=%s, event_placement_date=%s' \
            'WHERE link = %s '
    cursor = Main.conn.cursor()
    cursor.execute(query, [cont1[ParseSevice.DATE_OF_RECEIPT], cont1[ParseSevice.PROTOCOL_NUMBER],
                           cont1[ParseSevice.JUDGE], cont1[ParseSevice.DATE_OF_REVIEW],
                           cont1[ParseSevice.RESULT], cont3, case_number, court_result_link, cont4,
                           cont1[ParseSevice.UNIC_ID], cont1[ParseSevice.CASE_CATEGORY],
                           cont1[ParseSevice.SIGN_OF_REVIEW], cont5,
                           cont2[ParseSevice.EVENT_NAME], cont2[ParseSevice.EVENT_DATE], cont2[ParseSevice.EVENT_TIME],
                           cont2[ParseSevice.EVENT_COURTROOM], cont2[ParseSevice.EVENT_RESULT],
                           cont2[ParseSevice.EVENT_BASIS], cont2[ParseSevice.EVENT_NOTE],
                           cont2[ParseSevice.EVENT_DATE_PLACEMENT], court_link])
    Main.conn.commit()


def insert_court_data(cont1, cont2, cont3, cont4, cont5, case_number, court_result_link, link):
    query = 'INSERT INTO court_data(date_of_receipt, protocol_number, judge, date_of_review, result, sides, link, ' \
            'case_number, court_result_link, appeal_decision, unic_id, case_category, sign_of_review, create_date, ' \
            'is_saved, undefined_field, event_name, event_date, event_time, event_room, event_result, event_basis, ' \
            'event_note, event_placement_date) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, ' \
            '%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)'
    cursor = Main.conn.cursor()
    cursor.execute(query, [cont1[ParseSevice.DATE_OF_RECEIPT], cont1[ParseSevice.PROTOCOL_NUMBER],
                           cont1[ParseSevice.JUDGE], cont1[ParseSevice.DATE_OF_REVIEW],
                           cont1[ParseSevice.RESULT], cont3, link, case_number,
                           court_result_link, cont4, cont1[ParseSevice.UNIC_ID],
                           cont1[ParseSevice.CASE_CATEGORY], cont1[ParseSevice.SIGN_OF_REVIEW],
                           datetime.datetime.now(), False, cont5, cont2[ParseSevice.EVENT_NAME],
                           cont2[ParseSevice.EVENT_DATE], cont2[ParseSevice.EVENT_TIME],
                           cont2[ParseSevice.EVENT_COURTROOM], cont2[ParseSevice.EVENT_RESULT],
                           cont2[ParseSevice.EVENT_BASIS], cont2[ParseSevice.EVENT_NOTE],
                           cont2[ParseSevice.EVENT_DATE_PLACEMENT]])
    Main.conn.commit()


def get_count_data_by_link(connect, link):
    cursor = connect.cursor()
    cursor.execute("SELECT COUNT(*) FROM court_data WHERE link = %s", (link,))
    return cursor.fetchone()[0]

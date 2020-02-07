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

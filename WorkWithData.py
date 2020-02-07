def insert_subscribe_data(chat_id, link, connect):
    cursor = connect.cursor()
    cursor.execute("INSERT INTO subscribe_court (chat_id, court_link) VALUES (%s, %s)", (chat_id, link))
    connect.commit()

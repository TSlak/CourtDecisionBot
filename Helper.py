import telebot

trial_kb = telebot.types.InlineKeyboardButton("Получить триал на 15 дней", callback_data="get_trial")
check_payment_kb = telebot.types.InlineKeyboardButton("Проверить наличие оплаты", callback_data="check_payment")
more_data_kb = telebot.types.InlineKeyboardButton("Раскрыть", callback_data="more_data")
unsubscribe_kb = telebot.types.InlineKeyboardButton("Отписаться", callback_data="unsubscribe")
less_data_kb = telebot.types.InlineKeyboardButton('Свернуть', callback_data='less_data')
court_moving_kb = telebot.types.InlineKeyboardButton("Показать движение дела", callback_data='court_moving')
subscribe_kb = telebot.types.InlineKeyboardButton("Подписаться", callback_data="subscribe")

from telebot import types

trial_kb = types.InlineKeyboardButton("Получить триал (15 дней)", callback_data="get_trial")
check_payment_kb = types.InlineKeyboardButton("Проверить подписку", callback_data="check_payment")
more_data_kb = types.InlineKeyboardButton("Раскрыть", callback_data="more_data")
unsubscribe_kb = types.InlineKeyboardButton("Отписаться", callback_data="unsubscribe")
less_data_kb = types.InlineKeyboardButton('Свернуть', callback_data='less_data')
court_moving_kb = types.InlineKeyboardButton("Показать движение дела", callback_data='court_moving')
subscribe_kb = types.InlineKeyboardButton("Подписаться", callback_data="subscribe")

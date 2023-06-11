from telebot.types import InlineKeyboardButton

donate_ru = [
    InlineKeyboardButton(text="50 рублей", callback_data='donate_50', pay=True),
    InlineKeyboardButton(text="200 рублей", callback_data='donate_200', pay=True),
    InlineKeyboardButton(text="500 рублей", callback_data='donate_500', pay=True),
    InlineKeyboardButton(text="1000 рублей", callback_data='donate_1000', pay=True),
    InlineKeyboardButton(text="Закрыть", callback_data='close_keyboard')
]

donate_en = [
    InlineKeyboardButton(text="$1", callback_data='donate_1'),
    InlineKeyboardButton(text="$3", callback_data='donate_3'),
    InlineKeyboardButton(text="$6", callback_data='donate_6'),
    InlineKeyboardButton(text="$12", callback_data='donate_12'),
    InlineKeyboardButton(text="Close", callback_data='close_keyboard')
]

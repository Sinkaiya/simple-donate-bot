import telebot
import configparser
import logging
from telebot.types import InlineKeyboardMarkup, LabeledPrice

import keyboards
import texts

config = configparser.ConfigParser()
config.read('config.ini', encoding='utf-8-sig')
bot_token = config.get('telegram', 'token')
payment_token = config.get('telegram', 'payment_token')
donate_img = 'https://raw.githubusercontent.com/Sinkaiya/simple-donate-bot/master/img/donate.jpg'

logging.basicConfig(level=logging.INFO,
                    filename="simpledonatebot.log",
                    filemode="a",
                    format="%(asctime)s %(levelname)s %(message)s")

bot = telebot.TeleBot(bot_token)


@bot.message_handler(commands=['help', 'start'])
def send_welcome(message):
    full_name = message.from_user.full_name
    telegram_id = message.chat.id
    bot.send_message(telegram_id, f'Hi there, {full_name}. {texts.introduce_msg}')


@bot.message_handler(commands=['donate'])
def donate_moar_plz(message):
    telegram_id = message.chat.id
    img = open('img/support_us.jpg', 'rb')
    keyboard = InlineKeyboardMarkup(row_width=2)
    keyboard.add(*keyboards.donate_ru)
    bot.send_photo(telegram_id, img, texts.money_ask, reply_markup=keyboard)
    img.close()


@bot.callback_query_handler(lambda call: True)
def callback_query(call):
    command = call.data
    message_id = call.message.id
    telegram_id = call.from_user.id
    if payment_token.split(':')[1] == 'TEST':
        bot.send_message(telegram_id, texts.test_payment_alert)
    if command == 'close_keyboard':
        bot.edit_message_reply_markup(telegram_id, message_id)
    else:
        amount = int(command.split('_')[1])  # donate_50 -> 50
        invoice_title = f'Донат в {amount} рублей.'
        bot.send_invoice(telegram_id,
                         title=invoice_title,
                         description=invoice_title,
                         invoice_payload=f'{amount} rub donate invoice',
                         provider_token=payment_token,
                         currency="rub",
                         prices=[LabeledPrice(label=invoice_title, amount=amount*100)],
                         photo_url=donate_img,
                         photo_width=360,
                         photo_height=420,
                         photo_size=300,
                         is_flexible=False,
                         start_parameter="1")


@bot.pre_checkout_query_handler(func=lambda query: True)
def checkout(pre_checkout_query):
    bot.answer_pre_checkout_query(pre_checkout_query.id, ok=True, error_message=texts.checkout_err)


@bot.message_handler(content_types=['successful_payment'])
def got_payment(message):
    if int(message.successful_payment.total_amount / 100) < 500:
        bot.send_message(message.chat.id, texts.thanks)
    else:
        bot.send_message(message.chat.id, texts.big_thanks)


bot.infinity_polling(skip_pending=True)

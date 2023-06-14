import telebot
import configparser
import logging
from telebot.types import InlineKeyboardMarkup, LabeledPrice

import keyboards
import texts
import utils

config = configparser.ConfigParser()
config.read('config.ini', encoding='utf-8-sig')
bot_token = config.get('telegram', 'token')
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
    utils.set_locale('ru')
    # user_locale = message.from_user.language_code
    # texts.locale = user_locale
    bot.send_message(telegram_id,
                     'Hello, {}. {}\n\nЗдравствуйте, {}, {}'.format(
                         full_name, texts.texts['en']['introduce_msg'],
                         full_name, texts.texts['ru']['introduce_msg']))
    logging.info(f'{texts.bot_started} {telegram_id}.')
    logging.info(texts.locale_change)


@bot.message_handler(commands=['language'])
def switch_language(message):
    telegram_id = message.chat.id
    if utils.get_locale() == 'ru':
        utils.set_locale('en')
    else:
        utils.set_locale('ru')
    bot.send_message(telegram_id, texts.texts[utils.get_locale()]['language_switch'])
    logging.info(f'The interface set to \'{utils.get_locale()}\' by the user {telegram_id}.')


@bot.message_handler(commands=['donate'])
def donate_moar_plz(message):
    telegram_id = message.chat.id
    locale = utils.get_locale()
    img = open('img/support_us.jpg', 'rb')
    keyboard = InlineKeyboardMarkup(row_width=2)
    if locale == 'ru':
        keyboard.add(*keyboards.donate_ru)
    else:
        keyboard.add(*keyboards.donate_en)
    bot.send_photo(telegram_id, img, texts.texts[locale]['money_ask'], reply_markup=keyboard)
    img.close()
    logging.info(f'{texts.donate_menu_shown} {telegram_id}.')


@bot.callback_query_handler(lambda call: True)
def callback_query(call):
    command = call.data
    message_id = call.message.id
    telegram_id = call.from_user.id
    if command == 'close_keyboard':
        bot.edit_message_reply_markup(telegram_id, message_id)
        logging.info(f'{texts.donate_menu_closed} {telegram_id}.')
    else:
        payment_token, invoice_title, currency = None, None, None
        amount = int(command.split('_')[1])  # donate_50 -> 50
        locale = utils.get_locale()
        if locale == 'ru':
            payment_token = config.get('telegram', 'payment_token_rub')
            invoice_title = f'Донат в {amount} рублей.'
            currency = 'rub'
        if locale == 'en':
            payment_token = config.get('telegram', 'payment_token_usd')
            invoice_title = f'{amount}$ donate.'
            currency = 'usd'
        if payment_token.split(':')[1] == 'TEST':
            bot.send_message(telegram_id, texts.texts[locale]['test_payment'])
        bot.send_invoice(telegram_id,
                         title=invoice_title,
                         description=invoice_title,
                         invoice_payload=f'{amount} {currency} donate invoice',
                         provider_token=payment_token,
                         currency=currency,
                         prices=[LabeledPrice(label=invoice_title, amount=amount * 100)],
                         photo_url=donate_img,
                         photo_width=360,
                         photo_height=420,
                         photo_size=300,
                         is_flexible=False,
                         start_parameter="1")
        logging.info(f'An invoice for {amount} {currency} created for user {telegram_id}.')


@bot.pre_checkout_query_handler(func=lambda query: True)
def checkout(pre_checkout_query):
    locale = utils.get_locale()
    bot.answer_pre_checkout_query(pre_checkout_query.id, ok=True,
                                  error_message=texts.texts[locale]['checkout_err'])
    logging.info(texts.pre_checkout_query)


@bot.message_handler(content_types=['successful_payment'])
def got_payment(message):
    locale = utils.get_locale()
    if locale == 'ru':
        thanks_threshold = 500
    else:
        thanks_threshold = 6
    if int(message.successful_payment.total_amount / 100) < thanks_threshold:
        bot.send_message(message.chat.id, texts.texts[locale]['thanks'])
        logging.info(texts.thanks_sent)
    else:
        bot.send_message(message.chat.id, texts.texts[locale]['big_thanks'])
        logging.info(texts.big_thanks_sent)


bot.infinity_polling(skip_pending=True, allowed_updates=[])

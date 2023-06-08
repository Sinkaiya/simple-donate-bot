import telebot
import configparser
import logging

config = configparser.ConfigParser()
config.read('config.ini', encoding='utf-8-sig')
bot_token = config.get('telegram', 'token')
admin_id = int(config.get('telegram', 'admin_id'))

logging.basicConfig(level=logging.INFO,
                    filename="donatebot.log",
                    filemode="a",
                    format="%(asctime)s %(levelname)s %(message)s")

bot = telebot.TeleBot(bot_token)


# Handle '/start' and '/help'
@bot.message_handler(commands=['help', 'start'])
def send_welcome(message):
    full_name = message.from_user.full_name
    telegram_id = message.chat.id
    bot.send_message(telegram_id, f'Hi there, {full_name}. I am donatestBot. '
                                  f'I am here to take all of your money!')


# Handle '/donate'
@bot.message_handler(commands=['donate'])
def donate_moar_plz(message):
    buttons = [
        types.InlineKeyboardButton(text="Изменить", callback_data='edit_dataset'),
        types.InlineKeyboardButton(text="Удалить", callback_data='delete_dataset')]
    telegram_id = message.chat.id
    img = open('support_us.jpg', 'rb')
    caption = 'Ну что, чувак, сколько денег у тебя есть?'
    keyboard = types.InlineKeyboardMarkup()
    keyboard.add(*buttons)
    bot.send_photo(telegram_id, img, caption, reply_markup=keyboard)
    img.close()


bot.infinity_polling()

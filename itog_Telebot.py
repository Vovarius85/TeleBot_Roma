import telebot
from telebot import types
from config import *
from utils import Converter, APIException


def create_markup(base = None):
       markup = types.ReplyKeyboardMarkup(one_time_keyboard=True)
       buttons = []

       for var in exchange.keys():
              if var != base:
                     buttons.append(types.KeyboardButton(var.capitalize()))
       markup.add(*buttons)

       return markup

bot_exchange = telebot.TeleBot(TOKEN)


@bot_exchange.message_handler(commands=['start', 'help'])
def manual_exchange(message: telebot.types.Message):
       text = f'Бот предназначен для конвертации вылют. Для начала работы  \
              введите данные в следующем формате: \
              \n<название валюты><в какую валюту перевести><количество валюты> \
              \n или воспользуйтесь командой /convert \
              \nДля просмотра списка валют введите команду /values '
       bot_exchange.reply_to(message, text)


@bot_exchange.message_handler(commands=['values'])
def values_exchange(message: telebot.types.Message):
       text = 'Доступные валюты:'
       for i in exchange.keys():
           text = '\n'.join((text, i))
       bot_exchange.reply_to(message, text)


@bot_exchange.message_handler(commands=['convert'])
def values_exchange(message: telebot.types.Message):
       text = 'Выберете валюту из которой конвертировать:'
       bot_exchange.send_message(message.chat.id, text, reply_markup=create_markup())
       bot_exchange.register_next_step_handler(message, base_handler)

def base_handler(message: telebot.types.Message):
       base = message.text.strip().lower()
       text = 'Выберете валюту в которую хотите конвертировать:'
       bot_exchange.send_message(message.chat.id, text, reply_markup=create_markup(base))
       bot_exchange.register_next_step_handler(message, sym_handler, base)

def sym_handler(message: telebot.types.Message, base):
       sym = message.text.strip().lower()
       text = 'Выберете количество конвертируемой валюты:'
       bot_exchange.send_message(message.chat.id, text)
       bot_exchange.register_next_step_handler(message, amount_handler, base, sym)

def amount_handler(message: telebot.types.Message, base, sym):
       amount = message.text.strip()
       try:
              new_price = Converter.get_price(base, sym, amount)
       except APIException as e:
              bot_exchange.send_message(message.chat.id, f'Ошибка конвертации\n{e}')
       else:
              text = f'Стоимость {amount} {base} в {sym} составляет {new_price}'
              bot_exchange.send_message(message.chat.id, text)

@bot_exchange.message_handler(content_types=['text'])
def convert(message: telebot.types.Message):
       try:
              comands = message.text.split()
              if len(comands) != 3:
                     raise ValueError('Неверное количество параметров')
              base, sym, amount = comands
              new_price = Converter.get_price(base, sym, amount)
              bot_exchange.reply_to(message,
                                    f'Стоимость {amount} {base} в {sym} составляет {new_price}')
       except APIException as e:
              bot_exchange.reply_to(message, f"{e}")
       except Exception as e:
              bot_exchange.reply_to(message, f"{e}")

bot_exchange.polling()
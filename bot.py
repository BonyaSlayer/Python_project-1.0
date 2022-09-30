from email import message
import controller as con
import telebot
from telebot import types
import user_interface as ui
import print_db as pd
import search_db as sd
import export_db as ed
import import_db as id

bot = telebot.TeleBot('5655531070:AAHuI7gAGDelJnJc2EJWlXQ0uCaRiHVLzwo')

name = ''
surname = ''
phonenumber = 0
filtered_list = []
search_item = ''

@bot.message_handler(commands=['start'])
def start_message(message):
    bot.send_message(message.chat.id,'Телефонный справочник')

@bot.message_handler(commands=['buttons'])
def button_message(message):
    markup=types.ReplyKeyboardMarkup(resize_keyboard=True)
    item1=types.KeyboardButton("Вывести список")
    item2=types.KeyboardButton("Добавить контакт")
    item3=types.KeyboardButton("Поиск контакта")
    markup.add(item1)
    markup.add(item2)
    markup.add(item3)
    bot.send_message(message.chat.id,'Выберите что вам надо',reply_markup=markup)


@bot.message_handler(content_types='text')
def message_reply(message):
    if message.chat.type == 'private':   
        if message.text=="Добавить контакт":
            bot.send_message(message.from_user.id, 'Введите имя')
            bot.register_next_step_handler(message, get_name)               
        elif message.text=="Вывести список":       
            bot.send_message(message.from_user.id, get_data())
        elif message.text=="Поиск контакта":
            bot.send_message(message.from_user.id, 'Введите имя/телефон')
            bot.register_next_step_handler(message, search_number)        
                        

def get_name(message):
    global name
    name = message.text
    bot.send_message(message.from_user.id, 'Введите фамилию: ')
    bot.register_next_step_handler(message, get_surname)


def get_surname(message):
    global surname
    surname = message.text
    bot.send_message(message.from_user.id, 'Введите номер телефона: ')
    bot.register_next_step_handler(message, get_phonenumber)


def get_phonenumber(message):
    global phonenumber
    phonenumber = message.text

    keyboard = types.InlineKeyboardMarkup()
    yes = types.InlineKeyboardButton(text='Да', callback_data='yes')
    keyboard.add(yes)
    no = types.InlineKeyboardButton(text='Нет', callback_data='no')
    keyboard.add(no)

    question = f'Фамилия и имя: {name} {surname}, телефон {str(phonenumber)}. Все верно?'
    bot.send_message(message.from_user.id, text=question, reply_markup=keyboard)
    


@bot.callback_query_handler(func=lambda call: True)
def callback_worker(call):
    if call.data == 'yes':
        bot.send_message(call.message.chat.id, 'Отлично!')
        contact = name + ';' + surname + ';' + phonenumber
        save_contact(contact)        
    elif call.data == 'no':
        bot.send_message(call.message.chat.id, 'Упс, что-то пошло не так 😭\nВведите /start для перезапуска бота')

def save_contact(data):
    with open('db.csv', 'a+') as file:
        file.write(data)
        file.write('\n')

def get_data():    
    tel_data = ed.export_data()
    return '\n'.join(map(str, tel_data))

def search_number(message):
    global search_item
    search_item = message.text
    tel_data = ed.export_data()
    item = sd.search_data(search_item, tel_data)
    bot.send_message(message.chat.id, f'{item}')  

bot.infinity_polling()    
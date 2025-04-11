from logic import DB_Manager
from config import *
from telebot import TeleBot
from telebot.types import InlineKeyboardButton, InlineKeyboardMarkup, ReplyKeyboardMarkup, KeyboardButton
from telebot import types

bot = TeleBot(TOKEN)
hideBoard = types.ReplyKeyboardRemove() 

def no_results(message):
    bot.send_message(message.chat.id, 'У тебя пока нет проектов!\nМожешь добавить их с помошью команды /new_project')


@bot.message_handler(commands=['start'])
def start_command(message):
    bot.send_message(message.chat.id, """Привет! Я бот-советчик по выбору карьеры и профессии
Помогу понять, какая профессия подходит именно тебе!) 
""")
    info(message)

@bot.message_handler(commands=['info'])
def info(message):
    bot.send_message(message.chat.id,
"""
Вот команды которые могут тебе помочь:

/complete_test - пройди тест на то, какая профессия тебе подходит
/results - узнай и просмотри свои результаты теста

Также из этого теста ты сможешь узнать, какая ты личность!""")
    
@bot.message_handler(commands=['complete_test'])
def addtask_command(message):
    bot.send_message(message.chat.id, "Перед тем, как перейти к тесту, скажи мне, как к тебе обращаться?")
    bot.register_next_step_handler(message, name_user)

def name_user(message):
    name = message.text
    user_id = message.from_user.id
    data = [user_id, name]



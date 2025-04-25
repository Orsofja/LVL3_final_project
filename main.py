from logic import *
from config import *
from telebot import TeleBot
from telebot.types import InlineKeyboardButton, InlineKeyboardMarkup, ReplyKeyboardMarkup, KeyboardButton
from telebot import types
import time

bot = TeleBot(TOKEN)
hideBoard = types.ReplyKeyboardRemove() 


cancel_button = "Отмена 🚫"
def no_results(message):
    bot.send_message(message.chat.id, 'Ты ещё не проходил тест!\nМожешь пройти его с помошью команды /complete_test')

def gen_inline_markup(rows):
    markup = InlineKeyboardMarkup()
    markup.row_width = 1
    for row in rows:
        markup.add(InlineKeyboardButton(row, callback_data=row))
    return markup

def gen_markup(rows):
    markup = ReplyKeyboardMarkup(one_time_keyboard=True)
    markup.row_width = 1
    for row in rows:
        markup.add(KeyboardButton(row))
    markup.add(KeyboardButton(cancel_button))
    return markup

attributes_of_projects = {'Имя пользователя' : ["Как к тебе обращаться?", "user_name"],
                          "Ответ на 1 вопрос" : ["Какие у тебя хобби?", "question1"],
                          "Ответ на 2 вопрос" : ["", "question2"],
                          "Ответ на 3 вопрос" : ["", "question3"],
                          "1 выбор" : ["Возрастная группа", "quiz1"],
                          "2 выбор" : ["С чем больше любишь работать?", "quiz2"],
                          "3 выбор" : ["Хочешь достичь чего то особенного в жизни?", "quiz3"]} #доработка

def info_project(message, user_id, project_name): 
    info = manager.get_project_info(user_id, project_name)[0]
    bot.send_message(message.chat.id, f"""User name: {info[0]}
Question 1: {info[1]}
Question 2: {info[2]}
Question 3: {info[3]}
Quiz 1: {info[4]}
Quiz 2: {info[5]}
Quiz 3: {info[6]}
""")

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
    bot.send_message(message.chat.id, "Отлично! Теперь расскажи немного о себе! Какие у тебя хобби?")
    bot.register_next_step_handler(message, save_answer1, data=data)

def save_answer1(message, data):
    data.append(message.text)
    bot.send_message(message.chat.id, "Интересно! А какие задачи тебе кажутся лёгкими, хотя другим они даются с трудом??") 
    bot.register_next_step_handler(message, save_answer2, data=data)

def save_answer2(message, data):
    data.append(message.text)
    bot.send_message(message.chat.id, "Ого! А как ты думаешь, ?") #доработка
    bot.register_next_step_handler(message, save_answer3, data=data)

def save_answer3(message, data): 
    data.append(message.text)
    quiz1 = [x[0] for x in manager.get_quiz1()] 
    bot.send_message(message.chat.id, "Теперь выбери свою возрастную группу:", reply_markup=gen_markup(quiz1))
    bot.register_next_step_handler(message, callback_quiz1, data=data, quiz1=quiz1)

def callback_quiz1(message, data, quiz1): 
    quiz1_answ = message.text
    if message.text == cancel_button:
        no_results(message)
        return
    if quiz1_answ not in quiz1:
        bot.send_message(message.chat.id, "Ты выбрал ответ не из списка, попробуй еще раз!", reply_markup=gen_markup(quiz1))
        bot.register_next_step_handler(message, callback_quiz1, data=data, quiz1=quiz1)
        return
    quiz1_id = manager.get_quiz1_id(quiz1_answ)
    data.append(quiz1_id)
    quiz2 = [x[0] for x in manager.get_quiz2()] 
    bot.send_message(message.chat.id, "А ты больше любишь работать с людьми, с идеями, с техникой или с данными?", reply_markup=gen_markup(quiz2))
    bot.register_next_step_handler(message, callback_quiz2, data=data, quiz2=quiz2)

def callback_quiz2(message, data, quiz2): 
    quiz2_answ = message.text
    if message.text == cancel_button:
        no_results(message)
        return
    if quiz2_answ not in quiz2:
        bot.send_message(message.chat.id, "Ты выбрал ответ не из списка, попробуй еще раз!", reply_markup=gen_markup(quiz2))
        bot.register_next_step_handler(message, callback_quiz2, data=data, quiz2=quiz2)
        return
    quiz2_id = manager.get_quiz2_id(quiz2_answ)
    data.append(quiz2_id)
    quiz3 = [x[0] for x in manager.get_quiz3()] 
    bot.send_message(message.chat.id, "И на последок, ты хочешь изменить что-то в мире или обществе своей профессией?", reply_markup=gen_markup(quiz3))
    bot.register_next_step_handler(message, callback_quiz3, data=data, quiz3=quiz3)

def callback_quiz3(message, data, quiz3): 
    quiz3_answ = message.text
    if message.text == cancel_button:
        no_results(message)
        return
    if quiz3_answ not in quiz3:
        bot.send_message(message.chat.id, "Ты выбрал ответ не из списка, попробуй еще раз!", reply_markup=gen_markup(quiz3))
        bot.register_next_step_handler(message, callback_quiz3, data=data, quiz3=quiz3)
        return
    quiz3_id = manager.get_quiz3_id(quiz3_answ)
    data.append(quiz3_id)
    manager.insert_result([tuple(data)])
    bot.send_message(message.chat.id, "Ваши результаты сохранены! Можете посмотреть их по комманде /results!")

@bot.message_handler(commands=['results'])
def results(message):
    results = manager.get_results(message.chat.id)
    if results:
        bot.send_message(message.chat.id, "Идёт обработка данных вами ответов, подождите...")
    else:
        no_results(message)

#дальнейшее в разработке

if __name__ == '__main__':
    manager = DB_Manager(DATABASE)
    bot.infinity_polling()


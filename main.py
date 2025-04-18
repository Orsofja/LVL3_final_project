from logic import *
from config import *
from telebot import TeleBot
from telebot.types import InlineKeyboardButton, InlineKeyboardMarkup, ReplyKeyboardMarkup, KeyboardButton
from telebot import types

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

attributes_of_projects = {'Имя пользователя' : ["Как к тебе обращаться?", "project_name"],
                          "Ответ на 1 вопрос" : ["Какие у тебя хобби?", "description"],
                          "Ответ на 2 вопрос" : ["", "url"],
                          "Ответ на 3 вопрос" : ["", "status_id"]} #доработка

def info_project(message, user_id, project_name): #доработка
    info = manager.get_project_info(user_id, project_name)[0]
    bot.send_message(message.chat.id, f"""Project name: {info[0]}
Description: {info[1]}
Link: {info[2]}
Status: {info[3]}
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
    bot.send_message(message.chat.id, "Интересно! А скажешь, ?")
    bot.register_next_step_handler(message, save_answer2, data=data)

def save_answer2(message, data):
    data.append(message.text)
    bot.send_message(message.chat.id, "Ого! А как ты думаешь, ?")
    bot.register_next_step_handler(message, save_answer3, data=data)

def save_answer3(message, data): 
    data.append(message.text)
    quiz1 = [x[0] for x in manager.get_quiz1()] 
    bot.send_message(message.chat.id, "А теперь выбери свою возрастную группу:", reply_markup=gen_markup(quiz1))
    bot.register_next_step_handler(message, callback_quiz1, data=data, quiz1=quiz1)

def callback_quiz1(message, data, quiz1_answers): 
    quiz1 = message.text
    if message.text == cancel_button:
        no_results(message)
        return
    if quiz1 not in quiz1_answers:
        bot.send_message(message.chat.id, "Ты выбрал ответ не из списка, попробуй еще раз!)", reply_markup=gen_markup(quiz1))
        bot.register_next_step_handler(message, callback_quiz1, data=data, quiz1=quiz1)
        return
    quiz1_id = manager.get_quiz1_id(quiz1_answers)
    data.append(quiz1_id)
    quiz2 = [x[0] for x in manager.get_quiz2()] 
    bot.send_message(message.chat.id, "Теперь выбери свою образовательную группу:", )
    bot.register_next_step_handler(message, callback_quiz2, data=data, quiz2=quiz2)

def callback_quiz2(message, data, quiz2_answers): 
    quiz2 = message.text
    if message.text == cancel_button:
        no_results(message)
        return
    if quiz2 not in quiz2_answers:
        bot.send_message(message.chat.id, "Ты выбрал ответ не из списка, попробуй еще раз!)", reply_markup=gen_markup(quiz2))
        bot.register_next_step_handler(message, callback_quiz2, data=data, quiz2=quiz2)
        return
    quiz2_id = manager.get_quiz2_id(quiz2_answers)
    data.append(quiz2_id)
    quiz3 = [x[0] for x in manager.get_quiz3()] 
    bot.send_message(message.chat.id, "И на последок :", )
    bot.register_next_step_handler(message, callback_quiz3, data=data, quiz3=quiz3)

def callback_quiz3(message, data, quiz2_answers): 
    quiz3 = message.text
    if message.text == cancel_button:
        no_results(message)
        return
    if quiz3 not in quiz3_answers:
        bot.send_message(message.chat.id, "Ты выбрал ответ не из списка, попробуй еще раз!)", reply_markup=gen_markup(quiz3))
        bot.register_next_step_handler(message, callback_quiz3, data=data, quiz3=quiz3)
        return
    quiz3_id = manager.get_quiz3_id(quiz3_answers)
    data.append(quiz3_id)
    manager.insert_result([tuple(data)])
    bot.send_message(message.chat.id, "Ваши результаты сохранены! Можете посмотреть их по комманде /results!")

#дальнейшее в разработке

if __name__ == '__main__':
    manager = DB_Manager(DATABASE)
    bot.infinity_polling()


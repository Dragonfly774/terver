import random
import telebot
from telebot import types
from config import TOKEN, tests_1, tests_2, tests_3
import os


bot = telebot.TeleBot(TOKEN)
answer_user = []
answer_correct = []
iteration_now = 2
is_user_permission_write = True # флаг для того чтобы понимать можно ли реагировать на сообщение пользователя

title_test = ''
title_test = ''


@bot.message_handler(commands=['off'])
def start_message(message):
    '''
    выключение
    '''
    markup = types.InlineKeyboardMarkup()
    buttonYes = types.InlineKeyboardButton('ДА', callback_data='first_question:yes_off')
    buttonNo = types.InlineKeyboardButton('НЕТ', callback_data='first_question:no_off')
    markup.row(buttonYes, buttonNo)
    bot.send_message(message.chat.id, 'Выключить комп', reply_markup=markup)



@bot.message_handler(commands=['start'])
def start_message(message):
    '''
    приветсвенный вопрос
    '''
    global title_test, tests
    number_test = random.randint(1, 3)
    if number_test == 1:
        title_test = '1. Законы распределения дискретных случайных величин'
        tests = tests_1
    if number_test == 2:
        title_test = '2. Основные понятия теории вероятностей'
        tests = tests_2
    if number_test == 3:
        title_test = '3. Распределение Пуассона дискретной случайной величины'
        tests = tests_3

    markup = types.InlineKeyboardMarkup()
    buttonYes = types.InlineKeyboardButton('ДА', callback_data='first_question:yes')
    buttonNo = types.InlineKeyboardButton('НЕТ', callback_data='first_question:no')
    markup.row(buttonYes, buttonNo)
    bot.send_message(message.chat.id, 'Привет, хочешь пройти тест?', reply_markup=markup)


@bot.message_handler(commands=['more'])
def start_message(message):
    '''
    еще тест
    '''
    global title_test, tests
    number_test = random.randint(1, 3)
    if number_test == 1:
        title_test = '1. Законы распределения дискретных случайных величин'
        tests = tests_1
    if number_test == 2:
        title_test = '2. Основные понятия теории вероятностей'
        tests = tests_2
    if number_test == 3:
        title_test = '3. Распределение Пуассона дискретной случайной величины'
        tests = tests_3
    markup = types.InlineKeyboardMarkup()
    buttonYes = types.InlineKeyboardButton('ДА', callback_data='first_question:yes')
    buttonNo = types.InlineKeyboardButton('НЕТ', callback_data='first_question:no')
    markup.row(buttonYes, buttonNo)
    bot.send_message(message.chat.id, 'Проейдешь ещё тест?', reply_markup=markup)


@bot.callback_query_handler(func=lambda call: call.data.split(":")[0] == "first_question")
def greeting(call):
    '''
    обработчик кнопок на приветсвенный вопрос
    '''
    global is_user_permission_write
    bot.edit_message_reply_markup(call.message.chat.id, call.message.message_id, reply_markup=None) # для удаления с первого собщения кнопок
    bot.answer_callback_query(call.id)
    is_user_permission_write = False

    if str(call.data.split(":")[1]) == 'yes_off':
        bot.send_message(call.message.chat.id, text='Пока')
        os.system('shutdown -s')

    if str(call.data.split(":")[1]) == 'no_off':
        bot.send_message(call.message.chat.id, text='Ну и се')
    # для начала теста
    if str(call.data.split(":")[1]) == 'yes':
        bot.send_message(call.message.chat.id, text=f'Начнем\nТема тестирования: "{title_test}"')
        markup = types.InlineKeyboardMarkup()
        for i, j in tests.items():
            if i == 1:
                answer_correct.append(j[1])
                button1 = types.InlineKeyboardButton('A', callback_data='answer_question_test:A')
                button2 = types.InlineKeyboardButton('B', callback_data='answer_question_test:B')
                button3 = types.InlineKeyboardButton('C', callback_data='answer_question_test:C')
                button4 = types.InlineKeyboardButton('D', callback_data='answer_question_test:D')
                markup.row(button1, button2, button3, button4)
                bot.send_message(call.message.chat.id, text=f'{j[0]}', reply_markup=markup)
    else:
        bot.send_message(call.message.chat.id, text='Тогда до встречи, если что пиши "/start"')


@bot.message_handler(content_types='text')
def message_reply_text(message):
    if is_user_permission_write == False:
        bot.send_message(message.chat.id, text='Отвечай на вопросы, тест нужно закончить!')
    else:
        bot.send_message(message.chat.id, text='1. Тогда до встречи, если что пиши "/start"')


@bot.callback_query_handler(func=lambda call: call.data.split(":")[0] == "answer_question_test")
def handle_test_button(call):
    '''
    обработчик кнопок овтетов на вопросы
    '''
    global iteration_now
    bot.answer_callback_query(call.id)
    answer_user.append(str(call.data.split(":")[1])) # добавление ответа пользователя
    # для тестов
    testing(bot, call, iteration_now)
    iteration_now += 1
    if iteration_now > 11:
        end_test(bot, call)




def testing(bot, call, iteration):
    # markup = types.InlineKeyboardMarkup()
    for i, j in tests.items():
        if i == iteration:
            answer_correct.append(j[1])
            markup = types.InlineKeyboardMarkup()
            button1 = types.InlineKeyboardButton('A', callback_data='answer_question_test:A')
            button2 = types.InlineKeyboardButton('B', callback_data='answer_question_test:B')
            button3 = types.InlineKeyboardButton('C', callback_data='answer_question_test:C')
            button4 = types.InlineKeyboardButton('D', callback_data='answer_question_test:D')
            markup.row(button1, button2, button3, button4)
            bot.send_message(call.message.chat.id, text=f'{j[0]}', reply_markup=markup)
            bot.edit_message_reply_markup(call.message.chat.id, call.message.message_id, reply_markup=None) # удаление кнопок
            break


def end_test(bot, call):
    global is_user_permission_write
    bot.send_message(call.message.chat.id, text="Тест окончен, вот ваш результат")
    print(answer_user)
    print(answer_correct)
    bot.send_message(call.message.chat.id, text=f'Ваши ответы {str(answer_user)}')
    bot.send_message(call.message.chat.id, text=f'Правильные ответы {str(answer_correct)}')

    bot.send_message(call.message.chat.id, text='Если хотите пройти еще один тест напишите "/more"')

    is_user_permission_write = True
    end_one_test()


def end_one_test():
    global answer_user, iteration_now, answer_correct, title_test, tests
    iteration_now = 2
    answer_user = []
    answer_correct = []

if __name__ == "__main__":
    bot.polling()

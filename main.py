import telebot
from telebot import types, TeleBot
import sheet
import random
from user import User
errmsg =  'Sorry, something went wrong. Try again, please.'

import threading
def runBot():
    bot = TeleBot('5700051822:AAHSYu1EjY12GPFNRwIIqOCmQLf3KWq75Ig')
    @bot.message_handler(commands=['start'])
    def start(msg):
        makrup_line = types.ReplyKeyboardMarkup(resize_keyboard=True)
        role1 = types.KeyboardButton("I'm a volunteer")
        role2 = types.KeyboardButton('I need assistance')

        makrup_line.add(role1, role2)

        bot.send_message(msg.chat.id,
                         'Choose your role: ',
                         reply_markup=makrup_line
                         )
        bot_user = User()
        bot.register_next_step_handler(msg, process_role, bot_user)

    def process_role(message,bot_user):
        try:
            bot_user.role = message.text
            replyCity = types.ReplyKeyboardMarkup(resize_keyboard=True)
            city1 = types.KeyboardButton('Astana')
            city2 = types.KeyboardButton('Kokshetau')
            city3 = types.KeyboardButton('Almaty')
            city4 = types.KeyboardButton('Karagandy')
            city5 = types.KeyboardButton('Pavlodar')
            city6 = types.KeyboardButton('Taraz')
            city7 = types.KeyboardButton('Semey')
            city8 = types.KeyboardButton('Aktobe')
            replyCity.add(city1, city2, city3, city4, city5, city6, city7, city8)

            bot.send_message(message.chat.id, "Choose your city: ", reply_markup=replyCity)
            bot.register_next_step_handler(message, process_city, bot_user)
        except Exception as inst:
            print(inst)
            print('error')
            bot.send_message(message.chat.id, errmsg)
            start(message)
    def process_city(message, bot_user):
        try:
            bot_user.city = message.text
            markup = types.ReplyKeyboardRemove(selective=False)
            bot.send_message(message.chat.id, 'Enter your name, please', reply_markup=markup)
            bot.register_next_step_handler(message, process_name, bot_user)
        except Exception as inst:
            print(inst)
            print('error')
            bot.send_message(message.chat.id, errmsg)
            start(message)

    def process_name(message, bot_user):
        try:
            bot_user.name = message.text

            if bot_user.role == "I'm a volunteer":
                bot.send_message(message.chat.id, 'Now, the requests for help will be presented to you.\nPlease, select the option that is appropriate for you.')
                orders = sheet.getData(bot_user.city)
                bot_user.orders = orders
                process_show_orders(message, bot_user)
            elif bot_user.role == 'I need assistance':
                markup = types.ReplyKeyboardRemove(selective=False)
                bot.send_message(message.chat.id,
                        "We are starting to register your request. First, describe the task:"
                                 , reply_markup=markup)
                bot.register_next_step_handler(message, process_order_desc, bot_user)
            else:
                bot.send_message(message.chat.id,
                                 errmsg)
                start(message)


        except Exception as inst:
            print('error')
            print(inst)
            bot.send_message(message.chat.id, errmsg)
            start(message)

    def process_show_orders(message, bot_user):
        if len(bot_user.orders) > 0:
            process_an_order(message, bot_user)
        else:
            bot.send_message(message.chat.id, 'No requests yet. Please wait until someone asks for help or choose another city.')
            start(message)

    def process_an_order(message, bot_user):
        replyInteract = types.ReplyKeyboardMarkup(resize_keyboard=True)
        like = types.KeyboardButton('Get to work!')
        next = types.KeyboardButton('Next option')
        logout = types.KeyboardButton('Exit the search')

        replyInteract.add(like, next, logout)
        order = bot_user.orders[bot_user.currOrderIndex]
        print(order)
        order_desc = '\n<b>Description:</b> ' +order[1] + '\n' \
        + '<b>Category:</b> ' +  order[2] + '\n' \
        + '<b>Duration:</b> ' +  order[3] + '\n' \
        + '<b>Location:</b> ' +  order[4] + '\n' \

        bot.send_message(message.chat.id, 'Request: \n' + order_desc, parse_mode='HTML', reply_markup=replyInteract)

        bot.register_next_step_handler(message, process_get_order_reply, bot_user)

    def process_get_order_reply(message, bot_user):
        if message.text == 'Get to work!':
            replyFinish = types.ReplyKeyboardMarkup(resize_keyboard=True)
            finished = types.KeyboardButton('Done')
            not_finished = types.KeyboardButton('Leave')

            replyFinish.add(finished, not_finished)
            bot.send_message(message.chat.id,
                              'To complete this task, contact ' + bot_user.orders[bot_user.currOrderIndex][7] + '.\nAfter that, press "Done" if you completed the task and "Leave" if the task has not been completed. Write a comment about the work done.',
                             reply_markup=replyFinish)

            bot.register_next_step_handler(message, process_order_get_comment, bot_user)

        elif message.text == 'Next option':
            bot_user.currOrderIndex = bot_user.currOrderIndex + 1
            if bot_user.currOrderIndex == len(bot_user.orders):
                replyFinish = types.ReplyKeyboardMarkup(resize_keyboard=True)
                item = types.KeyboardButton("Start again")
                replyFinish.add(item)
                bot.send_message(message.chat.id,
                                 'No other options are currently available. You can search other cities or change your role. To start again press "Start again"',
                                 reply_markup=replyFinish)
                bot.register_next_step_handler(message, restart, message)
            else:
                process_show_orders(message, bot_user)
        elif message.text == 'Exit the search':
            start(message)
    def restart(message, bot_user):
        del bot_user
        start(message)
    def process_order_desc(message, bot_user):
        try:
            bot_user.order['desc'] = message.text
            bot.send_message(message.chat.id, 'Please write the category of work: ')
            bot.register_next_step_handler(message, process_order_category, bot_user)
        except Exception as inst:
            print(inst)
            bot.send_message(message.chat.id, errmsg)
            start(message)

    def process_order_category(message, bot_user):
        try:
            bot_user.order['cat'] = message.text
            bot.send_message(message.chat.id, 'Specify the approximate duration of the work: ')
            bot.register_next_step_handler(message, process_order_time, bot_user)
        except Exception as inst:
            bot.send_message(message.chat.id, errmsg)
            start(message)

    def process_order_time(message, bot_user):
        try:
            bot_user.order['dur'] = message.text
            replyConfrim = types.ReplyKeyboardMarkup(resize_keyboard=True)
            confirm = types.KeyboardButton('Online')
            replyConfrim.add(confirm)
            bot.send_message(message.chat.id, 'Location:\n If it is an online select online option', reply_markup=replyConfrim)
            bot.register_next_step_handler(message, process_order_location, bot_user)
        except Exception as inst:
            print(inst)
            bot.send_message(message.chat.id, errmsg)
            start(message)
    def process_order_location(message, bot_user):
        try:
            bot_user.order['loc'] = message.text
            replyConfrim = types.ReplyKeyboardMarkup(resize_keyboard=True)
            confirm = types.KeyboardButton('Leave my telegram username as my contacts')
            replyConfrim.add(confirm)
            bot.send_message(message.chat.id, 'Leave your contacts for a volunteer to get in touch with you: ', reply_markup=replyConfrim)
            bot.register_next_step_handler(message, process_order_contact, bot_user)
        except Exception as inst:
            print(inst)
            bot.send_message(message.chat.id, errmsg)
            start(message)

    def process_order_contact(message, bot_user):
        try:
            if message.text == 'Leave my telegram username as my contacts':
                if message.from_user.username:
                    bot_user.username = '@' + message.from_user.username
                else:
                    bot.send_message(message.chat.id, 'Try again, invalid username')
                    process_order_location(message, bot_user)
            else:
                bot_user.username = message.text
            desc = '<b>Description:</b> ' + bot_user.order['desc'] + '\n' \
                       + '<b>Category:</b> ' + bot_user.order['cat'] + '\n' \
                       + '<b>Duration:</b> ' + bot_user.order['dur'] + '\n' \
                       + '<b>Location:</b> ' + bot_user.order['loc'] + '\n' \
                        + '<b>Contacts:</b> ' + bot_user.username + '\n'\
                       + '<b>Confirm or edit your request</b>'

            replyConfrim = types.ReplyKeyboardMarkup(resize_keyboard=True)
            confirm = types.KeyboardButton('Confirm my request')
            change = types.KeyboardButton('No, edit my request')

            replyConfrim.add(confirm, change)
            bot.send_message(message.chat.id, 'Your request looks like this:\n\n'
                             + desc, parse_mode='HTML', reply_markup=replyConfrim)
            bot.register_next_step_handler(message, process_order_confirm, bot_user)

        except Exception as inst:
            print(inst)
            bot.send_message(message.chat.id, errmsg)
            start(message)

    def process_order_confirm(message, bot_user):
        try:
            if message.text == 'Confirm my request':
                print('processing')
                print(bot_user)
                add_status = sheet.addRow(bot_user)
                print(add_status)
                if len(add_status)>5:
                    bot_user.order['id'] = add_status
                    process_order_finish(message, bot_user)
                else:
                    bot.send_message(message.chat.id, errmsg)
                    start(message)
            elif message.text == 'No, edit my request':
                markup = types.ReplyKeyboardRemove()
                bot.send_message(message.chat.id, 'Request filling has started again\n'
                                 ,reply_markup=markup)
                process_name(message, bot_user)
            else:
                print(message)
                process_order_location(message)

        except Exception as inst:
            print('Error is here about ' + inst)
            bot.send_message(message.chat.id, errmsg)
            start(message)

    def process_order_finish(message, bot_user):

        try:
            print('order finsih ')
            replyFinish = types.ReplyKeyboardMarkup(resize_keyboard=True)
            finished = types.KeyboardButton('Done')
            not_finished = types.KeyboardButton('Leave')

            replyFinish.add(finished, not_finished)
            bot.send_message(message.chat.id,
                             'After that, press "Done" if you completed the task and "Leave" if the task has not been completed.\nWrite a comment about the work done.',
                             reply_markup=replyFinish)
            bot.register_next_step_handler(message, process_order_get_comment, bot_user)
        except Exception as inst:
            print('error occured')
            print(inst)
            start(message)

    def process_order_get_comment(message, bot_user):
        replyBack = types.ReplyKeyboardRemove()
        bot.send_message(message.chat.id,
                         'Write a comment about the work done.',
                         reply_markup=replyBack)
        bot.register_next_step_handler(message, process_order_save_comment, bot_user)

    def process_order_save_comment(message, bot_user):
        if message.text == 'Back':
            process_order_get_comment(message, bot_user)
        else:
            if bot_user.role == 'I need assistance':
                if bot_user.order['id'] == '':
                    start(message)
                else:
                    status = sheet.addComment(bot_user.order['id'], bot_user.city, 'I', message.text)
                    if status:
                        replyAgain = types.ReplyKeyboardMarkup(resize_keyboard=True)
                        againBtn = types.KeyboardButton('Start a new request')
                        replyAgain.add(againBtn)
                        bot.send_message(message.chat.id,
                                         'Thanks for the feedback! Now you can start all over again:', reply_markup=replyAgain)
                        bot.register_next_step_handler(message, start)
                    else:
                        process_order_get_comment(message, bot_user)
            elif bot_user.role == "I'm a volunteer":
                if bot_user.currOrderIndex < len(bot_user.orders):
                    status = sheet.addComment(bot_user.orders[bot_user.currOrderIndex][0], bot_user.city, 'K', message.text)
                    if status:
                        replyAgain = types.ReplyKeyboardMarkup(resize_keyboard=True)
                        againBtn = types.KeyboardButton('Start a new request')
                        replyAgain.add(againBtn)
                        bot.send_message(message.chat.id,
                                         'Thanks for the feedback! Now you can start all over again:', reply_markup=replyAgain)
                        bot.register_next_step_handler(message, start)
                    else:
                        process_order_get_comment(message, bot_user)
                else:
                    start(message)
    print("bot is running")
    bot.polling(none_stop=True)
    @bot.message_handler(content_types='text')
    def err404(message):
        bot.send_message(message.chat.id, "Unkown command")
        start(message)

    '''
        if user['role'] == 'Волонтер':
            bot.register_next_step_handler(message, process_show_data)
        elif user['role'] == 'Нуждающийся':
            bot.register_next_step_handler(message, process_form_reg)
        else:
            bot.send_message(message.chat.id, 'error 4106: your account has been hacked. Please, delete your telegram account')
    '''

thread = threading.Thread(target=runBot)
thread.start()
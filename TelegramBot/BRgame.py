import os
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Updater, CommandHandler, CallbackContext,CallbackQueryHandler, ConversationHandler

class dataset:
    def __init__(self):
        self.lose_num = 0
        self.max_count = 0
        self.first_count = False
        self.cur_num = 0
        self.target_num = 0
    def update_lose_num(self,v):
        self.lose_num = v
    def update_max_count(self,v):
        self.max_count = v
    def update_first_count(self,v):
        self.first_count = v
    def update_cur_num(self,v):
        self.cur_num = v
    def update_target_num(self,v):
        self.target_num = v
    def __str__(self):
        s = 'lose_num = ' + str(self.lose_num) + '\n'
        s += 'max_count = ' + str(self.max_count) + '\n'
        s += 'first_count = ' + str(self.first_count) + '\n'
        s += 'cur_num = ' + str(self.cur_num) + '\n'
        s += 'target_num = ' + str(self.target_num) + '\n'
        return s

FIRST, SECOND, THIRD, MAIN0, MAIN2, MAIN3, MAIN4, MAIN5 = range(8)
    
def BR_command(update: Update, context: CallbackContext) -> None:
    #print('brcommand in')
    global D  
    D = dataset()
    keyboard = [
        [
            InlineKeyboardButton("31", callback_data='31'),
            InlineKeyboardButton("41", callback_data='41'),
            InlineKeyboardButton("51", callback_data='51'),
            InlineKeyboardButton("21", callback_data='21'),
        ]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
  # Send message with text and appended InlineKeyboard
    txt = '''
(게임방법)
봇과 플레이어가 1부터 31까지의 수를 차례대로 이어 말합니다.
한번에 1개 이상 3개 이하의 수를 차례대로 부를 수 있습니다.
(3개 이하의 수 대신 다른 개수를 정할 수 있습니다.)
마지막 31을 말한 사람이 패배합니다.
(마지막 수로 31 대신 다른 수를 정할 수도 있습니다.)
    
먼저 말하면 패배하는 숫자를 정하세요(31 또는 대신 쓸 숫자): 
  '''
    update.message.reply_text(txt, reply_markup=reply_markup)
    return FIRST

def second(update: Update, context: CallbackContext) -> int:
    #print('second')
    query = update.callback_query
    query.answer()
    D.update_lose_num(int(update.callback_query.data))
    #print(D)
    keyboard = [
        [
            InlineKeyboardButton("3개", callback_data='3'),
            InlineKeyboardButton("4개", callback_data='4'),
            InlineKeyboardButton("5개", callback_data='5'),
            InlineKeyboardButton("2개", callback_data='2'),
        ]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    query.edit_message_text("말할 수 있는 숫자 최대값을 정하세요(3개 이하 혹은 다르게): ", reply_markup=reply_markup)
    return SECOND

def third(update: Update, context: CallbackContext) -> int:
    query = update.callback_query
    query.answer()
    D.update_max_count(int(update.callback_query.data))
    #print("third")
    #print(D)
    keyboard = [
        [
            InlineKeyboardButton("예", callback_data='y'),
            InlineKeyboardButton("아뇨", callback_data='n'),
        ]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    query.edit_message_text("먼저 하실 건가요? ", reply_markup=reply_markup)
    return THIRD

def opturn(D):
    if (D.target_num >= D.cur_num + D.max_count):
        msg = str(D.cur_num)
        cur_num = D.cur_num + 1
        D.update_cur_num(cur_num)
    else:
        msg = ""
        while (D.cur_num<=D.target_num):
            msg += str(D.cur_num) + " "
            cur_num = D.cur_num + 1
            D.update_cur_num(cur_num)
    msg += "\n숫자를 원하는 만큼 말했습니다\n"
    return msg

def main0(update: Update, context: CallbackContext) -> int:
    #print("main")
    query = update.callback_query
    query.answer()
    first_count = True if (update.callback_query.data == 'y') else False
    D.update_first_count(first_count)
    D.update_cur_num(1)
    countstring = str(D.max_count)
    #print(D)
    msg = "바로 시작하죠"
    target_num = (D.lose_num-1)-(D.max_count+1)*((D.lose_num-1)//(D.max_count+1))
    if (D.target_num == 0):
        target_num = target_num + D.max_count + 1
    D.update_target_num(target_num)
    if not first_count:
        #print(D)
        msg = "제가 먼저 숫자를 몇개 부를게요\n"
        msg += opturn(D)
        #print(D)
    keyboard = [
        [
            InlineKeyboardButton("시작!", callback_data=countstring),
        ]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    query.edit_message_text(msg, reply_markup=reply_markup)
    return MAIN0

def main2(update: Update, context: CallbackContext) -> int:
    #print("main2")
    query = update.callback_query
    query.answer()
    usrstr = "숫자를 얼마나 말할지 선택하세요\n{}을 먼저 말하면 패배합니다".format(D.lose_num)
    if (update.callback_query.data == '2'):
        D.update_max_count(2)
        msg = ''
    else:
        count = int(update.callback_query.data)
        cur_num = D.cur_num + count + 1
        D.update_cur_num(cur_num)
        if (D.cur_num == D.lose_num):
            keyboard = [
                [   InlineKeyboardButton('항복해!', callback_data='101')   ],
            ]
            reply_markup = InlineKeyboardMarkup(keyboard)
            usrstr = str(D.cur_num) + '!'
            query.edit_message_text(usrstr, reply_markup=reply_markup)
            return MAIN2
        if (D.target_num < D.cur_num):
            target_num = D.target_num + D.max_count + 1
            D.update_target_num(target_num)
        #print(D)
        msg = opturn(D)
        if (D.cur_num == D.lose_num):
            keyboard = [
                [   InlineKeyboardButton(str(D.cur_num), callback_data='100')   ],
            ]
            reply_markup = InlineKeyboardMarkup(keyboard)
            query.edit_message_text(msg+usrstr, reply_markup=reply_markup)
            return MAIN2
        
    str0 = str(D.cur_num)
    str1 = ', '.join([str(D.cur_num), str(D.cur_num+1)])
    
    #print(D)
    keyboard = [
        [   InlineKeyboardButton(str0, callback_data='0')   ],
        [   InlineKeyboardButton(str1, callback_data='1')   ],
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    query.edit_message_text(msg+usrstr, reply_markup=reply_markup)
    return MAIN2

def main3(update: Update, context: CallbackContext) -> int:
    #print("main3")
    query = update.callback_query
    query.answer()
    usrstr = "숫자를 얼마나 말할지 선택하세요\n{}을 먼저 말하면 패배합니다".format(D.lose_num)
    if (update.callback_query.data == '3'):
        D.update_max_count(3)
        msg = ''
    else:
        count = int(update.callback_query.data)
        cur_num = D.cur_num + count + 1
        D.update_cur_num(cur_num)
        if (D.cur_num == D.lose_num):
            keyboard = [
                [   InlineKeyboardButton('항복해!', callback_data='101')   ],
            ]
            reply_markup = InlineKeyboardMarkup(keyboard)
            usrstr = str(D.cur_num) + '!'
            query.edit_message_text(usrstr, reply_markup=reply_markup)
            return MAIN3
        if (D.target_num < D.cur_num):
            target_num = D.target_num + D.max_count + 1
            D.update_target_num(target_num)
        #print(D)
        msg = opturn(D)
        if (D.cur_num == D.lose_num):
            keyboard = [
                [   InlineKeyboardButton(str(D.cur_num), callback_data='100')   ],
            ]
            reply_markup = InlineKeyboardMarkup(keyboard)
            query.edit_message_text(msg+usrstr, reply_markup=reply_markup)
            return MAIN3
        
    str0 = str(D.cur_num)
    str1 = ', '.join([str(D.cur_num), str(D.cur_num+1)])
    str2 = ', '.join([str(D.cur_num), str(D.cur_num+1), str(D.cur_num+2)])
    
    #print(D)
    keyboard = [
        [   InlineKeyboardButton(str0, callback_data='0')   ],
        [   InlineKeyboardButton(str1, callback_data='1')   ],
        [   InlineKeyboardButton(str2, callback_data='2')   ],
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    query.edit_message_text(msg+usrstr, reply_markup=reply_markup)
    return MAIN3

def main4(update: Update, context: CallbackContext) -> int:
    #print("main4")
    query = update.callback_query
    query.answer()
    usrstr = "숫자를 얼마나 말할지 선택하세요\n{}을 먼저 말하면 패배합니다".format(D.lose_num)
    if (update.callback_query.data == '4'):
        D.update_max_count(4)
        msg = ''
    else:
        count = int(update.callback_query.data)
        cur_num = D.cur_num + count + 1
        D.update_cur_num(cur_num)
        if (D.cur_num == D.lose_num):
            keyboard = [
                [   InlineKeyboardButton('항복해!', callback_data='101')   ],
            ]
            reply_markup = InlineKeyboardMarkup(keyboard)
            usrstr = str(D.cur_num) + '!'
            query.edit_message_text(usrstr, reply_markup=reply_markup)
            return MAIN4
        if (D.target_num < D.cur_num):
            target_num = D.target_num + D.max_count + 1
            D.update_target_num(target_num)
        #print(D)
        msg = opturn(D)
        if (D.cur_num == D.lose_num):
            keyboard = [
                [   InlineKeyboardButton(str(D.cur_num), callback_data='100')   ],
            ]
            reply_markup = InlineKeyboardMarkup(keyboard)
            query.edit_message_text(msg+usrstr, reply_markup=reply_markup)
            return MAIN4
        
    str0 = str(D.cur_num)
    str1 = ', '.join([str(D.cur_num), str(D.cur_num+1)])
    str2 = ', '.join([str(D.cur_num), str(D.cur_num+1), str(D.cur_num+2)])
    str3 = ', '.join([str(D.cur_num), str(D.cur_num+1), str(D.cur_num+2), str(D.cur_num+3)])
    
    #print(D)
    keyboard = [
        [   InlineKeyboardButton(str0, callback_data='0')   ],
        [   InlineKeyboardButton(str1, callback_data='1')   ],
        [   InlineKeyboardButton(str2, callback_data='2')   ],
        [   InlineKeyboardButton(str3, callback_data='3')   ],
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    query.edit_message_text(msg+usrstr, reply_markup=reply_markup)
    return MAIN4

def main5(update: Update, context: CallbackContext) -> int:
    #print("main5")
    query = update.callback_query
    query.answer()
    usrstr = "숫자를 얼마나 말할지 선택하세요\n{}을 먼저 말하면 패배합니다".format(D.lose_num)
    if (update.callback_query.data == '5'):
        D.update_max_count(5)
        msg = ''
    else:
        count = int(update.callback_query.data)
        cur_num = D.cur_num + count + 1
        D.update_cur_num(cur_num)
        if (D.cur_num == D.lose_num):
            keyboard = [
                [   InlineKeyboardButton('항복해!', callback_data='101')   ],
            ]
            reply_markup = InlineKeyboardMarkup(keyboard)
            usrstr = str(D.cur_num) + '!'
            query.edit_message_text(usrstr, reply_markup=reply_markup)
            return MAIN5
        if (D.target_num < D.cur_num):
            target_num = D.target_num + D.max_count + 1
            D.update_target_num(target_num)
        #print(D)
        msg = opturn(D)
        if (D.cur_num == D.lose_num):
            keyboard = [
                [   InlineKeyboardButton(str(D.cur_num), callback_data='100')   ],
            ]
            reply_markup = InlineKeyboardMarkup(keyboard)
            query.edit_message_text(msg+usrstr, reply_markup=reply_markup)
            return MAIN5
        
    str0 = str(D.cur_num)
    str1 = ', '.join([str(D.cur_num), str(D.cur_num+1)])
    str2 = ', '.join([str(D.cur_num), str(D.cur_num+1), str(D.cur_num+2)])
    str3 = ', '.join([str(D.cur_num), str(D.cur_num+1), str(D.cur_num+2), str(D.cur_num+3)])
    str4 = ', '.join([str(D.cur_num), str(D.cur_num+1), str(D.cur_num+2), str(D.cur_num+3), str(D.cur_num+4)])
    
    #print(D)
    keyboard = [
        [   InlineKeyboardButton(str0, callback_data='0')   ],
        [   InlineKeyboardButton(str1, callback_data='1')   ],
        [   InlineKeyboardButton(str2, callback_data='2')   ],
        [   InlineKeyboardButton(str3, callback_data='3')   ],
        [   InlineKeyboardButton(str4, callback_data='4')   ],
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    query.edit_message_text(msg+usrstr, reply_markup=reply_markup)
    return MAIN5

def opwin(update: Update, context: CallbackContext) -> int:
    query = update.callback_query
    query.answer()
    query.edit_message_text(text="제가 이겼습니다!")
    return ConversationHandler.END

def playerwin(update: Update, context: CallbackContext) -> int:
    query = update.callback_query
    query.answer()
    query.edit_message_text(text="항복!! 플레이어가 이겼습니다!")
    return ConversationHandler.END

def main():
    updater = Updater(os.get_env('TOKEN'))

    dispatcher = updater.dispatcher
    conv_handler = ConversationHandler(
        entry_points=[CommandHandler('brgame', BR_command)],
        states={
            FIRST: [
                CallbackQueryHandler(second, pattern='^' + '31' + '$'),
                CallbackQueryHandler(second, pattern='^' + '41' + '$'),
                CallbackQueryHandler(second, pattern='^' + '51' + '$'),
                CallbackQueryHandler(second, pattern='^' + '21' + '$'),
            ],

            SECOND: [
                CallbackQueryHandler(third, pattern='^' + '3' + '$'),
                CallbackQueryHandler(third, pattern='^' + '4' + '$'),
                CallbackQueryHandler(third, pattern='^' + '5' + '$'),
                CallbackQueryHandler(third, pattern='^' + '2' + '$'),
            ],

            THIRD: [
                CallbackQueryHandler(main0, pattern='^' + 'y' + '$'),
                CallbackQueryHandler(main0, pattern='^' + 'n' + '$'),
            ],
            
            MAIN0: [
                CallbackQueryHandler(main2, pattern='^' + '2' + '$'),
                CallbackQueryHandler(main3, pattern='^' + '3' + '$'),
                CallbackQueryHandler(main4, pattern='^' + '4' + '$'),
                CallbackQueryHandler(main5, pattern='^' + '5' + '$'),
            ],
            
            MAIN2: [
                CallbackQueryHandler(main2, pattern='^' + '0' + '$'),
                CallbackQueryHandler(main2, pattern='^' + '1' + '$'),
                CallbackQueryHandler(opwin, pattern='^' + '100' + '$'),
                CallbackQueryHandler(playerwin, pattern='^' + '101' + '$'),
            ],
            
            MAIN3: [
                CallbackQueryHandler(main3, pattern='^' + '0' + '$'),
                CallbackQueryHandler(main3, pattern='^' + '1' + '$'),
                CallbackQueryHandler(main3, pattern='^' + '2' + '$'),
                CallbackQueryHandler(opwin, pattern='^' + '100' + '$'),
                CallbackQueryHandler(playerwin, pattern='^' + '101' + '$'),
            ],
            
            MAIN4: [
                CallbackQueryHandler(main4, pattern='^' + '0' + '$'),
                CallbackQueryHandler(main4, pattern='^' + '1' + '$'),
                CallbackQueryHandler(main4, pattern='^' + '2' + '$'),
                CallbackQueryHandler(main4, pattern='^' + '3' + '$'),
                CallbackQueryHandler(opwin, pattern='^' + '100' + '$'),
                CallbackQueryHandler(playerwin, pattern='^' + '101' + '$'),
            ],
            
            MAIN5: [
                CallbackQueryHandler(main5, pattern='^' + '0' + '$'),
                CallbackQueryHandler(main5, pattern='^' + '1' + '$'),
                CallbackQueryHandler(main5, pattern='^' + '2' + '$'),
                CallbackQueryHandler(main5, pattern='^' + '3' + '$'),
                CallbackQueryHandler(main5, pattern='^' + '4' + '$'),
                CallbackQueryHandler(opwin, pattern='^' + '100' + '$'),
                CallbackQueryHandler(playerwin, pattern='^' + '101' + '$'),
            ],
        },
        fallbacks=[CommandHandler('brgame', BR_command)],
)

    # Add ConversationHandler to dispatcher that will be used for handling updates
    dispatcher.add_handler(conv_handler)

    updater.start_polling()
    print('started')

    updater.idle()
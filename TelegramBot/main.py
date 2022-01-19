#from keepalive import keep_alive #for replit
from BRgame import FIRST, SECOND, THIRD, MAIN0, MAIN2, MAIN3, MAIN4, MAIN5, BR_command, second, third, main0, main2, main3, main4, main5, opwin, playerwin

import telegram
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup #upm package(python-telegram-bot)
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, CallbackContext, CallbackQueryHandler, ConversationHandler #upm package(python-telegram-bot)

token = '(your telegram bot token)'

#mybot = telegram.Bot(token = os.getenv("TOKEN")) #for replit
mybot = telegram.Bot(token=token)

def help_command(update: Update, context: CallbackContext) -> None:
    idx = update.message.chat.id
    if not (idx in chat_ids):
        update.message.reply_text("Blocked")
        return
    htext = '''
안녕하세요
.. 봇입니다

명령어 목록입니다
/help : 자기소개와 도움말을 보여줍니다
/brgame : 배스킨라빈스 미니게임을 합니다
'''
    update.message.reply_text(htext)


def main():
    #updater = Updater(os.getenv("TOKEN")) #for replit
    updater = Updater(token)

    dispatcher = updater.dispatcher
    dispatcher.add_handler(CommandHandler("start", help_command))
    dispatcher.add_handler(CommandHandler("help", help_command))
    

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

    dispatcher.add_handler(conv_handler)

    #keep_alive() #for replit

    updater.start_polling()

    updater.idle()

    


if __name__ == '__main__':
    main()

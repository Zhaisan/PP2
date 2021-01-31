from subprocess import Popen
from subprocess import PIPE

from telegram import Bot
from telegram import Update
from telegram.ext import Updater 
from telegram.ext import CommandHandler
from telegram.ext import MessageHandler
from telegram.ext import Filters

from echo.config import TG_TOKEN
#Обработчики событий от телеграма

def do_start(bot: Bot, update: Update):
    bot.send_message(
        chat_id=update.message.chat_id,
        text="Привет! Отправь мне что-нибудь",
    )

def do_help(bot: Bot, update: Update):
    bot.send_message(
        chat_id=update.message.chat_id,
        text="Это учебный бот\n\n"
            "Список доступных команд есть в меню\n\n"
            "Так же я отвечу на любое сообщение",
    )
def do_time(bot: Bot, update: Update):
    """ Узнать серверное время 
    """
    
    process = Popen(["date"], stdout=PIPE)  
    text, error = process.communicate() #подождать результат
    if error:
        text = "Произошла ошибка, время неизвестно"
    else:
        #Декодировать ответ команды из процесса
        text = text.decode("utf-8")
    bot.send_message(
        chat_id=update.message.chat_id,
        text=text,
    )
#Обрабатывать все входящие тексты

def do_echo(bot : Bot, update : Update):
    chat_id=update.message.chat_id
    text = "Ваш ID = {}\n{}".format(chat_id, update.message.text)
    bot.send_message(
        chat_id=chat_id,
        text=text,
    )

def main():
    bot = Bot(
        token=TG_TOKEN,
    )
    updater = Updater(
        bot=bot,
    )
    start_handler = CommandHandler("start", do_start)
    help_handler = CommandHandler("help", do_start)
    time_handler = CommandHandler("time", do_start)
    message_handler = MessageHandler(Filters.text, do_echo)


    updater.dispatcher.add_handler(start_handler)
    updater.dispatcher.add_handler(help_handler)
    updater.dispatcher.add_handler(time_handler)
    updater.dispatcher.add_handler(message_handler)
    
    

    updater.start_polling()
    updater.idle()

if __name__ == '__main__':
    main()


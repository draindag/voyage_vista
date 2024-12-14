import os

import telebot
from dotenv import load_dotenv
from flask import Flask, request

load_dotenv()

bot = telebot.TeleBot(os.getenv("SECRET_BOT_TOKEN"))


def create_webhook(app: Flask):
    @app.route('/webhook', methods=['POST'])
    def webhook():
        json_str = request.get_data().decode("UTF-8")
        update = telebot.types.Update.de_json(json_str)
        bot.process_new_updates([update])
        return '!', 200

    # Установка вебхука
    from threading import Thread

    def set_webhook():
        bot.remove_webhook()  # Удаляем предыдущий вебхук
        bot.set_webhook(url=f'{os.getenv("PUBLIC_URL")}/webhook')  # Установка нового

    Thread(target=set_webhook).start()  # Запускаем установку в отдельном потоке


@bot.message_handler(commands=["start", "help", "info"])
def command_help(message):
    info_string = "Вас приветствует бот уведомлений Voyage Vista!"
    bot.send_message(message.chat.id, info_string)


@bot.message_handler(commands=["commands"])
def command_commands(message):
    commands = ["/start", "/help", "/info", "/commands"]
    bot.send_message(message.chat.id, "\n".join(commands))

@bot.message_handler(func=lambda message: True)
def echo_all(message):
    bot.reply_to(message, message.text)

"""
Этот модуль отвечает за создание телеграм бота агенства по рассылке модераторам уведомлений о
вопросах посетителей: создание вебхука, определение команд, обработка сообщений, отправка уведомлений.
"""

import os

import requests
import telebot
from dotenv import load_dotenv
from flask import Flask, request

from webapp.models.TelegramAccount import TelegramAccount

load_dotenv()

bot = telebot.TeleBot(os.getenv("SECRET_BOT_TOKEN"))

api_access_key = os.getenv("SECRET_API_KEY")
api_url = os.getenv("PUBLIC_URL").rstrip('/')


def create_webhook(app: Flask):
    """
            Создание вебхука для работы телеграм бота
            ---
            """

    @app.route('/webhook', methods=['POST'])
    def webhook():
        json_str = request.get_data().decode("UTF-8")
        update = telebot.types.Update.de_json(json_str)
        bot.process_new_updates([update])
        return '!', 200

    from threading import Thread

    def set_webhook():
        bot.remove_webhook()
        bot.set_webhook(url=f'{os.getenv("PUBLIC_URL")}/webhook')

    Thread(target=set_webhook).start()


def get_request_api(endpoint: str, params=None) -> dict:
    """
            Функция для внутренней логики телеграм бота, отправки GET запроса
            ---
            """

    url = f"{api_url}/{endpoint.lstrip('/')}"
    if params is None:
        params = {}
    params = {'secret_key': api_access_key, **params}
    result = requests.get(url, params=params)
    return result.json()


def post_request_api(endpoint: str, data=None) -> dict:
    """
                Функция для внутренней логики телеграм бота, отправки POST запроса
                ---
                """

    url = f"{api_url}/{endpoint.lstrip('/')}"
    if data is None:
        data = {}
    params = {'secret_key': api_access_key}
    result = requests.post(url, params=params, json=data)
    return result.json()

def delete_request_api(endpoint: str, params=None) -> dict:
    """
                Функция для внутренней логики телеграм бота, отправки DELETE запроса
                ---
                """

    url = f"{api_url}/{endpoint.lstrip('/')}"
    if params is None:
        params = {}
    params = {'secret_key': api_access_key, **params}
    result = requests.delete(url, params=params)
    return result.json()


def is_account_connected(user_id: int):
    """
            Функция проверки - зарегистрирован ли уже этот телеграм аккаунт или ещё нет
            ---
            """

    response = get_request_api(f"/telegram-account/{user_id}")
    return response["success"] and response["connected"]


def send_notification(username, category, tour, question_text):
    """
            Функция рассылки уведомлений модераторам о новом вопросе от посетителя сайта
            ---
            """

    all_moderators_accounts = TelegramAccount.query.all()
    for account in all_moderators_accounts:
        bot.send_message(account.telegram_user_id,
                         f"Пользователь {username} задал вопрос '{question_text}' "
                         f"на странице тура '{tour}' в категории '{category}'\n\n<b>Ответьте ему как можно скорее!</b>",
                         parse_mode="html")


@bot.message_handler(commands=["commands"])
def command_commands(message):
    """
            Команда бота по выводу всех команд
            ---
            """

    commands = ["/start", "/delete", "/commands"]
    bot.send_message(message.chat.id, "\n".join(commands))


@bot.message_handler(commands=["start"])
def command_start(message):
    """
            Команда бота по ответу на команду /start
            ---
            """

    info_string = "Вас приветствует бот уведомлений Voyage Vista!"
    if is_account_connected(message.chat.id):
        status_line = "Ваш аккаунт подключён к для отправки уведомлений"
    else:
        status_line = "Ваш аккаунт не подключён для отправки уведомлений. Введите ваш email и код с сайта для подключения"
    lines = [info_string, status_line]
    bot.send_message(message.chat.id, "\n\n".join(lines))


@bot.message_handler(commands=["delete"])
def command_delete(message):
    """
            Команда бота по ответу на команду /delete - отвязка аккаунта от рассылки
            ---
            """

    if is_account_connected(message.chat.id):
        response = delete_request_api(f"/telegram-account/{message.chat.id}")
        bot.send_message(message.chat.id, response["message"])
    else:
        bot.send_message(message.chat.id, "Ваш аккаунт не подключён для отправки уведомлений")


@bot.message_handler()
def handle_message(message):
    """
            Команда бота по ответу на любое сообщение от пользователя -
            обработка возможного запроса на подключение рассылки
            ---
            """

    if is_account_connected(message.chat.id):
        bot.reply_to(message, "Вы уже подключили аккаунт. Ожидайте уведомлений")
        return
    lines = message.text.strip().split('\n')
    if len(lines) != 2:
        bot.reply_to(message, "Введите email и код со страницы профиля в формате:\n\n<email>\n<код>, "
                              "\n\nнапример:\nuser@example.com\n12345678")
        return
    email, verification_code = lines
    data = {
        "user_email": email,
        "verification_code": verification_code
    }
    response = post_request_api(f"/telegram-account/{message.chat.id}", data=data)
    if response["success"]:
        bot.reply_to(message, "Аккаунт успешно подключён! Ожидайте уведомлений")
    elif response["message"] in {"Пользователь не найден", "Неверный код верификации"}:
        bot.reply_to(message, "Email или код неверны. Проверьте данные и попробуйте ещё раз")
    elif response["message"] == "У пользователя уже есть привязанный аккаунт":
        bot.reply_to(message, "Уведомления уже настроены для другого аккаунта Telegram. Отключите их и попробуйте ещё раз")
    else:
        bot.reply_to(message, "Что-то пошло не так... Проверьте данные и попробуйте ещё раз")
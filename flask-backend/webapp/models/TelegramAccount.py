"""
Этот модуль определяет модель TelegramAccount для работы с телеграм аккаунтами.

Таблица связывает идентификаторы телеграм аккаунта и  профиль модератора на сайте.
"""

from webapp import db
from sqlalchemy.dialects.postgresql import UUID


class TelegramAccount(db.Model):
    __tablename__ = 'telegram_accounts'

    telegram_user_id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(UUID(as_uuid=True), db.ForeignKey('users.user_id'), primary_key=True)

    def __repr__(self):
        return f'<TelegramAccount(telegram_user_id={self.telegram_user_id}, user_id={self.user_id})>'

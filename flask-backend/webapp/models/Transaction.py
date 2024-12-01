"""
Этот модуль определяет ассоциативную таблицу transactions для хранения
информации о покупках туров пользователями.

Таблица связывает идентификаторы туров и пользователей, что позволяет
отслеживать совершенные транзакции.
"""

from webapp import db
from sqlalchemy.dialects.postgresql import UUID


transactions = db.Table('transactions',
    db.Column('tour_id', UUID(as_uuid=True), db.ForeignKey('tours.tour_id'), primary_key=True),
    db.Column('user_id', UUID(as_uuid=True), db.ForeignKey('users.user_id'), primary_key=True)
)

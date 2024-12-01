"""
Этот модуль определяет ассоциативную таблицу fav_tours для хранения
избранных туров пользователей.

Таблица связывает идентификаторы туров и пользователей, позволяя
реализовать функционал избранного в личном кабинете
"""

from webapp import db
from sqlalchemy.dialects.postgresql import UUID


fav_tours = db.Table('fav_tours',
    db.Column('tour_id', UUID(as_uuid=True), db.ForeignKey('tours.tour_id', ondelete='CASCADE'), primary_key=True),
    db.Column('user_id', UUID(as_uuid=True), db.ForeignKey('users.user_id', ondelete='CASCADE'), primary_key=True)
)

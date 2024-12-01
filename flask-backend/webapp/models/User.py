"""
Этот модуль определяет модель User для работы с пользователями веб-сайта.

Здесь описаны атрибуты пользователя, его роли и связи с отзывами,
ответами, избранными турами и транзакциями. Реализованы функции
для работы с паролями и изменения личных данных.
"""

import uuid

from sqlalchemy import CheckConstraint
from werkzeug.security import check_password_hash, generate_password_hash

from webapp import db
from sqlalchemy.dialects.postgresql import UUID
from webapp.models.Reply import Reply
from webapp.models.Review import Review
from webapp.models.FavTour import fav_tours
from webapp.models.Transaction import transactions


class User(db.Model):
    __tablename__ = 'users'

    user_id = db.Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    login = db.Column(db.String(30), index=True, unique=True, nullable=False)
    email = db.Column(db.Text, index=True, unique=True, nullable=False)
    password = db.Column(db.Text, nullable=False)
    role = db.Column(db.String(10), nullable=False, default="visitor")

    replies = db.relationship('Reply', backref='author', lazy='dynamic', cascade='all, delete-orphan')
    reviews = db.relationship('Review', backref='author', lazy='dynamic', cascade='all, delete-orphan')

    fav_tours = db.relationship('Tour', secondary=fav_tours, backref='favoured_by', lazy='dynamic')
    transactions = db.relationship('Tour', secondary=transactions, backref='paid_by', lazy='dynamic')

    __table_args__ = (
        CheckConstraint("role IN ('visitor', 'moderator', 'admin')", name="users_role_check"),
    )

    def get_id(self):
        return self.user_id

    def set_password(self, password):
        self.password = generate_password_hash(password)

    def set_email(self, new_email):
        self.email = new_email

    def set_login(self, new_login):
        self.login = new_login

    def check_password(self, password: str) -> bool:
        return check_password_hash(self.password, password)

    def set_moderator_role(self):
        self.role = "moderator"

    def __repr__(self):
        return '<User {}>'.format(self.login)

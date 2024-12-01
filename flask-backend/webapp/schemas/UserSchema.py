"""
Этот модуль определяет схемы сериализации и десериализации
для пользовательской информации с помощью библиотеки Marshmallow.

Схема UserSchema описывает поля данных пользователя для их сериализации
"""

from marshmallow import fields, post_load

from webapp import ma
from webapp.models.User import User


class UserSchema(ma.Schema):
    login = fields.String(required=True, error_messages={"required": "Поле 'Логин' обязательно для заполнения"})
    email = fields.Email(required=True, error_messages={"required": "Поле 'Email' обязательно для заполнения"})
    fav_tours = fields.Nested("TourSchema", dump_only=True, many=True, exclude=("tour_text",))
    transactions = fields.Nested("TourSchema", dump_only=True, many=True,
                                 exclude=("offers","tour_text", "tour_image"))

    @post_load
    def create_user(self, data, **kwargs):
        return User(**data)

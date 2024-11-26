from marshmallow import fields, post_load

from webapp import ma
from webapp.models.User import User


class UserSchema(ma.Schema):
    user_id = fields.UUID(dump_only=True)
    login = fields.String(required=True, error_messages={"required": "Поле 'Логин' обязательно для заполнения"})
    email = fields.Email(required=True, error_messages={"required": "Поле 'Email' обязательно для заполнения"})
    password = fields.String(required=True, error_messages={"required": "Поле 'Пароль' обязательно для заполнения"})
    role = fields.String()

    @post_load
    def create_review(self, data, **kwargs):
        return User(**data)

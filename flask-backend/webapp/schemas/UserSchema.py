from marshmallow import fields

from webapp import ma


class UserSchema(ma.Schema):
    user_id = fields.UUID(dump_only=True)
    login = fields.String(required=True, error_messages={"required": "Поле 'Логин' обязательно для заполнения"})
    email = fields.Email(required=True, error_messages={"required": "Поле 'Email' обязательно для заполнения"})
    password = fields.String(required=True, error_messages={"required": "Поле 'Пароль' обязательно для заполнения"})
    role = fields.String()

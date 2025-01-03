"""
Этот модуль определяет схемы валидации для формы входа в аккаунт
с помощью библиотеки Marshmallow.

Схема LoginSchema описывает поля формы, включая их валидацию
и обработку ошибок при неправильном вводе.
"""

from marshmallow import fields, validates, ValidationError

from webapp import ma


class LoginSchema(ma.Schema):
    email = fields.Email(required=True,
                         error_messages={"required": "Поле 'Email' обязательно для заполнения",
                                         "invalid": "Некорректный адрес электронной почты"})
    password = fields.String(required=True,
                             error_messages={"required": "Поле 'Пароль' обязательно для заполнения"})


    @validates('password')
    def validate_password(self, value):
        if not value.strip():
            raise ValidationError("Пароль не может быть пустым")

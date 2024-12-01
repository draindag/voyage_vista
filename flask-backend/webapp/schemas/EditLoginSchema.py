"""
Этот модуль определяет схемы валидации для формы изменения логина
с помощью библиотеки Marshmallow.

Схема EditLoginSchema описывает поля формы, включая их валидацию
и обработку ошибок при неправильном вводе.
"""

from marshmallow import fields, ValidationError, validates

from webapp import ma


class EditLoginSchema(ma.Schema):
    new_login = fields.String(required=True,
                              error_messages={"required": "Поле 'Логин' обязательно для заполнения"})
    password = fields.String(required=True,
                             error_messages={"required": "Поле 'Пароль' обязательно для заполнения"})

    @validates('new_login')
    def validate_login(self, value):
        if not value.strip():
            raise ValidationError("Поле 'Логин' не должно быть пустым")
        if len(value) > 30:
            raise ValidationError("Поле 'Логин' должно содержать не более 30 символов")

    @validates('password')
    def validate_password(self, value):
        if not value.strip():
            raise ValidationError("Пароль не может быть пустым")

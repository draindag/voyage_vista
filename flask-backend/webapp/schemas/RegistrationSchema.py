from marshmallow import fields, validates, ValidationError, validates_schema

from webapp import ma


class RegistrationSchema(ma.Schema):
    login = fields.String(required=True,
                                   error_messages={"required": "Поле 'Логин' обязательно для заполнения"})
    email = fields.Email(required=True,
                                   error_messages={"required": "Поле 'Email' обязательно для заполнения",
                                                   "invalid": "Некорректный адрес электронной почты"})
    password = fields.String(required=True,
                                   error_messages={"required": "Поле 'Пароль' обязательно для заполнения"})
    password_repeat = fields.String(required=True,
                                   error_messages={"required": "Поле 'Повторите пароль' обязательно для заполнения"})

    @validates('login')
    def validate_login(self, value):
        if not value.strip():
            raise ValidationError("Поле 'Логин' не должно быть пустым")
        if len(value) > 30:
            raise ValidationError("Поле 'Логин' должно содержать не более 30 символов")


    @validates('password')
    def validate_password(self, value):
        if not value.strip():
            raise ValidationError("Пароль не может быть пустым")


    @validates_schema
    def validate_password_repeat(self, data, **kwargs):
        if data["password_repeat"] != data["password"]:
            raise ValidationError("Пароли должны совпадать!")

"""
Этот модуль определяет схемы сериализации,десериализации и
валидации для туров с помощью библиотеки Marshmallow.

Схема TourSchema описывает поля тура, включая их валидацию
и обработку ошибок при неправильном вводе.
"""

from decimal import Decimal

from marshmallow import fields, validates, ValidationError, post_load, validates_schema

from webapp import ma
from webapp.models.Tour import Tour


class TourSchema(ma.Schema):
    tour_id = fields.UUID(dump_only=True)
    tour_title = fields.String(required=True, error_messages={"required": "Название тура обязательно для заполнения",
                                                              "null": "Название тура обязательно для заполнения"})
    tour_description = fields.String(required=True,
                                     error_messages={"required": "Описание тура обязательно для заполнения",
                                                     "null": "Описание тура обязательно для заполнения"})
    tour_text = fields.String(required=True, error_messages={"required": "Текст тура обязателен для заполнения",
                                                             "null": "Текст тура обязателен для заполнения"})
    tour_price = fields.Decimal(required=True, error_messages={"required": "Цена тура обязательна для заполнения",
                                                               "invalid": "Цена тура должна быть корректным числом",
                                                               "null": "Цена тура обязательна для заполнения"})
    tour_start_date = fields.Date(required=True,
                                  error_messages={"required": "Дата начала тура обязательна для заполнения",
                                                  "invalid": "Даты тура должны быть корректными",
                                                  "null": "Дата начала тура обязательна для заполнения"})
    tour_end_date = fields.Date(required=True,
                                error_messages={"required": "Дата окончания тура обязательна для заполнения",
                                                "invalid": "Даты тура должны быть корректными",
                                                "null": "Дата окончания тура обязательна для заполнения"})
    category_id = fields.UUID(required=True, load_only=True,
                                error_messages={"required": "Категория тура обязательна для указания",
                                                "invalid": "ID должен быть корректным UUID",
                                                "null": "Категория тура обязательна для указания"})
    country_id = fields.UUID(required=True, load_only=True,
                                error_messages={"required": "Страна тура обязательна для указания",
                                                "invalid": "ID должен быть корректным UUID",
                                                "null": "Страна тура обязательна для указания"})

    category = fields.Nested("CategorySchema", dump_only=True, exclude=("category_image",))
    country = fields.Nested("CountrySchema", dump_only=True, exclude=("country_image",))
    offers = fields.Nested("OfferSchema", dump_only=True, many=True)

    tour_image = fields.String(dump_only=True)
    price_with_discount = fields.Function(lambda tour: tour.get_price_with_discount(), dump_only=True)

    @validates('tour_title')
    def validate_title(self, value):
        if not value.strip():
            raise ValidationError("Название тура не должно быть пустым")
        if len(value) > 40:
            raise ValidationError("Название тура должно содержать не более 40 символов")

    @validates('tour_description')
    def validate_description(self, value):
        if not value.strip():
            raise ValidationError("Описание тура не должно быть пустым")
        if len(value) > 50:
            raise ValidationError("Описание тура должно содержать не более 50 символов")

    @validates('tour_text')
    def validate_text(self, value):
        if not value.strip():
            raise ValidationError("Текст тура не должен быть пустым")

    @validates('tour_price')
    def validate_price(self, value):
        if value is None:
            raise ValidationError("Цена тура не должна быть пустой")
        if not isinstance(value, (Decimal, float)) or value <= 0:
            raise ValidationError("Цена тура должна быть положительным числом")

    @validates('tour_start_date')
    def validate_start_date(self, value):
        if value is None:
            raise ValidationError("Дата начала тура не должна быть пустой")

    @validates('tour_end_date')
    def validate_end_date(self, value):
        if value is None:
            raise ValidationError("Дата окончания тура не должна быть пустой")

    @validates_schema
    def validate_dates(self, data, **kwargs):
        if data["tour_end_date"] < data["tour_start_date"]:
            raise ValidationError("Дата окончания тура не может быть ранее даты начала тура!")

    @post_load
    def create_tour(self, data, **kwargs):
        return Tour(**data)

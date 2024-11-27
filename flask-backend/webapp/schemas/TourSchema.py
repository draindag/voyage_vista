from decimal import Decimal

from marshmallow import fields, validates, ValidationError, post_load

from webapp import ma
from webapp.models.Tour import Tour


class TourSchema(ma.Schema):
    tour_id = fields.UUID(dump_only=True)
    tour_title = fields.String(required=True, error_messages={"required": "Название тура обязательно для заполнения"})
    tour_description = fields.String(required=True,
                                     error_messages={"required": "Описание тура обязательно для заполнения"})
    tour_text = fields.String(required=True, error_messages={"required": "Текст тура обязателен для заполнения"})
    tour_price = fields.Decimal(required=True, error_messages={"required": "Цена тура обязательна для заполнения",
                                                               "invalid": "Цена тура должна быть корректным числом"})
    tour_start_date = fields.Date(required=True,
                                  error_messages={"required": "Дата начала тура обязательна для заполнения",
                                                  "invalid": "Даты тура должны быть корректными"})
    tour_end_date = fields.Date(required=True,
                                error_messages={"required": "Дата окончания тура обязательна для заполнения",
                                                "invalid": "Даты тура должны быть корректными"})
    category_id = fields.UUID(required=True, load_only=True,
                                error_messages={"required": "Категория тура обязательна для указания",
                                                "invalid": "ID должен быть корректным UUID"})
    country_id = fields.UUID(required=True, load_only=True,
                                error_messages={"required": "Страна тура обязательна для указания",
                                                "invalid": "ID должен быть корректным UUID"})

    category = fields.Nested("CategorySchema", dump_only=True)
    country = fields.Nested("CountrySchema", dump_only=True)
    offers = fields.Nested("OfferSchema", dump_only=True, many=True)
    tour_replies = fields.Nested("ReplySchema", dump_only=True, many=True)

    rating = fields.Function(lambda tour: tour.get_rating(), dump_only=True)
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

    @post_load
    def create_tour(self, data, **kwargs):
        return Tour(**data)

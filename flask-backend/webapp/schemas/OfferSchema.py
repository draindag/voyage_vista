from marshmallow import fields, validates, ValidationError, post_load

from webapp import ma
from webapp.models.SpecialOffer import SpecialOffer


class OfferSchema(ma.Schema):
    offer_id = fields.UUID(dump_only=True)
    offer_title = fields.String(required=True,
                                   error_messages={"required": "Название категории обязательно для заполнения"})
    discount_size = fields.Float(required=True,
                                         error_messages={"required": "Описание категории обязательно для заполнения",
                                                         "invalid": "Размер скидки должен быть корректным числом"})
    end_date = fields.Date(required=True,
                                error_messages={"required": "Дата окончания скидки обязательна для заполнения",
                                                "invalid": "Дата окончания должна быть корректной"})

    @validates('offer_title')
    def validate_title(self, value):
        if not value.strip():
            raise ValidationError("Название скидки не должно быть пустым")
        if len(value) > 50:
            raise ValidationError("Название скидки должно содержать не более 50 символов")

    @validates('end_date')
    def validate_end_date(self, value):
        if value is None:
            raise ValidationError("Дата окончания скидки не должна быть пустой")

    @post_load
    def create_special_offer(self, data, **kwargs):
        return SpecialOffer(**data)
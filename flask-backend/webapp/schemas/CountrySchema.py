from marshmallow import fields, validates, ValidationError, post_load

from webapp import ma
from webapp.models.Country import Country


class CountrySchema(ma.Schema):
    country_id = fields.UUID(dump_only=True)
    country_name = fields.String(required=True,
                                   error_messages={"required": "Название страны обязательно для заполнения"})
    country_description = fields.String(required=True,
                                         error_messages={"required": "Описание страны обязательно для заполнения"})

    @validates('country_name')
    def validate_name(self, value):
        if not value.strip():
            raise ValidationError("Название страны не должно быть пустым")
        if len(value) > 30:
            raise ValidationError("Название страны должно содержать не более 30 символов")

    @validates('country_description')
    def validate_description(self, value):
        if not value.strip():
            raise ValidationError("Описание страны не должно быть пустым")

    @post_load
    def create_country(self, data, **kwargs):
        return Country(**data)
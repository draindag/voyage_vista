from marshmallow import fields, validates, ValidationError, post_load

from webapp import ma
from webapp.models.Country import Country


class CountrySchema(ma.Schema):
    country_id = fields.UUID(dump_only=True)
    country_name = fields.String(required=True)
    country_description = fields.String(required=True)

    @validates('country_name')
    def validate_name(self, value):
        if len(value) > 30:
            raise ValidationError("Название страны должно содержать не более 30 символов")

    @post_load
    def create_category(self, data, **kwargs):
        return Country(**data)
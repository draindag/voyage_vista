from marshmallow import fields, validates, ValidationError, post_load

from webapp import ma
from webapp.models.Tour import Tour
from webapp.schemas.CategorySchema import CategorySchema
from webapp.schemas.CountrySchema import CountrySchema


class TourSchema(ma.Schema):
    tour_id = fields.UUID(dump_only=True)
    tour_title = fields.String(required=True)
    tour_description = fields.String(required=True)
    tour_text = fields.String(required=True)
    tour_price = fields.Decimal(required=True)
    tour_start_date = fields.Date(required=True)
    tour_end_date = fields.Date(required=True)
    category_id = fields.UUID(required=True, load_only=True)
    country_id = fields.UUID(required=True, load_only=True)
    category = fields.Nested("CategorySchema", dump_only=True)
    country = fields.Nested("CountrySchema", dump_only=True)
    rating = fields.Function(lambda tour: tour.get_rating(), dump_only=True)

    @validates('tour_title')
    def validate_title(self, value):
        if len(value) > 40:
            raise ValidationError("Название тура должно содержать не более 40 символов")

    @validates('tour_description')
    def validate_description(self, value):
        if len(value) > 50:
            raise ValidationError("Описание тура должно содержать не более 50 символов")

    @post_load
    def create_category(self, data, **kwargs):
        return Tour(**data)

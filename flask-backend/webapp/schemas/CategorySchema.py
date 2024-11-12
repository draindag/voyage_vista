from marshmallow import fields, validates, ValidationError, post_load

from webapp import ma
from webapp.models.Category import Category


class CategorySchema(ma.Schema):
    category_id = fields.UUID(dump_only=True)
    category_title = fields.String(required=True)
    category_description = fields.String(required=True)

    @validates('category_title')
    def validate_title(self, value):
        if len(value) > 30:
            raise ValidationError("Название категории должно содержать не более 30 символов")

    @post_load
    def create_category(self, data, **kwargs):
        return Category(**data)
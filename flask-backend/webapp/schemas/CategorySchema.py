from marshmallow import fields, validates, ValidationError, post_load

from webapp import ma
from webapp.models.Category import Category


class CategorySchema(ma.Schema):
    category_id = fields.UUID(dump_only=True)
    category_title = fields.String(required=True,
                                   error_messages={"required": "Название категории обязательно для заполнения"})
    category_description = fields.String(required=True,
                                         error_messages={"required": "Описание категории обязательно для заполнения"})

    @validates('category_title')
    def validate_title(self, value):
        if not value.strip():
            raise ValidationError("Название категории не должно быть пустым")
        if len(value) > 30:
            raise ValidationError("Название категории должно содержать не более 30 символов")

    @validates('category_description')
    def validate_description(self, value):
        if not value.strip():
            raise ValidationError("Описание категории не должно быть пустым")

    @post_load
    def create_category(self, data, **kwargs):
        return Category(**data)
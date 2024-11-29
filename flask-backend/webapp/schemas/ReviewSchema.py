from marshmallow import fields, validates, ValidationError, post_load

from webapp import ma
from webapp.models.Review import Review


class ReviewSchema(ma.Schema):
    review_id = fields.UUID(dump_only=True)
    review_text = fields.String(required=True,
                                   error_messages={"required": "Текст отзыва обязателен для заполнения"})
    review_value = fields.Float(required=True,
                                         error_messages={"required": "Оценка тура обязательна для заполнения",
                                                         "invalid": "Оценка тура должна быть корректным целым числом"})
    author_id = fields.UUID(required=True, load_only=True,
                                error_messages={"required": "Автор отзыва обязателен для указания",
                                                "invalid": "ID должен быть корректным UUID"})
    tour_id = fields.UUID(required=True, load_only=True,
                                error_messages={"required": "Тур отзыва обязателен для указания",
                                                "invalid": "ID должен быть корректным UUID"})

    author = fields.Nested("UserSchema", dump_only=True, exclude=("fav_tours","transactions"))
    tour = fields.Nested("TourSchema", dump_only=True, exclude=("offers","tour_text", "tour_image"))

    @validates('review_text')
    def validate_text(self, value):
        if not value.strip():
            raise ValidationError("Текст отзыва не должен быть пустым")

    @validates('review_value')
    def validate_review_value(self, value):
        if not (isinstance(value, float) and value.is_integer() and 1 <= value <= 5):
            raise ValidationError("Оценка должна быть целым числом в диапазоне от 1 до 5!")

    @post_load
    def create_review(self, data, **kwargs):
        return Review(**data)
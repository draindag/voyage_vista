from marshmallow import fields, post_load

from webapp import ma
from webapp.models.User import User


class UserSchema(ma.Schema):
    login = fields.String(required=True, error_messages={"required": "Поле 'Логин' обязательно для заполнения"})
    email = fields.Email(required=True, error_messages={"required": "Поле 'Email' обязательно для заполнения"})
    fav_tours = fields.Nested("TourSchema", dump_only=True, many=True,
                              exclude=("tour_replies","tour_text"))
    transactions = fields.Nested("TourSchema", dump_only=True, many=True,
                                 exclude=("tour_replies","offers","tour_text"))

    @post_load
    def create_review(self, data, **kwargs):
        return User(**data)

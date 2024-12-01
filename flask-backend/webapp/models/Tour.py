"""
Этот модуль определяет модель Tour для работы с турами.

Здесь описаны атрибуты тура, его отношения с отзывами,
ответами и специальными предложениями, а также методы
для получения изображения тура и расчета цены со скидкой.
"""

import os
import uuid
from decimal import Decimal, ROUND_HALF_UP

from sqlalchemy import Date, UniqueConstraint

from webapp import db
from sqlalchemy.dialects.postgresql import UUID, NUMERIC
from webapp.models.SpecialOffer import SpecialOffer
from webapp.models.Reply import Reply
from webapp.models.Review import Review
from webapp.models.FavTour import fav_tours
from webapp.models.OffersAndTours import offers_tours

upload_folder = os.getenv("UPLOADED_PHOTOS_DEST")
file_ext = os.getenv("COVER_IMAGES_EXT")


class Tour(db.Model):
    __tablename__ = 'tours'

    tour_id = db.Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    tour_title = db.Column(db.String(40), nullable=False)
    tour_description = db.Column(db.String(50), nullable=False)
    tour_text = db.Column(db.Text, nullable=False)
    tour_price = db.Column(NUMERIC(10, 2), index=True, nullable=False)
    tour_start_date = db.Column(Date, index=True, nullable=False)
    tour_end_date = db.Column(Date, index=True, nullable=False)
    category_id = db.Column(UUID(as_uuid=True), db.ForeignKey('categories.category_id'), nullable=False)
    country_id = db.Column(UUID(as_uuid=True), db.ForeignKey('countries.country_id'), nullable=False)

    replies  = db.relationship('Reply', backref='tour', lazy='dynamic', cascade='all, delete-orphan')
    reviews = db.relationship('Review', backref='tour', lazy='dynamic', cascade='all, delete-orphan')

    offers = db.relationship('SpecialOffer', secondary=offers_tours, backref='offer_on', lazy='dynamic')

    __table_args__ = (
        UniqueConstraint('tour_title', 'category_id', name='uq_tour_title_category_id'),
    )

    @property
    def tour_replies(self):
        return self.replies.filter(Reply.parent_reply_id.is_(None))

    @property
    def tour_image(self):
        return f"{upload_folder}{self.tour_id}{file_ext}"

    def __repr__(self):
        return f"<Tour(title={self.tour_title}, price={self.tour_price})>"

    def get_price_with_discount(self):
        offer = self.offers.first()
        if offer:
            price_with_discount = self.tour_price * Decimal((100 - offer.discount_size)/100)
            return price_with_discount.quantize(Decimal('0.00'), rounding=ROUND_HALF_UP)
        return None

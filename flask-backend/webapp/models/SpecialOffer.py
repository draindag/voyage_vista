"""
Этот модуль определяет модель SpecialOffer для работы со специальными предложениями на туры.

Модель включает атрибуты для идентификатора акции, названия, размера скидки
и даты окончания акции.
"""

import uuid

from sqlalchemy import Date

from webapp import db
from sqlalchemy.dialects.postgresql import UUID


class SpecialOffer(db.Model):
    __tablename__ = 'special_offers'

    offer_id = db.Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    offer_title = db.Column(db.String(50),  nullable=False)
    discount_size = db.Column(db.Float, nullable=False, default=None)
    end_date = db.Column(Date, nullable=False)

    def __repr__(self):
        return f"<Special offer(title={self.offer_title}, discount={self.discount_size})>"

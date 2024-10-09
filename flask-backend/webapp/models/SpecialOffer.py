from sqlalchemy import Date

from webapp import db
from sqlalchemy.dialects.postgresql import UUID


class SpecialOffer(db.Model):
    __tablename__ = 'special_offers'

    offer_id = db.Column(UUID(as_uuid=True), primary_key=True)
    offer_title = db.Column(db.String(50),  nullable=False)
    discount_size = db.Column(db.Integer, nullable=False, default=None)
    end_date = db.Column(Date, nullable=False)
    tour_id = db.Column(UUID(as_uuid=True), db.ForeignKey('tours.tour_id'), nullable=False)

    def __repr__(self):
        return f"<Special offer(title={self.offer_title}, discount={self.discount_size})>"

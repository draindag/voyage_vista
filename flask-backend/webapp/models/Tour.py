import uuid
from sqlalchemy import Date, UniqueConstraint

from webapp import db
from sqlalchemy.dialects.postgresql import UUID, NUMERIC
from webapp.models.SpecialOffer import SpecialOffer
from webapp.models.FavTour import FavTour


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
    offers = db.relationship('SpecialOffer', backref='tour', lazy='dynamic')
    users = db.relationship('FavTour', backref='tour', lazy='dynamic')
    reviews = db.relationship('Review', backref='tour', lazy='dynamic')

    __table_args__ = (
        UniqueConstraint('tour_title', 'category_id', name='uq_tour_title_category_id'),
    )

    def __repr__(self):
        return f"<Tour(title={self.tour_title}, price={self.tour_price})>"


    def get_rating(self):
        all_reviews = [review.review_value for review in self.reviews]
        rating = sum(all_reviews) / len(all_reviews) if len(all_reviews) != 0 else 0
        return rating

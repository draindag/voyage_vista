from sqlalchemy import Date

from webapp import db
from sqlalchemy.dialects.postgresql import UUID, MONEY
from webapp.models.SpecialOffer import SpecialOffer
from webapp.models.FavTour import FavTour


class Tour(db.Model):
    __tablename__ = 'tours'

    tour_id = db.Column(UUID(as_uuid=True), primary_key=True)
    tour_title = db.Column(db.String(40), unique=True, nullable=False)
    tour_description = db.Column(db.String(50), nullable=False)
    tour_text = db.Column(db.Text, nullable=False)
    tour_price = db.Column(MONEY, index=True, nullable=False)
    tour_start_date = db.Column(Date, index=True, nullable=False)
    tour_end_date = db.Column(Date, index=True, nullable=False)
    category_id = db.Column(UUID(as_uuid=True), db.ForeignKey('categories.category_id'), nullable=False)
    country_id = db.Column(UUID(as_uuid=True), db.ForeignKey('countries.country_id'), nullable=False)
    offers = db.relationship('SpecialOffer', backref='tour', lazy='dynamic')
    users = db.relationship('FavTour', backref='tour', lazy='dynamic')
    reviews = db.relationship('Review', backref='tour', lazy='dynamic')

    def __repr__(self):
        return f"<Tour(title={self.tour_title}, price={self.tour_price})>"

    def to_dict(self):
        return {
            'tour_id': str(self.tour_id),
            'tour_title': self.tour_title,
            'tour_description': self.tour_description,
            'tour_text': self.tour_text,
            'tour_price': self.tour_price,
            'tour_start_date': self.tour_start_date.isoformat(),
            'tour_end_date': self.tour_end_date.isoformat(),
        }

    def get_rating(self):
        all_reviews = [review.review_value for review in self.reviews]
        rating = sum(all_reviews) / len(all_reviews) if len(all_reviews) != 0 else 0
        return rating

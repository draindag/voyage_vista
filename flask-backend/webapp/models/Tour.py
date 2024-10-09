from sqlalchemy import Date

from webapp import db
from sqlalchemy.dialects.postgresql import UUID, MONEY


class Tour(db.Model):
    __tablename__ = 'tours'

    tour_id = db.Column(UUID(as_uuid=True), primary_key=True)
    tour_title = db.Column(db.String(40), unique=True, nullable=False)
    tour_description = db.Column(db.String(50), nullable=False)
    tour_text = db.Column(db.Text, nullable=False)
    tour_price = db.Column(MONEY, index=True, nullable=False)
    tour_start_date = db.Column(Date, index=True, nullable=False)
    tour_end_date = db.Column(Date, index=True, nullable=False)
    country_id = db.Column(UUID(as_uuid=True), db.ForeignKey('countries.country_id'), nullable=False)
    offers = db.relationship('SpecialOffer', backref='tour', lazy='dynamic')
    users = db.relationship('FavTour', backref='tour', lazy='dynamic')
    reviews = db.relationship('Review', backref='tour', lazy='dynamic')

    def __repr__(self):
        return f"<Tour(title={self.tour_title}, price={self.tour_price})>"

from webapp import db
from sqlalchemy.dialects.postgresql import UUID


class Country(db.Model):
    __tablename__ = 'countries'

    country_id = db.Column(UUID(as_uuid=True), primary_key=True)
    country_name = db.Column(db.String(30), index=True, unique=True, nullable=False)
    country_type = db.Column(db.String(20), index=True, nullable=True, default=None)
    country_description = db.Column(db.Text, nullable=False)
    cover_image = db.Column(db.LargeBinary, nullable=True, default=None)
    tours = db.relationship('Tour', backref='country', lazy='dynamic')

    def __repr__(self):
        return f"<Country(name={self.country_name}, type={self.country_type}, description={self.country_description})>"

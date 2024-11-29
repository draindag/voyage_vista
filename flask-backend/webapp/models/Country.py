import os
import uuid

from webapp import db
from sqlalchemy.dialects.postgresql import UUID

upload_folder = os.getenv("UPLOADED_PHOTOS_DEST")
file_ext = os.getenv("COVER_IMAGES_EXT")


class Country(db.Model):
    __tablename__ = 'countries'

    country_id = db.Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    country_name = db.Column(db.String(30), index=True, unique=True, nullable=False)
    country_description = db.Column(db.Text, nullable=False)
    tours = db.relationship('Tour', backref='country', lazy='dynamic', cascade='all, delete-orphan')

    @property
    def country_image(self):
        return f"{upload_folder}{self.country_id}{file_ext}"

    def __repr__(self):
        return f"<Country(name={self.country_name}, description={self.country_description})>"

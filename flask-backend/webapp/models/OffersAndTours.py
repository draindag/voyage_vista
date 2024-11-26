from sqlalchemy import UniqueConstraint

from webapp import db
from sqlalchemy.dialects.postgresql import UUID


offers_tours = db.Table('offers_tours',
    db.Column('tour_id', UUID(as_uuid=True), db.ForeignKey('tours.tour_id', ondelete='CASCADE'), primary_key=True),
    db.Column('offer_id', UUID(as_uuid=True), db.ForeignKey('special_offers.offer_id', ondelete='CASCADE'),
              primary_key=True),

    UniqueConstraint('tour_id', 'offer_id', name='uq_tour_id_offer_id')
)

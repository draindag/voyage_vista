from webapp import db
from sqlalchemy.dialects.postgresql import UUID


class FavTour(db.Model):
    __tablename__ = 'fav_tours'

    tour_id = db.Column(UUID(as_uuid=True), db.ForeignKey('tours.tour_id'), primary_key=True)
    user_id = db.Column(UUID(as_uuid=True), db.ForeignKey('users.user_id'), primary_key=True)

    def __repr__(self):
        return f"<Fav_tour(user_id={self.user_id}, tour_id={self.tour_id})>"

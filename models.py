# models.py
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class Car(db.Model):
    __tablename__ = 'cars'
    id = db.Column(db.Integer, primary_key=True)
    brand = db.Column(db.String(80), nullable=False)
    model = db.Column(db.String(80), nullable=False)
    type = db.Column(db.String(80), nullable=False)   # SUV / Sedan / etc.
    gps = db.Column(db.Boolean, default=False)
    rental_rate = db.Column(db.Float, nullable=False)
    availability = db.Column(db.String(20), nullable=False, default='Available')
    description = db.Column(db.Text, nullable=True)

    def to_dict(self):
        return {
            "id": self.id,
            "brand": self.brand,
            "model": self.model,
            "type": self.type,
            "gps": self.gps,
            "rental_rate": self.rental_rate,
            "availability": self.availability,
            "description": self.description
        }

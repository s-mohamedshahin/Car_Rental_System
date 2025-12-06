# seed_db.py
from app import create_app
from models import db, Car

app = create_app()

cars_data = [
    {"brand": "Toyota", "model": "Corolla", "type": "Sedan", "gps": True, "rental_rate": 25.0,
     "availability": "Available", "description": "Comfortable and efficient."},
    {"brand": "Toyota", "model": "RAV4", "type": "SUV", "gps": True, "rental_rate": 40.0,
     "availability": "Available", "description": "Spacious family SUV."},
    {"brand": "Hyundai", "model": "Elantra", "type": "Sedan", "gps": False, "rental_rate": 22.0,
     "availability": "Rented", "description": "Economic and reliable."},
    {"brand": "Nissan", "model": "X-Trail", "type": "SUV", "gps": True, "rental_rate": 38.0,
     "availability": "Available", "description": "Comfort SUV for all trips."}
]

with app.app_context():
    db.create_all()
    for c in cars_data:
        exists = Car.query.filter_by(brand=c['brand'], model=c['model']).first()
        if not exists:
            new_car = Car(**c)
            db.session.add(new_car)
    db.session.commit()
    print("Database seeded with sample cars!")

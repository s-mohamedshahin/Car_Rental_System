# repo.py
from models import Car, db

def get_all_cars():
    return Car.query.all()

def get_car_by_id(car_id):
    return Car.query.get(car_id)

def update_car_status(car_id, status):
    car = Car.query.get(car_id)
    if car:
        car.availability = status
        db.session.commit()
        return True
    return False

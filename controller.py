# controller.py
"""
Controller layer for the Car Rental System.
Handles business logic and request processing for car-related operations.
"""
from flask import request, jsonify
from models import Car, db
from sqlalchemy import func, select


class CarController:
    """Controller class handling all car-related business logic"""
    
    @staticmethod
    def get_all_cars_filtered():
        """Get all cars with optional filtering based on request parameters"""
        q = db.session.query(Car)
        
        # Extract filter parameters from request
        brand = request.args.get('brand')
        model_q = request.args.get('model')
        type_q = request.args.get('type')
        gps_q = request.args.get('gps')
        only_available = request.args.get('only_available')
        min_price = request.args.get('min_price')
        max_price = request.args.get('max_price')
        sort_by = request.args.get('sort_by', '')
        
        # Apply filters
        if brand:
            q = q.filter(Car.brand.ilike(f"%{brand}%"))
        if model_q:
            q = q.filter(Car.model.ilike(f"%{model_q}%"))
        if type_q:
            q = q.filter(Car.type.ilike(f"%{type_q}%"))
        if gps_q == "1":
            q = q.filter(Car.gps.is_(True))
        if only_available == "1":
            q = q.filter(Car.availability == "Available")
        if min_price:
            q = q.filter(Car.rental_rate >= float(min_price))
        if max_price:
            q = q.filter(Car.rental_rate <= float(max_price))
        
        # Apply sorting
        if sort_by == 'price_asc':
            q = q.order_by(Car.rental_rate.asc())
        elif sort_by == 'price_desc':
            q = q.order_by(Car.rental_rate.desc())
        elif sort_by == 'brand':
            q = q.order_by(Car.brand.asc(), Car.model.asc())
        elif sort_by == 'availability':
            q = q.order_by(Car.availability.desc())
        
        return q.all()
    
    @staticmethod
    def get_car_by_id(car_id):
        """Get a single car by ID or return 404"""
        car = db.session.get(Car, car_id)
        if car is None:
            from werkzeug.exceptions import NotFound
            raise NotFound(f"Car with id {car_id} not found")
        return car
    
    @staticmethod
    def update_car_status(car_id):
        """Update car availability status via JSON request"""
        car = db.session.get(Car, car_id)
        if car is None:
            return jsonify({"error": "Car not found"}), 404
            
        data = request.get_json() or {}
        status = data.get("availability")
        
        # Validate status
        if status not in ('Available', 'Rented'):
            return jsonify({"error": "Invalid status"}), 400
        
        # Update and commit
        car.availability = status
        db.session.commit()
        return jsonify({"message": "Status updated", "car": car.to_dict()})
    
    @staticmethod
    def get_statistics():
        """Get overall statistics about the car rental inventory"""
        total_cars = db.session.query(func.count(Car.id)).scalar() or 0
        available_cars = db.session.query(func.count(Car.id)).filter(
            Car.availability == 'Available'
        ).scalar() or 0
        rented_cars = db.session.query(func.count(Car.id)).filter(
            Car.availability == 'Rented'
        ).scalar() or 0
        
        # Average rental rate
        avg_rate = db.session.query(func.avg(Car.rental_rate)).scalar() or 0
        
        # Most popular type (most cars of this type)
        type_counts = db.session.query(
            Car.type, func.count(Car.id)
        ).group_by(Car.type).order_by(func.count(Car.id).desc()).first()
        
        most_popular_type = type_counts[0] if type_counts else "N/A"
        
        # Price range
        min_price = db.session.query(func.min(Car.rental_rate)).scalar() or 0
        max_price = db.session.query(func.max(Car.rental_rate)).scalar() or 0
        
        return {
            'total_cars': total_cars,
            'available_cars': available_cars,
            'rented_cars': rented_cars,
            'avg_rate': round(avg_rate, 2),
            'most_popular_type': most_popular_type,
            'min_price': min_price,
            'max_price': max_price
        }
    
    @staticmethod
    def get_filtered_statistics(cars):
        """Get statistics for a filtered list of cars"""
        if not cars:
            return {
                'count': 0,
                'avg_price': 0,
                'min_price': 0,
                'max_price': 0
            }
        
        prices = [car.rental_rate for car in cars]
        return {
            'count': len(cars),
            'avg_price': round(sum(prices) / len(prices), 2),
            'min_price': min(prices),
            'max_price': max(prices)
        }

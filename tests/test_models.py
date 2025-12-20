"""
Unit tests for Car model and CarController.
"""
import pytest
from models import Car, db
from controller import CarController


class TestCarModel:
    """Tests for the Car model."""
    
    def test_car_creation(self, app):
        """Test creating a Car instance."""
        with app.app_context():
            car = Car(
                brand="Tesla",
                model="Model 3",
                type="Sedan",
                gps=True,
                rental_rate=55.0,
                availability="Available",
                description="Electric sedan"
            )
            db.session.add(car)
            db.session.commit()
            
            assert car.id is not None
            assert car.brand == "Tesla"
            assert car.model == "Model 3"
            assert car.type == "Sedan"
            assert car.gps is True
            assert car.rental_rate == 55.0
            assert car.availability == "Available"
    
    def test_car_to_dict(self, app):
        """Test Car to_dict method."""
        with app.app_context():
            car = Car.query.first()
            car_dict = car.to_dict()
            
            assert isinstance(car_dict, dict)
            assert 'id' in car_dict
            assert 'brand' in car_dict
            assert 'model' in car_dict
            assert 'type' in car_dict
            assert 'gps' in car_dict
            assert 'rental_rate' in car_dict
            assert 'availability' in car_dict
            assert 'description' in car_dict


class TestCarController:
    """Tests for the CarController class."""
    
    def test_get_car_by_id(self, app):
        """Test getting a car by ID."""
        with app.app_context():
            car = CarController.get_car_by_id(1)
            assert car is not None
            assert car.id == 1
            assert car.brand == "Toyota"
    
    def test_get_car_by_invalid_id(self, app):
        """Test getting a car with invalid ID raises 404."""
        with app.app_context():
            with pytest.raises(Exception):  # get_or_404 raises exception
                CarController.get_car_by_id(9999)
    
    def test_get_all_cars_no_filter(self, app, client):
        """Test getting all cars without filters."""
        with app.app_context():
            with client:
                client.get('/cars')  # Establish request context
                cars = CarController.get_all_cars_filtered()
                assert len(cars) == 4
    
    def test_get_all_cars_brand_filter(self, app, client):
        """Test filtering cars by brand."""
        with app.app_context():
            with client:
                client.get('/cars?brand=Toyota')
                cars = CarController.get_all_cars_filtered()
                assert len(cars) == 2
                assert all(car.brand == "Toyota" for car in cars)
    
    def test_get_all_cars_type_filter(self, app, client):
        """Test filtering cars by type."""
        with app.app_context():
            with client:
                client.get('/cars?type=SUV')
                cars = CarController.get_all_cars_filtered()
                assert len(cars) == 2
                assert all(car.type == "SUV" for car in cars)
    
    def test_get_all_cars_gps_filter(self, app, client):
        """Test filtering cars with GPS."""
        with app.app_context():
            with client:
                client.get('/cars?gps=1')
                cars = CarController.get_all_cars_filtered()
                assert len(cars) == 3
                assert all(car.gps is True for car in cars)
    
    def test_get_all_cars_availability_filter(self, app, client):
        """Test filtering only available cars."""
        with app.app_context():
            with client:
                client.get('/cars?only_available=1')
                cars = CarController.get_all_cars_filtered()
                assert len(cars) == 3
                assert all(car.availability == "Available" for car in cars)
    
    def test_update_car_status_valid(self, app, client):
        """Test updating car status with valid data."""
        with app.app_context():
            with client:
                response = client.put('/api/cars/1/status',
                                     json={"availability": "Rented"})
                result = CarController.update_car_status(1)
                
                car = Car.query.get(1)
                assert car.availability == "Rented"
    
    def test_update_car_status_invalid(self, app, client):
        """Test updating car status with invalid data."""
        with app.app_context():
            with client:
                response = client.put('/api/cars/1/status',
                                     json={"availability": "Invalid"})
                result = CarController.update_car_status(1)
                
                # Should return error response
                assert result[1] == 400  # HTTP 400 Bad Request

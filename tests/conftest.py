"""
Pytest configuration and fixtures for the car rental application tests.
"""
import pytest
import sys
import os

# Add parent directory to path to import app modules
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from app import create_app
from models import db, Car


@pytest.fixture
def app():
    """Create and configure a test application instance."""
    app = create_app('sqlite:///:memory:')  # Use in-memory database for tests
    app.config['TESTING'] = True
    
    with app.app_context():
        db.create_all()
        # Seed test data
        test_cars = [
            Car(brand="Toyota", model="Corolla", type="Sedan", gps=True, 
                rental_rate=25.0, availability="Available", description="Test car 1"),
            Car(brand="Honda", model="Civic", type="Sedan", gps=False, 
                rental_rate=22.0, availability="Available", description="Test car 2"),
            Car(brand="Ford", model="Explorer", type="SUV", gps=True, 
                rental_rate=45.0, availability="Rented", description="Test car 3"),
            Car(brand="Toyota", model="RAV4", type="SUV", gps=True, 
                rental_rate=40.0, availability="Available", description="Test car 4"),
        ]
        for car in test_cars:
            db.session.add(car)
        db.session.commit()
    
    yield app
    
    with app.app_context():
        db.drop_all()


@pytest.fixture
def client(app):
    """Create a test client for the app."""
    return app.test_client()


@pytest.fixture
def runner(app):
    """Create a test CLI runner for the app."""
    return app.test_cli_runner()

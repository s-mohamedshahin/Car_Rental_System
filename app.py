# app.py
from flask import Flask, render_template, redirect, url_for
from models import db
from controller import CarController

import os

def create_app(db_path=None):
    app = Flask(__name__)
    
    # Ensure instance folder exists
    instance_path = os.path.join(os.path.abspath(os.path.dirname(__file__)), 'instance')
    if not os.path.exists(instance_path):
        os.makedirs(instance_path)

    if db_path is None:
        db_path = 'sqlite:///' + os.path.join(instance_path, 'cars.db')

    app.config['SQLALCHEMY_DATABASE_URI'] = db_path
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    
    db.init_app(app)

    @app.route('/')
    def index():
        return redirect(url_for('list_cars'))

    @app.route('/cars')
    def list_cars():
        cars = CarController.get_all_cars_filtered()
        stats = CarController.get_filtered_statistics(cars)
        return render_template('cars.html', cars=cars, stats=stats)
    
    @app.route('/dashboard')
    def dashboard():
        stats = CarController.get_statistics()
        return render_template('dashboard.html', stats=stats)

    @app.route('/cars/<int:car_id>')
    def car_details(car_id):
        car = CarController.get_car_by_id(car_id)
        return render_template('car_details.html', car=car)

    @app.route('/api/cars/<int:car_id>/status', methods=['PUT'])
    def update_status(car_id):
        return CarController.update_car_status(car_id)

    return app


if __name__ == '__main__':
    app = create_app()
    with app.app_context():
        db.create_all()
    app.run(debug=True)

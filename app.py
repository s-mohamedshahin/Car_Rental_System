# app.py
from flask import Flask, render_template, request, redirect, url_for, jsonify
from models import db, Car

def create_app(db_path='sqlite:///cars.db'):
    app = Flask(__name__)
    app.config['SQLALCHEMY_DATABASE_URI'] = db_path
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    
    db.init_app(app)

    @app.route('/')
    def index():
        return redirect(url_for('list_cars'))

    @app.route('/cars')
    def list_cars():
        q = Car.query

        brand = request.args.get('brand')
        model_q = request.args.get('model')
        type_q = request.args.get('type')
        gps_q = request.args.get('gps')
        only_available = request.args.get('only_available')

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

        cars = q.all()
        return render_template('cars.html', cars=cars)

    @app.route('/cars/<int:car_id>')
    def car_details(car_id):
        car = Car.query.get_or_404(car_id)
        return render_template('car_details.html', car=car)

    @app.route('/api/cars/<int:car_id>/status', methods=['PUT'])
    def update_status(car_id):
        car = Car.query.get_or_404(car_id)
        data = request.get_json() or {}
        status = data.get("availability")

        if status not in ('Available', 'Rented'):
            return jsonify({"error": "Invalid status"}), 400

        car.availability = status
        db.session.commit()
        return jsonify({"message": "Status updated", "car": car.to_dict()})

    return app


if __name__ == '__main__':
    app = create_app()
    with app.app_context():
        db.create_all()
    app.run(debug=True)

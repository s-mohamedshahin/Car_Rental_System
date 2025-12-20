# Car Rental System

A Flask-based car rental management system implementing the Model-View-Controller (MVC) pattern. This application allows users to browse, search, and filter available rental cars.

## 🎯 Features

- **Car Browsing**: View all available rental cars
- **Advanced Search & Filtering**: Filter by brand, model, type, GPS availability, and rental status
- **Car Details**: View detailed information about specific vehicles
- **Status Management**: API endpoint to update car availability status
- **Responsive Design**: Clean, user-friendly interface

## 🏗️ Architecture

This project follows the **MVC (Model-View-Controller)** pattern:

- **Model** (`models.py`): Contains `Car` model and database operations
- **View** (`templates/`): HTML templates using Jinja2
- **Controller** (`models.py`): `CarController` class handles business logic

## 📋 Requirements

- Python 3.12+
- Flask 3.0.0
- Flask-SQLAlchemy 3.1.1
- Docker (for containerized deployment)

## 🚀 Installation & Setup

### Option 1: Local Installation

1. **Clone the repository**
   ```bash
   git clone <repository-url>
   cd car_rental_proj
   ```

2. **Create virtual environment**
   ```bash
   python -m venv venv
   venv\Scripts\activate  # Windows
   # source venv/bin/activate  # Linux/Mac
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Initialize database**
   ```bash
   python seed_db.py
   ```

5. **Run the application**
   ```bash
   python app.py
   ```

6. **Access the application**
   Open your browser and navigate to `http://localhost:5000`

### Option 2: Docker Deployment (Recommended)

1. **Build and run with Docker Compose**
   ```bash
   docker-compose up --build
   ```

2. **Access the application**
   Open your browser and navigate to `http://localhost:5000`

3. **Stop the application**
   ```bash
   docker-compose down
   ```

## 🧪 Running Tests

### Run all tests
```bash
pytest tests/ -v
```

### Run with coverage report
```bash
pytest tests/ -v --cov=. --cov-report=term-missing
```

## 🔍 API Endpoints

### GET `/`
Redirects to the cars listing page.

### GET `/cars`
Lists all cars with optional filtering.

**Query Parameters:**
- `brand` (string): Filter by car brand
- `model` (string): Filter by car model
- `type` (string): Filter by car type (e.g., "Sedan", "SUV")
- `gps` (1): Filter cars with GPS
- `only_available` (1): Filter only available cars

**Example:**
```
GET /cars?brand=Toyota&only_available=1
```

### GET `/cars/<int:car_id>`
View details of a specific car.

### PUT `/api/cars/<int:car_id>/status`
Update the availability status of a car.

**Request Body:**
```json
{
  "availability": "Available" | "Rented"
}
```

**Response:**
```json
{
  "message": "Status updated",
  "car": { ... }
}
```

## 📊 Database Schema

### Car Table
| Column | Type | Description |
|--------|------|-------------|
| id | Integer | Primary key |
| brand | String(80) | Car manufacturer |
| model | String(80) | Car model |
| type | String(80) | Vehicle type (Sedan, SUV, etc.) |
| gps | Boolean | GPS availability |
| rental_rate | Float | Daily rental rate ($) |
| availability | String(20) | "Available" or "Rented" |
| description | Text | Car description |

## 👥 Team Contribution

Member 2 Work: Car Search & Browsing Module

## 📝 License

This project is part of a university software engineering course.

## 🔗 Additional Documentation

- [Technical Documentation](docs/TECHNICAL_DOCUMENTATION.md)
- [Testing Documentation](docs/TESTING_DOCUMENTATION.md)

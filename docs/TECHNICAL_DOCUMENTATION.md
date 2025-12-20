# Technical Documentation
## Car Rental System

---

## 1. System Architecture

### 1.1 MVC Pattern Implementation

This application strictly follows the **Model-View-Controller (MVC)** architectural pattern:

#### **Model Layer** (`models.py`)
```
- Car (SQLAlchemy Model)
  - Represents car entities in the database
  - Provides to_dict() method for JSON serialization
  
- CarController (Controller Logic)
  - get_all_cars_filtered(): Retrieves and filters cars
  - get_car_by_id(): Fetches specific car
  - update_car_status(): Updates car availability
```

#### **View Layer** (`templates/`)
```
- layout.html: Base template with consistent styling
- cars.html: Car listing page with search form
- car_details.html: Individual car details page
```

#### **Controller Layer**
The `CarController` class in `models.py` acts as the controller, separating business logic from route handlers in `app.py`.

### 1.2 Application Flow

```
User Request → Flask Route → CarController → Database (SQLAlchemy)
                    ↓                              ↓
              Jinja2 Template ← Data Processing ← Query Results
                    ↓
               HTML Response
```

---

## 2. Database Architecture

### 2.1 Database: SQLite
- **File**: `instance/cars.db`
- **ORM**: Flask-SQLAlchemy
- **Configuration**: In-memory for tests, file-based for production

### 2.2 Schema Design

```sql
CREATE TABLE cars (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    brand VARCHAR(80) NOT NULL,
    model VARCHAR(80) NOT NULL,
    type VARCHAR(80) NOT NULL,
    gps BOOLEAN DEFAULT 0,
    rental_rate FLOAT NOT NULL,
    availability VARCHAR(20) NOT NULL DEFAULT 'Available',
    description TEXT
);
```

### 2.3 Entity Relationship

Currently single-entity system. Future enhancements could include:
- Users table (customers, admins)
- Rentals table (booking records)
- Reviews table (customer feedback)

---

## 3. API Design

### 3.1 RESTful Endpoints

| Method | Endpoint | Purpose | Request | Response |
|--------|----------|---------|---------|----------|
| GET | `/` | Redirect to cars list | - | 302 Redirect |
| GET | `/cars` | List all cars (filtered) | Query params | HTML page |
| GET | `/cars/<id>` | Car details | - | HTML page |
| PUT | `/api/cars/<id>/status` | Update status | JSON body | JSON response |

### 3.2 Request/Response Format

#### Update Car Status
**Request:**
```json
PUT /api/cars/1/status
Content-Type: application/json

{
  "availability": "Rented"
}
```

**Success Response:**
```json
HTTP 200 OK
{
  "message": "Status updated",
  "car": {
    "id": 1,
    "brand": "Toyota",
    "model": "Corolla",
    "type": "Sedan",
    "gps": true,
    "rental_rate": 25.0,
    "availability": "Rented",
    "description": "Comfortable and efficient."
  }
}
```

**Error Response:**
```json
HTTP 400 Bad Request
{
  "error": "Invalid status"
}
```

---

## 4. Technology Stack

| Component | Technology | Version |
|-----------|-----------|---------|
| **Backend** | Flask | 3.0.0 |
| **ORM** | Flask-SQLAlchemy | 3.1.1 |
| **Database** | SQLite | 3.x |
| **Testing** | Pytest | 7.4.3 |
| **Containerization** | Docker | - |
| **CI/CD** | GitHub Actions | - |
| **Frontend** | HTML/CSS + Jinja2 | - |

---

## 5. File Structure

```
car_rental_proj/
├── app.py                    # Flask application factory and routes
├── models.py                 # Car model and CarController
├── seed_db.py                # Database seeding script
├── requirements.txt          # Python dependencies
├── Dockerfile                # Docker container configuration
├── docker-compose.yml        # Docker Compose orchestration
├── .dockerignore             # Docker build exclusions
├── .gitignore                # Git exclusions
├── README.md                 # User documentation
├── .github/
│   └── workflows/
│       └── ci.yml            # GitHub Actions CI/CD pipeline
├── docs/
│   ├── TECHNICAL_DOCUMENTATION.md
│   └── TESTING_DOCUMENTATION.md
├── instance/
│   └── cars.db               # SQLite database (created at runtime)
├── templates/
│   ├── layout.html           # Base template
│   ├── cars.html             # Car listing page
│   └── car_details.html      # Car detail page
└── tests/
    ├── __init__.py
    ├── conftest.py           # Pytest fixtures
    ├── test_models.py        # Model and controller tests
    └── test_app.py           # Route integration tests
```

---

## 6. Design Decisions & Assumptions

### 6.1 Key Design Decisions

1. **MVC in Single File**
   - Controller logic placed in `models.py` as per project requirements
   - Keeps model and controller logic together for this small-scale application

2. **SQLite Database**
   - Lightweight, file-based database
   - Suitable for development and small deployments
   - Easy to containerize with no external database server needed

3. **In-Memory Testing**
   - Tests use `sqlite:///:memory:` for isolation
   - Fast test execution
   - No test data pollution

4. **Docker Volume for Persistence**
   - Database stored in mounted volume
   - Survives container restarts
   - Easy backup and migration

### 6.2 Assumptions

1. **Single User Context**
   - No authentication/authorization required in current phase
   - All users have full access to all features

2. **Simple Status Model**
   - Only two statuses: "Available" and "Rented"
   - No reservation system or booking dates

3. **No Payment Processing**
   - Rental rates displayed but no payment integration

4. **Static Car Inventory**
   - Cars added via seed script
   - No admin interface for car management (could be future enhancement)

---

## 7. Future Enhancements

1. **User Authentication**: Login system for customers and admins
2. **Booking System**: Date-based reservations with calendar
3. **Payment Integration**: Online payment processing
4. **Admin Dashboard**: CRUD operations for car inventory
5. **Review System**: Customer ratings and feedback
6. **Email Notifications**: Booking confirmations
7. **Advanced Search**: Price ranges, location-based filtering
8. **PostgreSQL Migration**: For production scalability

---

## 8. Performance Considerations

1. **Database Indexing**
   - Primary key indexed by default
   - Consider adding indexes on frequently queried fields (brand, type, availability)

2. **Query Optimization**
   - Filters applied at database level (SQL WHERE clauses)
   - Efficient LIKE queries for text search

3. **Caching** (Future)
   - Consider Flask-Caching for frequently accessed data
   - Redis for session storage in production

---

## 9. Security Considerations

Current implementation is for development/educational purposes. For production:

1. **Input Validation**: Implement comprehensive input sanitization
2. **SQL Injection**: SQLAlchemy provides protection, but validate user input
3. **HTTPS**: Deploy with SSL/TLS certificates
4. **CORS**: Configure appropriate CORS policies for API
5. **Rate Limiting**: Implement to prevent abuse
6. **Environment Variables**: Store sensitive configuration externally

---

## 10. Deployment Guide

### 10.1 Docker Deployment

```bash
# Build image
docker build -t car-rental-app .

# Run container
docker run -p 5000:5000 -v $(pwd)/instance:/app/instance car-rental-app

# Or use docker-compose
docker-compose up --build
```

### 10.2 Production Recommendations

1. Use WSGI server (Gunicorn) instead of Flask development server
2. Set up reverse proxy (Nginx)
3. Configure logging and monitoring
4. Implement database backups
5. Use environment-based configuration

---

**Document Version**: 1.0  
**Last Updated**: December 2025  
**Project**: Car Rental System - Phase 5

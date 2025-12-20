"""
Integration tests for Flask routes and application endpoints.
"""
import json


class TestRoutes:
    """Tests for Flask application routes."""
    
    def test_index_redirect(self, client):
        """Test that index redirects to /cars."""
        response = client.get('/')
        assert response.status_code == 302  # Redirect
        assert '/cars' in response.location
    
    def test_list_cars_page(self, client):
        """Test the cars listing page loads."""
        response = client.get('/cars')
        assert response.status_code == 200
        assert b'Cars' in response.data
    
    def test_list_cars_shows_data(self, client):
        """Test that cars are displayed on the page."""
        response = client.get('/cars')
        assert response.status_code == 200
        assert b'Toyota' in response.data
        assert b'Honda' in response.data
    
    def test_car_details_page(self, client):
        """Test car details page loads correctly."""
        response = client.get('/cars/1')
        assert response.status_code == 200
        assert b'Toyota' in response.data
        assert b'Corolla' in response.data
    
    def test_car_details_404(self, client):
        """Test car details with invalid ID returns 404."""
        response = client.get('/cars/9999')
        assert response.status_code == 404
    
    def test_api_update_status_valid(self, client):
        """Test API endpoint for updating car status with valid data."""
        response = client.put(
            '/api/cars/1/status',
            data=json.dumps({"availability": "Rented"}),
            content_type='application/json'
        )
        assert response.status_code == 200
        data = json.loads(response.data)
        assert data['message'] == 'Status updated'
        assert data['car']['availability'] == 'Rented'
    
    def test_api_update_status_invalid(self, client):
        """Test API endpoint with invalid status value."""
        response = client.put(
            '/api/cars/1/status',
            data=json.dumps({"availability": "InvalidStatus"}),
            content_type='application/json'
        )
        assert response.status_code == 400
        data = json.loads(response.data)
        assert 'error' in data
    
    def test_search_filter_brand(self, client):
        """Test search filtering by brand."""
        response = client.get('/cars?brand=Toyota')
        assert response.status_code == 200
        assert b'Toyota' in response.data
        # Should show Toyota Corolla and RAV4
        assert response.data.count(b'Toyota') >= 2
    
    def test_search_filter_type(self, client):
        """Test search filtering by type."""
        response = client.get('/cars?type=SUV')
        assert response.status_code == 200
        assert b'SUV' in response.data
        assert b'Explorer' in response.data or b'RAV4' in response.data
    
    def test_search_filter_gps(self, client):
        """Test search filtering for cars with GPS."""
        response = client.get('/cars?gps=1')
        assert response.status_code == 200
        # Should only show cars with GPS
        assert b'Corolla' in response.data  # Has GPS
    
    def test_search_filter_availability(self, client):
        """Test search filtering for only available cars."""
        response = client.get('/cars?only_available=1')
        assert response.status_code == 200
        # Should show available cars, not rented ones
        assert b'Available' in response.data

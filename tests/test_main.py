"""
Unit tests for main .py 
Testing the /DevOps and /Token endpoints.
"""

import os
import jwt
import pytest
import json
from app.main import app
from app.jwt_manager import JWTManager
from dotenv import load_dotenv
load_dotenv('.env.test')

@pytest.fixture
def client():
    """
    Fixture for test client of Flask app.
    """
    app.config['TESTING'] = True
    with app.test_client() as client:
        yield client
        
@pytest.fixture
def jwt_token():
    """
    Fixture to generate a valid JWT token for testing.
    """
    jwt_manager = JWTManager()
    token = jwt_manager.generate_token(user_id="test-user")
    return token

@pytest.fixture
def headers(jwt_token):
    """
    Fixture to provide headers with valid API key and JWT token.
    """
    API_KEY = os.getenv("API_KEY_TEST")
    return {
        'X-Parse-REST-API-Key': f'{API_KEY}',
        'X-JWT-KWY': jwt_token,
        'Content-Type': 'application/json'
    }

class TestDevOpsEndpoint:
    """
    Test cases for /DevOps endpoint.
    """
    
    def test_successful_post_request(self, client, headers):
        """
        Test a successful POST request to /DevOps with valid payload.
        """
        payload = {
            "message": "This is a test",
            "to": "Juan Perez",
            "from": "Rita Asturia",
            "timeToLifeSec": 45
        }
        
        response = client.post('/DevOps', data=json.dumps(payload), headers=headers)
        
        assert response.status_code == 200
        data = response.get_json()
        assert data['message'] == "Hello Juan Perez your message will be send"
        
    def test_post_with_different_name(self, client, headers):
        """
        Test POST request to /DevOps with a different 'to' name.
        """
        payload = {
            "message": "Another test message",
            "to": "Alice Johnson",
            "from": "Bob Smith",
            "timeToLifeSec": 30
        }
        
        response = client.post('/DevOps', data=json.dumps(payload), headers=headers)
        
        assert response.status_code == 200
        data = response.get_json()
        assert data['message'] == "Hello Alice Johnson your message will be send"
        
    def test_missing_api_key(self, client, jwt_token):
        """
        Test: Request without API key should return 401.
        """
        headers = {
            'Content-Type': 'application/json',
            'X-JWT-KWY': f'{jwt_token}'
        }
        
        payload = {
            "message": "Test",
            "to": "Juan",
            "from": "Rita",
            "timeToLifeSec": 45
        }
        
        response = client.post('/DevOps', data=json.dumps(payload), headers=headers)
        
        assert response.status_code == 401
    
    def test_invalid_api_key(self, client, jwt_token):
        """
        Test: API key invalid should return 403.
        """
        
        headers = {
            'X-Parse-REST-API-Key': 'invalid-key',
            'X-JWT-KWY': jwt_token,
            'Content-Type': 'application/json'
        }
        payload = {
            "message": "Test",
            "to": "Juan",
            "from": "Rita",
            "timeToLifeSec": 45
        }
        
        response = client.post('/DevOps', data=json.dumps(payload), headers=headers)
        
        assert response.status_code == 403
    
    def test_missing_jwt(self, client):
        """Test: Request sin JWT debe fallar"""
        API_KEY = os.getenv("API_KEY_TEST")
        headers = {
            'X-Parse-REST-API-Key': f'{API_KEY}',
            'Content-Type': 'application/json'
        }
        payload = {
            "message": "Test",
            "to": "Juan",
            "from": "Rita",
            "timeToLifeSec": 45
        }
        
        response = client.post('/DevOps',data=json.dumps(payload),headers=headers)
        
        assert response.status_code == 401
    
    def test_invalid_jwt_signature(self, client):
        """Test: JWT con firma inválida debe fallar"""
        JWT_SECRET = os.getenv("JWT_SECRET_TEST")
        API_KEY = os.getenv("API_KEY_TEST")
        
        # Generar un token con un secret diferente
        invalid_token = jwt.encode(
            {"user_id": "test"}, 
            f"{JWT_SECRET}",  # Secret incorrecto
            algorithm="HS256"
        )
        headers = {
            'X-Parse-REST-API-Key': f'{API_KEY}',
            'X-JWT-KWY': invalid_token,
            'Content-Type': 'application/json'
        }
        payload = {
            "message": "Test",
            "to": "Juan",
            "from": "Rita",
            "timeToLifeSec": 45
        }
        
        response = client.post('/DevOps', data=json.dumps(payload), headers=headers)
        
        assert response.status_code == 403
    
    def test_missing_required_field_message(self, client, headers):
        """Test: shortage required field 'message'"""
        payload = {
            "to": "Juan Perez",
            "from": "Rita Asturia",
            "timeToLifeSec": 45
        }
        
        response = client.post('/DevOps', data=json.dumps(payload), headers=headers)
        
        assert response.status_code == 400
    
    def test_missing_required_field_to(self, client, headers):
        """Test: shortage required field 'to'"""
        payload = {
            "message": "Test",
            "from": "Rita Asturia",
            "timeToLifeSec": 45
        }
        
        response = client.post('/DevOps', data=json.dumps(payload), headers=headers)
        
        assert response.status_code == 400
    
    def test_invalid_content_type(self, client, jwt_token):
        """Test: Content-Type invalid"""
        API_KEY = os.getenv("API_KEY_TEST")

        headers = {
            'X-Parse-REST-API-Key': f'{API_KEY}',
            'X-JWT-KWY': jwt_token,
            'Content-Type': 'text/plain'
        }
        
        response = client.post('/DevOps', data='invalid data', headers=headers)
        
        assert response.status_code == 400
    
    def test_get_method_returns_error(self, client):
        """Test: GET method should return ERROR"""
        response = client.get('/DevOps')
        assert response.status_code == 405
        assert response.data.decode() == "ERROR"
    
    def test_put_method_returns_error(self, client):
        """Test: PUT method should return ERROR"""
        response = client.put('/DevOps')
        assert response.status_code == 405
        assert response.data.decode() == "ERROR"
    
    def test_delete_method_returns_error(self, client):
        """Test: DELETE method should return ERROR"""
        response = client.delete('/DevOps')
        assert response.status_code == 405
        assert response.data.decode() == "ERROR"
    
    def test_patch_method_returns_error(self, client):
        """Test: PATCH method should return ERROR"""
        response = client.patch('/DevOps')
        assert response.status_code == 405
        assert response.data.decode() == "ERROR"


class TestJWTGeneration:
    """Tests para generación de JWT"""
    
    def test_generate_jwt_with_api_key(self, client):
        """Test: Generar JWT con API Key válido"""
        API_KEY = os.getenv("API_KEY_TEST")

        headers = {
            'X-Parse-REST-API-Key': f'{API_KEY}',
            'Content-Type': 'application/json'
        }
        
        body = {}
        response = client.post('/generate-jwt', data=json.dumps(body), headers=headers)
        
        
        assert response.status_code == 200
        data = json.loads(response.data)
        assert 'token' in data
    
    def test_generate_jwt_without_api_key(self, client):
        """Test: Generar JWT sin API Key debe fallar"""
        response = client.post('/generate-jwt')
        assert response.status_code == 401
        
        
        
class TestHealthEndpoints:
    """Tests para health check endpoints"""
    
    def test_health_check(self, client):
        """Test: Health check endpoint"""
        response = client.get('/health')
        assert response.status_code == 200
        data = json.loads(response.data)
        assert data['status'] == 'healthy'
    
    def test_readiness_check(self, client):
        """Test: Readiness check endpoint"""
        response = client.get('/ready')
        assert response.status_code == 200
        data = json.loads(response.data)
        assert data['status'] == 'ready'
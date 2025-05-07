import pytest
from app import app

@pytest.fixture
def client():
    app.config['TESTING'] = True
    with app.test_client() as client:
        yield client

def test_index_page(client):
    """Test that the index page loads successfully"""
    response = client.get('/')
    assert response.status_code == 200
    assert b'Welcome to Flask App' in response.data

def test_url_params_page_empty(client):
    """Test URL parameters page with no parameters"""
    response = client.get('/url_params')
    assert response.status_code == 200
    assert b'No URL parameters provided' in response.data

def test_url_params_page_with_params(client):
    """Test URL parameters page with parameters"""
    response = client.get('/url_params?param1=value1&param2=value2')
    assert response.status_code == 200
    assert b'param1' in response.data
    assert b'value1' in response.data
    assert b'param2' in response.data
    assert b'value2' in response.data

def test_headers_page(client):
    """Test headers page displays request headers"""
    response = client.get('/headers')
    assert response.status_code == 200
    assert b'Request Headers' in response.data
    assert b'User-Agent' in response.data

def test_cookies_page_set_cookie(client):
    """Test cookies page sets special cookie when not present"""
    response = client.get('/cookies')
    assert response.status_code == 200
    assert b'special_cookie' not in response.data
    assert 'special_cookie' in response.headers.get('Set-Cookie', '')

def test_cookies_page_delete_cookie(client):
    """Test cookies page deletes special cookie when present"""
    # First request sets the cookie
    client.get('/cookies')
    # Second request should delete it
    response = client.get('/cookies')
    assert response.status_code == 200
    assert b'special_cookie' in response.data
    assert 'special_cookie=;' in response.headers.get('Set-Cookie', '')

def test_form_params_page_get(client):
    """Test form parameters page GET request"""
    response = client.get('/form_params')
    assert response.status_code == 200
    assert b'Form Parameters' in response.data
    assert b'name="name"' in response.data
    assert b'name="email"' in response.data

def test_form_params_page_post(client):
    """Test form parameters page POST request"""
    response = client.post('/form_params', data={
        'name': 'Test User',
        'email': 'test@example.com'
    })
    assert response.status_code == 200
    assert b'Test User' in response.data
    assert b'test@example.com' in response.data

def test_phone_validation_page_get(client):
    """Test phone validation page GET request"""
    response = client.get('/phone')
    assert response.status_code == 200
    assert b'Phone Number Validation' in response.data
    assert b'name="phone"' in response.data

def test_phone_validation_valid_numbers(client):
    """Test phone validation with valid numbers"""
    valid_numbers = [
        '+7 (123) 456-75-90',
        '8(123)4567590',
        '123.456.75.90'
    ]
    for number in valid_numbers:
        response = client.post('/phone', data={'phone': number})
        assert response.status_code == 200
        assert b'is-invalid' not in response.data
        assert b'Success!' in response.data

def test_phone_validation_invalid_length(client):
    """Test phone validation with invalid length"""
    invalid_numbers = [
        '123456789',  # Too short
        '123456789012'  # Too long
    ]
    for number in invalid_numbers:
        response = client.post('/phone', data={'phone': number})
        assert response.status_code == 200
        assert b'is-invalid' in response.data
        assert 'Неверное количество цифр'.encode() in response.data

def test_phone_validation_invalid_characters(client):
    """Test phone validation with invalid characters"""
    invalid_numbers = [
        '123@456-7890',
        '123#456-7890',
        '123$456-7890'
    ]
    for number in invalid_numbers:
        response = client.post('/phone', data={'phone': number})
        assert response.status_code == 200
        assert b'is-invalid' in response.data
        assert 'В номере телефона встречаются недопустимые символы'.encode() in response.data

def test_phone_validation_formatting(client):
    """Test phone number formatting"""
    test_cases = [
        ('+7 (123) 456-75-90', '8-123-456-75-90'),
        ('8(123)4567590', '8-123-456-75-90'),
        ('123.456.75.90', '8-123-456-75-90')
    ]
    for input_number, expected_format in test_cases:
        response = client.post('/phone', data={'phone': input_number})
        assert response.status_code == 200
        assert expected_format.encode() in response.data 
import pytest
from app import create_app, db
from app.models import User, Role

@pytest.fixture
def app():
    app = create_app()
    app.config['TESTING'] = True
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///:memory:'
    app.config['WTF_CSRF_ENABLED'] = False  # Disable CSRF for testing
    app.config['SECRET_KEY'] = 'test-secret-key'  # Set a fixed secret key for testing
    
    with app.app_context():
        db.drop_all()  # Drop all tables first
        db.create_all()
        # Create test roles
        admin_role = Role(name='admin', description='Administrator')
        user_role = Role(name='user', description='Regular user')
        db.session.add(admin_role)
        db.session.add(user_role)
        db.session.commit()
        
        # Create test user
        user = User(
            login='testuser',
            first_name='Test',
            last_name='User',
            role_id=user_role.id
        )
        user.set_password('Test123!')
        db.session.add(user)
        db.session.commit()
        
        yield app
        
        db.session.remove()
        db.drop_all()

@pytest.fixture
def client(app):
    return app.test_client()

@pytest.fixture
def auth_client(client):
    client.post('/login', data={
        'login': 'testuser',
        'password': 'Test123!'
    })
    return client

def test_login_page(client):
    response = client.get('/login')
    assert response.status_code == 200
    assert b'Login' in response.data

def test_login_success(client):
    response = client.post('/login', data={
        'login': 'testuser',
        'password': 'Test123!'
    }, follow_redirects=True)
    assert response.status_code == 200
    assert b'Users' in response.data

def test_login_invalid_credentials(client):
    response = client.post('/login', data={
        'login': 'testuser',
        'password': 'wrongpassword'
    }, follow_redirects=True)
    assert response.status_code == 200
    assert b'Invalid login or password' in response.data

def test_logout(client):
    # First login
    client.post('/login', data={
        'login': 'testuser',
        'password': 'Test123!'
    })
    # Then logout
    response = client.get('/logout', follow_redirects=True)
    assert response.status_code == 200
    assert b'Login' in response.data

def test_change_password_page_requires_auth(client):
    response = client.get('/change-password', follow_redirects=True)
    assert response.status_code == 200
    assert b'Login' in response.data

def test_change_password_success(auth_client):
    response = auth_client.post('/change-password', data={
        'old_password': 'Test123!',
        'new_password': 'NewPass123!',
        'confirm_password': 'NewPass123!'
    }, follow_redirects=True)
    assert response.status_code == 200
    assert b'Password has been changed successfully' in response.data

def test_change_password_wrong_old_password(auth_client):
    response = auth_client.post('/change-password', data={
        'old_password': 'WrongPass123!',
        'new_password': 'NewPass123!',
        'confirm_password': 'NewPass123!'
    }, follow_redirects=True)
    assert response.status_code == 200
    assert b'Invalid old password' in response.data

def test_change_password_mismatch(auth_client):
    response = auth_client.post('/change-password', data={
        'old_password': 'Test123!',
        'new_password': 'NewPass123!',
        'confirm_password': 'DifferentPass123!'
    }, follow_redirects=True)
    assert response.status_code == 200
    assert b'Passwords do not match' in response.data 
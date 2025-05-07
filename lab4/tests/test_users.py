import pytest
from app import create_app, db
from app.models import User, Role

@pytest.fixture
def app():
    app = create_app()
    app.config['TESTING'] = True
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///:memory:'
    app.config['WTF_CSRF_ENABLED'] = False
    app.config['SECRET_KEY'] = 'test-secret-key'
    
    with app.app_context():
        db.drop_all()
        db.create_all()
        # Create test roles
        admin_role = Role(name='admin', description='Administrator')
        user_role = Role(name='user', description='Regular user')
        db.session.add(admin_role)
        db.session.add(user_role)
        db.session.commit()
        
        yield app
        
        db.session.remove()
        db.drop_all()

@pytest.fixture
def client(app):
    return app.test_client()

@pytest.fixture
def auth_client(app, client):
    # Create test user
    with app.app_context():
        user = User(
            login='testuser',
            first_name='Test',
            last_name='User',
            role_id=1  # admin role
        )
        user.set_password('Test123!')
        db.session.add(user)
        db.session.commit()

    # Log in
    client.post('/login', data={
        'login': 'testuser',
        'password': 'Test123!'
    })
    
    return client

def test_user_list_page(client):
    response = client.get('/')
    assert response.status_code == 200
    assert b'Users' in response.data

def test_create_user_page_requires_auth(client):
    response = client.get('/users/create', follow_redirects=True)
    assert response.status_code == 200
    assert b'Please log in' in response.data

def test_create_user(auth_client):
    response = auth_client.post('/users/create', data={
        'login': 'newuser',
        'password': 'NewUser123!',
        'first_name': 'New',
        'last_name': 'User',
        'role_id': 1
    }, follow_redirects=True)
    assert response.status_code == 200
    assert b'User created successfully' in response.data

def test_create_user_validation(auth_client):
    response = auth_client.post('/users/create', data={
        'login': 'test@123',  # Invalid characters
        'password': 'weak',
        'first_name': '',
        'last_name': 'User',
        'role_id': 1
    }, follow_redirects=True)
    assert response.status_code == 200
    assert b'Login must contain only Latin letters and numbers' in response.data

def test_view_user(app, client):
    # Create test user
    with app.app_context():
        user = User(
            login='testuser',
            first_name='Test',
            last_name='User',
            role_id=1  # admin role
        )
        user.set_password('Test123!')
        db.session.add(user)
        db.session.commit()

    response = client.get('/users/1')
    assert response.status_code == 200
    assert b'testuser' in response.data  # Check login
    assert b'Test' in response.data      # Check first name
    assert b'User' in response.data      # Check last name

def test_edit_user_requires_auth(client):
    response = client.get('/users/1/edit', follow_redirects=True)
    assert response.status_code == 200
    assert b'Please log in' in response.data

def test_edit_user(auth_client):
    response = auth_client.post('/users/1/edit', data={
        'first_name': 'Updated',
        'last_name': 'User',
        'role_id': 1
    }, follow_redirects=True)
    assert response.status_code == 200
    assert b'User updated successfully' in response.data

def test_delete_user_requires_auth(client):
    response = client.post('/users/1/delete', follow_redirects=True)
    assert response.status_code == 200
    assert b'Please log in' in response.data

def test_delete_user(auth_client):
    response = auth_client.post('/users/1/delete', follow_redirects=True)
    assert response.status_code == 200
    assert b'User deleted successfully' in response.data 
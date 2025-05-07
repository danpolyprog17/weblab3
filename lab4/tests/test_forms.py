import pytest
from app import create_app, db
from app.models import User, Role
from app.forms import UserForm, EditUserForm, ChangePasswordForm

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
        
        yield app
        
        db.session.remove()
        db.drop_all()

def test_user_form_validation(app):
    with app.app_context():
        form = UserForm()
        form.role_id.choices = [(1, 'admin'), (2, 'user')]
        
        # Test empty form
        assert not form.validate()
        assert 'This field is required' in str(form.login.errors)
        assert 'This field is required' in str(form.password.errors)
        assert 'This field is required' in str(form.first_name.errors)
        
        # Test invalid login (too short)
        form.login.data = 'test'
        form.password.data = 'Test123!'
        form.first_name.data = 'Test'
        form.role_id.data = 1
        assert not form.validate()
        assert 'Login must be between 5 and 50 characters' in str(form.login.errors)
        
        # Test invalid login (invalid characters)
        form.login.data = 'test@123'
        assert not form.validate()
        assert 'Login must contain only Latin letters and numbers' in str(form.login.errors)
        
        # Test valid form
        form.login.data = 'testuser'
        assert form.validate()

def test_edit_user_form_validation(app):
    with app.app_context():
        form = EditUserForm()
        form.role_id.choices = [(1, 'admin'), (2, 'user')]
        
        # Test empty form
        assert not form.validate()
        assert 'This field is required' in str(form.first_name.errors)
        
        # Test valid form
        form.first_name.data = 'Test'
        form.role_id.data = 1
        assert form.validate()

def test_change_password_form_validation(app):
    with app.app_context():
        form = ChangePasswordForm()
        
        # Test empty form
        assert not form.validate()
        assert 'This field is required' in str(form.old_password.errors)
        assert 'This field is required' in str(form.new_password.errors)
        assert 'This field is required' in str(form.confirm_password.errors)
        
        # Test password mismatch
        form.old_password.data = 'OldPass123!'
        form.new_password.data = 'NewPass123!'
        form.confirm_password.data = 'DifferentPass123!'
        assert not form.validate()
        assert 'Passwords do not match' in str(form.confirm_password.errors)
        
        # Test invalid password format
        form.new_password.data = 'weak'
        form.confirm_password.data = 'weak'
        assert not form.validate()
        assert 'Password must be between 8 and 128 characters' in str(form.new_password.errors)
        
        # Test valid form
        form.new_password.data = 'NewPass123!'
        form.confirm_password.data = 'NewPass123!'
        assert form.validate() 
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from datetime import datetime

db = SQLAlchemy()
login_manager = LoginManager()

def create_app():
    app = Flask(__name__)
    app.config['SECRET_KEY'] = 'your-secret-key-here'  # Change this in production
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///users.db'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

    db.init_app(app)
    login_manager.init_app(app)
    login_manager.login_view = 'auth.login'

    from app.models import User, Role
    from app.routes import main, auth, users

    app.register_blueprint(main.bp)
    app.register_blueprint(auth.bp)
    app.register_blueprint(users.bp)

    with app.app_context():
        print("Creating database tables...")  # Debug print
        db.create_all()
        
        # Check if we have any roles
        roles = Role.query.all()
        print(f"Found {len(roles)} roles")  # Debug print
        
        if not roles:
            print("Creating default roles...")  # Debug print
            admin_role = Role(name='admin', description='Administrator')
            user_role = Role(name='user', description='Regular user')
            db.session.add(admin_role)
            db.session.add(user_role)
            db.session.commit()
            print("Default roles created")  # Debug print

            # Create test user
            print("Creating test user...")  # Debug print
            test_user = User(
                login='admin',
                first_name='Admin',
                last_name='User',
                role_id=admin_role.id
            )
            test_user.set_password('Admin123!')
            db.session.add(test_user)
            db.session.commit()
            print("Test user created")  # Debug print
        else:
            # Check if we have any users
            users = User.query.all()
            print(f"Found {len(users)} users")  # Debug print
            if not users:
                print("Creating test user...")  # Debug print
                admin_role = Role.query.filter_by(name='admin').first()
                test_user = User(
                    login='admin',
                    first_name='Admin',
                    last_name='User',
                    role_id=admin_role.id
                )
                test_user.set_password('Admin123!')
                db.session.add(test_user)
                db.session.commit()
                print("Test user created")  # Debug print

    return app 
from flask import Blueprint, render_template
from flask_login import login_required, current_user
from app.models import User

bp = Blueprint('main', __name__)

@bp.route('/')
def index():
    users = User.query.all()
    return render_template('index.html', users=users) 
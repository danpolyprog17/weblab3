from flask import Blueprint, render_template, redirect, url_for, flash, request
from flask_login import login_user, logout_user, login_required, current_user
from app.models import User
from app.forms import LoginForm, ChangePasswordForm
from app import db

bp = Blueprint('auth', __name__)

@bp.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('main.index'))
    form = LoginForm()
    if form.validate_on_submit():
        print(f"Form data: {form.data}")  # Debug print
        user = User.query.filter_by(login=form.login.data).first()
        print(f"Attempting login for user: {form.login.data}")  # Debug print
        if user:
            print(f"User found: {user.login}, role_id: {user.role_id}")  # Debug print
            if user.check_password(form.password.data):
                print("Password correct, logging in")  # Debug print
                login_user(user)
                print(f"User authenticated: {current_user.is_authenticated}")  # Debug print
                next_page = request.args.get('next')
                return redirect(next_page or url_for('main.index'))
            else:
                print("Password incorrect")  # Debug print
        else:
            print(f"No user found with login: {form.login.data}")  # Debug print
            # Print all users in database
            all_users = User.query.all()
            print(f"All users in database: {[(u.login, u.role_id) for u in all_users]}")  # Debug print
        flash('Invalid login or password')
    return render_template('auth/login.html', form=form)

@bp.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('main.index'))

@bp.route('/change-password', methods=['GET', 'POST'])
@login_required
def change_password():
    form = ChangePasswordForm()
    if form.validate_on_submit():
        if current_user.check_password(form.old_password.data):
            current_user.set_password(form.new_password.data)
            db.session.commit()
            flash('Password has been changed successfully')
            return redirect(url_for('main.index'))
        flash('Invalid old password')
    return render_template('auth/change_password.html', form=form) 
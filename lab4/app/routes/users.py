from flask import Blueprint, render_template, redirect, url_for, flash, request, jsonify
from flask_login import login_required, current_user
from app.models import User, Role
from app.forms import UserForm, EditUserForm
from app import db

bp = Blueprint('users', __name__)

@bp.route('/users/create', methods=['GET', 'POST'])
@login_required
def create():
    form = UserForm()
    form.role_id.choices = [(r.id, r.name) for r in Role.query.all()]
    if form.validate_on_submit():
        user = User(
            login=form.login.data,
            last_name=form.last_name.data,
            first_name=form.first_name.data,
            middle_name=form.middle_name.data,
            role_id=form.role_id.data
        )
        user.set_password(form.password.data)
        db.session.add(user)
        try:
            db.session.commit()
            flash('User created successfully')
            return redirect(url_for('main.index'))
        except Exception as e:
            db.session.rollback()
            flash('Error creating user')
    return render_template('users/form.html', form=form, title='Create User')

@bp.route('/users/<int:id>')
def view(id):
    user = User.query.get_or_404(id)
    return render_template('users/view.html', user=user)

@bp.route('/users/<int:id>/edit', methods=['GET', 'POST'])
@login_required
def edit(id):
    user = User.query.get_or_404(id)
    form = EditUserForm(obj=user)
    form.role_id.choices = [(r.id, r.name) for r in Role.query.all()]
    if form.validate_on_submit():
        user.last_name = form.last_name.data
        user.first_name = form.first_name.data
        user.middle_name = form.middle_name.data
        user.role_id = form.role_id.data
        try:
            db.session.commit()
            flash('User updated successfully')
            return redirect(url_for('main.index'))
        except Exception as e:
            db.session.rollback()
            flash('Error updating user')
    return render_template('users/form.html', form=form, title='Edit User')

@bp.route('/users/<int:id>/delete', methods=['POST'])
@login_required
def delete(id):
    user = User.query.get_or_404(id)
    try:
        db.session.delete(user)
        db.session.commit()
        flash('User deleted successfully')
    except Exception as e:
        db.session.rollback()
        flash('Error deleting user')
    return redirect(url_for('main.index')) 
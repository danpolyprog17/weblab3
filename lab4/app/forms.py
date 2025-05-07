from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SelectField, SubmitField
from wtforms.validators import DataRequired, Length, ValidationError, EqualTo, Regexp

class LoginForm(FlaskForm):
    login = StringField('Login', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    submit = SubmitField('Login')

class UserForm(FlaskForm):
    login = StringField('Login', validators=[
        DataRequired(),
        Regexp(r'^[a-zA-Z0-9]+$', message='Login must contain only Latin letters and numbers'),
        Length(min=5, max=50, message='Login must be between 5 and 50 characters')
    ])
    password = PasswordField('Password', validators=[
        DataRequired(),
        Length(min=8, max=128, message='Password must be between 8 and 128 characters'),
        Regexp(r'^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)(?=.*[@$!%*?&])[A-Za-z\d@$!%*?&]+$',
               message='Password must contain at least one uppercase letter, one lowercase letter, one number, and one special character')
    ])
    first_name = StringField('First Name', validators=[DataRequired()])
    last_name = StringField('Last Name')
    middle_name = StringField('Middle Name')
    role_id = SelectField('Role', coerce=int)
    submit = SubmitField('Save')

class EditUserForm(FlaskForm):
    first_name = StringField('First Name', validators=[DataRequired()])
    last_name = StringField('Last Name')
    middle_name = StringField('Middle Name')
    role_id = SelectField('Role', coerce=int)
    submit = SubmitField('Save')

class ChangePasswordForm(FlaskForm):
    old_password = PasswordField('Old Password', validators=[DataRequired()])
    new_password = PasswordField('New Password', validators=[
        DataRequired(),
        Length(min=8, max=128, message='Password must be between 8 and 128 characters'),
        Regexp(r'^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)(?=.*[@$!%*?&])[A-Za-z\d@$!%*?&]+$',
               message='Password must contain at least one uppercase letter, one lowercase letter, one number, and one special character')
    ])
    confirm_password = PasswordField('Confirm Password', validators=[
        DataRequired(),
        EqualTo('new_password', message='Passwords do not match')
    ])
    submit = SubmitField('Change Password') 
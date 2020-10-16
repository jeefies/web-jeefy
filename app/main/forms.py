from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, BooleanField, FileField, PasswordField
from wtforms.validators import DataRequired, IPAddress, Length,  Regexp, EqualTo, Email


class NameForm(FlaskForm):
    name = StringField('Enter your name', validators=[DataRequired()])
    submit = SubmitField('Submit')


class LoginForm(FlaskForm):
    name = StringField('Enter your name or email', validators=[DataRequired()])
    password = PasswordField('How about your password?',
                             validators=[DataRequired()])
    submit = SubmitField('Submit')


class LogoutForm(FlaskForm):
    sure = BooleanField('Click to make sure')
    submit = SubmitField('Sure I do')


class RegisterForm(FlaskForm):
    username = StringField('User name(Do not use uncommon letter)', validators=[
                           DataRequired(), Length(3, 20)])
    email = StringField('Your email', validators=[DataRequired(), Email()])
    regist_passwd = StringField('Regist password', validators=[
                                DataRequired(), Length(4, 16)])
    password = PasswordField('Password', validators=[DataRequired(), EqualTo(
        'passwd', message='Password must match.'), Length(4, 16)])
    passwd = PasswordField('Confirm password', validators=[DataRequired()])
    submit = SubmitField('Submit')

from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, BooleanField, FileField, PasswordField, TextAreaField
from wtforms.validators import DataRequired, IPAddress, Length,  Regexp, EqualTo


class TestForm(FlaskForm):
    area = TextAreaField('Text area', validators=[DataRequired()])
    submit = SubmitField('Submit')


'''
class NameForm(FlaskForm):
    name = StringField('Enter your name', validators=[DataRequired()])
    submit = SubmitField('Submit')

class LoginForm(FlaskForm):
    name = StringField('Enter your name', validators=[DataRequired()])
    password = PasswordField('How about your password?', validators=[DataRequired()])
    submit = SubmitField('Submit')

class LogoutForm(FlaskForm):
    sure = BooleanField('Click to make sure')
    submit = SubmitField('Sure I do')

class RegisterForm(FlaskForm):
    username = StringField('User name', validators=[DataRequired(), Length(5,20), Regexp('^[A-Za-z][A-Za-z0-9_.]*$', 0, 'Username must only letters, numbers, dots or underscores.')])
    regist_passwd = StringField('Regist password', validators=[DataRequired(), Length(4,16)])
    password = PasswordField('Password', validators=[DataRequired(), EqualTo('passwd', message = 'Password must match.'), Length(4,16)])
    passwd = PasswordField('Confirm password', validators=[DataRequired()])
    submit = SubmitField('Submit')
'''
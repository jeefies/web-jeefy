from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, BooleanField, FileField, PasswordField, TextAreaField
from wtforms.validators import DataRequired, IPAddress, Length,  Regexp, EqualTo


class ChatForm(FlaskForm):
    con = TextAreaField('', validators=[DataRequired()])
    submit = SubmitField('put up')


class RegForm(FlaskForm):
    name = StringField('Room name', validators=[DataRequired(), Length(3, 10)])
    intro = TextAreaField(validators=[DataRequired()])
    passwd = PasswordField("Room Password(not required)")
    verifypasswd = PasswordField('verify your password', validators=[EqualTo('passwd')])
    submit = SubmitField()


class NameForm(FlaskForm):
    name = StringField('room name', validators=[DataRequired()])
    submit = SubmitField()

class PasswdForm(FlaskForm):
    passwd = PasswordField('the password to get into the room', validators=[DataRequired()])
    submit = SubmitField('Submit')
"""
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
"""

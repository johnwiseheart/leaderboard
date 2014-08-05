from wtforms.validators import Required, DataRequired
from flask_security.forms import RegisterForm
from wtforms import TextField, PasswordField
from flask.ext.security import Security
from app import app
from flask.ext.wtf import Form

class ExtendedRegisterForm(RegisterForm):
    email = TextField('Email Address', [DataRequired()])
    password = PasswordField('Password', [DataRequired()])
    retype_password = PasswordField('Retype Password', [DataRequired()])
    name = TextField('Team Name', [DataRequired()])
    players = TextField('Players', [DataRequired()])

# class LoginForm(Form):
#     remember_me = BooleanField('remember_me', default = False)

class PasswordForm(Form):
	password = TextField('password', validators = [DataRequired()])

# class SettingsForm(Form):
# 	name = TextField('name')
# 	players = TextField('players')
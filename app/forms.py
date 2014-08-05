from wtforms.validators import Required, DataRequired, Regexp, Length
from flask_security.forms import RegisterForm
from wtforms import TextField, PasswordField
from flask.ext.security import Security
from app import app
from flask.ext.wtf import Form
from models import Team

class ExtendedRegisterForm(RegisterForm):
    name = TextField('Team Name', [Regexp(r'^[\w._-]+$',message='You may only use alphanumeric characters, hyphens and underscores.'), Length(min=5, max=25,message="Password must be between 5 and 25 characters."), DataRequired()])
    players = TextField('Players', [DataRequired()])

class PasswordForm(Form):
	password = TextField('password', validators = [DataRequired()])

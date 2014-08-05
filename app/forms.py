from wtforms.validators import Required, DataRequired
from flask_security.forms import RegisterForm
from wtforms import TextField, PasswordField
from flask.ext.security import Security
from app import app
from flask.ext.wtf import Form
from models import Team

class ExtendedRegisterForm(RegisterForm):
    name = TextField('Team Name', [DataRequired()])
    players = TextField('Players', [DataRequired()])

class PasswordForm(Form):
	password = TextField('password', validators = [DataRequired()])

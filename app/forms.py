from flask.ext.wtf import Form
from wtforms import TextField, BooleanField
from wtforms.validators import DataRequired

class LoginForm(Form):
    remember_me = BooleanField('remember_me', default = False)

class PasswordForm(Form):
	password = TextField('password', validators = [DataRequired()])

class SettingsForm(Form):
	name = TextField('name')
	players = TextField('players')
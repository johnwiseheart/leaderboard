from flask import Flask
from flask.ext.sqlalchemy import SQLAlchemy
from flask_mail import Mail
from werkzeug.utils import secure_filename
import os




app = Flask(__name__)

app.config.from_object('config')
db = SQLAlchemy(app)
mail = Mail(app)



from leaderboard import views, models

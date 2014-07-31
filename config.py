import os
basedir = os.path.abspath(os.path.dirname(__file__))

SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(basedir, 'app.db')
SQLALCHEMY_MIGRATE_REPO = os.path.join(basedir, 'db_repository')

CSRF_ENABLED = True
SECRET_KEY = 'you-will-never-guess'

GOOGLE_LOGIN_CLIENT_ID	= "302093234688-2076di79tco6iqqd0bkm7o32o19hkf33.apps.googleusercontent.com"
GOOGLE_LOGIN_CLIENT_SECRET	= "DMiO05rGMA5AWa8bftLoCtzl"
GOOGLE_LOGIN_CLIENT_SCOPES = ".profile"
GOOGLE_LOGIN_REDIRECT_URI = "https://leaderboard.johnwiseheart.me/oauth2callback"
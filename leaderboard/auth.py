from flask.ext.security import Security, SQLAlchemyUserDatastore, \
    UserMixin, RoleMixin, login_required
from app import app, db
from models import Team, Role
# Setup Flask-Security
user_datastore = SQLAlchemyUserDatastore(db, Team, Role)
security = Security(app, user_datastore)
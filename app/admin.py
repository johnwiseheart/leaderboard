from flask.ext.admin import Admin, expose
from flask.ext.admin.contrib.sqla import ModelView
from app import app, db
from models import Team, Event, Role
from flask.ext.security import UserMixin, login_required, current_user


class MyView(ModelView):
    def is_accessible(self):
    	if not current_user.is_authenticated(): 
    		return False
        return current_user.has_role('Admin')



admin = Admin(app, name="Leaderboard")
admin.add_view(MyView(Team, db.session))
admin.add_view(MyView(Event, db.session))
admin.add_view(MyView(Role, db.session))
from flask import g

from flask.ext.admin import Admin, expose
from flask.ext.admin.contrib.sqla import ModelView
from app import app, db
from models import Team, Event, ROLE_TEAM, ROLE_ADMIN

class MyView(ModelView):
    def is_accessible(self):
    	if g.team.is_authenticated():
    		return g.team.role == ROLE_ADMIN
    	return False


admin = Admin(app, name="Leaderboard")
admin.add_view(MyView(Team, db.session))
admin.add_view(MyView(Event, db.session))
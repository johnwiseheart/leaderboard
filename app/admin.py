from flask.ext.admin import Admin, expose
from flask.ext.admin.contrib.sqla import ModelView
from app import app, db
from models import Team, Event, Role
from flask.ext.security import UserMixin, login_required, current_user


class AdminView(ModelView):
    @expose('/')
    def index(self):
        # Get URL for the test view method
        url = url_for('.test')
        return self.render('index.html', url=url)

    column_exclude_list = ('password','unlock_message')

    def is_accessible(self):
    	if not current_user.is_authenticated(): 
    		return False
        return current_user.has_role('Admin')

class TeamAdminView(AdminView):
	form_excluded_columns = ('password')

admin = Admin(app, name="Leaderboard", endpoint='admin')
admin.add_view(TeamAdminView(Team, db.session))
admin.add_view(AdminView(Event, db.session))
admin.add_view(AdminView(Role, db.session))
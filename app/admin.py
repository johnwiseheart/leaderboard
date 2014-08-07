from flask.ext.admin import Admin, expose, BaseView, form
from flask.ext.admin.contrib.sqla import ModelView
from app import app, db
from models import *
from flask.ext.security import UserMixin, login_required, current_user
from jinja2 import Markup
from flask import url_for, flash
import os
import os.path as op
import PIL

file_path = op.join(op.dirname(__file__), 'static')

class AdminView(ModelView):
    column_exclude_list = ('password','unlock_message')
    form_widget_args = {
        'filename':{
            'disabled':True
        }
    }
    def is_accessible(self):
    	if not current_user.is_authenticated(): 
    		return False
        return current_user.has_role('Admin')

    @expose('/imagelist')
    def image_list(self):
        return self.render('admin/index.html')

class AdminImageView(AdminView):
    def _list_thumbnail(view, context, model, name):
        if not model.filename:
            return ''

        return Markup('<img src="%s">' % url_for('uploaded_file',
                                                 filename=model.filename))

    def after_model_change(self,form, model, is_created):
    	t = Team.query.filter_by(id = model.team.id).first()
    	t.events.append(model.event)
    	db.session.commit()
    	

    column_formatters = {
        'filename': _list_thumbnail
    }

     # Alternative way to contribute field is to override it completely.
    # In this case, Flask-Admin won't attempt to merge various parameters for the field.
    form_extra_fields = {
        'filename': form.ImageUploadField('Image',
                                      base_path=file_path)
    }

class TeamAdminView(AdminView):
	form_excluded_columns = ('password')
	form_columns = ('email', 'name', 'players', 'roles', 'events', 'active', 'last_password_time')


class EventAdminView(AdminView):
	form_columns = ('name', 'description', 'password', 'unlock_message', 'points', 'teams')



admin = Admin(app, name="Leaderboard", endpoint='admin')
admin.add_view(TeamAdminView(Team, db.session, endpoint="teams"))
admin.add_view(EventAdminView(Event, db.session, endpoint="events"))
admin.add_view(AdminView(Role, db.session, endpoint="roles"))
admin.add_view(AdminImageView(Image, db.session, endpoint="images"))
admin.add_view(AdminView(Metadata, db.session, endpoint="settings"))
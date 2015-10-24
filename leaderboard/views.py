from flask import render_template, flash, g, redirect, Response, url_for, request
from flask.ext.security import Security, SQLAlchemyUserDatastore, UserMixin, RoleMixin, login_required, current_user
from leaderboard import app, db, admin, forms
from models import *
from forms import PasswordForm
from datetime import datetime
from flask.ext.security.signals import user_registered
from flask.ext.wtf import Form
from flask import send_from_directory
from werkzeug.utils import secure_filename
import os
from calendar import timegm
import time

# Setup Flask-Security
user_datastore = SQLAlchemyUserDatastore(db, Team, Role)
security = Security(app, user_datastore, register_form=forms.ExtendedRegisterForm)


@app.before_request
def before_request():
    g.team = current_user

@user_registered.connect_via(app)
def user_registered_sighandler(app, user, confirm_token):
    default_role = user_datastore.find_role("Team")
    user_datastore.add_role_to_user(user, default_role)
    db.session.commit()

@app.route('/')
@app.route('/index')
def index():
    g.team = current_user
    metadata = Metadata.query.filter_by(key='time').first()
    return render_template('index.html',
        title = 'Home',
        metadata=metadata)

@app.route('/uploads/<filename>')
def uploaded_file(filename):
    return send_from_directory(app.config['UPLOAD_FOLDER'],
                               filename)

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1] in app.config['ALLOWED_EXTENSIONS']

@app.route('/upload', methods=['GET', 'POST'])
@login_required
def upload_file():
    if request.method == 'POST':
        file = request.files['file']
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))

            f = Image(file.filename, g.team.id, datetime.utcnow())
            db.session.add(f)
            db.session.commit()
            flash("Image submitted. An admin will shortly process it.", 'info')
            return redirect(url_for('index'))
        else:
        	flash("This type of file not allowed", 'danger')
    return render_template('submit_image.html',
		title = 'Submit Password')

@app.route('/help')
def help():
    return render_template('help.html',
        title = 'Help')

@app.route('/submit', methods = ['GET', 'POST'])
@login_required
def password_submit():
	form = PasswordForm()
	if form.validate_on_submit():
		#if the password matches any of the events
		#add that event to the user

		m = Metadata.query.filter_by(key='time').first()
		e = Event.query.filter_by(password = form.password.data).first()
		if int(timegm(time.gmtime()))<int(m.data):
			# if it finds a password that matches
			if e and form.password.data:
				# get the current team
				t = Team.query.filter_by(email = g.team.email).first()
				# if the event isnt in the teams events, add it
				if not e in t.events:
					if e.unlock_message:
						flash(e.unlock_message, 'info')
					else:
						flash("Task " + e.name + " completed.")
					t.last_password_time = datetime.utcnow()
					t.events.append(e)
					db.session.commit()
					return redirect(url_for('index'))
				#otherwise flash nope
				else:
					flash("You have already completed this task.", 'warning')
			else: 
				flash("I don't think so. Try again!", 'warning')
		else:
			flash("The competition has ended! You can't submit any more!", 'warning')
			
	return render_template('submit.html',
		title = 'Submit Password',
		form = form)

@app.route('/team/<name>')
def team_page(name):
    team = user_datastore.find_user(name=name)
    if team == None:
        flash('That team was not found.', 'info')
        return redirect(url_for('index'))

    return render_template('team.html',
        team = team)

@app.route('/event/<id>')
def event_page(id):
    m = Metadata.query.filter_by(key='time').first()
    if int(m.data) == -1:
	flash("You cannot view this yet")
	return redirect(url_for('index'))
    event = Event.query.filter_by(id = id).first()
    if event == None:
        flash('That event was not found.', 'info')
        return redirect(url_for('index'))

    return render_template('event.html',
        event = event)

@app.route('/events')
def events():
    m = Metadata.query.filter_by(key='time').first()
    if int(m.data) == -1:
	flash("You cannot view this yet")
	return redirect(url_for('index'))
    events = Event.query.all()
    return render_template('events.html',
    	title = "Events List",
        events = events)

@app.route('/json')
def json_out():
    teams = Team.query.all()
    json_out = '['
    for team in teams:
    	if team.has_role('Team'):
	    	json_out += '{"team":"'
	    	json_out += team.name
	    	json_out += '","points":"'
	    	json_out += str(team.getPoints())
	    	json_out += '"},'
    json_out = json_out[:-1]
    json_out += ']'

    return Response(response=json_out,
    				status=200,
    	 			mimetype="application/json")

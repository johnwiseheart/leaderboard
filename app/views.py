from flask import render_template, flash, g, redirect, Response, url_for
from flask.ext.security import Security, SQLAlchemyUserDatastore, UserMixin, RoleMixin, login_required, current_user
from app import app, db, admin, forms
from models import Team, Role, Event
from forms import PasswordForm
from datetime import datetime
from flask.ext.security.signals import user_registered


# Setup Flask-Security
user_datastore = SQLAlchemyUserDatastore(db, Team, Role)
security = Security(app, user_datastore)


@app.before_request
def before_request():
    g.team = current_user

@user_registered.connect_via(app)
def user_registered_sighandler(app, user, confirm_token):
    default_role = user_datastore.find_role("Team")
    user.name = user.email
    user_datastore.add_role_to_user(user, default_role)
    db.session.commit()

@app.route('/')
@app.route('/index')
def index():
    team = current_user
    g.team = current_user
    return render_template('index.html',
        title = 'Home',
        team = team)

@app.route('/submit', methods = ['GET', 'POST'])
@login_required
def password_submit():
	pass
	form = PasswordForm()
	if form.validate_on_submit():
		#if the password matches any of the events
		#add that event to the user


		e = Event.query.filter_by(password = form.password.data).first()
		# if it finds a password that matches
		if e:
			
			# get the current team
			t = Team.query.filter_by(email = g.team.email).first()
			# if the event isnt in the teams events, add it
			if not e in t.events:
				if e.unlock_message:
					flash(e.unlock_message)
				else:
					flash("Task " + e.name + " completed.")
				t.last_password_time = datetime.utcnow()
				t.events.append(e)
				db.session.commit()
				return redirect(url_for('index'))
			#otherwise flash nope
			else:
				if e.unlock_message:
					flash(e.unlock_message)
				flash("You have already completed this task.")
			
	return render_template('submit.html',
		title = 'Submit Password',
		form = form)

@app.route('/team/<email>')
def team_page(email):
    team = user_datastore.find_user(email=email)
    if team == None:
        flash('That team was not found.')
        return redirect(url_for('index'))

    return render_template('team.html',
        team = team)

@app.route('/event/<id>')
def event_page(id):
    event = Event.query.filter_by(id = id).first()
    if event == None:
        flash('That event was not found.')
        return redirect(url_for('index'))

    return render_template('event.html',
        event = event)

@app.route('/events')
def events():
    events = Event.query.all()
    return render_template('events.html',
        events = events)

@app.route('/json')
def json_out():
    teams = Team.query.all()
    json_out = '['
    for team in teams:
    	if team.has_role('Team'):
	    	json_out += '{"team":"'
	    	json_out += team.email
	    	json_out += '","points":"'
	    	json_out += str(team.getPoints())
	    	json_out += '"},'
    json_out = json_out[:-1]
    json_out += ']'

    return Response(response=json_out,
    				status=200,
    	 			mimetype="application/json")

from flask import render_template, flash, redirect, session, url_for, request, g, Response
from flask.ext.login import login_required
from app import app, db, lm, auth, admin
from models import Team, Event, ROLE_TEAM, ROLE_ADMIN
from forms import PasswordForm, SettingsForm
from flask.ext.wtf import Form
from wtforms.ext.sqlalchemy.orm import model_form

@app.route('/')
@app.route('/index')
def index():
    team = g.team
    return render_template('index.html',
        title = 'Home',
        team = team)

@app.route('/submit', methods = ['GET', 'POST'])
@login_required
def password_submit():
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
				flash("Task " + e.name + " completed.")
				t.events.append(e)
				db.session.commit()
				return redirect(url_for('index'))
			#otherwise flash nope
			else:
				flash("You have already completed this task.")
			
	return render_template('submit.html',
		title = 'Submit Password',
		form = form)

@app.route('/settings', methods = ['GET', 'POST'])
@login_required
def settings():
	t = Team.query.filter_by(email = g.team.email).first()
	form = SettingsForm(obj=t)
	if form.validate_on_submit():
		t = Team.query.filter_by(email = g.team.email).first()
		t.name = form.name.data
		t.players = form.players.data
		db.session.commit()
	return render_template('settings.html',
		title = 'Settings',
		form = form)

@app.route('/team/<name>')
def team_page(name):
    team = Team.query.filter_by(name = name).first()
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

@app.route('/json')
def json_out():
    teams = Team.query.all()
    json_out = '['
    for team in teams:
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

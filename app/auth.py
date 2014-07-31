from flask import render_template, flash, redirect, session, url_for, request, g
from flask.ext.login import login_user, logout_user, current_user, login_required
from app import app, db, lm, oid
from forms import LoginForm
from models import Team, Event, ROLE_TEAM, ROLE_ADMIN

@lm.user_loader
def load_user(id):
    return Team.query.get(int(id))

@app.before_request
def before_request():
    g.team = current_user

@app.route('/login', methods = ['GET', 'POST'])
@oid.loginhandler
def login():
    if g.team is not None and g.team.is_authenticated():
        return redirect(url_for('index'))
    form = LoginForm()
    if form.validate_on_submit():
        session['remember_me'] = form.remember_me.data
        return oid.try_login("https://www.google.com/accounts/o8/id", ask_for = ['nickname', 'email'])
    return render_template('login.html', 
        title = 'Sign In',
        form = form,
        providers = app.config['OPENID_PROVIDERS'])

@oid.after_login
def after_login(resp):
    if resp.email is None or resp.email == "":
        flash('Invalid login. Please try again.')
        return redirect(url_for('login'))
    team = Team.query.filter_by(email = resp.email).first()
    if team is None:
        name = resp.nickname
        if name is None or name == "":
            name = resp.email.split('@')[0]
        team = Team(name = name, email = resp.email, role = ROLE_TEAM)
        db.session.add(team)
        db.session.commit()
    remember_me = False
    if 'remember_me' in session:
        remember_me = session['remember_me']
        session.pop('remember_me', None)
    login_user(team, remember = remember_me)
    return redirect(request.args.get('next') or url_for('index'))


@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('index'))

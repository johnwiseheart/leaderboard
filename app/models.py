from app import db
from flask import Flask, render_template
from flask.ext.sqlalchemy import SQLAlchemy
from flask.ext.security import Security, SQLAlchemyUserDatastore, \
    UserMixin, RoleMixin, login_required

events = db.Table('events',
    db.Column('event_id', db.Integer, db.ForeignKey('event.id')),
    db.Column('team_id', db.Integer, db.ForeignKey('team.id'))
)


roles_users = db.Table('roles_users',
        db.Column('team_id', db.Integer(), db.ForeignKey('team.id')),
        db.Column('role_id', db.Integer(), db.ForeignKey('role.id')))

class Team(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key = True)
    email = db.Column(db.String(120), unique = True)
    password = db.Column(db.String(255))
    active = db.Column(db.Boolean())
    name = db.Column(db.String(64), index = True, unique = True)
    players = db.Column(db.String(255))
    last_password_time = db.Column(db.DateTime)
    events = db.relationship('Event', secondary=events,
        backref=db.backref('teams', lazy='dynamic'))
    roles = db.relationship('Role', secondary=roles_users,
                            backref=db.backref('teams', lazy='dynamic'))

    def get_id(self):
        return self.id

    def is_active(self):
        return self.active

    def is_authenticated(self):
        return True

    def is_anonymous(self):
        return False

    def getPoints(self):
        points = 0
        for event in self.events:
            points += event.points
        return points


    def __repr__(self):
        return '<Team %r>' % (self.name)

class Role(db.Model, RoleMixin):
    id = db.Column(db.Integer(), primary_key=True)
    name = db.Column(db.String(80), unique=True)
    description = db.Column(db.String(255))

    def __repr__(self):
        return '<Role %r>' % (self.name)

class Event(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    name = db.Column(db.String(140))
    description = db.Column(db.String(255))
    password = db.Column(db.String(140), index = True, unique = True)
    points = db.Column(db.Integer)
    unlock_message = db.Column(db.String(255))

    def __repr__(self):
        return '<Event %r>' % (self.name)
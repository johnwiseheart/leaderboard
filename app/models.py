from app import db

ROLE_TEAM = 0
ROLE_ADMIN = 1

events = db.Table('events',
    db.Column('event_id', db.Integer, db.ForeignKey('event.id')),
    db.Column('team_id', db.Integer, db.ForeignKey('team.id'))
)

class Team(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    email = db.Column(db.String(120), unique = True)
    name = db.Column(db.String(64), index = True, unique = True)
    players = db.Column(db.String(255))
    role = db.Column(db.SmallInteger, default = ROLE_TEAM)
    events = db.relationship('Event', secondary=events,
        backref=db.backref('teams', lazy='dynamic'))
	
    def is_authenticated(self):
        return True

    def is_active(self):
        return True

    def is_anonymous(self):
        return False

    def is_admin(self):
    	return self.role==ROLE_ADMIN

    def get_id(self):
        return unicode(self.id)

    def getPoints(self):
        points = 0
        for event in self.events:
            points += event.points
        return points


    def __repr__(self):
        return '<Team %r>' % (self.name)

class Event(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    name = db.Column(db.String(140))
    description = db.Column(db.String(255))
    password = db.Column(db.String(140), index = True, unique = True)
    points = db.Column(db.Integer)

    def __repr__(self):
        return '<Event %r>' % (self.name)
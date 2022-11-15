from datetime import datetime
from app import db

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), index=True, unique=True)
    personalnummer = db.Column(db.Integer, index=True, unique=True)

    def __repr__(self):
        return f"User {self.username}"

class Buchungen(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    timestamp = db.Column(db.DateTime, index=True, default=datetime.utcnow)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    kommen = db.Column(db.DateTime, default=datetime.utcnow)
    gehen = db.Column(db.DateTime)

    def __repr__(self):
        return f"Gestempelt um: {self.timestamp}"



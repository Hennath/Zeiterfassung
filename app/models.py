from datetime import datetime
from app import db

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    vorname = db.Column(db.String(64), index=True)
    nachname = db.Column(db.String(64), index=True)
    personalnummer = db.Column(db.Integer, index=True, unique=True)
    #anwesend = db.Column(db.Boolean, default=False)

    def kommen(self):
        if not self.anwesend:
            self.anwesend = True

    def __repr__(self):
        return f"User {self.vorname} {self.nachname} Personalnummer{self.personalnummer}"

class Buchungen(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    timestamp = db.Column(db.DateTime, index=True, default=datetime.utcnow)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    kommen = db.Column(db.Boolean, default=False)
    gehen = db.Column(db.Boolean, default=False)

    def __repr__(self):
        return f"Gestempelt um: {self.timestamp}"



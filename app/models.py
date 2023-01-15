from datetime import datetime
from app import db


class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    vorname = db.Column(db.String(64), index=True)
    nachname = db.Column(db.String(64), index=True)
    personalnummer = db.Column(db.Integer, index=True, unique=True)
    # Relationship between User and Buchungen
    buchungen = db.relationship("Buchungen", back_populates="user", lazy=True)
    

    
    # Stamp function. vorgang argument: either stamp in or out
    def stempeln(self, vorgang):
        # Check for last entry for this user
        letzte_buchung = (
            Buchungen.query.filter(Buchungen.user_id == self.id)
            .order_by(Buchungen.timestamp.desc())
            .first()
        )
        # Check if user's last entry was stampig in or out
        if letzte_buchung:
            if getattr(letzte_buchung, vorgang):
                # Error if user was already stamped in/out
                return f"Fehler: {vorgang} bereits vorhanden!"

        # Create Buchungen object for this entry
        b = Buchungen(user_id=self.id)
        # Set vorgang attribute in Buchungen to True
        setattr(b, vorgang, True)
        # Commit entry to database
        db.session.add(b)
        db.session.commit()
        return f"{self.vorname} {self.nachname} - {vorgang} um {b.timestamp}"

    # Needed for grid.js
    def to_dict(self):
        return {
            "id": self.id,
            "vorname": self.vorname,
            "nachname": self.nachname,
            "personalnummer": self.personalnummer,
        }

    def __repr__(self):
        return (
            f"User {self.vorname} {self.nachname} Personalnummer{self.personalnummer}"
        )


class Buchungen(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    timestamp = db.Column(db.DateTime, index=True, default=datetime.utcnow)
    user_id = db.Column(db.Integer, db.ForeignKey("user.id"))
    kommen = db.Column(db.Boolean, default=False)
    gehen = db.Column(db.Boolean, default=False)
    # Relationship between User and Buchungen
    user = db.relationship("User", back_populates="buchungen", lazy=True)

    def to_dict(self):
        if self.kommen:
            return {
                "id": self.id,
                "timestamp": self.timestamp,
                "user_id": self.user_id,
                "vorgang": "kommen",
                "user": self.user.vorname,
            }

        if self.gehen:
            return {
                "id": self.id,
                "timestamp": self.timestamp,
                "user_id": self.user_id,
                "vorgang": "gehen",
                "user": self.user.vorname,
            }

    def __repr__(self):
        return f"Gestempelt um: {self.timestamp}"

import rfid.read as read
from app import app, db, migrate
from app.models import Buchungen, User
from datetime import datetime

app_context = app.app_context()
app_context.push()

rfid = read.read()
print("read rfid")
print(f"{rfid}")

if(rfid):
    u = User(
            vorname="Meppo", nachname="Meppersen", personalnummer=f"{rfid}"
        )
    db.session.add(u)
    db.session.commit()
    print("added user")
import rfid.read as read
from app import app, db, migrate
from app.models import Buchungen, User
from datetime import datetime

app_context = app.app_context()
app_context.push()


name = input("User name: ")
last_name = input("User last name: ")
print("RFID tag please")
rfid = read.read()
print("read rfid")
print(f"{rfid}")

if(rfid):
    u = User(
            vorname=name, nachname=last_name, personalnummer=f"{rfid}"
        )
    db.session.add(u)
    db.session.commit()
    print("added user")
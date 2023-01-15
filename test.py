from app import app, db
from app.models import Buchungen, User

app_context = app.app_context()
app_context.push()


users = User.query.all()

for user in users:
    print("-------------------------------------")
    print("Vorname: ", user.vorname)
    print("Nachname: ", user.nachname)
    print("Personalnummer: ", user.personalnummer)
    #print("Anwesend:", user.anwesend)

buchungen = Buchungen.query.all()

for b in buchungen:
    print("-------------------------------------")
    print("ID: ", b.id)
    print("Timestamp: ", b.timestamp)
    print("User ID:", b.user_id)
    print("User: ", b.user)
    print("Kommen: ", b.kommen)
    print("Gehen: ", b.gehen)

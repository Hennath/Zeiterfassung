from app import app, db
from app.models import Buchungen, User

app_context = app.app_context()
app_context.push()



def stempeln(ein_aus):
    if ein_aus == "kommen":
        u = User.query.filter(User.personalnummer == 111111).first()          
        b = Buchungen(user_id=u.id, gehen=True)
        db.session.add(b)
        db.session.commit()




users = User.query.filter(User.personalnummer == 111111).all()

stempeln("kommen")
# for user in users:
#     print("Vorname: ", user.vorname)
#     print("Nachname: ", user.nachname)
#     print("Personalnummer: ", user.personalnummer)
#     #print("Anwesend:", user.anwesend)

buchungen = Buchungen.query.all()

for b in buchungen:
    print("ID: ", b.id)
    print("Timestamp: ", b.timestamp)
    print("User ID:", b.user_id)
    print("Kommen: ", b.kommen)
    print("Gehen: ", b.gehen)
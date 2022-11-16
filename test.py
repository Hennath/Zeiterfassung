from app import app, db
from app.models import User, Buchungen

app_context = app.app_context()
app_context.push()


users = User.query.all()

for user in users:
    print("Vorname: ", user.vorname)
    print("Nachname: ", user.nachname)
    print("Personalnummer: ", user.personalnummer)
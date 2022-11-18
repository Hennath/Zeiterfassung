from app import app, db
from app.models import Buchungen, User

app_context = app.app_context()
app_context.push()

db.session.query(User).delete()
db.session.query(Buchungen).delete()




for i in range(1, 6):
    u = User(vorname=f"user{i}", nachname=f"Fluser{i}", personalnummer=f"{i}{i}{i}{i}{i}{i}")
    db.session.add(u)

db.session.commit()
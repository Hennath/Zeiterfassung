from app import app, db
from app.models import Buchungen, User

app_context = app.app_context()
app_context.push()


def stempeln(vorgang):
    u = User.query.filter(User.personalnummer == 111111).first()
    letzte_buchung = (
        Buchungen.query.filter(Buchungen.user_id == u.id)
        .order_by(Buchungen.timestamp.desc())
        .first()
    )
    print(letzte_buchung)
    # if vorgang == "kommen":
    if letzte_buchung:
        if getattr(letzte_buchung, vorgang):
            # if letzte_buchung.kommen:
            print(f"Fehler: {vorgang} bereits vorhanden!")

    # b = Buchungen(user_id=u.id, kommen=True)
    b = Buchungen(user_id=u.id)
    setattr(b, vorgang, True)
    db.session.add(b)
    db.session.commit()
    print(f"{u.vorname} {u.nachname} - {vorgang} um {b.timestamp}")
    # elif vorgang == "gehen":
    #     if letzte_buchung.gehen:
    #         print("User noch nicht eingestempelt")
    #     else:
    #         b = Buchungen(user_id=u.id, gehen=True)
    #         db.session.add(b)
    #         db.session.commit()


users = User.query.filter(User.personalnummer == 111111).all()
buchungen = Buchungen.query.filter(Buchungen.id == 1).first()

stempeln("kommen")
# for user in users:
#     print("Vorname: ", user.vorname)
#     print("Nachname: ", user.nachname)
#     print("Personalnummer: ", user.personalnummer)
#     #print("Anwesend:", user.anwesend)

# buchungen.gehen = True
# db.session.commit()

buchungen2 = Buchungen.query.all()

# for b in buchungen2:
#     print("ID: ", b.id)
#     print("Timestamp: ", b.timestamp)
#     print("User ID:", b.user_id)
#     print("Kommen: ", b.kommen)
#     print("Gehen: ", b.gehen)

# buchungen.gehen = True
# db.session.commit()

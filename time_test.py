from app import app, db, migrate
from app.models import Buchungen, User
from datetime import datetime
import rfid.mark as mark

app_context = app.app_context()
app_context.push()


# u = User.query.first()
# print(u)

# b = Buchungen.query.filter(Buchungen.user_id == u.id).all()
# for i in b:
#     print(i.timestamp)

# print(b[0].timestamp-b[1].timestamp)

# user = User.query.get(1)
buchungen = User.query.get(1).buchungen
# #print(user)
for b in buchungen:
    print(b.to_dict())

print(buchungen.to_dict() for buchungen in User.query.get(1).buchungen)

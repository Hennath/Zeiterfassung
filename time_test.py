from app import app, db
from app.models import Buchungen, User
from datetime import datetime

app_context = app.app_context()
app_context.push()

u = User.query.first()
print(u)

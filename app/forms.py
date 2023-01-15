from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField
from wtforms.validators import DataRequired

# Form used for users to check in with their user code
class CodeForm(FlaskForm):
    user_code = StringField("Personalnummer", validators=[DataRequired()])
    submit = SubmitField("Anmelden")

# Form used for creating new users
class UserForm(FlaskForm):
    vorname = StringField("Vorname", validators=[DataRequired()])
    nachname = StringField("Nachname", validators=[DataRequired()])
    user_code = StringField("Personalnummer", validators=[DataRequired()])
    submit = SubmitField("Anlegen")

from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField
from wtforms.validators import DataRequired

class CodeForm(FlaskForm):
    user_code = StringField('Personalnummer', validators=[DataRequired()])
    submit = SubmitField('Anmelden')


from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField

class SubmitForm(FlaskForm):
    cowID = StringField('cowID')
    submit= SubmitField('submit')
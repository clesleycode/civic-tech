from flask_wtf import Form
from wtforms import StringField, BooleanField, DateField, SelectField, TextField, IntegerField, SubmitField
from wtforms import validators


class LoginForm(Form):
	remember_me = BooleanField('remember_me', default=False)


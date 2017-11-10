from flask_wtf import Form
from wtforms import StringField, BooleanField, DateField, SelectField, TextField, IntegerField, SubmitField
from wtforms import validators


class LoginForm(Form):
	remember_me = BooleanField('remember_me', default=False)


class Companies(Form): 
	name = TextField('name')
	address = StringField('Address', validators=None)


class Contacts(Form):
	name = StringField('name', validators=None)
	company = SelectField('type', choices=insert_student.get_companies())
	number = TextField('Phone Number', [validators.length(max=11)])
	email = TextField('email', validators=[validators.Email()])
	position = StringField('Position', validators=None)
	notes = StringField('Notes', validators=None)

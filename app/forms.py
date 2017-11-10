from flask_wtf import Form
from wtforms import StringField, BooleanField, DateField, SelectField, TextField, IntegerField, SubmitField
from wtforms import validators
import db_functions


class LoginForm(Form):
	remember_me = BooleanField('remember_me', default=False)


class AddCompanies(Form): 
	name = TextField('name')
	address = StringField('Address', validators=None)


class Contacts(Form):
	name = StringField('name', validators=None)
	company = SelectField('type', choices=db_functions.get_companies())
	number = TextField('Phone Number', [validators.length(max=11)])
	email = TextField('email', validators=[validators.Email()])
	position = StringField('Position', validators=None)
	notes = StringField('Notes', validators=None)

class AddCompany(Form):
	name = TextField('name')


class AddTechTalks(Form):
	name = TextField('name')

class AddWorkshop(Form):
	name =  StringField('Workshop Name', validators=None)

class AddProjects(Form):
	name =  StringField('Pillar Name', validators=None)

class AddEvents(Form):
	name = StringField('Pillar Name', validators=None)
	location = StringField('Location', validators=None)
	eventTime = DateField('Event Time', [validators.Required()], format='%d/%m/%Y')
	numberAttendees = StringField('Number of Attendees', validators=None)

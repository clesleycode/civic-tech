"""from flask_wtf import FlaskForm
from wtforms import StringField, BooleanField, DateField, SelectField, TextField, IntegerField, SubmitField
from wtforms import validators"""
import db_functions

#from flask_wtf import Form
from wtforms import  StringField, BooleanField, DateField, SelectField, TextField, IntegerField, SubmitField
from wtforms.validators import Required, InputRequired, Email
from flask_wtf import FlaskForm as Form
class LoginForm(Form):
	remember_me = BooleanField('remember_me', default=False)


class AddCompanies(Form): 
	name = StringField('name')
	address = StringField('Address', validators=None)


class Contacts(Form):
	name = StringField('name', validators=None)
	company = SelectField('type', choices=db_functions.get_companies())
	number = StringField('Phone Number',  [InputRequired("Please enter your number.")])
	email = StringField('email', validators= [InputRequired("Please enter your email address."), Email("This field requires a valid email address")])
	position = StringField('Position', validators=None)
	notes = StringField('Notes', validators=None)

class AddCompany(Form):
	name = StringField('name')


class AddTechTalks(Form):
	name = StringField('name')

class AddWorkshop(Form):
	name =  StringField('Workshop Name', validators=None)

class AddProjects(Form):
	name =  StringField('Pillar Name', validators=None)

class AddEvents(Form):
	name = StringField('Pillar Name', validators=None)
	location = StringField('Location', validators=None)
	eventTime = DateField('Event Time', [InputRequired("Please enter event date")])
	numberAttendees = StringField('Number of Attendees', validators=None)

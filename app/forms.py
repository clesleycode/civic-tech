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


class Person(Form):
	name = StringField('name')
	semester_start = StringField('semester-start')
	project = SelectField('type', choices=db_functions.get_projects())
	company = SelectField('type', choices=db_functions.get_companies())

class AddCompany(Form):
	name = StringField('name')


class AddTechTalks(Form):
	name = StringField('name')
	company = SelectField('type', choices=db_functions.get_companies())

class AddWorkshop(Form):
	name =  StringField('Workshop Name')
	hosts = SelectField('type', choices=db_functions.get_users())

class AddProjects(Form):
	name =  StringField('Pillar Name', validators=None)

class AddEvents(Form):
	name = StringField('Pillar Name', validators=None)
	location = StringField('Location', validators=None)
	eventTime = DateField('Event Time', [InputRequired("Please enter event date")])
	numberAttendees = StringField('Number of Attendees', validators=None)

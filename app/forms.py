"""from flask_wtf import FlaskForm
from wtforms import StringField, BooleanField, DateField, SelectField, TextField, IntegerField, SubmitField
from wtforms import validators"""
import db_functions

#from flask_wtf import Form
from wtforms import  StringField, BooleanField, DateField, SelectField, TextField, IntegerField, SubmitField, DateTimeField, validators
from wtforms.validators import Required, InputRequired, Email
from flask_wtf import FlaskForm as Form
import datetime
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
	name =  StringField('Pillar Name')

class AddEvents(Form):
	name = StringField('Pillar Name')
	location = StringField('Location')
	#eventTime = DateField('Event Time')
	eventTime = DateTimeField(
        "Until", format="%Y-%m-%dT%H:%M:%S",
        default=datetime.date.today(), ## Now it will call it everytime.
        validators=[validators.DataRequired()])
	numberAttendees = StringField('Number of Attendees')
	pillar = SelectField('type', choices=db_functions.get_projects())

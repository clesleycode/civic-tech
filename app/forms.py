#import db_functions
from wtforms import  StringField, BooleanField, DateField, SelectField, TextField, IntegerField, SubmitField, DateTimeField, validators
from wtforms.validators import Required, InputRequired, Email
from flask_wtf import FlaskForm as Form
import datetime


class LoginForm(Form):
	remember_me = BooleanField('remember_me', default=False)


class AddCompanies(Form): 
	name = StringField('name')

'''
class Person(Form):
	name = StringField('name')
	semester_start = StringField('semester-start')
	#project = SelectField('type', choices=db_functions.get_projects())
	#company = SelectField('type', choices=db_functions.get_companies())
	project = SelectField('type')
	company = SelectField('company')
	def __init__(self, *args, **kwargs):
		super(Person, self).__init__(*args, **kwargs)
		self.project.choices = db_functions.get_projects()
		self.company.choices = db_functions.get_companies()
'''

class AddCompany(Form):
	name = StringField('name')

'''
class AddTechTalks(Form):
	name = StringField('name')
	company = SelectField('company')
	def __init__(self, *args, **kwargs):
		super(AddTechTalks, self).__init__(*args, **kwargs)
		self.company.choices = db_functions.get_companies()

'''
class UpdateTechTalk(Form):
	name = StringField('name')
	talkId = SelectField('type')
	def __init__(self, *args, **kwargs):
		super(UpdateTechTalk, self).__init__(*args, **kwargs)
		self.talkId.choices = db_functions.get_techtalks_names()


class AddJob(Form):
	name =  StringField('Company')
	hosts = SelectField('Position')
	def __init__(self, *args, **kwargs):
		super(AddJob, self).__init__(*args, **kwargs)
		self.hosts.choices = ["Software Engineer", "Data Scientist", "Product Manager"]


class AddProjects(Form):
	name =  StringField('Pillar Name')

'''
class AddEvents(Form):
	name = StringField('Pillar Name')
	location = StringField('Location')
	eventTime = DateTimeField(
        "Until", format="%Y-%m-%dT%H:%M:%S",
        default=datetime.date.today(), ## Now it will call it everytime.
        validators=[validators.DataRequired()])
	numberAttendees = StringField('Number of Attendees')
	pillar = SelectField('type')
	def __init__(self, *args, **kwargs):
		super(AddEvents, self).__init__(*args, **kwargs)
		self.pillar.choices = db_functions.get_projects()


class RemoveEvents(Form):
	events_list = SelectField('type')
	def __init__(self, *args, **kwargs):
		super(RemoveEvents, self).__init__(*args, **kwargs)
		self.events_list.choices = db_functions.get_event_ids()
'''

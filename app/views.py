from app import app
from flask import render_template, flash, redirect, g, make_response, request, url_for
from .forms import LoginForm
import json
import flask
import httplib2
from apiclient import discovery
import requests 
from oauth2client import client
from flask_basicauth import BasicAuth
from wtforms.validators import DataRequired
from flask_oauthlib.client import OAuth
import db_functions
from .forms import AddCompanies, Person, AddCompany, AddTechTalks, AddWorkshop, AddProjects, AddEvents
import requests 
import psycopg2

basic_auth = BasicAuth(app)

oauth = OAuth(app)
app.debug = True
app.secret_key = 'kj1VHtx6sPDLUL1L'

@app.route('/', methods=['GET', 'POST'])
def index():
	if 'credentials' not in flask.session:
		return flask.redirect(flask.url_for('oauth2callback'))
	credentials = client.OAuth2Credentials.from_json(flask.session['credentials'])
	if credentials.access_token_expired:
		return flask.redirect(flask.url_for('oauth2callback'))
	else:
		#should add a check
		#if query db for user info based on email, return home, else return make a profile page
		if True:
			return redirect(url_for('contact'))
		else:
			return redirect(url_for('contact'))


@app.route('/oauth2callback')
def oauth2callback():
	'''
	purpose: authenticates a user, each of whom will correspond to a student
	'''
	flow = client.flow_from_clientsecrets(
		'client_secrets.json',
		scope='https://www.googleapis.com/auth/userinfo.profile', 
		redirect_uri=flask.url_for('oauth2callback', _external=True))
	if 'code' not in flask.request.args:
		auth_uri = flow.step1_get_authorize_url()
		return flask.redirect(auth_uri)
	else:
		auth_code = flask.request.args.get('code')
		credentials = flow.step2_exchange(auth_code)
		flask.session['credentials'] = credentials.to_json()
		stud = get_user_info(credentials)
		return flask.redirect(flask.url_for('index'))

@app.route('/login', methods=['GET', 'POST']) # create mappings
def login():
	'''
	purpose: sign in page that redirects to google sign in
	'''
	form = LoginForm()
	if form.validate_on_submit():
		flash('Sign in Successful!')
		return(redirect('/oauth2callback'))
	return(render_template('login.html',
							title='Sign in!', 
							form=form))

def get_user_info(credentials):
	# sends request to the UserInfo API to retrieve the user's information
	user_info_service = discovery.build(
		serviceName='oauth2', version='v2',
		http=credentials.authorize(httplib2.Http()))
	user_info = None
	try:
		user_info = user_info_service.userinfo().get().execute()
	except errors.HttpError as e:
		logging.error('An error occurred: %s', e)
	if user_info and user_info.get('id'):
		return user_info
	else:
		raise NoUserIdException()


@app.route('/events', methods=['GET', 'POST']) # create mappings
def events():
	try: 
		conn = psycopg2.connect("dbname='proj1part2' user='wke2102' host='35.196.90.148' password='adi-tools'")
		curr = conn.cursor()
		print("connected!!")
	except:
		print("this failed to connect")
	form = AddEvents()
	if request.method == 'POST':
		print("that's cool")
		return render_template('events.html',  form=form)
	else:
		return render_template('events.html',  form=form)


@app.route('/companies', methods=['GET', 'POST']) # create mappings
def company():
	form = AddCompanies()
	if form.validate_on_submit():
		flash('Success!')
		return(redirect('/companies'))
	#db_functions.insert_company(form.name.data, form.address.data)
	return(render_template('companies.html',
							title='Submit a company!', 
							form=form))

@app.route('/projects', methods=['GET', 'POST']) 
def projects():
	form = AddProjects()
	return render_template('projects.html',  form=form)

@app.route('/workshops', methods=['GET', 'POST']) 
def workshops():
	if request.method == 'POST':
		return render_template('workshop.html')
	form = AddWorkshop()
	return render_template('workshop.html',  form=form)

@app.route('/techtalks', methods=['GET', 'POST']) 
def techtalks():
	if request.method == 'POST':
		return render_template('techtalks.html')
	else:
		form  = AddTechTalks()
		return render_template('techtalks.html', form=form)

@app.route('/addcompany', methods=['GET', 'POST']) 
def addCompany():
	if request.method == 'POST':
		print("should be validating an addcompany request here")
		form = AddCompany(request.form)
		if form.validate_on_submit():
			db_functions.insert_company(form.name.data)
			return render_template('companies.html')

		return render_template('addCompany.html', form=form)
	else:
		form = AddCompany()
		return render_template('addCompany.html', form=form)

@app.route('/addevent', methods=['GET', 'POST']) 
def addevents():
	if request.method == 'POST':
		print("in add events post method")
		form = AddEvents(request.form)
		if form.validate_on_submit():
			print("here")
			return render_template('events.html')
		print("if statement failed")
		return render_template('addEvents.html', form=form)
	else:
		form = AddEvents()
		return render_template('addEvents.html', form=form)

@app.route('/addworkshop', methods=['GET', 'POST']) 
def addworkshop():
	if request.method == 'POST':
		form = AddEvents(request.form)
		if form.validate_on_submit():
			return render_template('workshop.html')
		else:
			print("in else")
			flash("Please fill out all fields")
			return render_template('addWorkshop.html', form=form)
	else:
		form = AddWorkshop()
		return render_template('addWorkshop.html', form=form)

@app.route('/addtechtalk', methods=['GET', 'POST']) 
def addtechtalk():
	if request.method == 'POST':
		form = AddTechTalks()
		if form.validate_on_submit():
			return render_template('techtalks.html')
		else:
			return render_template('addTechTalks.html', form=form)
	else:
		form = AddTechTalks()
		return render_template('addTechTalks.html', form=form)

@app.route('/profile', methods=['GET', 'POST']) # create mappings
def contact():
	if request.method == 'POST':
		form = Person(request.form)
		print(form.errors)
		print("hello db")
		if form.validate_on_submit():
			print("checking validate here")
			db_functions.insert_contact(form.name.data, form.semester_start.data, form.project.data, form.company.data)
			return render_template('events.html')
		else:
			form = Person()	
			return render_template('join.html', title='Submit a contact!', form=form)	
	else:
		form = Person()	
		return render_template('join.html', title='Submit a contact!', form=form)				


# following code taken from server.py
@app.before_request
def before_request():
  """
  This function is run at the beginning of every web request 
  (every time you enter an address in the web browser).
  We use it to setup a database connection that can be used throughout the request.

  The variable g is globally accessible.
  """
  try:
    g.conn = engine.connect()
  except:
    print("uh oh, problem connecting to database")
    import traceback; traceback.print_exc()
    g.conn = None

@app.teardown_request
def teardown_request(exception):
  """
  At the end of the web request, this makes sure to close the database connection.
  If you don't, the database could run out of memory!
  """
  try:
    g.conn.close()
  except Exception as e:
    pass


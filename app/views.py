from app import app
from flask import render_template, flash, redirect, make_response, request
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
from .forms import Companies, Contacts
import requests 

basic_auth = BasicAuth(app)

oauth = OAuth(app)
app.debug = True
app.secret_key = 'kj1VHtx6sPDLUL1L'

@app.route('/')
def index():
	user = {'nickname': 'Lesley'}  # fake user
	if 'credentials' not in flask.session:
		return flask.redirect(flask.url_for('oauth2callback'))
	credentials = client.OAuth2Credentials.from_json(flask.session['credentials'])
	if credentials.access_token_expired:
		return flask.redirect(flask.url_for('oauth2callback'))
	else:
		#should add a check
		#if query db for user info based on email, return home, else return make a profile page
		if True:
			form = Contacts()
			return render_template('join.html', title='Join', form=form)
		else:
			return render_template('index.html', title='Home', user=user)


# https://stackoverflow.com/questions/26357278/how-to-get-email-address-from-linkedin-using-flask-oauthlib
@app.route('/authorized')
def authorized():
    resp = linkedin.authorized_response()
    if resp is None:
        return 'Access denied:'
    session['linkedin_token'] = (resp['access_token'], '')
    me = linkedin.get('people/~')  # <== HOW can I get this line to return the email address?
    return jsonify(me.data)


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
		print(stud)
#		if (insert_student.check_student(stud['id']) == None): 
#			insert_student.new_student(stud['id'], stud['name'])
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
	if request.method == 'POST':
		print("that's cool")
		return render_template('events.html')
	else:
		return render_template('events.html')


@app.route('/companies', methods=['GET', 'POST']) # create mappings
def company():
	form = Companies()
	if form.validate_on_submit():
		flash('Success!')
		return(redirect('/companies'))
	db_functions.insert_company(form.name.data, form.address.data)
	return(render_template('companies.html',
							title='Submit a company!', 
							form=form))

@app.route('/projects', methods=['GET', 'POST']) # create mappings
def projects():
	return render_template('events.html')

@app.route('/workshops', methods=['GET', 'POST']) # create mappings
def workshops():
	return render_template('events.html')

@app.route('/techtalks', methods=['GET', 'POST']) # create mappings
def techtalks():
	return render_template('events.html')

@app.route('/join', methods=['GET', 'POST']) # create mappings
def contact():
	form = Contacts()
	if form.validate_on_submit():
		flash('Sucess!')
		return(redirect('/contact'))
	db_functions.insert_contact(form.name.data, form.number.data, form.email.data, form.company.data, form.position.data, form.notes.data)
	return(render_template('join.html',
							title='Submit a contact!', 
							form=form))						


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


from app import app
from flask import render_template, flash, redirect, make_response
from .forms import LoginForm, Interactions, Companies, Contacts, Offers, SearchForm
import json
import flask
import httplib2
from apiclient import discovery
import requests 
from oauth2client import client
from database import insert_student
from flask_basicauth import BasicAuth
from wtforms.validators import DataRequired
from flask_oauthlib.client import OAuth


@app.route('/')
@app.route('/index')
def index():
	user = {'nickname': 'Lesley'}  # fake user
	if 'credentials' not in flask.session:
		return flask.redirect(flask.url_for('oauth2callback'))
	credentials = client.OAuth2Credentials.from_json(flask.session['credentials'])
	if credentials.access_token_expired:
		return flask.redirect(flask.url_for('oauth2callback'))
	else:
		return render_template('index.html',
							title='Home',
							user=user)

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
		if (insert_student.check_student(stud['id']) == None): 
			insert_student.new_student(stud['id'], stud['name'])
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
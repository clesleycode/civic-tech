import pandas as pd
from sqlalchemy import * 
import uuid
from flask import g
import datetime as dt

# project database URL
DATABASEURI = "postgresql:///civic-tech-for-beginners:myinstance:35.202.43.58/civic-tech"

# connect to db
engine = create_engine(DATABASEURI)
cursor = engine.connect()


'''
Inserts a new entry into the Company table
	Input: 
		name -- the name of the company 
'''
def insert_company(name):
	unique_id = str(uuid.uuid4().int)[:9]
	cursor.execute(''' INSERT INTO Company (companyId, companyName) VALUES (%s, %s) ''', (unique_id, str(name)))


'''
Inserts a new profile into the Person table
	Input: 
		name -- the name of the person
		semester_start -- when the person began ADI
		pillarId -- the project the student is on 
		companyId -- where the student has worked before 
'''
def insert_person(name, semester_start, pillarId, companyId):
	personId = str(uuid.uuid4().int)[:9]
	cursor.execute(''' INSERT INTO Person (personId, personName, semester_start, pillarId, companyId) VALUES (%s, %s, %s, %s, %s) ''', (str(personId), str(name), str(semester_start), str(pillarId), str(companyId)))


'''
Inserts a new event into the Events table & new event leader into IN_CHARGE_OF table
	Input: 
		name -- the name of the company 
		eventTime -- when the event began
		location -- where the event was
		numberAttendees -- how many students attended
		pillarID -- which project was in charge
'''
def insert_event(name, eventTime, location, numberAttendees, pillarId):
	eventId = str(uuid.uuid4().int)[:9]
	cursor.execute(''' INSERT INTO Events (eventId, name, eventTime, location, numberAttendees) VALUES (%s, %s, %s, %s, %s) ''', (str(eventId), str(name), str(eventTime), str(location), str(numberAttendees)))
	cursor.execute(''' INSERT INTO IN_CHARGE_OF (eventId, pillarId) VALUES (%s, %s) ''', (str(eventId), str(pillarId)))
	

'''
Inserts a new workshop into the Workshops table
	Input: 
		workshopTopic -- what the topic is about
		personID -- who was in charge 
'''
def insert_workshop(workshopTopic, personId):
	workshop_id = str(uuid.uuid4().int)[:9]
	cursor.execute(''' INSERT INTO Workshops (workshopId, workshopTopic) VALUES (%s, %s) ''', (workshop_id, str(workshopTopic)))
	cursor.execute(''' INSERT INTO HOSTS (personId, workshopID) VALUES (%s, %s) ''', (str(personId), str(workshop_id)))


'''
Inserts a new event into the TechTalks table
	Input: 
		talkName -- the name of the tech talk
		companyID -- which company hosted the talk 
'''
def insert_techtalk(talkName, companyId):
	talk_id = str(uuid.uuid4().int)[:9]
	cursor.execute(''' INSERT INTO TechTalks (talkId, companyId, name) VALUES (%s, %s, %s) ''', (str(talk_id), str(companyId), str(talkName)))


'''
Deletes an event from the Events table
	Input: 
		eventId -- specific id of the deleted event
'''
def delete_event(eventId):
	cursor.execute(''' DELETE FROM Events WHERE eventId = %s''', (str(eventId)))



'''
The following methods are various get methods for convenient queries of the tables
	- these were typically needed for things like filling the dropdown options. 
'''
def get_event_ids():
	return list(cursor.execute(''' SELECT eventId, name FROM Events ORDER BY name DESC; '''))

def get_companies():
	return list(cursor.execute(''' SELECT companyId, companyName FROM Company ORDER BY companyName ASC; '''))

def get_events():
	return list(cursor.execute(''' SELECT name, eventTime, location, numberAttendees FROM Events ORDER BY eventTime DESC; '''))

def get_workshops():
	return list(cursor.execute(''' SELECT Workshops.workshopTopic, Person.personName FROM Workshops INNER JOIN HOSTS on Workshops.workshopId = HOSTS.workshopID INNER JOIN Person on HOSTS.personId = Person.personId; '''))

def get_techtalks():
	return list(cursor.execute('''SELECT T.name, C.companyName, T.talkId FROM TechTalks T, Company C WHERE T.companyId = C.companyId ORDER BY T.talkId ASC; '''))

def get_techtalks_names():
	return list(cursor.execute('''SELECT talkId, name FROM TechTalks ORDER BY name DESC; '''))

def get_projects():
	return list(cursor.execute('''SELECT pillarId, pillar from Projects ORDER BY pillar ASC;'''))

def get_users():
	return list(cursor.execute('''SELECT personId, personName from Person ORDER BY personName DESC;'''))

def get_comps():
	return list(cursor.execute(''' SELECT Company.companyName, Person.personName FROM Company INNER JOIN Person on Person.companyId = Company.companyId GROUP BY Company.companyName, Person.personName; '''))

'''
This function updates an entry of the TechTalks table
	Input: 
		talkName -- NEW name of tech talk
		talkId -- id of tech talk to be updated.
'''
def update_techtalks(talkName, talkId):
	cursor.execute(''' UPDATE TechTalks SET name = %s WHERE talkId = %s''', (str(talkName), str(talkId)))
	#cursor.execute(''' UPDATE TechTalks SET name = %s WHERE talkdId = %s eventId = %s''', (str(talkName), str(talkId)))
	#cursor.execute('''UPDATE TechTalks SET name = '%s' WHERE talkId = %s; '''), (str(talkName), talkId)


'''
The following functions use pandas and the get methods above to display the contents 
of our tables on each home page of our website. 
'''
def disp_companies():
	results = get_companies()
	db = pd.DataFrame(results)
	db.columns = ["Index", "Companies"]
	return pd.DataFrame(db['Companies']).to_html(index=False)


def disp_companies():
	results = get_comps()
	db = pd.DataFrame(results)
	db.columns = ["Company", "Student"]
	return db.to_html(index=False)


def disp_events():
	results = get_events()
	db = pd.DataFrame(results)
	db.columns = ["Name", "When", "Location", "Number Attended"]
	f1 = lambda x: dt.datetime.strptime(str(x),'%Y-%m-%d %X').strftime("%b %d, %-I%p")
	db["When"] = db["When"].apply(f1)
	return db.to_html(index=False)
	#return pd.DataFrame(db['Companies']).to_html()


def disp_projects():
	results = get_projects()
	db = pd.DataFrame(results)
	db.columns = ["Number of People", "Name"]
	return db.to_html(index=False)


def disp_workshops():
	results = get_workshops()
	db = pd.DataFrame(results)
	db.columns = ["Name", "Person"]
	return db.to_html(index=False)


def disp_techtalks():
	results = get_techtalks()
	db = pd.DataFrame(results)
	db.columns = ["Talk Name", "Company Name", "Other"]
	del db['Other']
	return db.to_html(index=False)


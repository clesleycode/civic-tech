import pandas as pd
from sqlalchemy import * 
import uuid
from flask import g
import datetime as dt
DATABASEURI = "postgresql://wke2102:8061@35.196.90.148/proj1part2"


engine = create_engine(DATABASEURI)
cursor = engine.connect()


def insert_company(name):
	unique_id = str(uuid.uuid4().int)[:9]
	cursor.execute(''' INSERT INTO Company (companyId, companyName) VALUES (%s, %s) ''', (unique_id, str(name)))


def insert_person(name, semester_start, pillarId, companyId):
	personId = str(uuid.uuid4().int)[:9]
	cursor.execute(''' INSERT INTO Person (personId, personName, semester_start, pillarId, companyId) VALUES (%s, %s, %s, %s, %s) ''', (str(personId), str(name), str(semester_start), str(pillarId), str(companyId)))


def insert_event(name, eventTime, location, numberAttendees, pillarId):
	eventId = str(uuid.uuid4().int)[:9]
	cursor.execute(''' INSERT INTO Events (eventId, name, eventTime, location, numberAttendees) VALUES (%s, %s, %s, %s, %s) ''', (str(eventId), str(name), str(eventTime), str(location), str(numberAttendees)))
	cursor.execute(''' INSERT INTO IN_CHARGE_OF (eventId, pillarId) VALUES (%s, %s) ''', (str(eventId), str(pillarId)))
	
def insert_workshop(workshopTopic,personId):
	workshop_id = str(uuid.uuid4().int)[:9]
	cursor.execute(''' INSERT INTO Workshops (workshopId, workshopTopic) VALUES (%s, %s) ''', (workshop_id, str(workshopTopic)))
	cursor.execute(''' INSERT INTO HOSTS (personId, workshopID) VALUES (%s, %s) ''', (str(personId), str(workshop_id)))


def insert_techtalk(talkName, companyId):
	talk_id = str(uuid.uuid4().int)[:9]
	cursor.execute(''' INSERT INTO TechTalks (talkId, companyId, name) VALUES (%s, %s, %s) ''', (str(talk_id), str(companyId), str(talkName)))


def delete_event(eventId):
	cursor.execute(''' DELETE FROM Events WHERE eventId = %s''', (str(eventId)))

def get_event_ids():
	return list(cursor.execute(''' SELECT eventId, name FROM Events ORDER BY name DESC; '''))

def get_companies():
	return list(cursor.execute(''' SELECT companyId, companyName FROM Company ORDER BY companyName ASC; '''))


def get_events():
	return list(cursor.execute(''' SELECT name, eventTime, location, numberAttendees FROM Events ORDER BY eventTime DESC; '''))


def get_workshops():
	return list(cursor.execute(''' SELECT workshopTopic FROM Workshops ORDER BY workshopTopic ASC; '''))


def get_techtalks():
	return list(cursor.execute('''SELECT T.name, C.companyName, T.talkId FROM TechTalks T, Company C WHERE T.companyId = C.companyId ORDER BY T.talkId ASC; '''))

def get_techtalks_names():
	return list(cursor.execute('''SELECT talkId, name FROM TechTalks ORDER BY name DESC; '''))

def update_techtalks(talkName, talkId):
	cursor.execute(''' UPDATE TechTalks SET name = %s WHERE talkId = %s''', (str(talkName), str(talkId)))
	#cursor.execute(''' UPDATE TechTalks SET name = %s WHERE talkdId = %s eventId = %s''', (str(talkName), str(talkId)))
	#cursor.execute('''UPDATE TechTalks SET name = '%s' WHERE talkId = %s; '''), (str(talkName), talkId)


def get_projects():
	return list(cursor.execute('''SELECT pillarId, pillar from Projects ORDER BY pillar ASC;'''))

def get_users():
	return list(cursor.execute('''SELECT personId, personName from Person ORDER BY personName DESC;'''))


def disp_companies():
	results = get_companies()
	db = pd.DataFrame(results)
	db.columns = ["Index", "Companies"]
	return pd.DataFrame(db['Companies']).to_html(index=False)


def disp_companies():
	results = get_companies()
	db = pd.DataFrame(results)
	db.columns = ["Index", "Companies"]
	return pd.DataFrame(db['Companies']).to_html(index=False)


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
	db.columns = ["Name"]
	return db.to_html(index=False)


def disp_techtalks():
	results = get_techtalks()
	db = pd.DataFrame(results)
	db.columns = ["Talk Name", "Company Name", "Other"]
	del db['Other']
	return db.to_html(index=False)





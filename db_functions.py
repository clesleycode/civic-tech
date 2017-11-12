import sqlite3
import pandas as pd
from sqlalchemy import * 
import uuid
from flask import g
DATABASEURI = "postgresql://wke2102:8061@35.196.90.148/proj1part2"


engine = create_engine(DATABASEURI)
cursor = engine.connect()

def insert_company(name):
	unique_id = str(uuid.uuid4().int)[:9]
	cursor.execute(''' INSERT INTO Company (companyId, companyName) VALUES (%s, %s) ''', (unique_id, str(name)))

def insert_person(name, semester_start, pillarId, companyId):
	person_id = str(uuid.uuid4().int)[:9]
	cursor.execute(''' INSERT INTO Person (personId, personName, semester_start, pillarId, companyId) VALUES (%s, %s, %s, %s, %s) ''', (str(personId), str(name), str(semester_start), str(pillarId), str(companyId)))

def insert_event(name, eventTime, location, numberAttendees):
	#NEED to also trigger a call to get a logged in user's pillarId to then connect with IN_CHARGE_OF table
	event_id = str(uuid.uuid4().int)[:9]
	cursor.execute(''' INSERT INTO Events (eventId, name, eventTime, location, numberAttendees) VALUES (%s, %s, %s, %s, %s) ''', (str(eventId), str(name), str(eventTime), str(location), str(numberAttendees)))
	
def insert_workshop(workshopTopic):
	#need to also trigger call to get user's personId and then insert workshopId and personId into HOSTS table
	workshop_id = str(uuid.uuid4().int)[:9]
	cursor.execute(''' INSERT INTO Workshops (workshopId, workshopTopic) VALUES (%s, %s) ''', (workshop_id, str(workshopTopic)))

def insert_techtalk(companyId):
	#relies on getting companyId passed in to function
	talk_id = str(uuid.uuid4().int)[:9]
	cursor.execute(''' INSERT INTO TechTalks (talkId, companyId) VALUES (%s, %s) ''', (str(talk_id), str(companyId)))

def delete_event(eventId):
	cursor.execute(''' DELETE FROM Events WHERE eventId = %s''', (str(eventId)))


def get_companies():
	companies =  list(cursor.execute(''' SELECT companyId, companyName FROM Company ORDER BY companyName ASC; '''))
	return companies

def get_events():
	return list(cursor.execute(''' SELECT name, eventTime, location, numberAttendees FROM Events ORDER BY eventTime DESC; '''))

def get_workshops():
	return list(cursor.execute(''' SELECT workshopTopic FROM Workshops ORDER BY workshopTopic ASC; '''))

def get_techtalks():
	return list(cursor.execute('''SELECT C.companyName, T.talkId FROM TechTalks T, Company C WHERE T.companyId = C.companyId ORDER BY T.talkId ASC; '''))

def get_projects():
	return list(cursor.execute('''SELECT pillarId, pillar from Projects ORDER BY pillar ASC;'''))


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
	personId = str(uuid.uuid4().int)[:9]
	cursor.execute(''' INSERT INTO Person (personId, personName, semester_start, pillarId, companyId) VALUES (%s, %s, %s, %s, %s) ''', (str(personId), str(name), str(semester_start), str(pillarId), str(companyId)))

def insert_event(name, eventTime, location, numberAttendees):
	#NEED to also trigger a call to get a logged in user's pillarId to then connect with IN_CHARGE_OF table
	eventId = str(uuid.uuid4().int)[:9]
	cursor.execute(''' INSERT INTO Events (eventId, name, eventTime, location, numberAttendees) VALUES (%s, %s, %s, %s, %s) ''', (str(eventId), str(name), str(eventTime), str(location), str(numberAttendees)))
	
def insert_workshop(workshopTopic,personId):
	#need to also trigger call to get user's personId and then insert workshopId and personId into HOSTS table
	workshop_id = str(uuid.uuid4().int)[:9]
	cursor.execute(''' INSERT INTO Workshops (workshopId, workshopTopic) VALUES (%s, %s) ''', (workshop_id, str(workshopTopic)))
	cursor.execute(''' INSERT INTO HOSTS (personId, workshopID) VALUES (%s, %s) ''', (str(personId), str(workshop_id)))

def insert_techtalk(talkName, companyId):
	talk_id = str(uuid.uuid4().int)[:9]
	cursor.execute(''' INSERT INTO TechTalks (talkId, companyId, name) VALUES (%s, %s, %s) ''', (str(talk_id), str(companyId), str(talkName)))

def delete_event(eventId):
	cursor.execute(''' DELETE FROM Events WHERE eventId = %s''', (str(eventId)))

def get_companies():
	return list(cursor.execute(''' SELECT companyId, companyName FROM Company ORDER BY companyName ASC; '''))

def get_events():
	return list(cursor.execute(''' SELECT name, eventTime, location, numberAttendees FROM Events ORDER BY eventTime DESC; '''))

def get_workshops():
	return list(cursor.execute(''' SELECT workshopTopic FROM Workshops ORDER BY workshopTopic ASC; '''))

def get_techtalks():
	return list(cursor.execute('''SELECT C.companyName, T.talkId FROM TechTalks T, Company C WHERE T.companyId = C.companyId ORDER BY T.talkId ASC; '''))

def get_projects():
	return list(cursor.execute('''SELECT pillarId, pillar from Projects ORDER BY pillar ASC;'''))

def get_users():
	return list(cursor.execute('''SELECT personId, personName from Person ORDER BY personName DESC;'''))






import sqlite3
import pandas as pd
from sqlalchemy import * 

DATABASEURI = "postgresql://wke2102:8061@35.196.90.148/proj1part2"

# make new account
# query all projects
# add event 
# check the project leading the event (in charge of table)
# creating a new workshop
# check which person is hosting the workshop (host table)

#db = sqlite3.connect("./database.db", check_same_thread=False)
#cursor = db.cursor()

engine = create_engine(DATABASEURI)
cursor = engine.connect()


def insert_company(name, address):	
	cursor.execute(''' INSERT INTO companies (name, address, hires) VALUES (?, ?, ?) ''', (str(name), str(address), 0,))
	db.commit()


def insert_contact(name, number, email, company_id, position, notes):
	cursor.execute(''' INSERT INTO contacts (name, number, email, company_id, position, notes) VALUES (?, ?, ?, ?, ?, ?) ''', (str(name), str(number), str(email), str(company_id), str(position), str(notes), ))
	db.commit()


def get_companies():
	return list(cursor.execute(''' SELECT id, name FROM companies; '''))
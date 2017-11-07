from flask import Flask
import psycopg2
from flask import g

# set up
app = Flask(__name__)
app.config.from_object('config')

def get_db():
	db = getattr(g, '_database', None)
	if db is None:
		db = g._database = sqlite3.connect(DATABASE)
	return(db)

@app.teardown_appcontext
def close_connection(exception):
	db = getattr(g, '_database', None)
	if db is not None:
		db.close()

from app import views 
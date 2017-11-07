from flask import Flask
import psycopg2
from flask import g

# set up
app = Flask(__name__)
app.config.from_object('config')


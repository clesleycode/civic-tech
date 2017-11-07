import os

import os

WTF_CSRF_ENABLED = True # for security
SECRET_KEY = 'you-will-never-guess'


basedir = os.path.abspath(os.path.dirname(__file__))

DATABASE = os.path.join(basedir, 'database/database.db')

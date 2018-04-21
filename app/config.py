import os

basedir = os.path.abspath(os.path.dirname(__file__))

DATABASE = 'flasktaskr.db'
#USERNAME = 'admin'
#PASSWORD = 'admin'
CSRF_ENABLED = True
SECRET_KEY = 'my_super_precious'


DATABASE_PATH = os.path.join(basedir, DATABASE)

#the database uri
SQLALCHEMY_DATABASE_URI = 'sqlite:///'+DATABASE_PATH
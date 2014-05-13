# This file initializes the app module to the Flask framework.
# It also routes default paths to the /app/static folder
# The route handlers are imported from views.

import os
from sqlite3 import dbapi2 as sqlite3
from flask import Flask, request, session, g, redirect, url_for, abort
app = Flask(__name__, static_url_path='')
app.secret_key = os.urandom(24)

database_file = os.path.join(app.root_path, 'app.db')
schema_file = os.path.join(app.root_path, 'schema.sql')

def connect_db():
  """Connects to the specific database."""
  rv = sqlite3.connect(database_file)
  rv.row_factory = sqlite3.Row
  return rv

def get_db():
  """Opens a new database connection if there is none yet for the
  current application context.
  """
  if not hasattr(g, 'sqlite_db'):
    g.sqlite_db = connect_db()
  return g.sqlite_db

def init_db():
  """Initializes the database."""
  with app.app_context():
    db = get_db()
    with app.open_resource(schema_file, mode='r') as f:
      db.cursor().executescript(f.read())
    db.commit()

@app.teardown_appcontext
def close_db(error):
  """Closes the database again at the end of the request."""
  if hasattr(g, 'sqlite_db'):
    g.sqlite_db.close()

# only init the db if it doesn't exist.
if not os.path.isfile(database_file):
  init_db()

from q_classes import QueueServer
with app.app_context():
  queue_server = QueueServer()

from app import views

# This file initializes the app module to the Flask framework.
# It also routes default paths to the /app/static folder
# The route handlers are imported from views.

from flask import Flask

app = Flask(__name__, static_url_path='')
from app import views

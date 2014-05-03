#!flask/bin/python
# used by developers to run Flask's SimpleHTTP server
# on local machine for local development and testing.
from app import app
app.run(debug = True)

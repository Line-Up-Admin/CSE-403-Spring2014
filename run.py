#!flask/bin/python
# used by developers to run Flask's SimpleHTTP server
# on local machine for local development and testing.
from app import app
print 'importing debug views.'
from app import debug_views
app.run(debug = True, host='0.0.0.0')

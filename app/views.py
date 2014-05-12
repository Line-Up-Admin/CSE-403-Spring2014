# This is the file that contains all the route handlers.
from app import app
import database_utilities as db_util
import sqlite3
from flask import request, session, g, redirect, url_for, abort, jsonify

from q_classes import QueueServer
server = QueueServer()

# This procedure picks up the default route and returns index.html.
@app.route('/')
def root():
   return app.send_static_file('index.html')

@app.route('/join', methods=['POST'])
def add_to_queue():

   return 'Not implemented yet!'

@app.route('/login', methods=['GET','POST'])
def login():
    return 'Not implemented yet!'

@app.route('/dequeue')
def dequeue():
    return 'Not implemented yet!'

@app.route('/searchResults')
def get_search_results():
	return 'Not implemented yet!'

@app.route('/search')
def search():
	return 'Not implemented yet!'

@app.route('/memberQueue/<qid>')
def get_member_queue(qid):
	return 'Not implemented yet!'

@app.route('/employeeQueue/<qid>')
def get_employee_queue(qid):
	return 'Not implemented yet!'

@app.route('/adminQueue/<qid>')
def get_admin_queue(qid):
	return

@app.route('/queueStatus')
def get_queue_status():
	return 'Not implemented yet!'

@app.route('/myQueues')
def get_my_queues():
	return 'Not implemented yet!'

@app.route('/remove')
def remove_queue_member():
	return 'Not implemented yet!'

@app.route('/qtracks')
def queue_tracks():
	return 'Not implemented yet!'

@app.route('/qtracksData')
def queue_tracks_data():
	return 'Not implemented yet!'

@app.route('/createUser')
def create_user():
	return 'Not implemented yet!'

@app.route('/createQueue', methods=['POST'])
def create_queue():
   # q_settings = request.form.copy()
   q_settings = request.json
   try:
      q_settings['id'] = db_util.create_queue(q_settings)
      return jsonify(q_settings)
   except sqlite3.Error as e:
      return e.message

@app.route('/logout')
def logout():
	return 'Not implemented yet!'

# Takes the '/helloworld' route and returns "Hello, World!"
@app.route('/helloworld')
def hello_world():
    return "Hello, World!"

# Temporary: debugging purposes only.
@app.route('/debug/getuser')
def get_user_debug():
	if not app.debug:
	    abort(404)
	username = request.args.get('username')
	password = request.args.get('password')
	try:
		user = db_util.get_user(username, password)
		return jsonify(user)
	except sqlite3.Error as e:
		return e.message
	except db_util.ValidationException as e:
		return e.message

# Temporary: debugging purposes only.
@app.route('/debug/gettempuser')
def get_temp_user_debug():
	if not app.debug:
		abort(404)
	id = request.args.get('id')
	try:
		temp_user = db_util.get_temp_user(id)
		return jsonify(temp_user)
	except sqlite3.Error as e:
		return e.message
	except db_util.ValidationException as e:
		return e.message

# Temporary: debugging purposes only.
@app.route('/debug/createuser')
def create_user_debug():
	if not app.debug:
		abort(404)
	user = request.args.copy()
	try:
		user['id'] = db_util.create_user(user)
		return jsonify(user)
	except sqlite3.Error as e:
		return e.message

#@app.route('/debug/getqueuesettings')
@app.route('/debug/getqueuesettings', methods=['POST'])
def get_queue_settings_debug():
   #queueID = request.args.get('qid')
   queueID = request.json
   try:
      queue = db_util.get_queue_settings(queueID)
      return jsonify(queue)
   except sqlite3.Error as e:
      return e.message

@app.route('/debug/createqueue', methods=['GET'])
def create_queue_debug():
   queueSettings = copy_request_args(request)
   try:
      queueSettings['id'] = db_util.create_queue(queueSettings)
      return jsonify(queueSettings)
   except sqlite3.Error as e:
      return e.message

@app.route('/debug/createtempuser')
def create_temp_user_debug():
   if not app.debug:
      abort(404)
   user = copy_request_args(request)
   user['id'] = None
   try:
      user['id'] = db_util.create_user(user)
      return jsonify(user)
   except sqlite3.Error as e:
      return e.message


def copy_request_args(origRequest):
   res = dict()
   for key in origRequest.args.keys():
      res[key] = origRequest.args.get(key)
   return res;

# This is the file that contains all the route handlers.
from app import app
import database_utilities as db_util
import user_module
from flask import request, session, g, redirect, url_for, abort, jsonify

from q_classes import QueueServer
from user_module import UserModule
server = QueueServer()
module = UserModule()

# This procedure picks up the default route and returns index.html.
@app.route('/')
def root():
    return app.send_static_file('index.html')

@app.route('/join')
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

@app.route('/createQueue')
def create_queue():
	return 'Not implemented yet!'

@app.route('/logout')
def logout():
	return 'Not implemented yet!'

# Takes the '/helloworld' route and returns "Hello, World!"
@app.route('/helloworld')
def hello_world():
    return "Hello, World!"

# Temporary: debugging purposes only.
@app.route('/user')
def get_user():
	username = request.args.get('username')
	password = request.args.get('password')
	try:
		user = db_util.get_user(username, password)
		return jsonify(user)
	except db_util.DatabaseException as e:
		return e.message
	except db_util.ValidationException as e:
		return e.message
	
		
# This is the file that contains all the route handlers.
from app import app, queue_server
import database_utilities as db_util
import sqlite3
from flask import request, session, g, redirect, url_for, abort, jsonify
import permissions

from q_classes import QueueServer, QueueMember, QueueSettings

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
   queueID = request.args.get('qid')
   try:
      #permissions.has_flag
      queue = db_util.get_queue_settings(queueID)
      return jsonify(queue)
   except sqlite3.Error as e:
      return e.message

@app.route('/debug/createqueue', methods=['GET'])
def create_queue_debug():
   queueSettings = copy_request_args(request)
   try:
      queueSettings['id'] = queue_server.create(queueSettings)
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

@app.route('/debug/popular', methods=['GET'])
def get_popular_queues_debug():
   q_info_list = queue_server.get_all_queues_info()
   return jsonify(queue_info_list=[q_info.__dict__ for q_info in q_info_list])
      

@app.route('/debug/queueStatus/<int:qid>', methods=['POST'])
def get_queue_info_debug(qid):
    q_info = queue_server.get_info(None, qid)
    return jsonify(q_info.__dict__)

@app.route('/debug/join/<int:qid>', methods=['POST'])
def add_to_queue_debug(qid):
   if not app.debug:
      abort(404)
   uid = None
   username = None
   if session.has_key('logged_in') and session['logged_in']:
      uid = session['uid']
      username = session['uname']
   else:
      temp = True
      temp_user = dict()
      temp_user['uname'] = request.args['uname']
      try:
         temp_user['id'] = db_util.create_temp_user(temp_user)
      except sqlite3.Error as e:
         return e.message
      username = temp_user['uname']
      uid = temp_user['id']
   if not permissions.has_flag(uid, qid, permissions.BLOCKED_USER):
      q_member = QueueMember(username, uid)
      queue_server.add(q_member, qid)
      q_info = queue_server.get_info(q_member, qid)
      q_info_dict = dict(q_info.__dict__)
      if temp:
         q_info_dict['confirmation_number'] = uid
      return jsonify(q_info_dict)
   else:
      return 'User is blocked from this queue.'

@app.route('/debug/dequeue/<int:qid>', methods=['POST'])
def dequeue_debug(qid):
   if not app.debug:
      abort(404)
   uid = None
   if session.has_key('logged_in') and session['logged_in']:
      uid = session['id']
   else:
      uid = request.args['employee']
   if permissions.has_flag(uid, qid, permissions.EMPLOYEE):
      q_member = queue_server.dequeue(qid)
      if q_member is None:
         return 'The queue is empty.'
      return jsonify(q_member.__dict__)
   else:
      return 'You must be an employee to dequeue.'

def copy_request_args(origRequest):
   res = dict()
   for key in origRequest.args.keys():
      res[key] = origRequest.args.get(key)
   return res;

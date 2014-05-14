# This is the file that contains all the route handlers.
from app import app, queue_server
import database_utilities as db_util
import sqlite3
from flask import request, session, g, redirect, url_for, abort, jsonify
import permissions

from q_classes import QueueServer, QueueMember, QueueSettings

# This procedure picks up the default route and returns index.html.
@app.route('/')
def root():
   return app.send_static_file('index.html')

@app.route('/join', methods=['POST'])
def add_to_queue():
   """Joins a queue defined by the 'qid' passed as a parameter.

   If the session is not logged in, assumes that the user is a temporary user,
   and looks for a 'uname' parameter as well. This will create a temporary
   user.

   Returns: example return value below
      {
         "avg_wait_time": null,
         "confirmation_number": 1472823387,
         "expected_wait": null,
         "member_position": 0,
         "qname": "ohhey",
         "qid": 556035656,
         "size": 1
      }
   """
   
   uid = None
   username = None
   qid = int(request.json['qid'])
   temp = None
   if session.has_key('logged_in') and session['logged_in']:
      uid = session['id']
      username = session['uname']
   else:
      temp = True
      temp_user = dict()
      temp_user['uname'] = request.json['uname']
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

@app.route('/login')
def login():
   if request.method == 'GET':
      return app.send_static_file('login.html')
   else:
      # POST message
      if session.has_key('logged_in') and session['logged_in']:
          # user is already logged in
          return 'User is already logged in.'
      try:
         user = db_util.get_user(request.json['username'], request.json['password'])
         session['logged_in'] = True
         session['id'] = user['id']
      except sqlite3.Error as e:
         return e.message
      except db.util.ValidationException as e:
         session['logged_in'] = False
         return 'Invalid username or password'

@app.route('/dequeue/<int:qid>', methods=['POST'])
def dequeue():
   uid=None
   if session.has_key('logged_in') and session['logged_in']:
      uid=session['id']
   else:
      if app.debug:
         uid=int(request.json)
      else:
         return "You must be logged in as an employee to dequeue."
   if permissions.has_flag(uid, qid, permissions.EMPLOYEE):
      q_member = queue_server.dequeue(qid)
      if q_member is None:
         return 'The queue is empty.'
      return jsonify(q_member.__dict__)
   else:
      return 'You must be an employee to dequeue.'

@app.route('/searchResults')
def get_search_results():
   return 'Not implemented yet!'

@app.route('/search', methods=['POST'])
def search():
   q_info_list = queue_server.get_all_queues_info()
   return jsonify(queue_info_list=[q_info.__dict__ for q_info in q_info_list])

@app.route('/popular', methods=['GET'])
def get_popular_queues():
   q_info_list = queue_server.get_all_queues_info()
   return jsonify(queue_info_list=[q_info.__dict__ for q_info in q_info_list])

@app.route('/memberQueue', methods=['POST'])
def get_member_queue():
   return 'Not implemented yet!'

@app.route('/employeeView/<qid>', methods=['POST'])
def get_employee_queue(qid):
   uid = None
   if session.has_key('logged_in') and session['logged_in']:
      uid = session['id']
   else:
      return "You must be logged in as an employee to dequeue."
   if permissions.has_flag(uid, qid, permissions.EMPLOYEE):
      members = queue_server.get_members(qid)
      q_info = queue_server.get_info(None, qid)
      return jsonify(queue_info=q_info.__dict__, member_list=[member.__dict__ for member in members])

@app.route('/adminQueue/<qid>')
def get_admin_queue(qid):
	return

@app.route('/getQueueSettings', methods=['POST'])
def get_queue_settings():
   """

   Returns: example return value
      {
         "active": 1,
         "qid": 2789801433,
         "keywords": "seattle",
         "location": "seattle",
         "max_size": 10,
         "qname": "bestqueueever"
      }
   """
   queueID = request.json
   try:
      #permissions.has_flag
      queue = db_util.get_queue_settings(queueID)
      return jsonify(queue)
   except sqlite3.Error as e:
      return e.message

@app.route('/queueStatus/<qid>')
def get_queue_status():
   """View the queue with the given qid.

   Returns: example return value below
      {
         "avg_wait_time": null,
         "confirmation_number": null,
         "expected_wait": null,
         "member_position": null,
         "qname": "ohhey",
         "qid": 556035656,
         "size": 1
      }
   """
   q_info = queue_server.get_info(None, qid)
   return jsonify(q_info.__dict__)

@app.route('/myQueues', methods=['POST'])
def get_my_queues():
   uid = None
   if session.has_key('logged_in') and session['logged_in']:
      uid = session['id']
   else:
      uid = int(request.json)
   q_info_list = queue_server.get_queue_info_list(uid)
   return jsonify(queue_info_list=[q_info.__dict__ for q_info in q_info_list])

@app.route('/remove')
def remove_queue_member():
	return 'Not implemented yet!'

@app.route('/qtracks')
def queue_tracks():
	return 'Not implemented yet!'

@app.route('/qtracksData')
def queue_tracks_data():
	return 'Not implemented yet!'

@app.route('/createUser', methods=['POST'])
def create_user():
   user_data = request.json
   try:
      user_data['id'] = db_util.create_user(user_data)
      return jsonify(user_data)
   except sqlite3.Error as e:
      return e.message

@app.route('/createQueue', methods=['POST'])
def create_queue():
   # q_settings = request.form.copy()
   """need to add validation"""
   q_settings = request.json
   try:
      q_settings['qid'] = queue_server.create(q_settings)
      return jsonify(q_settings)
   except sqlite3.Error as e:
      return e.message

@app.route('/logout')
def logout():
	return 'Not implemented yet!'

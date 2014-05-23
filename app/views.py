# This is the file that contains all the route handlers.
from app import app, queue_server
import database_utilities as db_util
import sqlite3
from flask import request, session, g, redirect, url_for, abort, jsonify
import permissions

from q_classes import QueueServer, QueueMember, QueueSettings

def Failure(message):
   return {'SUCCESS':False, 'error_message':message}

# This procedure picks up the default route and returns index.html.
@app.route('/')
def root():
	# If user is already logged in, let them log in again.
  # if session.has_key('logged_in') and session['logged_in']:
		# user is already logged in
		# return app.send_static_file('index.html')
	return app.send_static_file('index.html')


#############################################
# Queue routes:
#############################################

@app.route('/createQueue', methods=['POST'])
def create_queue():
   """Creates a queue. If the user is logged in, they will become an admin for the queue.

   Args:
   {
      active: 0 or 1
      admins: [] (optional, a list of usernames)
      blocked_users: [] (optional, a list of usernames)
      employees: [] (optional, a list of usernames)
      keywords:
      location:
      max_size:
      qname:
   }

   Returns:
      {
         active:
         admins: [] (optional, a list of usernames)
         blocked_users: [] (optional, a list of usernames)
         employees: [] (optional, a list of usernames)
         keywords:
         location:
         max_size:
         qid:
         qname:
      }

   """
   q_settings = request.json
   if not session.has_key('logged_in') or not session['logged_in']:
      return jsonify(Failure('You cannot create a queue if you are not logged in!'))
   if not q_settings.has_key('admins'):
      q_settings['admins']=list()
   if not session['uname'] in q_settings['admins']:
      q_settings['admins'].append(session['uname'])
   try:
      q_settings['qid'] = queue_server.create(q_settings)
      return jsonify(q_settings)
   except sqlite3.Error as e:
      return jsonify(Failure(e.message));
   except ValidationException as e:
      return jsonify(Failure(e.message))

@app.route('/join', methods=['POST'])
def add_to_queue():
   """Joins a queue.

   Args:
      qid: the id of the queue to join.
      uname: the uname to create a temporary user. This is ignored if the user is logged in.

   Returns: example return value below
   If user is a temporary user:
      {
         "avg_wait_time": null,
         "confirmation_number": 1472823387,
         "expected_wait": null,
         "member_position": 0,
         "qname": "ohhey",
         "qid": 556035656,
         "size": 1
      }
   If user is logged in:
      {
         "avg_wait_time": null,
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

@app.route('/dequeue/<int:qid>', methods=['POST'])
def dequeue(qid):
   """Dequeues a member from the specified queue. If the queue is empty, returns an empty json object.

   Args:
      None. The route handles the argument. Example route: /dequeue/12345

   Returns:
      {
         optional_data:
         uid:
         uname:
      }

   """
   uid=None
   if session.has_key('logged_in') and session['logged_in']:
      uid=session['id']
   else:
      return "You must be logged in as an employee to dequeue."
   if permissions.has_flag(uid, qid, permissions.EMPLOYEE):
      q_member = queue_server.dequeue(qid)
      if q_member is None:
         return jsonify({})
      return jsonify(q_member.__dict__)
   else:
      return 'You must be an employee to dequeue.'

@app.route('/searchResults')
def get_search_results():
   return 'Not implemented yet!'

@app.route('/search', methods=['POST'])
def search():
   """Searches for relevant queues.

   Right now, this ignores all arguments and returns all queues.
   Improved search functionality is coming in the Feature Complete Release.

   Args:
      keywords:
      location:
      qname:

   Returns:
      {
         "queue_info_list"= [
            {
               "avg_wait_time":
               "expected_wait":
               "member_position":
               "qid":
               "qname":
               "size":
             },
             {
               "avg_wait_time":
               "expected_wait":
               "member_position":
               "qid":
               "qname":
               "size":
             }
             etc...
         ]
      }

   """
   q_info_list = queue_server.get_all_queues_info()
   return jsonify(queue_info_list=[q_info.__dict__ for q_info in q_info_list])

@app.route('/popular', methods=['GET'])
def get_popular_queues():
   """Searches for popular queues.

   Right now, this does no logic and returns all queues.
   Improved popularity logic is coming in the Feature Complete Release.

   Args: none.

   Returns:
      {
         "queue_info_list"= [
            {
               "avg_wait_time":
               "expected_wait":
               "member_position":
               "qid":
               "qname":
               "size":
             },
             {
               "avg_wait_time":
               "expected_wait":
               "member_position":
               "qid":
               "qname":
               "size":
             }
             etc...
         ]
      }

   """
   q_info_list = queue_server.get_all_queues_info()
   return jsonify(queue_info_list=[q_info.__dict__ for q_info in q_info_list])

@app.route('/memberQueue', methods=['POST'])
def get_member_queue():
   return 'Not implemented yet!'

@app.route('/employeeView/<int:qid>', methods=['POST'])
def get_employee_queue(qid):
   """Allows the employee to view the queue info and the queue members.

   Args: none. The qid should be included with the url. Example: /employeeView/12345

   Returns: example return value
      {
        "member_list": [
          {
            "optional_data": "party_size:3",
            "uid": 0,
            "uname": "Creator"
          },
          {
            "optional_data": "party_size:5",
            "uid": 1,
            "uname": "Jim"
          },
          {
            "optional_data": null,
            "uid": 2317776437,
            "uname": "TheCreator"
          }
        ],
        "queue_info": {
          "avg_wait_time": null,
          "expected_wait": 10,
          "member_position": null,
          "qid": 0,
          "qname": "tgr4",
          "size": 3
        }
      }

   """
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

   Args:
      qid:

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
   if session.has_key('logged_in') and session['logged_in']:
      uid = session['id']
   else:
      return jsonify(Failure('You must be logged in with an admin account to view queue settings.'))
   try:
      if permissions.has_flag(uid, pid, permissions.ADMIN):
         queue = db_util.get_queue_settings(queueID)
         return jsonify(queue)
      else:
         return jsonify(Failure('You must be an admin of the queue to see queue settings.'))
   except sqlite3.Error as e:
      return e.message

@app.route('/queueStatus/<int:qid>')
def get_queue_status(qid):
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
   userid = None
   q_member = None
   if session.has_key('logged_in') and session['logged_in']:
      userid = session['id']
      q_member = QueueMember(uid=userid)
   elif request.json is not None:
      userid = int(request.json)
      rows = db_util.get_temp_user(userid)
      if rows:
         q_member = QueueMember(uid=userid)
   q_info = queue_server.get_info(q_member, qid)
   if q_info is None:
      return jsonify(Failure('The queue does not exist.'))
   return jsonify(q_info.__dict__)

@app.route('/myQueues', methods=['POST'])
def get_my_queues():
   """Gets the info about the queues you are in.

   If you are logged in, no args are needed.
   If you are a temp user, you can pass your confirmation number (temp uid) in
   to get the queues you are in.

   Args:
      uid: the confirmation number given to a temporary user when they join a queue.

   Returns: example return value.
      {
         "queue_info_list": [
            {
               "avg_wait_time": null,
               "expected_wait": 10,
               "member_position": 3,
               "qid": 0,
               "qname": "tgr4",
               "size": 4
            },
            {
               "avg_wait_time": null,
               "expected_wait": 10,
               "member_position": 1,
               "qid": 2,
               "qname": "bestqueueever",
               "size": 2
            }
         ]
      }
   """
   uid = None
   if session.has_key('logged_in') and session['logged_in']:
      uid = session['id']
   elif (request.json is not None) and db_util.get_temp_user(request.json):
      uid = request.json
   else:
      return jsonify(Failure('User is not logged in, and no uid was provided.'))
   q_info_list = queue_server.get_queue_info_list(uid)
   if q_info_list is None:
      return jsonify({})
   return jsonify(queue_info_list=[q_info.__dict__ for q_info in q_info_list])

@app.route('/remove')
def remove_queue_member():
	return jsonify(Failure('Not implemented yet!'))

@app.route('/qtracks')
def queue_tracks():
	return jsonify(Failure('Not implemented yet!'))

@app.route('/qtracksData')
def queue_tracks_data():
	return jsonify(Failure('Not implemented yet!'))


###############################################
# User routes:
###############################################

@app.route('/createUser', methods=['POST'])
def create_user():
   """

   Args:
      {
         email:
         fname:
         lname:
         pw:
         temp:
         uname:
      }

   Returns:
      {
        SUCCESS:
        error_message: (only if failure)
      }

   """
   print 'enter createUser route'
   user_data = request.json
   try:
      user_data['id'] = db_util.create_user(user_data)
      print 'exit create user route sucess.'
      return jsonify({'SUCCESS':True})
   except sqlite3.Error as e:
      print 'exit create user route failure.'
      return jsonify(Failure('Failed to create user.'))

@app.route('/login', methods=['GET', 'POST'])
def login():
   """

   Args:
      {
         uname:
         pw:
      }

   Returns:
      {
         SUCCESS:
         error_message: (only if failure)
      }

   """
   if request.method == 'GET':
      return app.send_static_file('partials/login.html')
   else:
      # If user is already logged in, let them log in again.
      # if session.has_key('logged_in') and session['logged_in']:
          # user is already logged in
          # return jsonify({'SUCCESS':True})
      try:
         user = db_util.get_user(request.json['uname'], request.json['pw'])
         session['logged_in'] = True
         session['id'] = user['id']
         session['uname'] = user['uname']
         return jsonify({'SUCCESS':True})
      except sqlite3.Error as e:
         return jsonify(Failure('login failed.'))
      except db_util.ValidationException as e:
         session['logged_in'] = False
         return jsonify(Failure('Invalid username or password'))

@app.route('/logout')
def logout():
   """

   Args: none.
   Returns: a string describing what happened.

   """
   if session.has_key('logged_in'):
      if session['logged_in']:
         for key in  session.keys():
            session[key] = None
         return 'Logged out.'
   return 'You are not logged in!'

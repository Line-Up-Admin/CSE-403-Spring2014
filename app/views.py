# This is the file that contains all the route handlers.
from app import app, queue_server
import database_utilities as db_util
import validators
import sqlite3
from flask import request, session, g, redirect, url_for, abort, jsonify
import permissions

from q_classes import QueueServer, QueueMember, QueueSettings, QueueNotFoundException, MemberNotFoundException, QueueFullException

def Failure(message):
   return {'SUCCESS':False, 'error_message':message}

def Success(dict_to_be_jsonified):
   dict_to_be_jsonified['SUCCESS'] = True
   return dict_to_be_jsonified

# This procedure picks up the default route and returns index.html.
@app.route('/')
def root():
	# If user is already logged in, let them log in again
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

   

   """
   try:
      q_settings = request.get_json()
   except:
      return abort(500)
   q_settings = validators.validate_q_settings(q_settings)
   if not q_settings['SUCCESS']:
      return jsonify(q_settings)
   if not session.has_key('logged_in') or not session['logged_in']:
      return jsonify(Failure('You cannot create a queue if you are not logged in!'))
   try:
      q_settings['qid'] = queue_server.create(q_settings)
      return jsonify(q_settings)
   except db_util.ValidationException as e:
      q_settings['SUCCESS'] = False
      return jsonify(q_settings)
   except sqlite3.Error as e:
      return abort(500)

@app.route('/setActive/<int:qid>', methods=['POST'])
def set_active(qid):
   if not session.has_key('logged_in') or not session['logged_in']:
      return jsonify(Failure('You are not logged in!'))
   if not permissions.has_flag(session['id'], qid, permissions.MANAGER):
      return jsonify(Failure('You must be logged in as a manager to deactivate the queue.'))
   active = request.get_json()
   if active is None or type(active) is not int:
      return abort(500)
   try:
      queue_server.set_active(qid, active)
      return jsonify(Success({}))
   except sqlite3.Error:
      abort(500)
   except QueueNotFoundException as e:
      return jsonify(Failure('The queue was not found.'))

@app.route('/join', methods=['POST'])
def add_to_queue():
   """Joins a queue.

   Args:
      qid: the id of the queue to join.
      uname: the uname to create a temporary user. This is ignored if the user is logged in.
      optional_data:

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
   optional_data = None
   qid = int(request.json['qid'])
   if request.json.has_key('optional_data'):
      optional_data = request.json['optional_data']
   if not queue_server.is_active(qid):
      return jsonify(Failure('The queue is not active!'))
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
         return abort(500)
      username = temp_user['uname']
      uid = temp_user['id']
      session['logged_in'] = True
      session['id'] = uid
      session['uname'] = username
   if not permissions.has_flag(uid, qid, permissions.BLOCKED_USER):
      q_member = QueueMember(username, uid, optional_data)
      try:
         queue_server.add(q_member, qid)
      except sqlite3.Error:
         return abort(500)
      except QueueFullException as e:
         return jsonify(Failure(e.message))
      except QueueNotFoundException as e:
         return jsonify(Failure(e.message))
      q_info = queue_server.get_info(q_member, qid)
      q_info_dict = dict(q_info.__dict__)
      if temp:
         q_info_dict['confirmation_number'] = uid
      return jsonify(q_info_dict)
   else:
      return 'User is blocked from this queue.'

@app.route('/enqueue/<int:qid>', methods=['POST'])
def enqueue(qid):
   if not session.has_key('logged_in') or not session['logged_in']:
      return jsonify(Failure('You are not logged in!'))
   if not queue_server.is_active(qid):
      return jsonify(Failure('The queue is not active.'))
   temp_user = dict()
   optional_data = None
   data = request.get_json()
   fail = dict()
   fail['SUCCESS'] = True
   uname_msg = 'Name is required.'
   optional_data_required = False
   try:
      settings = queue_server.get_settings(qid)
      if settings.prompt is not None and len(settings.prompt) > 0:
         optional_data_required = True
   except QueueNotFoundException as e:
      return jsonify(Failure(e.message))
   if data is None or len(data) == 0:
      fail['SUCCESS'] = False
      fail['uname'] = uname_msg
   else:
      if data.has_key('optional_data') and len(data['optional_data']) > 0:
         optional_data = data['optional_data']
      if data.has_key('uname') and len(data['uname']) > 0:
         temp_user['uname'] = data['uname']
   if not temp_user.has_key('uname'):
      fail['SUCCESS'] = False
      fail['uname'] = uname_msg
   if optional_data is None and optional_data_required:
      fail['SUCCESS'] = False
      fail['optional_data'] = 'Required'
   if not fail['SUCCESS']:
      return jsonify(fail)
   if not permissions.has_flag(session['id'], qid, permissions.MANAGER):
      return jsonify(Failure('You must be logged in as a manager to enqueue.'))
   # got the temp uname, manager logged in and confirmed.
   try:
      temp_user['id'] = db_util.create_temp_user(temp_user)
   except sqlite3.Error as e:
      return abort(500)
   try:
      queue_server.add(QueueMember(temp_user['uname'], temp_user['id'], optional_data), qid)
      return jsonify(Success({}))
   except sqlite3.Error:
      return abort(500)
   except QueueNotFoundException as e:
      return jsonify(Failure(e.message))
   except QueueFullException as e:
      return jsonify(Failure(e.message))

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
      return "You must be logged in as an manager to dequeue."
   if permissions.has_flag(uid, qid, permissions.MANAGER):
      q_member = queue_server.dequeue(qid)
      if q_member is None:
         return jsonify({})
      return jsonify(q_member.__dict__)
   else:
      return 'You must be an manager to dequeue.'

@app.route('/postpone', methods=['POST'])
def postpone():
   """
   Args:
   {
      qid:
   }

   Returns:
   {
      'SUCCESS': True or False
      (if SUCCESS is true)
      'qname':
      'qid':
      'size':
      'expected_wait:
      'avg_wait_time':
      'member_position':
      'organization':
      'prompt':
      'disclaimer':
      'website':
      'location':
      (if SUCCESS is false)
      'error_message':
   }
   
   """
   if session.has_key('logged_in') and session['logged_in']:
      uid = session['id']
   else:
      return jsonify(Failure('You are not logged in!'))
   qid= request.json
   try:
      queue_server.postpone(QueueMember(uid=uid), qid)
      q_info = queue_server.get_info(QueueMember(uid=uid), qid)
      q_info_dict = dict(q_info.__dict__)
      return jsonify(Success(q_info_dict))
   except QueueNotFoundException as e:
      return jsonify(Failure(e.message))
   except MemberNotFoundException as e:
      return jsonify(Failure(e.message))
   except sqlite3.Error as e:
      return jsonify(Failure(e.message))

@app.route('/managerPostpone', methods=['POST'])
def manager_postpone():
   """
   Args:
   {
      qid:
      uid:
   }

   Returns:
   {
      'SUCCESS': True or False
      (if SUCCESS is true)
      'qname':
      'qid':
      'size':
      'expected_wait:
      'avg_wait_time':
      'member_position':
      'organization':
      'prompt':
      'disclaimer':
      'website':
      'location':
      (if SUCCESS is false)
      'error_message':
   }
   
   """
   if session.has_key('logged_in') and session['logged_in']:
      manager_id = session['id']
   else:
      return jsonify(Failure('You are not logged in!'))
   qid = int(request.json['qid'])
   uid = int(request.json['uid'])
   try:
      if not permissions.has_flag(manager_id, qid, permissions.MANAGER):
         return jsonify(Failure('You must be a manager of the queue to postpone someone!'))
      queue_server.postpone(QueueMember(uid=uid), qid)
      q_info = queue_server.get_info(QueueMember(uid=uid), qid)
      q_info_dict = dict(q_info.__dict__)
      return jsonify(Success(q_info_dict))
   except QueueNotFoundException as e:
      return jsonify(Failure(e.message))
   except MemberNotFoundException as e:
      return jsonify(Failure(e.message))
   except sqlite3.Error as e:
      return jsonify(Failure(e.message))

@app.route('/leaveQueue', methods=['POST'])
def leave_queue():
   """
   Args:
   {
      qid
   }

   Returns:
   {
      'SUCCESS': True or False
      (if SUCCESS is true)
      'qname':
      'qid':
      'size':
      'expected_wait:
      'avg_wait_time':
      'member_position':
      'organization':
      'prompt':
      'disclaimer':
      'website':
      'location':
      (if SUCCESS is false)
      'error_message':
   }

   """
      
   if not session.has_key('logged_in') and session['logged_in']:
      return jsonify(Failure('You are not logged in!'))
   uid=session['id']
   qid=request.json
   try:
      queue_server.remove(QueueMember(uid=uid), qid)
      return jsonify(Success({}))
   except sqlite3.Error as e:
      return jsonify(Failure('Failed to leave the queue.'))
   except QueueNotFoundException as e:
      return jsonify(Failure(e.message))

@app.route('/searchResults')
def get_search_results():
   return 'Not implemented yet!'

@app.route('/search', methods=['POST'])
def search():
   """Searches for relevant queues.

   Right now, this ignores all arguments and returns all queues.
   Improved search functionality is coming in the Feature Complete Release.

   Args:
      search_string:

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

   search_string = request.data
   qids = queue_server.search(search_string)
   q_info_list = [queue_server.get_info(None, qid) for qid in qids]
   return jsonify(queue_info_list=[q_info.__dict__ for q_info in q_info_list])

@app.route('/popular', methods=['GET'])
def get_popular_queues():
   """Searches for popular queues.

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
   #Filter the top 4
   qids = queue_server.get_popular()[:4]
   q_info_list = [queue_server.get_info(None, qid) for qid in qids]
   return jsonify(queue_info_list=[q_info.__dict__ for q_info in q_info_list])

@app.route('/memberQueue', methods=['POST'])
def get_member_queue():
   return 'Not implemented yet!'



@app.route('/managerView/<int:qid>', methods=['POST'])
def get_manager_queue(qid):
   """Allows the manager to view the queue info and the queue members.

   Args: none. The qid should be included with the url. Example: /managerView/12345

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
      return jsonify(Failure("You must be logged in as an manager to dequeue."))
   if permissions.has_flag(uid, qid, permissions.MANAGER):
      members = queue_server.get_members(qid)
      q_info = queue_server.get_info(None, qid)
      return jsonify(queue_info=q_info.__dict__, member_list=[member.__dict__ for member in members])
   else:
      return jsonify(Failure('You must be a manager of the queue to view queue members.'))

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
   qid = request.json
   if session.has_key('logged_in') and session['logged_in']:
      uid = session['id']
   else:
      return jsonify(Failure('You must be logged in with an admin account to view queue settings.'))
   try:
      if permissions.has_flag(uid, qid, permissions.ADMIN):
         queue = queue_server.get_settings(qid)
         return jsonify(queue.__dict__)
      else:
         return jsonify(Failure('You must be an admin of the queue to see queue settings.'))
   except sqlite3.Error as e:
      return abort(500)

@app.route('/queueStatus/<int:qid>')
def get_queue_status(qid):
   """View the queue with the given qid.

   Returns: example return value below
      {
         "avg_wait_time": null,
         "confirmation_number": null,
         "expected_wait": null,
         "logged_in": True or False
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
   q_info_dict = dict(q_info.__dict__)
   q_info_dict['logged_in'] = session.has_key('logged_in') and session['logged_in']
   return jsonify(Success(q_info_dict))


@app.route('/editQueue', methods=['POST'])
def edit_queue():
   """Change the settings for a queue.
   Args:
      {
         qid:
         q_settings:
      }
   Returns:
      {
         SUCCESS:
         error_message: (only if failure)
      }
   """
   uid = None
   if session.has_key('logged_in') and session['logged_in']:
      uid = session['id']
      qsettings = request.json['q_settings']
      qsettings = validators.validate_q_settings(qsettings)
      if not qsettings['SUCCESS']:
         return jsonify(qsettings)
      if permissions.has_flag(uid, qsettings['qid'], permissions.ADMIN):
         try:
            queue_server.edit_queue(qsettings['qid'], qsettings)
            return jsonify({'SUCCESS':True})
         except QueueNotFoundException as e:
            return jsonify(Failure(e.message))
      else:
        return jsonify(Failure("You must be logged in as an admin to edit queue settings."))
   else:
     return jsonify(Failure("You must at least be logged in to edit queue settings."))
      
@app.route('/myQueues', methods=['GET', 'POST'])
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
   queues_in_info_list = queue_server.get_queue_info_list(uid)
   if queues_in_info_list is None:
      queues_in_info_list = list()
   qids_admin_rows = db_util.get_permissioned_qids(uid, permissions.ADMIN)
   if qids_admin_rows is None:
      queues_admin_info_list = list()
   else:
      queues_admin_info_list = [queue_server.get_info(None, row['qid']) for row in qids_admin_rows]
   qids_manager_rows = db_util.get_permissioned_qids(uid, permissions.MANAGER)
   if qids_manager_rows is None:
      queues_manager_info_list = list()
   else:
      queues_manager_info_list = [queue_server.get_info(None, row['qid']) for row in qids_manager_rows]
   return jsonify(queues_in=[q_info.__dict__ for q_info in queues_in_info_list],
                  queues_admin=[q_info.__dict__ for q_info in queues_admin_info_list],
                  queues_manager=[q_info.__dict__ for q_info in queues_manager_info_list],
                  SUCCESS=True)

@app.route('/remove', methods=['POST'])
def remove_queue_member():
   """
   Args:
      {
         qid:
         uid:
      }
   
   Returns:
      {
         SUCCESS:
         error_message: (only if failure)
      }

   """
   uid = None
   if session.has_key('logged_in') and session['logged_in']:
      manager_id = session['id']
      qid = int(request.json['qid'])
      uid = int(request.json['uid'])
      if permissions.has_flag(manager_id, qid, permissions.MANAGER):
         try:
            print 'QueueMember ID = ', uid, ', qid = ', qid
            queue_server.remove(QueueMember(uid=uid), qid)
            return jsonify({'SUCCESS':True})
         except QueueNotFoundException as e:
            return jsonify(Failure(e.message))
      else:
        return jsonify(Failure("You must be a manager to remove a user."))
   else:
     return jsonify(Failure("You must be logged in as a manager to remove a user."))

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
#   print 'header:'
#   print request.headers
#   print 'data:'
#   print request.data
#   print 'json:'
#   print request.json
   
   try:
      user_data = request.get_json()
   except:
      abort(500)
   user_data = validators.validate_user(user_data)
   if not user_data['SUCCESS']:
      return jsonify(user_data)
   try:
      user_data['id'] = db_util.create_user(user_data)
      print 'exit create user route sucess.'
      return jsonify({'SUCCESS':True})
   except sqlite3.Error as e:
      print 'exit create user route failure.'
      return abort(500)
   except db_util.ValidationException as e:
      return jsonify({'SUCCESS':False, 'uname':'The User Name is already taken'})
      
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
      # if user is already logged in, home should just take them to user home
			# but if they somehow get to index.html, they are able to log in again as normal
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
         return '<meta http-equiv="refresh" content="0; url=/" />'
   return 'You are not logged in!'

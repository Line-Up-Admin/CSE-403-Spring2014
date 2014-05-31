# This is the file that contains all the route handlers.
from app import app, queue_server
import database_utilities as db_util
import sqlite3
from flask import request, session, g, redirect, url_for, abort, jsonify
import permissions
import validators

from q_classes import QueueServer, QueueMember, QueueSettings, QueueNotFoundException, MemberNotFoundException, QueueFullException

def Failure(message):
   return {'SUCCESS':False, 'error_message':message}

def Success(dict_to_be_jsonified):
   dict_to_be_jsonified['SUCCESS'] = True
   return dict_to_be_jsonified

# Temporary: debugging purposes only.
@app.route('/helloworld', methods=['GET', 'POST'])
def helloworld():
    return 'Hello World!'

@app.route('/debug/getUser', methods=['GET', 'POST'])
def get_user_debug():
	if not app.debug:
	    abort(404)
	username = request.args.get('uname')
	password = request.args.get('pw')
	try:
		user = db_util.get_user(username, password)
		return jsonify(user)
	except sqlite3.Error as e:
		return e.message
	except db_util.ValidationException as e:
		return e.message

# Temporary: debugging purposes only.
@app.route('/debug/gettempuser', methods=['GET', 'POST'])
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
@app.route('/debug/createuser', methods=['GET', 'POST'])
def create_user_debug():
	if not app.debug:
		abort(404)
	user = request.args.copy()
	try:
		user['id'] = db_util.create_user(user)
		return jsonify(user)
	except sqlite3.Error as e:
		return e.message

@app.route('/debug/getQueueSettings', methods=['GET', 'POST'])
def get_queue_settings_debug():
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
   qid = int(request.args['qid'])
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
      return jsonify(Failure(e.message))

@app.route('/debug/modifyQueue', methods=['GET', 'POST'])
def debug_modify_queue_settings():
   uid = None
   if not session.has_key('logged_in') or not session['logged_in']:
      return jsonify(Failure('You are not logged in!'))
   uid = session['id']
   try:
      qsettings = copy_request_args(request)
      print qsettings
   except:
      return abort(500)
   if not permissions.has_flag(uid, qsettings['qid'], permissions.ADMIN):
      return jsonify(Failure('You must own this queue to modify settings!'))
   qsettings = validators.validate_q_settings(qsettings)
   if not qsettings['SUCCESS']:
      return jsonify(qsettings)
   try:
      queue_server.edit_queue(qsettings['qid'], qsettings)
      return jsonify({'SUCCESS':True})
   except QueueNotFoundException as e:
      return jsonify(Failure(e.message))

@app.route('/debug/search', methods=['GET'])
def search_debug():
   search_string = request.args["search_string"]
   qids = queue_server.search(search_string)
   print qids
   q_info_list = [queue_server.get_info(None, qid) for qid in qids]
   return jsonify(queue_info_list=[q_info.__dict__ for q_info in q_info_list])



@app.route('/debug/createqueue', methods=['GET', 'POST'])
def create_queue_debug():
   queueSettings = copy_request_args(request)
   if not session.has_key('logged_in') or not session['logged_in']:
      return 'You are not logged in.'
   if queueSettings.has_key('admins'):
      queueSettings['admins'] = [admin.strip() for admin in queueSettings['admins'].split(',')]
   else:
      queueSettings['admins'] = list()
   if not session['uname'] in queueSettings['admins']:
      queueSettings['admins'].append(session['uname'])
   if queueSettings.has_key('managers'):
      queueSettings['managers'] = [e.strip() for e in queueSettings['managers'].split(',')]
   if queueSettings.has_key('blocked_users'):
      queueSettings['blocked_users'] = [b.strip() for b in queueSettings['blocked_users'].split(',')]
   print queueSettings
   queueSettings['qid'] = queue_server.create(queueSettings)
   return jsonify(queueSettings)

@app.route('/debug/createtempuser', methods=['GET', 'POST'])
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

@app.route('/debug/popular', methods=['GET', 'POST'])
def get_popular_queues_debug():
   q_info_list = queue_server.get_all_queues_info()
   return jsonify(queue_info_list=[q_info.__dict__ for q_info in q_info_list])
      

@app.route('/debug/login', methods=['GET', 'POST'])
def login_debug():
   if session.has_key('logged_in'):
      if session['logged_in']:
         # user is already logged in
         return 'User is already logged in.'
   try:
      user = db_util.get_user(request.args.get('uname'), request.args.get('pw'))
      session['logged_in'] = True
      session['id'] = user['id']
      session['uname'] = user['uname']
      return jsonify(user)
   except sqlite3.Error as e:
      return e.message
   except db_util.ValidationException as e:
      session['logged_in'] = False
      return e.message

@app.route('/debug/logout', methods=['GET', 'POST'])
def logout_debug():
    if session.has_key('logged_in'):
        if session['logged_in']:
            for key in  session.keys():
                session[key] = None
            return 'Logged out.'
    return 'You are not logged in!'

@app.route('/debug/queueStatus/<int:qid>', methods=['GET', 'POST'])
def get_queue_info_debug(qid):
   q_info = queue_server.get_info(None, qid)
   return jsonify(q_info.__dict__)

@app.route('/debug/myqueues', methods=['GET', 'POST'])
def get_my_queues_debug():
   if not app.debug:
      abort(404)
   uid = None
   if session.has_key('logged_in') and session['logged_in']:
      uid = session['id']
   else:
      uid = int(request.args.get('uid'))
   q_info_list = queue_server.get_queue_info_list(uid)
   if q_info_list is None:
       return jsonify(queue_info_list={})
   return jsonify(queue_info_list=[q_info.__dict__ for q_info in q_info_list])
       
@app.route('/debug/managerView/<int:qid>', methods=['GET', 'POST'])
def get_queue_info_and_members(qid):
    if not app.debug:
        abort(404)
    uid = None
    if session.has_key('logged_in') and session['logged_in']:
        uid = session['id']
    else:
        uid = int(request.args.get('uid'))
    if permissions.has_flag(uid, qid, permissions.MANAGER):
        members = queue_server.get_members(qid)
        q_info = queue_server.get_info(None, qid)
        return jsonify(queue_info=q_info.__dict__, member_list=[member.__dict__ for member in members])

@app.route('/debug/setActive/<int:qid>', methods=['GET', 'POST'])
def set_active_debug(qid):
   if not session.has_key('logged_in') or not session['logged_in']:
      return jsonify(Failure('You are not logged in!'))
   if not permissions.has_flag(session['id'], qid, permissions.MANAGER):
      return jsonify(Failure('You must be logged in as a manager to deactivate the queue.'))
   active = int(request.args['active'])
   if active is None or type(active) is not int:
      return abort(500)
   try:
      queue_server.set_active(qid, active)
      return jsonify(Success({}))
   except sqlite3.Error:
      abort(500)
   except QueueNotFoundException as e:
      return jsonify(Failure('The queue was not found.'))

@app.route('/debug/join/<int:qid>', methods=['GET', 'POST'])
def add_to_queue_debug(qid):
   if not app.debug:
      abort(404)
   if not queue_server.is_active(qid):
      return jsonify(Failure('The queue is not active!'))
   uid = None
   username = None
   temp = False
   if session.has_key('logged_in') and session['logged_in']:
      uid = session['id']
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
      try:
         queue_server.add(q_member, qid)
      except QueueFullException as e:
         return jsonify(Failure(e.message))
      q_info = queue_server.get_info(q_member, qid)
      q_info_dict = dict(q_info.__dict__)
      if temp:
         q_info_dict['confirmation_number'] = uid
      return jsonify(q_info_dict)
   else:
      return 'User is blocked from this queue.'

@app.route('/debug/enqueue/<int:qid>', methods=['GET', 'POST'])
def enqueue_debug(qid):
   if not session.has_key('logged_in') or not session['logged_in']:
      return jsonify(Failure('You are not logged in!'))
   if not queue_server.is_active(qid):
      return jsonify(Failure('The queue is not active.'))
   temp_user = dict()
   optional_data = None
   data = request.args
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

@app.route('/debug/dequeue/<int:qid>', methods=['GET', 'POST'])
def dequeue_debug(qid):
   mid = None
   try:
      uid = int(request.args['uid'])
   except:
      return abort(500)
   if session.has_key('logged_in') and session['logged_in']:
      mid=session['id']
   else:
      return jsonify(Failure("You must be logged in as an manager to dequeue."))
   if permissions.has_flag(mid, qid, permissions.MANAGER):
      try:
         member = queue_server.peek(qid)
         if not member.uid == uid:
            return jsonify(Failure('This person is no longer at the front of the queue!'))
         q_member = queue_server.dequeue(qid)
         if q_member is None:
            return jsonify({})
         return jsonify(q_member.__dict__)
      except QueueNotFoundException as e:
         return jsonify(Failure(e.message))
   else:
      return jsonify(Failure('You must be an manager to dequeue.'))

@app.route('/debug/remove', methods=['GET', 'POST'])
def debug_remove():
   qid = int(request.args['qid'])
   uid = int(request.args['uid'])
   queue_server.remove(QueueMember(uid=uid), qid)
   return {'SUCCESS':True}

@app.route('/debug/postpone', methods=['GET', 'POST'])
def dequeue_postpone():
   if not app.debug:
      abort(404)
   if session.has_key('logged_in') and session['logged_in']:
      uid = session['id']
   else:
      raise Exception('You are not logged in!')
   qid=int(request.args.get('qid'))
   queue_server.postpone(QueueMember(uid=uid), qid)
   q_info_dict = dict(queue_server.get_info(QueueMember(uid=uid), qid).__dict__)
   return jsonify(Success(q_info_dict))

def copy_request_args(origRequest):
   res = dict()
   for key in origRequest.args.keys():
      res[key] = origRequest.args.get(key)
   return res;

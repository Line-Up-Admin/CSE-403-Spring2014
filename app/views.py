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
   uid = None
   username = None
   qid = request.json['qid']
   if session['logged_in']:
      uid = session['uid']
      username = session['username']
   else:
      temp_user = dict()
      temp_user['username'] = request.json['username']
      try:
         temp_user['id'] = db_util.create_user(temp_user)
      except sqlite3.Error as e:
         return e.message
      username = temp_user['username']
      uid = temp_user['id']
   if not permissions.has_flag(uid, qid, permissions.BLOCKED_USER):
      q_member = QueueMember(username, uid)
      queue_server.add(q_member, qid)
      q_info = queue_server.get_info(q_member, qid)
      return jsonify(q_info.__dict__)
   else:
      return 'User is blocked from this queue.'

@app.route('/login', methods=['GET','POST'])
def login():
   return 'Not implemented yet!'

@app.route('/dequeue', methods=['POST'])
def dequeue():
   uid = None
   if not session['logged_in']:
      raise

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
   q_settings = request.json
   try:
      q_settings['id'] = db_util.create_queue(q_settings)
      return jsonify(q_settings)
   except sqlite3.Error as e:
      return e.message

@app.route('/logout')
def logout():
	return 'Not implemented yet!'

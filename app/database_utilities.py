"""Database Utilities to be used by higher application layers.

All methods throw a DatabaseException if the database operation failed.
No classes have to be instantiated except the initial database declared in
__init__.py in app. All methods are static.
"""

from sys import maxint

# Query constants
GET_SPECIAL_UNAMES_BY_QID = 'select u.uname from users as u join permissions as p on p.pid=u.id and p.qid=? and p.permission_level=?'
GET_ALL_QUEUES = 'select * from queues'
GET_ALL_QUEUE_SETTINGS = 'select * from qsettings'
GET_MEMBER_DATA_BY_QID = 'select qi.uid, u.uname, qi.relative_position, qi.optional_data from qindex as qi join users as u on qi.qid=? and qi.uid=u.id order by qi.relative_position'
GET_PERMISSIONED_QIDS_BY_UID = 'select qid from permissions where pid=? and permission_level=?'
GET_POSITION = 'select relative_position from qindex where uid=? and qid=?'
GET_PROFILED_USER_BY_USERNAME = 'select * from users where temp=0 and uname=?'
GET_Q_HISTORY_BY_QID = 'select * from qhistory where qid=? and join_time is not null and leave_time is not null'
GET_QUEUES_BY_UID = 'select * from qindex where uid=?'
GET_QUEUE_SETTINGS_BY_ID = 'select * from qsettings where qid=?'
GET_TEMP_USER_BY_ID = 'select * from users where temp=1 and id=?'
INSERT_INTO_QUEUE_HISTORY = 'insert into QHistory values (?, ?, ?, ?)'
INSERT_MEMBER_INTO_QUEUE = 'insert into QIndex values(?, ?, (select ending_index from Queues where id=?), ?)'
INSERT_PROFILED_USER = 'insert into users values(?, ?, ?, ?, ?, ?, ?, ?)'
INSERT_QUEUE = 'insert into queues values(?, 0, 0)'
INSERT_QUEUE_SETTINGS = 'insert into qsettings values(?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)'
INSERT_TEMP_USER = 'insert into users values(?, 1, ?, NULL, NULL, NULL, NULL, NULL)'
REMOVE_MEMBER_FROM_QUEUE = 'delete from qindex where uid=? and qid=?'
UPDATE_POSITION = 'update qindex set relative_position=? where uid=? and qid=?'
UPDATE_QUEUE_FOR_ADD = 'update Queues set ending_index=ending_index+1 where id=?'
UPDATE_QUEUE_FOR_REMOVE = 'update queues set starting_index=starting_index+1 where id=?'
UPDATE_QUEUE_HISTORY = 'update qhistory set leave_time=? where uid=? and qid=? and leave_time is null'
UPDATE_QUEUE_SETTINGS = 'update qsettings set qname=?, max_size=?, keywords=?, location=?, active=?, min_wait_rejoin=?, website=?, organization=?, disclaimer=?, prompt=? where qid=?'


def query_db(query, args=()):
  db = get_db()
  cursor = db.execute(query, args)
  rows = cursor.fetchall()
  cursor.close()
  return rows

def check_usernames(usernames):
  result = {'SUCCESS': False}
  for username in usernames:
    rows = query_db(GET_PROFILED_USER_BY_USERNAME, (username,))
    if (not rows) or (len(rows) == 0):
      result['username'] = username
      return result
  result['SUCCESS'] = True
  return result

def user_dict_to_db_tuple(user_dict):
  return (user_dict['id'],
          user_dict['temp'] if user_dict.has_key('temp') else 0,
          user_dict['uname'],
          user_dict['fname'] if user_dict.has_key('fname') else None,
          user_dict['lname'] if user_dict.has_key('lname') else None,
          user_dict['email'] if user_dict.has_key('email') else None,
          user_dict['pw'],
          user_dict['salt']
          )

def qsettings_dict_to_db_tuple(qsettings):
  return (qsettings['qid'],
          qsettings['qname'],
          qsettings['max_size'] if qsettings.has_key('max_size') else maxint,
          qsettings['keywords'] if qsettings.has_key('keywords') else None,
          qsettings['location'] if qsettings.has_key('location') else None,
          qsettings['active'] if qsettings.has_key('active') else 1,
          qsettings['min_wait_rejoin'] if qsettings.has_key('min_wait_rejoin') else 0,
          qsettings['website'] if qsettings.has_key('website') else None,
          qsettings['organization'] if qsettings.has_key('organization') else None,
          qsettings['disclaimer'] if qsettings.has_key('disclaimer') else None,
          qsettings['prompt'] if qsettings.has_key('prompt') else None
          )

def qsettings_dict_to_db_tuple_modify(qsettings):
  return (qsettings['qname'],
          qsettings['max_size'] if qsettings.has_key('max_size') else maxint,
          qsettings['keywords'] if qsettings.has_key('keywords') else None,
          qsettings['location'] if qsettings.has_key('location') else None,
          qsettings['active'] if qsettings.has_key('active') else 1,
          qsettings['min_wait_rejoin'] if qsettings.has_key('min_wait_rejoin') else maxint,
          qsettings['website'] if qsettings.has_key('website') else None,
          qsettings['organization'] if qsettings.has_key('organization') else None,
          qsettings['disclaimer'] if qsettings.has_key('disclaimer') else None,
          qsettings['prompt'] if qsettings.has_key('prompt') else None,
          qsettings['qid']
          )

class DatabaseException(Exception):
  pass

class PermissionException(Exception):
  pass

class ValidationException(Exception):
  pass

# Database Utilities
import permissions
import validators
import sqlite3
import time
from app import get_db

#############################################
# User related utilities.
#############################################

def create_temp_user(user_dict):
  db = get_db()
  user_dict['id'] = validators.get_unique_user_id()
  db.execute(INSERT_TEMP_USER, (user_dict['id'], user_dict['uname']))
  db.commit()
  return user_dict['id']

def create_user_profile(user_dict):
  try:
    print 'enter db_util.create_user_profile'
    db = get_db()
    rows = query_db(GET_PROFILED_USER_BY_USERNAME, (user_dict['uname'],))
    if (rows and (len(rows) > 0)):
      raise ValidationException('The given username is already in use.')
    result = validators.encrypt_password(user_dict['pw'])
    user_dict['pw'] = result[0]
    user_dict['salt'] = result[1]
    user_dict['id'] = validators.get_unique_user_id()
    user_dict['temp'] = 0
    db.execute(INSERT_PROFILED_USER, user_dict_to_db_tuple(user_dict))
    db.commit()
    print 'exit db_util.create_user_profile: success.'
    return user_dict['id']
  except sqlite3.Error as e:
    print 'exit db_util.create_user_profile: failure. '
    print e.message
    raise e

def create_user(user_dict):
  """Adds a user defined by user_data to the database.

  Args:
    user_data: the data about the user to be added to the database. The uid will be ignored if included.

  Returns:
    The new uid if the user was successfully added to the database.

  Raises:
    sqlite3.Error: the database operation failed.
    ValidationError: the username is already in use (only applies if account isn't temporary).
  """
  if not user_dict.has_key('temp') or not user_dict['temp']:
    user_dict['id'] = create_user_profile(user_dict)
  else:
    user_dict['id'] = create_temp_user(user_dict)
  return user_dict['id']

def modify_user(user_data):
  """Modfiy the user to match the user_data.

  The uid, username, and password are obtained from the current session, not the user_data.

  Args:
    user_data: the data about the user to be modified in the database. The id will be used to find the user in the database.

  Returns:
    None if the user's data was successfully updated.

  Raises:
    DatabaseException: the uid does not exist in the database.
    ValidationException: the current session user is not logged in.
    ValueError: the given user_data is invalid.
  """
  raise NotImplementedError()

def delete_user():
  """Deletes the current session user from the database.

  Returns:
    None if the deletion was a success.

  Raises:
    sqlite3.Error: database operation failed.
    ValidationException: the current session user is not logged in.
    PermissionException: the current session does not have the required permissions.
  """
  raise NotImplementedError()

def get_user_by_uname(username):
  rows = query_db(GET_PROFILED_USER_BY_USERNAME, (username,))
  if (not rows) or (len(rows) == 0):
    raise ValidationException('The username', username, 'was not found.')
  else:
    return rows[0]

def get_uids(usernames):
  uids = list()
  for username in usernames:
    rows = query_db(GET_PROFILED_USER_BY_USERNAME, (username,))
    if rows is not None and len(rows) > 0:
      uids.append(rows[0]['id'])
  return uids

def get_user(username, given_password):
  """Retrieves the User associated with this user.

  Returns:
    A User object if the user was found. No temporary users are considered.

  Raises:
    sqlite3.Error: database operation failed.
    ValidationException: the username password combination is invalid.
  """
  err = 'The username password combination is invalid.'
  rows = query_db(GET_PROFILED_USER_BY_USERNAME, (username,))
  if (not rows) or (len(rows) == 0):
    raise ValidationException(err)
  else:
    encrypted_password = rows[0]['pw']
    salt = rows[0]['salt']
    if validators.are_matching(encrypted_password, salt, given_password):
      return rows[0]
    else:
      print 'passwords did not match.'
      raise ValidationException(err)

def get_user_by_uid(uid):
  rows = query_db('select * from users where uid=?', (uid,))
  return rows

def get_temp_user(temp_uid):
  """Retrieves the user data associated with the given user id, only if the uid matches a temporary user.

  Returns:
    A User object if the user was found. Only temporary users are examined.

  Raises:
    DatabaseException: the temp_uid was not a temporary user.
  """
  rows = query_db(GET_TEMP_USER_BY_ID, (temp_uid,))
  if (not rows) or (len(rows) == 0):
    return None
  else:
    return rows[0]

def get_special_users(qid, permission_level):
  unames = list()
  rows = query_db(GET_SPECIAL_UNAMES_BY_QID, (qid, permission_level))
  if rows is not None:
    unames = [row[0] for row in rows]
  return unames
  

#################################################
# Queue related utilities.
#################################################

def get_history(qid):
   # This will be expanded upon
   rows = query_db(GET_Q_HISTORY_BY_QID, (qid,))
   return rows

def create_queue(q_settings):
  """Creates a new queue with the defined settings. All settings except qid must exist.

  Args:
    q_settings: the settings for the new queue. The qid will be ignored if included.

  Returns:
    The new qid if the queue was successfully created.

  Raises:
    ValidationException: the username <uname> was not found.
  """
  q_settings['qid'] = validators.get_unique_queue_id()
  if q_settings.has_key('admins'):
    permissions.add_permission_list(get_uids(q_settings['admins']), q_settings['qid'], permissions.ADMIN)
  if q_settings.has_key('managers'):
    permissions.add_permission_list(get_uids(q_settings['managers']), q_settings['qid'], permissions.MANAGER)
  if q_settings.has_key('blocked_users'):
    permissions.add_permission_list(get_uids(q_settings['blocked_users']), q_settings['qid'], permissions.BLOCKED_USER)
  db = get_db()
  db.execute(INSERT_QUEUE, (q_settings['qid'],))
  db.execute(INSERT_QUEUE_SETTINGS, qsettings_dict_to_db_tuple(q_settings))
  db.commit()
  return q_settings['qid']

def modify_queue_settings(q_settings):
  """Modifies the queue with the qid defined in q_settings to match the q_settings given.

  If the user's session does not have proper permissions, a PermissionException will be raised.

  Args:
    q_settings: the settings for the queue to be modified. The qid will be used to find the queue in the database.

  Returns:
    void if the queue's settings were successfully updated.

  Raises:
    DatabaseException:
      (1) The queue doesn't exist.
      (2) The q_settings are invalid.
    PermissionException: the current session user does not have permission to modify this queue's settings.
  """
  db = get_db()
  db.execute(UPDATE_QUEUE_SETTINGS, qsettings_dict_to_db_tuple_modify(q_settings))
  db.commit()

def delete_queue(qid):
  """Deletes the queue with the given qid.

  Args:
    qid: the id of the queue to be deleted.

  Returns:
    void if the queue was successfully deleted.

  Raises:
    DatabaseException: the queue doesn't exist.
    PermissionException: the current session user does not have permission to delete this queue.
  """
  raise NotImplementedError()

def get_queue_settings(qid):
  """Retrieves the queue_settings associated with qid.

  Returns:
    The QSettings associated with the qid.

  Raises:
    DatabaseException: the queue doesn't exist.
    PermissionException: the current session user does not have permission to view this queue.
  """
  db = get_db()
  rows = query_db(GET_QUEUE_SETTINGS_BY_ID, (qid,))
  if (not rows) or (len(rows) == 0):
    raise sqlite3.Error('The queue does not exist.')
  return rows[0]

def get_all_queues():
  db = get_db()
  settings_rows = query_db(GET_ALL_QUEUE_SETTINGS)
  queue_rows = query_db(GET_ALL_QUEUES)
  return (settings_rows, queue_rows)

def get_permissioned_qids(uid, permission_level):
  rows = query_db(GET_PERMISSIONED_QIDS_BY_UID, (uid, permission_level))
  return rows

def add_to_queue(uid, qid, optional_data):
  db = get_db()
  db.execute(INSERT_MEMBER_INTO_QUEUE, (uid, qid, qid, optional_data))
  db.execute(UPDATE_QUEUE_FOR_ADD, (qid,))
  db.execute(INSERT_INTO_QUEUE_HISTORY, (uid, qid, int(time.time()), None))
  db.commit()

def swap(uid1, uid2, qid):
  rows1 = query_db(GET_POSITION, (uid1, qid))
  relative_position1 = rows1[0]['relative_position']
  rows2 = query_db(GET_POSITION, (uid2, qid))
  relative_position2 = rows2[0]['relative_position']
  db = get_db()
  db.execute(UPDATE_POSITION, (relative_position2, uid1, qid))
  db.execute(UPDATE_POSITION, (relative_position1, uid2, qid))
  db.commit()
  

def remove_by_uid_qid(uid, qid):
  """

  Returns:
    nothing is returned. The q_member data should have been obtained from the software model.
  """
  db = get_db()
  db.execute(REMOVE_MEMBER_FROM_QUEUE, (uid, qid))
  db.execute(UPDATE_QUEUE_FOR_REMOVE, (qid,))
  db.execute(UPDATE_QUEUE_HISTORY, (int(time.time()), uid, qid))
  db.commit()

def get_queue_members(qid):
  rows = query_db(GET_MEMBER_DATA_BY_QID, (qid,))
  return rows

"""Database Utilities to be used by higher application layers.

All methods throw a DatabaseException if the database operation failed.
No classes have to be instantiated except the initial database declared in
__init__.py in app. All methods are static.
"""

# Query constants
GET_PROFILED_USER_BY_USERNAME = 'select * from users where temp=0 and uname=?'
GET_TEMP_USER_BY_ID = 'select * from users where temp=1 and id=?'
INSERT_PROFILED_USER = 'insert into users values(?, ?, ?, ?, ?, ?, ?)'
INSERT_TEMP_USER = 'insert into users values(?, 1, ?, NULL, NULL, NULL, NULL)'
GET_QUEUE_BY_ID = 'select * from qsettings where id=?'
INSERT_QUEUE = 'insert into qsettings values(?, ?, ?, ?, ?, ?)'

def query_db(query, args=()):
  db = get_db()
  cursor = db.execute(query, args)
  rows = cursor.fetchall()
  cursor.close()
  return rows
  
def user_dict_to_db_tuple(user_dict):
  return (user_dict['id'], user_dict['temp'], user_dict['uname'], user_dict['fname'], user_dict['lname'], user_dict['email'], user_dict['pw'])

def qsettings_dict_to_db_tuple(qsettings):
  return (qsettings['id'], qsettings['qname'], qsettings['max_size'], qsettings['keywords'], qsettings['location'], qsettings['active'])

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
  db = get_db()
  rows = query_db(GET_PROFILED_USER_BY_USERNAME, (user_dict['uname'],))
  if (rows and (len(rows) > 0)):
    raise ValidationException('The given username is already in use.')
  user_dict['pw'] = validators.encrypt_password(user_dict['pw'])
  user_dict['id'] = validators.get_unique_user_id()
  db.execute(INSERT_PROFILED_USER, user_dict_to_db_tuple(user_dict))
  db.commit()
  return user_dict['id']

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
  if not user_dict['temp']:
    user_dict['id'] = create_temp_user(user_dict)
  else:
    user_dict['id'] = create_user_profile(user_dict)
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

def get_user(username, given_password):
  """Retrieves the User associated with this user.

  Returns:
    A User object if the user was found. No temporary users are considered.

  Raises:
    sqlite3.Error: database operation failed.
    ValidationException: the username password combination is invalid.
  """
  rows = query_db(GET_PROFILED_USER_BY_USERNAME, (username,))
  if (not rows) or (len(rows) == 0):
    raise ValidationException('The username password combination is invalid.')
  else:
    encrypted_password = rows[0]['pw']
    if validators.are_matching(encrypted_password, given_password):
      return rows[0]
    else:
      raise ValidationException('the username password combination is invalid.')

def get_temp_user(temp_uid):
  """Retrieves the user data associated with the given user id, only if the uid matches a temporary user.

  Returns:
    A User object if the user was found. Only temporary users are examined.

  Raises:
    DatabaseException: the temp_uid was not a temporary user.
  """
  rows = query_db(GET_TEMP_USER_BY_ID, (temp_uid,))
  if (not rows) or (len(rows) == 0):
    raise ValidationException('The user could not be found.')
  else:
    return rows[0]

#################################################
# Queue related utilities.
#################################################

def create_queue(q_settings):
  """Creates a new queue with the defined settings. All settings except qid must exist.

  Args:
    q_settings: the settings for the new queue. The qid will be ignored if included.

  Returns:
    The new qid if the queue was successfully created.

  Raises:
    DatabaseException: the q_settings are invalid.
  """
  db = get_db()
  q_settings['id'] = validators.get_unique_queue_id()
  db.execute(INSERT_QUEUE, qsettings_dict_to_db_tuple(q_settings))
  db.commit()
  return q_settings['id']

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
  raise NotImplementedError()

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
  raise NotImplementedError()

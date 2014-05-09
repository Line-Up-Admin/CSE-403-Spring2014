"""Database Utilities to be used by higher application layers.

All methods throw a DatabaseException if the database operation failed.
No classes have to be instantiated except the initial database declared in
__init__.py in app. All methods are static.
"""

# Query constants
GET_USER_BY_USERNAME = 'select * from users where temp=0 and uname=?'

# Database Utilities
import permissions
import validators
from user_module import User, user_from_db_row
from app import get_db()

class DatabaseException(Exception):
  pass

class PermissionException(Exception):
  pass

class ValidationException(Exception):
  pass

def query_db(query, args=())
  db = get_db()
  cursor = db.execute(query, args)
  rows = cursor.fetchall()
  cursor.close()
  return rows

#############################################
# User related utilities.
#############################################

def create_user(user_data):
  """Adds a user defined by user_data to the database.

  Args:
    user_data: the data about the user to be added to the database. The uid will be ignored if included.

  Returns:
    The new uid if the user was successfully added to the database.

  Raises:
    DatabaseException: the database operation failed.
    ValueError: the given user_data is invalid.
  """
  raise NotImplementedError()

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
    DatabaseException: the uid does not exist in the database.
    ValidationException: the current session user is not logged in.
    PermissionException: the current session does not have the required permissions.
  """
  raise NotImplementedError()

def get_user(username, given_password):
  """Retrieves the User associated with this user.

  Returns:
    A User object if the user was found. No temporary users are considered.

  Raises:
    DatabaseException: the username password combination is invalid.
    ValidationException: the username password combination is invalid.
  """
  rows = query_db(GET_USER_BY_USERNAME, username)
  if (not rows) or (len(rows) == 0):
    raise DatabaseException('The username password combination is invalid.')
  else:
    encrypted_password = rows[0]['pw']
    if validators.are_matching(encrypted_password, given_password):
      return user_from_db_row(rows[0])
    else:
      raise ValidationException('the username password combination is invalid.')

def get_temp_user(temp_uid):
  """Retrieves the user data associated with the given user id, only if the uid matches a temporary user.

  Returns:
    A User object if the user was found. Only temporary users are examined.

  Raises:
    DatabaseException: the temp_uid was not a temporary user.
  """
  raise NotImplementedError()

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
  raise NotImplementedError()

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

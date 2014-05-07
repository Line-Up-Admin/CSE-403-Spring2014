"""Database Utilities to be used by higher application layers.

All methods throw a DatabaseException if the database operation failed.
No classes have to be instantiated except the initial database declared in
__init__.py in app. All methods are static.
"""

# Query constants


# Database Utilities
class DatabaseException(Exception):
  pass

def create_user(user_data):
  """Adds a user defined by user_data to the database.

  Args:
    user_data: the data about the user to be added to the database. The uid will be ignored if included.

  Returns:
    The new uid if the user was successfully added to the database.

  Raises:
    DatabaseException: the database operation failed.
  """
  raise NotImplementedError()

def modify_user(user_data):
  """Modfiy the user defined by the id in user_data to match the user_data.

  Args:
    user_data: the data about the user to be modified in the database. The id will be used to find the user in the database.

  Returns:
    void if the user's data was successfully updated.

  Raises:
    DatabaseException: the database operation failed.
  """
  raise NotImplementedError()

def delete_user(user_data):
  """Deletes a user from the database.

  Args:
    user_data: the user to be deleted. The username and password must match.

  Returns:
    void if the deletion was a success.

  Raises:
    DatabaseException: the database operation failed.
  """
  raise NotImplementedError()

def create_queue(q_settings):
  """Creates a new queue with the defined settings. All settings that are left blank will be left as Null.

  Args:
    q_settings: the settings for the new queue. The qid will be ignored if included.

  Returns:
    The new qid if the queue was successfully created.

  Raises:
    DatabaseException: the database operation failed.
  """
  raise NotImplementedError()

def modify_queue(q_settings):
  """Modifies the queue with the qid defined in q_settings to match the q_settings given.

  Args:
    q_settings: the settings for the queue to be modified. The qid will be used to find the queue in the database.

  Returns:
    void if the queue's settings were successfully updated.

  Raises:
    DatabaseException: the database operation failed.
  """
  raise NotImplementedError()

def delete_queue(qid):
  """Deletes the queue with the given qid.

  Args:
    qid: the id of the queue to be deleted.

  Returns:
    void if the queue was successfully deleted.

  Raises:
    DatabaseException: the database operation failed.
  """
  raise NotImplementedError()

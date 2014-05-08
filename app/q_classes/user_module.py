
""" This file contains the UserModule class and a mock Database class"""


class UserModule(object):
   """ A user module object is used to keep track of whether
      the user is logged in. """
   def login(self, uname, password):
      pass
   def get_user_data(self, user_ID):
      pass
   def logout(self, user_ID):
      pass
   def update_user(self, user_ID):
      pass
   def create_user(self, user_ID):
      pass
   def remove_user(self, user_ID):
      pass



class MockDatabase(object):
   """ The database is a store of all the information about user accounts. 
      (And other things?) """
   def __init__(self):
      pass
   add_to_q(self, user_ID, q_ID):
      pass
   create_q(self, q_settings):
      pass
   get_permissions(self, user_ID, q_ID):
      pass
   create_user(self, user):
      pass


class User(object):
   """ This class stores information about a user """
   def __init__(self, username, email, firstname, lastname, 
         ID, password, temporary):
      self.username = username
      self.email = email
      self.firstname = firstname
      self.lastname = lastname
      self.ID = ID
      self.password = password
      self.temporary = temporary






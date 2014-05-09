
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
   def add_to_q(self, user_ID, q_ID):
      pass
   def create_q(self, q_settings):
      pass
   def get_permissions(self, user_ID, q_ID):
      pass
   def create_user(self, user):
      pass


class User(object):
   """ This class stores information about a user """
   def __init__(self, id, temp, uname, fname, lname, email, pw):
      self.id = id
      self.temp = temp
      self.uname = uname
      self.fname = fname
      self.lname = lname
      self.email = email
      self.pw = pw

def user_from_dict(user_dict):
   return User(user_dict['id'], user_dict['temp'], user_dict['uname'], user_dict['fname'], user_dict['lname'], user_dict['email'], user_dict['pw'])
   
def dict_from_user(user):
   user_dict = dict()
   user_dict['id'] = user.id
   user_dict['temp'] = user.temp
   user_dict['uname'] = user.uname
   user_dict['fname'] = user.fname
   user_dict['lname'] = user.lname
   user_dict['email'] = user.email
   user_dict['pw'] = user.pw
   return user_dict
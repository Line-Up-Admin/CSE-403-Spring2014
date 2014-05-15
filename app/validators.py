from os import urandom
from struct import unpack

def are_matching(encrypted_password, given_password):
  return encrypted_password == given_password

def encrypt_password(password):
  return password

def get_unique_user_id():
  return unpack("<L", urandom(4))[0]
  
def get_unique_queue_id():
   return unpack("<L", urandom(4))[0]

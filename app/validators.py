from os import urandom
from struct import unpack
from flask import session
import re
import hashlib

Q_MAX_STR_LEN = {
   'qname': 32,
   'keywords': 256,
   'location': 64,
   'website': 128,
   'organization': 128,
   'disclaimer': 512,
   'prompt': 512
}

USER_MAX_STR_LEN = {
   'uname': 32,
   'fname': 20,
   'lname': 20,
   'email': 32,
   'pw': 32
}

def check_max_str_len(key, dictionary, max_dict, fail):
   if dictionary.has_key(key):
      if len(dictionary[key]) > max_dict[key]:
         fail[key] = str(key) + ' text is too long. Max length is ' + str(max_dict[key])
         dictionary['SUCCESS'] = False
   
def are_matching(encrypted_password, salt, given_password):
   given_password = given_password + unicode(salt)
   given_password_encrypted = hashlib.sha224(given_password).hexdigest()
   print 'salt is ', salt, 'given password is', given_password
   return encrypted_password == given_password_encrypted

def encrypt_password(password):
   print 'given password = ', password
   salt = unpack('I', urandom(4))[0]
   print 'salt created', salt
   password = password + unicode(salt)
   encrypted_pw = hashlib.sha224(password).hexdigest()
   return (encrypted_pw, salt)

def get_unique_user_id():
   return unpack("<L", urandom(4))[0]
  
def get_unique_queue_id():
   return unpack("<L", urandom(4))[0]

def validate_q_settings(q_settings):
   q_settings['SUCCESS'] = True
   fail = dict()
   fail['SUCCESS'] = False
   if not q_settings.has_key('qname') or q_settings['qname'] is None or len(q_settings['qname']) == 0:
      fail['qname'] = 'Required'
      q_settings['SUCCESS'] = False
   else:
      check_max_str_len('qname', q_settings, Q_MAX_STR_LEN, fail)
   check_max_str_len('keywords', q_settings, Q_MAX_STR_LEN, fail)
   check_max_str_len('location', q_settings, Q_MAX_STR_LEN, fail)  
   check_max_str_len('website', q_settings, Q_MAX_STR_LEN, fail)
   check_max_str_len('organization', q_settings, Q_MAX_STR_LEN, fail)
   check_max_str_len('disclaimer', q_settings, Q_MAX_STR_LEN, fail)
   check_max_str_len('prompt', q_settings, Q_MAX_STR_LEN, fail)
   if q_settings.has_key('max_size'):
      try:
         max_size = int(q_settings['max_size'])
      except ValueError:
         fail['max_size'] = 'Maximum size must be an int.'
         q_settings['SUCCESS'] = False
      if max_size < 1:
         fail['max_size'] = 'Maximum size must be greater than zero.'
         q_settings['SUCCESS'] = False
   if q_settings.has_key('min_wait_rejoin'):
      try:
         mwr = int(q_settings['min_wait_rejoin'])
      except ValueError:
         fail['min_wait_rejoin'] = 'Minimum wait to rejoin queue must be an int.'
         q_settings['SUCCESS'] = False
      if mwr < 0:
         fail['min_wait_rejoin'] = 'Minimum wait to rejoin queue must be non-negative.'
         q_settings['SUCCESS'] = False
   if not q_settings.has_key('admins'):
      q_settings['admins']= list()
   else:
      q_settings['admins'] = list(set(admin.strip() for admin in q_settings['admins'].split(',')))
   if not session['uname'] in q_settings['admins']:
      q_settings['admins'].append(session['uname'])
   if q_settings.has_key('managers'):
      q_settings['managers'] = list(set(e.strip() for e in q_settings['managers'].split(',')))
   if q_settings.has_key('blocked_users'):
      q_settings['blocked_users'] = list(set(b.strip() for b in q_settings['blocked_users'].split(',')))
   if not q_settings['SUCCESS']:
      return fail
   return q_settings

def validate_user(user):
   """
	id INTEGER PRIMARY KEY,
	temp int,
	uname varchar(32),
	fname varchar(20),
	lname varchar(20),
	email varchar(32),
	pw varchar(32),
   """
   user['SUCCESS'] = True
   fail = dict()
   fail['SUCCESS'] = False
   if not user.has_key('uname') or user['uname'] is None or len(user['uname']) == 0:
      fail['uname'] = 'Required'
      user['SUCCESS'] = False
   elif ',' in user['uname']:
      fail['uname'] = 'commas are not allowed in the User Name.'
      user['SUCCESS'] = False
   else:
      check_max_str_len('uname', user, USER_MAX_STR_LEN, fail)
   check_max_str_len('fname', user, USER_MAX_STR_LEN, fail)
   check_max_str_len('lname', user, USER_MAX_STR_LEN, fail)
   if not user.has_key('email') or user['email'] is None or len(user['email']) == 0:
      fail['email'] = 'Required'
      user['SUCCESS'] = False
   else:
      if not re.match('.+\@.+\..+', user['email']):
         fail['email'] = 'Invalid Email'
         user['SUCCESS'] = False
      else:
         check_max_str_len('email', user, USER_MAX_STR_LEN, fail)
   """The next line should be removed once the proper regex is found."""
   check_max_str_len('pw', user, USER_MAX_STR_LEN, fail)
   """
   if user.has_key('pw'):
      if not re.match('NEED REGEX HERE', user['pw']):
         fail['pw'] = 'password does not meet complexity requirements.'
         user['SUCCESS'] = False
      else:
         check_max_str_len('pw', user, USER_MAX_STR_LEN, fail)
   else:
      fail['pw'] = 'Required.'
      user['SUCCESS'] = False
   """
   if not user['SUCCESS']:
      return fail
   return user

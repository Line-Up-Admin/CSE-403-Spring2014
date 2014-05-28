from os import urandom
from struct import unpack
from flask import session

MAX_STR_LEN = {
   'qname': 32,
   'keywords': 256,
   'location': 64,
   'website': 128,
   'organization': 128,
   'disclaimer': 512,
   'prompt': 512
}

def check_max_str_len(key, dictionary):
   if dictionary.has_key(key):
      if len(dictionary[key]) > MAX_STR_LEN[key]:
         dictionary[key] = key + ' text is too long. Max length is ' + MAX_STR_LEN[key]
         dictionary['SUCCESS'] = False
   
def are_matching(encrypted_password, given_password):
   return encrypted_password == given_password

def encrypt_password(password):
   return password

def get_unique_user_id():
   return unpack("<L", urandom(4))[0]
  
def get_unique_queue_id():
   return unpack("<L", urandom(4))[0]

def validate_q_settings(q_settings):
   """
   Args:
   the jsonified dictionary
   """
   q_settings['SUCCESS'] = True
   if not q_settings.has_key('qname') or q_settings['qname'] is None or len(q_settings['qname']) == 0:
      q_settings['qname'] = 'Required'
      q_settings['SUCCESS'] = False
   else:
      check_max_str_len('qname', q_settings)
   check_max_str_len('keywords', q_settings)
   check_max_str_len('location', q_settings)  
   check_max_str_len('website', q_settings)
   check_max_str_len('organization', q_settings)
   check_max_str_len('disclaimer', q_settings)
   check_max_str_len('prompt', q_settings)
   if q_settings.has_key('max_size'):
      try:
         max_size = int(q_settings['max_size'])
      except ValueError:
         q_settings['max_size'] = 'Invalid maximum size.'
         q_settings['SUCCESS'] = False
      if max_size < 1:
         q_settings['max_size'] = 'Max size must be greater than zero.'
         q_settings['SUCCESS'] = False
   if q_settings.has_key('min_wait_rejoin'):
      try:
         mwr = int(q_settings['min_wait_rejoin'])
      except ValueError:
         q_settings['min_wait_rejoin'] = 'Invalid minimum wait to rejoin queue.'
         failure = True
      if mwr < 0:
         q_settings['min_wait_rejoin'] = 'Minimum wait to rejoin queue must be non-negative.'
         failure = True
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
   return q_settings

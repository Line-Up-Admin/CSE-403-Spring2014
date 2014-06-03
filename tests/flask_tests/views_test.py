import os
import sys
sys.path.insert(0, '.') # CSE-403-Spring2014 level
sys.path.insert(0, '../app')
sys.path.insert(0, '../..')
sys.path.insert(0, '..')
from app import app, database_utilities
import unittest
from flask import json
from app import get_db
from app import init_db
import sqlite3
import pdb

test_db_file = os.path.join(app.root_path, 'apptest.db')

class ViewsTestCase(unittest.TestCase):

   def setUp(self):
      app.config['DB_FILE'] = test_db_file
      try:
         init_db()
      except sqlite3.Error as e:
         os.remove(test_db_file)
         init_db()
      self.appTest = app.test_client()

   def tearDown(self):
      os.remove(test_db_file)

   def test_create_user(self):
      # attempt to create user 'testUser'
      assert self.createUser('testUser', 'somePassword')['result'] == 0

   def test_login_correct(self):
      # create user 'testUser'
      self.createUser('testUser', 'testPassword')
      # attempt to log in as 'testUser'
      assert self.login('testUser', 'testPassword')['result'] == 0

   def test_create_duplicate_user(self):
      # create user 'testUser'
      print 'in test_create_duplicate_user'
      self.createUser('testUser', 'somePassword')
      # attempt to create another user called 'testUser'
      assert self.createUser('testUser', 'otherPassword')['result'] == 1

   def test_login_incorrect(self):
      # create user 'userTest'
      self.createUser('userTest', 'userPass')
      # attempt to log in as 'userTest'
      assert self.login('userTest', 'wrongPassword')['result'] == 1
   
   def test_logout_correct(self):
      # create account 'testUser'
      self.createUser('testUser', 'testPassword')
      # login as 'testUser'
      self.login('testUser', 'testPassword')
      # logout
      assert self.logout()['result'] == 0

   def test_logout_incorrect(self):
      # attempt to log out when not logged in
      assert self.logout()['result'] == 1

   def test_create_queue_correct(self):
      # create 'userQ'
      self.createUser('userQ', 'passwordQ')
      # log in as 'userQ'
      self.login('userQ', 'passwordQ')
      # attempt to create queue 'CSE 403 wait list'
      assert self.createQueue('CSE 403 wait list')['result'] == 0

   def test_create_queue_empty_name(self):
      # create 'userQ'
      self.createUser('userQ', 'passwordQ')
      # log in as 'userQ'
      self.login('userQ', 'passwordQ')
      # attempt to create queue with empty name
      assert self.createQueue('')['result'] == 1
   
   def test_create_queue_not_logged_in(self):
      # attempt to create queue 'bad queue'
      assert self.createQueue('CSE 403')['result'] == 1

   def test_multiple_users_login_logout(self):
      # create two users, 'userA' and 'userB'
      self.createUser('userA', 'passwordA')
      self.createUser('userB', 'passwordB')
      # log in as 'userA'
      self.login('userA', 'passwordA')
      # log out as 'userA' and log in as 'userB'
      assert (self.logout()['result'] == 0 and
              self.login('userB', 'passwordB')['result'] == 0)
      
   def test_join_queue_correct(self):
      # create two users, 'userX' and 'userY'
      self.createUser('userX', 'passwordX')
      self.createUser('userY', 'passwordY')
      # log in as 'userX'
      self.login('userX', 'passwordX')
      # create queue 'userX's queue' as 'userX'
      q_settings = self.createQueue('userX\'s queue')
      # logout as 'userX'
      self.logout()
      # log in as 'userY'
      self.login('userY', 'passwordY')
      # attempt to join queue 'userX's queue'
      assert self.joinQueue(q_settings['qid'])['result'] == 0
      
   def test_join_nonexistent_queue(self):
      # create user 'Shakira'
      self.createUser('Shakira', 'hipsdontlie')
      # log in as 'Shakira'
      self.login('Shakira', 'hipsdontlie')
      # attempt to join queue that does not exist
      assert self.joinQueue(12345)['result'] == 1
      
   def test_leave_queue(self):
      # create two users, 'userX' and 'userY'
      self.createUser('userX', 'passwordX')
      self.createUser('userY', 'passwordY')
      # log in as 'userX'
      self.login('userX', 'passwordX')
      # create queue 'userX's queue' as 'userX'
      q_settings = self.createQueue('userX\'s queue')
      # logout as 'userX'
      self.logout()
      # log in as 'userY'
      self.login('userY', 'passwordY')
      # join queue 'userAs queue' as 'userB'
      self.joinQueue(q_settings['qid'])['result'] == 0
      # attempt to leave queue 'userA's queue' as 'userB'
      assert self.leaveQueue(q_settings['qid'])['result'] == 0
      
   def test_remove_user_correct(self):
      # create two users, 'BuffyTheVampireSlayer' and 'Vampire'
      self.createUser('BuffyTheVampireSlayer', 'sarahmichellegellar')
      self.createUser('Vampire', 'blood')
      # log in as 'BuffyTheVampireSlayer' and create queue 'No Vampires Allowed'
      self.login('BuffyTheVampireSlayer', 'sarahmichellegellar')
      q_settings = self.createQueue('No Vampires Allowed')
      # log out as 'BuffyTheVampireSlayer' and log in as 'Vampire'
      self.logout()
      self.login('Vampire', 'blood')
      # join queue 'No Vampires Allowed' as user 'Vampire'
      self.joinQueue(q_settings['qid'])
      # log out as 'Vampire' and log back in as 'BuffyTheVampireSlayer'
      self.logout()
      self.login('BuffyTheVampireSlayer', 'sarahmichellegellar')
      # attempt to remove user 'Vampire' from queue 'No Vampires Allowed'
      assert self.removeFromQueue(q_settings['qid'],
                                  'Vampire')['result'] == 0

   def test_remove_user_bad_permissions(self):
      # create three users, 'Leonardo,' 'Michelangelo', and 'Donatello'
      self.createUser('Michelangelo', 'sistine')
      self.createUser('Donatello', 'david')
      self.createUser('Leonardo', 'monalisa')
      # log in as 'Michelangelo,' create queue 'TMNT!' and log out
      self.login('Michelangelo', 'sistine')
      q_settings = self.createQueue('TMNT!')
      self.logout()
      # log in as 'Leonardo' and join queue 'TMNT!'
      self.login('Leonardo', 'monalisa')
      self.joinQueue(q_settings['qid'])
      # log out as 'Leonardo' and log in as 'Donatello'
      self.logout()
      self.login('Donatello', 'david')
      # as user 'Donatello, attempt to remove user 'Leonardo' from queue 'TMNT!'
      assert self.removeFromQueue(q_settings['qid'],
                                  'Leonardo')['result'] == 1
   
   def test_postpone(self):
      # create three users, 'RKelly,' 'RobHalford,' and 'CaptainAmerica'
      self.createUser('RKelly', 'trappedinthecloset')
      self.createUser('RobHalford', 'painkiller')
      self.createUser('CaptainAmerica', 'spandex')
      # log in as 'RKelly' and create queue 'Poppin Bottles'
      self.login('RKelly', 'trappedinthecloset')
      q_settings = self.createQueue('Poppin Bottles')
      # log out as 'RKelly' and log in as 'RobHalford'
      self.logout()
      self.login('RobHalford', 'painkiller')
      # join queue 'Poppin Bottles' as user 'RobHalford' and then log out
      self.joinQueue(q_settings['qid'])
      self.logout()
      # log in as user 'CaptainAmerica' and join queue 'Poppin Bottles'
      self.login('CaptainAmerica', 'spandex')
      self.joinQueue(q_settings['qid'])
      # log out as 'CaptainAmerica' and log back in as 'RobHalford'
      self.logout()
      self.login('RobHalford', 'painkiller')
      # attempt to postpone place in queue 'Poppin Bottles' as user 'RobHalford'
      assert self.postpone(q_settings['qid'])['result'] == 0
   
   def createQueue(self, qname):
      #pdb.set_trace()
      """Helper method for creating a queue in the database.
         Returns:
            0    ->    if queue was successfully created
            1    ->    if server reply was SUCCESS:False
            2    ->    if there was an error communicating
                         with the server (i.e. unparsable JSON
                         or otherwise invalid response)
      """
      dataTest = dict()
      dataTest['qname'] = qname
      dataString = json.dumps(dataTest)
      with app.test_request_context('/createQueue', method='POST'):
         r = self.appTest.post('/createQueue', headers={'content-type':'application/json'}, data=dataString)
      try:
         j = json.loads(r.data)
         if j['SUCCESS'] == True:
            j['result'] = 0
            return j
         j['result'] = 1
         return j
      except ValueError as e:
         print 'Returned value could not be parsed as a JSON object'
         return {'result':2}
 
   def logout(self):
      """Helper method for creating a user in the database.
         Returns:
            0    ->    if user was successfully logged out
            1    ->    if logout failed (user not logged in)
      """
      with app.test_request_context('/logout', method='GET'):
         r = self.appTest.get('/logout', headers={'content-type':'application/json'})
      if 'You are not logged in!' in r.data:
         return {'result':1}
      return {'result':0}
   
   def createUser(self, username, password):
      """Helper method for creating a user in the database.
         Returns:
            0    ->    if user was successfully created
            1    ->    if server reply was SUCCESS:False
            2    ->    if there was an error communicating
                         with the server (i.e. unparsable JSON
                         or otherwise invalid response)
      """
      dataTest = dict()
      dataTest['uname'] = username
      dataTest['pw'] = password
      dataTest['email'] = 'something@something.com' # to satisfy required field
      dataString = json.dumps(dataTest)
      with app.test_request_context('/createUser', method='POST'):
         r = self.appTest.post('/createUser', headers={'content-type':'application/json'}, data=dataString)
      try:
         j = json.loads(r.data)
         if j['SUCCESS'] == True:
            j['result'] = 0
            return j
         j['result'] = 1
         return j
      except ValueError as e:
         print 'Returned value could not be parsed as a JSON object'
         return {'result':2}
 
      
   def login(self, username, password):
      """Helper method for logging in a user.
         Returns:
            0    ->    if user was successfully logged in
            1    ->    if username/password combination was
                        incorrect
            2    ->    if there was an error communicating
                         with the server (i.e. unparsable JSON
                         or otherwise invalid response)
      """
      dataTest = dict()
      dataTest['uname'] = username
      dataTest['pw'] = password
      dataString = json.dumps(dataTest)
      with app.test_request_context('/login', method='POST'):
         r = self.appTest.post('/login', headers={'content-type':'application/json'}, data=dataString)
      try:
         j = json.loads(r.data)
         if j['SUCCESS'] == True:
            j['result'] = 0
            return j
         j['result'] = 1
         return j
      except ValueError as e:
         print 'Returned value could not be parsed as a JSON object'
         return {'result':2}

   def joinQueue(self, qid):
      """Helper method for joining a queue as the currently logged-in user
         Returns:
            0    ->    if user successfully joined queue
            1    ->    if server reply was SUCCESS:False
            2    ->    if there was an error communicating
                         with the server (i.e. unparsable JSON
                         or otherwise invalid response)
      """
      dataTest = dict()
      dataTest['qid'] = qid
      dataString = json.dumps(dataTest)
      with app.test_request_context('/join', method='POST'):
         r = self.appTest.post('/join', headers={'content-type':'application/json'}, data=dataString)
      try:
         j = json.loads(r.data)
         if j['SUCCESS'] == True:
            j['result'] = 0
            return j
         j['result'] = 1
         return j
      except ValueError as e:
         print 'Returned value could not be parsed as a JSON object'
         return {'result':2}

   def leaveQueue(self, qid):
      """Helper method for leaving a queue as the currently logged-in user
         Returns:
            0    ->    if user successfully left queue
            1    ->    if server reply was SUCCESS:False
            2    ->    if there was an error communicating
                         with the server (i.e. unparsable JSON
                         or otherwise invalid response)
      """
      dataTest = qid
      dataString = json.dumps(dataTest)
      with app.test_request_context('/leaveQueue', method='POST'):
         r = self.appTest.post('/leaveQueue', headers={'content-type':'application/json'}, data=dataString)
      try:
         j = json.loads(r.data)
         if j['SUCCESS'] == True:
            j['result'] = 0
            return j
         j['result'] = 1
         return j
      except ValueError as e:
         print 'Returned value could not be parsed as a JSON object'
         return {'result':2}

   def removeFromQueue(self, qid, uname):
      """Helper method for removing someone from a queue as the currently logged-in user (must be an admin or manager of queue)
         Returns:
            0    ->    if user successfully was removed from queue
            1    ->    if server reply was SUCCESS:False
            2    ->    if there was an error communicating
                         with the server (i.e. unparsable JSON
                         or otherwise invalid response)
      """
      dataTest = dict()
      dataTest['qid'] = qid
      with app.test_request_context('/remove', method='POST'):
         dataTest['uid'] = database_utilities.get_user_by_uname(uname)['id']
         dataString = json.dumps(dataTest)
         r = self.appTest.post('/remove', headers={'content-type':'application/json'}, data=dataString)
      try:
         j = json.loads(r.data)
         if j['SUCCESS'] == True:
            j['result'] = 0
            return j
         j['result'] = 1
         return j
      except ValueError as e:
         print 'Returned value could not be parsed as a JSON object'
         return {'result':2}

   def postpone(self, qid):
      """Helper method for postponing oneself in a queue
         Returns:
            0    ->    if user successfully was postponed in queue
            1    ->    if server reply was SUCCESS:False
            2    ->    if there was an error communicating
                         with the server (i.e. unparsable JSON
                         or otherwise invalid response)
      """
      dataString = json.dumps(qid)
      with app.test_request_context('/postpone', method='POST'):
         r = self.appTest.post('/postpone', headers={'content-type':'application/json'}, data=dataString)
      try:
         j = json.loads(r.data)
         if j['SUCCESS'] == True:
            j['result'] = 0
            return j
         j['result'] = 1
         return j
      except ValueError as e:
         print 'Returned value could not be parsed as a JSON object'
         return {'result':2}

if __name__ == '__main__':
    unittest.main()

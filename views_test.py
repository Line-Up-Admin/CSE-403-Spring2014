import os
from app import app
import unittest
from flask import json
from app import get_db
from app import init_db
import sqlite3

class ViewsTestCase(unittest.TestCase):

   def setUp(self):
      try:
         init_db()
      except sqlite3.Error as e:
         pass
      self.appTest = app.test_client()
      #app.init_db()

   def tearDown(self):
      os.remove('app/app.db')
#      os.close(self.db_fd)
#      os.unlink(app.config['DATABASE'])
#      os.remove(self.db_fd)

   def test_create_user(self):
      with app.test_request_context('/createUser', method='POST'):
         dataTest = dict()
         dataTest['uname'] = 'testUser'
         dataTest['pw'] = 'testPassword'
         dataTest['email'] = 'test@test.com'
         dataString = json.dumps(dataTest)
         result = self.appTest.post('/createUser', headers={'content-type':'application/json'}, data=dataString)
         try:
            j = json.loads(result.data)
            assert j['SUCCESS'] == True
         except ValueError as e:
            print 'Returned value could not be parsed as a JSON object'
            assert False

   def test_create_duplicate_user(self):
      with app.test_request_context('/createUser', method='POST'):
         dataTest = dict()
         dataTest['uname'] = 'testUser'
         dataTest['pw'] = 'testPassword'
         dataString = json.dumps(dataTest)
         self.appTest.post('/createUser', headers={'content-type':'application/json'}, data=dataString)
         r = self.appTest.post('/createUser', headers={'content-type':'application/json'}, data=dataString)
         try:
            j = json.loads(r.data)
            assert j['SUCCESS'] == False
         except ValueError as e:
            print 'Returned value could not be parsed as a JSON object'
            assert False
         
   #def test_login_correct
   
   #def test_login_incorrect
   #def test_logout
   #def test_create_queue
   #def test_join_queue
   #def test_leave_queue
   #def test_postpone
   #def test

if __name__ == '__main__':
    unittest.main()

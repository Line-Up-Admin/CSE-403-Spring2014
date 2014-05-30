import os
import sys
sys.path.insert(0, '../..')
sys.path.insert(0, '..')
from app import app
import unittest
from flask import json
from app import get_db
from app import init_db
import sqlite3


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

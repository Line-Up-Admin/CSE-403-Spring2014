import os
from app import app
import unittest
import tempfile
from flask import request, jsonify
import json

class ViewsTestCase(unittest.TestCase):

   def setUp(self):
      #self.db_fd, app.config['DATABASE'] = app.get_db()
      #app.app.config['TESTING'] = True
      self.appTest = app.test_client()
      #app.init_db()

   def tearDown(self):
      pass
      #os.close(self.db_fd)
      #os.unlink(app.config['DATABASE'])

   def test_create_user(self):
      with app.test_request_context('/createUser', method='POST'):
         dataTest = dict()
         dataTest['uname'] = 'testUser'
         dataTest['pw'] = 'testPassword'
         result = self.appTest.post('/createUser', data=dataTest)
         try:
            json.loads(result.data)
            assert True
         except ValueError as e:
            print 'Returned value could not be parsed as a JSON object'
            assert False

   #def test_create_duplicate_user
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

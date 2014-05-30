import os
from app import app
import unittest
import tempfile
from flask import request, jsonify

class ViewsTestCase(unittest.TestCase):

   def setUp(self):
      self.db_fd, app.config['DATABASE'] = app.get_db()
      app.config['TESTING'] = True
      self.appTest = app.test_client()
      #app.init_db()

   def tearDown(self):
      os.close(self.db_fd)
      os.unlink(app.config['DATABASE'])

   def test_create_user(self):
      with app.test_request_context('/createUser', method='POST'):
         dataTest = dict()
         dataTest['uname'] = 'testUser'
         dataTest['pw'] = 'testPassword'
         result = self.appTest.post('/createUser', data=dataTest)
         assert result.data['SUCCESS'] == True

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

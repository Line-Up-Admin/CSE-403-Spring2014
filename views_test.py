import os
import app
import unittest
import tempfile
from flask import jsonify

class ViewsTestCase(unittest.TestCase):

   def setUp(self):
      self.db_fd, app.app.config['DATABASE'] = tempfile.mkstemp()
      app.app.config['TESTING'] = True
      self.app = app.app.test_client()
      #app.init_db()

   def tearDown(self):
      os.close(self.db_fd)
      os.unlink(app.app.config['DATABASE'])

   def test_create_user(self):
      result = self.app.post('/createUser', data=jsonify(dict(uname='testUser',pw='testPassword')))
      assert result['SUCCESS'] == True

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

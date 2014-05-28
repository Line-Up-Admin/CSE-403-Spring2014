import os
import app
import unittest
import tempfile

class ViewsTestCase(unittest.TestCase):

   def setUp(self):
      self.db_fd, views.app.config['DATABASE'] = tempfile.mkstemp()
      views.app.config['TESTING'] = True
      self.app = views.app.test_client()
      views.init_db()

   def tearDown(self):
      os.close(self.db_fd)
      os.unlink(views.app.config['DATABASE'])
  
   def test_login

if __name__ == '__main__':
    unittest.main()

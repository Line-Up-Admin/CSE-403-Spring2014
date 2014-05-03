import os
import unittest
import sys
sys.path.insert(0, '../..')
from app import app

class TestCase(unittest.TestCase):
  def setUp(self):
    app.config['TESTING'] = True
    self.application = app.test_client()

  def tearDown(self):
    pass

  def test_HelloWorld(self):
    rv = self.application.get('/helloworld')
    assert 'Hello, World!' in rv.data

  def test_Fail(self):
    rv = self.application.get('/helloworld')
    assert 'Goodbye, World!' in rv.data

if __name__ == '__main__':
  unittest.main()

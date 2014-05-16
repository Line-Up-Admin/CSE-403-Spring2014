"""
This file creates a Queue and a QueueMember and tests 
some basic functionality associated with the Queue and the
QueueMemeber.
"""

import os
import unittest
import sys
sys.path.insert(0, '../..')
sys.path.insert(0, '..')
from app import app
from app.q_classes import *

class SomeTest(unittest.TestCase):

   def setUp(self):
      pass

   def tearDown(self):
      pass

   def test_add_dequeue(self):
      """ Add 2 people to a queue, and dequeue them both. """
      qq = Queue(112)
      m1 = QueueMember("bob", 123)
      m2 = QueueMember("carol", 125)
      qq.add(m1)
      assert len(qq) == 1
      qq.add(m2)
      assert len(qq) == 2
      first_off = qq.dequeue()
      assert first_off != None
      assert first_off.uname == "bob"
      assert first_off.uid == 123
      second_off = qq.dequeue()
      assert second_off != None
      assert second_off.uname == "carol"
      assert second_off.uid == 125
 
   def test_max_size(self):
      """ Test that a queue has a maximum size """
      # Max size is 2, everything else empty
      q_set = QueueSettings()
      q_set.max_size = 2
      qq = Queue(100, q_set)
      m1 = QueueMember("alice", 44)
      m2 = QueueMember("bob", 123)
      m3 = QueueMember("carol", 125)
      qq.add(m1)
      qq.add(m2)
      print qq.q_settings
      print qq.q_settings
      self.assertRaises(QueueFullException, qq.add, m3)
   
   def test_postpone(self):
      """Test postponing in the queue """
      qq = Queue(112)
      m1 = QueueMember("bob", 122)
      m2 = QueueMember("carol", 123)
      m3 = QueueMember("dave", 124)
      m4 = QueueMember("evan", 125)

      qq.add(m1)
      qq.add(m2)
      qq.add(m3)
      qq.add(m4)
      assert len(qq) == 4
      # get_position is a zero based index from the front.
      assert qq.get_position(m2) == 1
      assert qq.get_position(m3) == 2
      assert qq.get_position(m4) == 3

      qq.postpone(m2)
      assert qq.get_position(m3) == 1
      assert qq.get_position(m2) == 2
      assert qq.get_position(m4) == 3
      qq.postpone(m2)
      assert qq.get_position(m3) == 1
      assert qq.get_position(m4) == 2
      assert qq.get_position(m2) == 3
      # tests that the queue ignores someone being postponed
      #    at the end of the line.
      qq.postpone(m2)
      qq.postpone(m2)
      qq.postpone(m2)
      assert qq.get_position(m3) == 1
      assert qq.get_position(m4) == 2
      assert qq.get_position(m2) == 3
      assert len(qq) == 4


if __name__ == '__main__':
   unittest.main()


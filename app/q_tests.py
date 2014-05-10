"""
This file creates a Queue and a QueueMember and tests 
some basic functionality associated with the Queue and the
QueueMemeber.
"""

import os
import unittest
import sys
from q_classes import *


class SomeTest(unittest.TestCase):

   def setUp(self):
      pass

   def tearDown(self):
      pass

   def test_add_remove(self):
      """ Add 2 people to a queue, and remove them both. """
      qq = Queue(112)
      m1 = QueueMember("bob", 123)
      m2 = QueueMember("carol", 125)
      qq.add(m1)
      assert len(qq) == 1
      qq.add(m2)
      assert len(qq) == 2
      first_off = qq.dequeue()
      assert first_off != None
      assert first_off.username == "bob"
      assert first_off.ID == 123
      second_off = qq.dequeue()
      assert second_off != None
      assert second_off.username == "carol"
      assert second_off.ID == 125
 
   def test_max_size(self):
      """ Test that a queue has a maximum size """
      # Max size is 2, everything else empty
      q_set = QueueSettings(2, None, None, None, None, None, None)
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
      pass


   def test_queue_info(self):
      """ Test making a queue and getting an info object about it. """
      pass


if __name__ == '__main__':
   unittest.main()




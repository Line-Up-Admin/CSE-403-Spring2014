"""
This file creates a Queue and a QueueMember and tests 
some basic functionality associated with the Queue and the
QueueMemeber.
"""

import os
import unittest
import sys
from q_classes import Queue
from q_classes import QueueMember


class SomeTest(unittest.TestCase):

   def setUp(self):
      self.q = Queue(114)
      self.mem1 = QueueMember("bob", 123)
      self.mem2 = QueueMember("carol", 125)

   def tearDown(self):
      pass

   def test_everything(self):
      qq = self.q
      m = self.mem1
      qq.add(m)
      assert len(qq) == 1
      qq.add(self.mem2)
      assert len(qq) == 2
      m2 = qq.deq()
      print m2 != None
      assert m2 != None
      assert m2.username == "bob"
      assert m2.ID == 123
 

if __name__ == '__main__':
   unittest.main()




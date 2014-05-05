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
      self.q = Queue(114)
      self.mem1 = QueueMember("bob", 123)
      self.mem2 = QueueMember("carol", 125)

   def tearDown(self):
      pass

   def test_everything(self):
      """ Add 2 people to a queue, and remove them both. """
      print "Helllo"
      qq = self.q
      m1 = self.mem1
      m2 = self.mem2
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
 

if __name__ == '__main__':
   unittest.main()




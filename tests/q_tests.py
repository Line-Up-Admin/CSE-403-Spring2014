"""
This file creates a Queue and a QueueMember and tests 
some basic functionality associated with the Queue and the
QueueMemeber.

These tests can be run at the command line by typing: 
      python q_tests.py
"""

import os
import unittest
import sys
import time
sys.path.insert(0, '../..') 
sys.path.insert(0, '..') # the tests folder 
sys.path.insert(0, '.') # CSE-403-Spring2014 level
sys.path.insert(0, '../app')

#sys.path.insert(0, )
#from app import app
from app.q_classes import *

class SomeTest(unittest.TestCase):

   def setUp(self):
      pass

   def tearDown(self):
      pass

   def test_add_dequeue(self):
      """ Add 2 people to a queue, and dequeue them both. 
      Methods tested:
         add
         dequeue
      """
      print "test_add_dequeue..."

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
      """ Test that a queue has a maximum size, and that an
         exception is raised when the max size is reached."""
      print "test_max_size..."
      # Max size is 2, everything else empty
      q_set = QueueSettings()
      q_set.max_size = 2
      qq = Queue(100, q_set)
      m1 = QueueMember("alice", 44)
      m2 = QueueMember("bob", 123)
      m3 = QueueMember("carol", 125)
      qq.add(m1)
      qq.add(m2)
      self.assertRaises(QueueFullException, qq.add, m3)
   
   def test_postpone(self):
      """Test postponing in the queue. 
      methods tested:
         postpone
         get_position   
      """
      print "test_postpone..."

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

   def test_remove(self):
      """ Tests that a specific member can be removed from the 
         middle of the queue, and also tests getting
         a queue member back, or getting back a list of
         queue members
      methods tested:
         len
         remove
         get_member
         get_members
         """
      print "test_remove..."

      qq = Queue(112)
      m1 = QueueMember("bob", 122)
      m2 = QueueMember("carol", 123)
      m3 = QueueMember("dave", 124)
      m4 = QueueMember("evan", 125)
      m5 = QueueMember("waldo", 987)

      qq.add(m1)
      qq.add(m2)
      qq.add(m3)
      qq.add(m4)
      assert len(qq) == 4
      b1 = qq.remove(m3)
      assert b1
      assert len(qq) == 3
      #removing someone not in the queue should return false
      b2 = qq.remove(m5)
      assert not b2

      # a queue can give back the user in it with a certain id
      mm1 = qq.get_member(122)
      assert mm1.uname == "bob"

      lst = qq.get_members()
      assert lst == [m1, m2, m4]


   def test_popularity(self):
      """ Tests the get_popularity method of a queue 
      popularity is defined as the number of people that
      have entered the queue. 
      methods tested:
         get_popularity
      """
      print "test_popularity..."
      qq = Queue(112)
      m1 = QueueMember("bob", 123)
      m2 = QueueMember("carol", 125)
      m3 = QueueMember("dave", 126)
      assert qq.get_popularity() == 0
      qq.add(m1)
      qq.add(m2)
      assert qq.get_popularity() == 2
      qq.add(m3)
      assert qq.get_popularity() == 3
      qq.dequeue()
      qq.dequeue()
      assert qq.get_popularity() == 3
      qq.dequeue()
      assert qq.get_popularity() == 3

   def test_waiting(self):
      """ Tests some basic things about the wait times
      of a queue. This is a bit odd to test, since
      it depends on timing. Here, we assume that the program runs 
      fast enough that the sleep times overwhelm execution time.
      methods tested:
         get_avg_wait
         get_expected_wait
      """
      print "test_waiting..."
      a = time.time()
      def close(a, b):
         return abs(a-b) < 0.01
      qq = Queue(112)
      m1 = QueueMember("alice", 123)
      m2 = QueueMember("bob", 124)
      m3 = QueueMember("carol", 125)
      # add people to the queue, dequeue them, see how long they waited
      qq.add(m1)
      qq.add(m2)
      time.sleep(0.2)
      qq.add(m3)
      time.sleep(0.1)
      qq.postpone(m2)
      #dequeue m1 and m3 (m2 postponed)
      qq.dequeue()  # waited 0.3
      qq.dequeue()  # waited 0.1
      #average wait time returned is in minutes
      wait =  qq.get_avg_wait() * 60
      assert close(wait, 0.2)
      time.sleep(0.2)
      #dequeue m2
      qq.dequeue()  # waited 0.5
      wait =  qq.get_avg_wait() * 60
      assert close(wait, 0.3)

      #  Test expected wait
      assert(len(qq) == 0)
      m4 = QueueMember("dave", 126)
      qq.add(m4)
      #special case
      assert qq.get_expected_wait(m4) == 0
      m5 = QueueMember("evan", 127)
      qq.add(m5)
      ex_wait = qq.get_expected_wait(m5)
      expected_ex_wait = qq.get_avg_wait() * 1.5/ 2
      assert close(ex_wait, expected_ex_wait)


if __name__ == '__main__':
   unittest.main()




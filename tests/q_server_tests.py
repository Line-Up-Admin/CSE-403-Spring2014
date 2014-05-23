"""
This file creates a QueueServer and does some very basic things
with it to test it. Currently does not integrate with the database.

This tests can be run at the command line with:
    python q_server_tests.py 
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

   def test_add_get_members(self):
      """ Tests create, add, get_members, 
      and get_member_queues on a QueueServer object. """
      # This is set to false so the Server doesn't talk to the database
      qs = QueueServer(False)
      m1 = QueueMember("bob", 123)
      m2 = QueueMember("carol", 124)
      m3 = QueueMember("doug", 125)
      qs1 = {"max_size":4, "qname":"water_park"}
      qs2 = {"max_size":7, "qname":"lunch_spot"}
      # create 2 queues using the settings
      qid_1 = qs.create(qs1)
      qid_2 = qs.create(qs2)
      # For testing purposes, 500 was chosen as the default
      #  starting id.
      assert qid_1 == 500
      assert qid_2 == 501
      qs.add(m1, qid_1)
      qs.add(m2, qid_2)
      
      mems = qs.get_members(qid_1)
      assert len(mems) == 1
      assert mems[0].uname == 'bob'

      #add a user to two queues, and check they are in both
      qs.add(m3, qid_1)
      qs.add(m3, qid_2)
      dougs_qs = qs.get_member_queues(m3.uid)
      print dougs_qs
      assert len(dougs_qs) == 2

   def test_search(self):
      # Note: This test currently does not pass, since the search
      #  functionality has not been implemented.
      # create queues with keywords
      qs = QueueServer(False)

      #queue settings for some queues with different names and locations
      qs1 = {"qname":"water park", "location":"Seattle"}
      qs2 = {"qname":"lunch spot", "location":"Seattle"}
      qs3 = {"qname":"dragon castle", "location":"Fire Mountain"}
      qs4 = {"qname":"lunch spot", "location":"Berlin"}
      qs5 = {"qname":"dragon park", "location":"Fire Mountain"}

      # create queues using the settings
      qid_1 = qs.create(qs1)
      qid_2 = qs.create(qs2)
      qid_3 = qs.create(qs3)
      qid_4 = qs.create(qs4)
      qid_5 = qs.create(qs5)

      #search for a queue by name
      res1 = qs.search("water park")
      assert len(res1) == 2
      assert res1[0] == qid_1
      assert res1[1] == qid_5

      #search by location
      res2 = qs.search("Seattle")
      assert len(res2) == 2
      assert qid_1 in res2
      assert qid_2 in res2

      #search with both
      res3 = qs.search("lunch spot seattle")
      assert len(res3) == 3
      assert res3[0] == qid_2
      assert res3[1] == qid_4
      assert res3[2] == qid_1
      assert qid_2 in res3


if __name__ == '__main__':
   unittest.main()


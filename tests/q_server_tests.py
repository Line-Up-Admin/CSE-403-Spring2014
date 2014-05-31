"""
This file creates a QueueServer and does some very basic things
with it to test it. Currently does not integrate with the database.

This tests can be run at the command line with:
    python q_server_tests.py 
"""

import os
import unittest
import sys
#sys.path.insert(0, '../..') 
sys.path.insert(0, '..') # the tests folder 
sys.path.insert(0, '.') # CSE-403-Spring2014 level
sys.path.insert(0, '../app')
#from app import app
from app.q_classes import *


class SomeTest(unittest.TestCase):

   def setUp(self):
      pass

   def tearDown(self):
      pass

   def test_a_few_things(self):
      """ Tests create, add, get_members, 
      and get_member_queues on a QueueServer object. 
      methods tested:
         add 
         create
         dequeue
         remove
         get_popular
         get_members
         get_member_queues
      """
      print "testing a few things"
      qs = QueueServer(sync_db = False)
      m1 = QueueMember("alice", 122)
      m2 = QueueMember("bob", 123)
      m3 = QueueMember("carol", 124)
      m4 = QueueMember("doug", 125)
      m5 = QueueMember("evan", 126)
      m6 = QueueMember("franklin", 127)
      m7 = QueueMember("gregory", 128)
      m8 = QueueMember("hank", 129)
      qs1 = {"max_size":4, "qname":"Apocolypse Garden"}
      qs2 = {"max_size":7, "qname":"A world of magic"}
      qs3 = {"max_size":7, "qname":"Dragon Palace"}
      # create 2 queues using the settings
      qid_1 = qs.create(qs1)
      qid_2 = qs.create(qs2)
      qid_3 = qs.create(qs3)
      # For testing purposes, 500 was chosen as the default
      #  starting id.
      assert qid_1 == 500
      assert qid_2 == 501
      assert qid_3 == 502
      qs.add(m1, qid_1)
      #Most people in q2
      qs.add(m2, qid_2)
      qs.add(m3, qid_2)
      qs.add(m4, qid_2)
      
      mems = qs.get_members(qid_2)
      assert len(mems) == 3
      assert mems[0].uname == 'bob'

      # test removing from the middle
      qs.remove(m3, qid_2)
      mems = qs.get_members(qid_2)
      assert len(mems) == 2
      # test removing from the end
      qs.remove(m4, qid_2)
      mems = qs.get_members(qid_2)
      assert len(mems) == 1

      #add a user to two queues, and check they are in both
      qs.add(m6, qid_1)
      qs.add(m6, qid_2)
      franklins_qs = qs.get_member_queues(m6.uid)
      assert len(franklins_qs) == 2

      qs.add(m7, qid_2)
      
      # 3 members currently in qid_2: m2, m6, m7
      # 2 member currently in qid_1: m1, m6
      popular_qs = qs.get_popular()
      assert popular_qs[0] == qid_2

      ### test dequeue
      # test dequeue raises exception with bad queue
      self.assertRaises(QueueNotFoundException, qs.dequeue, 9999999)
      mm2 = qs.dequeue(qid_2)
      assert mm2.uid == m2.uid
      assert mm2.uname == m2.uname
      mm6 = qs.dequeue(qid_2)
      assert mm2.uid == m2.uid
      assert mm2.uname == m2.uname

      qs.dequeue(qid_2)
      # Queue is now empty
      non = qs.dequeue(qid_2)
      assert non == None

   def test_search(self):
      """
      methods tested:
         search 
      """
      print "testing search"
      qs = QueueServer(False)

      #queue settings for some queues with different names and locations
      qs1 = {"qname":"water park", "location":"Seattle"}
      qs2 = {"qname":"lunch spot", "location":"Seattle"}
      qs3 = {"qname":"dragon castle", "location":"Fire Mountain"}
      qs4 = {"qname":"lunch spot", "location":"Berlin"}
      qs5 = {"qname":"dragon park", "location":"Fire Mountain"}
      qs6 = {"qname":"twilight struggle", "keywords":"board;game:fun;;seattle"}

      # create queues using the settings
      qid_1 = qs.create(qs1)
      qid_2 = qs.create(qs2)
      qid_3 = qs.create(qs3)
      qid_4 = qs.create(qs4)
      qid_5 = qs.create(qs5)
      qid_6 = qs.create(qs6)

      #search for a queue by name
      res1 = qs.search("water park")
      assert len(res1) == 2
      assert res1[0] == qid_1
      assert res1[1] == qid_5

      #search by location
      res2 = qs.search("Seattle")
      assert len(res2) == 3
      assert qid_1 in res2
      assert qid_2 in res2
      assert qid_6 in res2

      #search with both
      res3 = qs.search("lunch spot seattle")
      assert len(res3) == 4
      assert res3[0] == qid_2
      assert res3[1] == qid_4
      assert qid_1 in res3
      assert qid_6 in res3

if __name__ == '__main__':
   unittest.main()


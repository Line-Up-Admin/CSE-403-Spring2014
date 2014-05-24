""" 
The purpose of this file is to contain a number of Queue classes.
These classes will be used by our route handler to handle the
actual data structures involved. 
"""

# deque is Python's double ended queue implementation.
# append adds to the right, and popleft removes from the left.
# (similar methods are pop and appendleft if we wanted the queue to go
#   the other direction.)
from collections import deque

#Used for analytics of wait times
from datetime import datetime

import database_utilities as db_util
import re
from operator import itemgetter

# Custom Exception
class QueueFullException(Exception):
   pass

class QueueNotFoundException(Exception):
   pass

class MemberNotFoundException(Exception):
   pass

class Queue(object):
   """ A Queue object stores the actual in-memory representation 
      of a Queue. """

   def __init__(self, qid, q_settings = None):
      # This is the actual Queue field of the object. It stores the
      # QueueMemeber as well as the time the Queue was entered. 
      # (Time entered is for the purposes of analytics.)
      self.my_q = deque()

      # This q_settings object defaults to None if it is not
      # passed in to the constructor. A Queue with no
      # Queue settings is a 'default' queue, with no max size,
      # no admins, etc.
      self.q_settings = q_settings
      self.id = qid

      # A queue keeps track of the wait times of every person
      # that has been in the queue. This is currently a dictionary from
      # QueueMember to list of tuple pairs. Each tuple is an in time and
      # out time. Ex: {qm:[(101.1,300.4),(50.3,79.2)]}
      self.wait_times = {}

      # A Queue also has an average wait, but this is recalculated
      # on the fly every time it is asked for.

   def __len__(self):
      """ This allows the size of the queue object 'q' to be
         obtained by calling len(q) """
      return len(self.my_q)

   def get_avg_wait(self):
      """ This currently returns the average wait time in minutes 
      of everyone who has ever been in the queue. """
      if len(self.wait_times) == 0:
         # This shouldn't really be 0, but the users might not 
         #  like a display of 'undefined'
         return 0
      else:
         total_num = 0
         total_time = 0.0
         for waits in self.wait_times.values():
            for wait in waits:
               total_num += 1
               total_time += (wait[1] - wait[0]).total_seconds()
         # divide by 60 because time() is in seconds.
         return total_time / float(total_num * 60)

   def add(self, member):
      """ Adds a Queue Member to a Queue. (If there is room.) """
      if self.q_settings and len(self.my_q) >= self.q_settings.max_size:
         raise QueueFullException("Queue is already at maximum size")
      else:
         self.my_q.append( (member, datetime.now()) )

   def remove(self, member):
      """ Removes a Queue Member from a Queue """
      pos = self.get_position(member)
      if pos == None:
         return False
      # if someone is removed from the middle, we do not take their
      # wait time into account for analytics.
      q = self.my_q
      del q[pos]
      return True

   def postpone(self, member, sync_db = False):
      """ Postpones a Queue Member's position in a Queue.
         If a user attempt to postpone past the end of the line,
         the position is not affected."""
      pos = self.get_position(member)
      if pos == None:
         raise MemberNotFoundException("Member is not in queue.")
      elif pos + 1 < len(self.my_q):
         #There is room to move the user back a position in the queue.
         temp = self.my_q[pos]
         next_member = self.my_q[pos + 1]
         if sync_db:
            db_util.swap(temp[0].uid, next_member[0].uid, self.id)
         self.my_q[pos] = self.my_q[pos + 1]
         self.my_q[pos + 1] = temp
      #else: member is already at the end of the queue

   def get_expected_wait(self, member):
      """ Returns the estimated wait time of a user in a Queue in minutes
         (not in UML)"""

      # the expected wait time here could be improved to be something
      #  more intelligent. Currently, it is average wait time of the queue
      #  times the proportion of the queue remaining.
      avg_wait = self.get_avg_wait()
      position = self.get_position(member)

      if position == 0:
         return 0
      if avg_wait and position:
         #avg_wait is already in minutes
         ex_wait = avg_wait * (position + 0.5)/len(self.my_q)
         return ex_wait
      else:
         # This is currently fake data for demoing purposes.
         return 10

   def dequeue(self):
      """ Dequeues the next QueueMember from the Queue. """
      if len(self.my_q) > 0:
         item = self.my_q.popleft()
         # Record the wait time of the person dequeued.
         member = item[0]
         in_time = item[1]
         out_time = datetime.now()
         if member not in self.wait_times:
            self.wait_times[member] = []
         self.wait_times[member].append( (in_time, out_time) )
         return member
      else:
         return None

   def get_position(self, member):
      """ Returns the current position in the queue of the Queue member
         being asked about. This is a 0-based index from the front
         of the line. """
      if member is None:
         return None
      for i, j in enumerate(self.my_q):
         if j[0].uid == member.uid:
            return i
      return None

   def get_member(self, userid):
      """
      Returns:
         the saved QueueMember object associated with the uid."""
      q_member = QueueMember(uid=userid)
      for item in self.my_q:
         # QueueMember equality is defined by having the same id.
         if item[0] == q_member:
            return item[0]
      return None

   def get_members(self):
      """ 
      Returns: a list of copies of all of the members of the queue """
      members = list()
      for member in self.my_q:
         # remove the time from result
         members.append(member[0])
      return members

   def get_popularity(self):
        """
        Returns the number of people who have been enqued and dequed
        from this queue"""
        total = 0
        for item in self.wait_times.values():
           total += len(item)
        return total

class QueueMember(object):
      """  This is a person / anonymous user in a queue. More
         fields may be added to this object to support more options
         such as party size. """
      def __init__(self, uname=None, uid=None, optional_data=None):
         self.uname = uname
         self.uid = uid
         self.optional_data = optional_data

      def __eq__(self, other):
         """ Queue Members are defined to be equal only if they
            have the same ID. """
         if other == None:
            return False
         else:
            return self.uid == other.uid

      @staticmethod
      def from_dict(member_dict):
         q_member = QueueMember()
         for key in member_dict.keys():
            if hasattr(q_member, key):
               setattr(q_member, key, member_dict[key])
         return q_member

class QueueSettings(object):
   """ This class is used to store all the settings that an administrator
      might want to set regarding a queue. """
   def __init__(self):
      self.max_size = 100
      # keywords may be a list of strings in the future
      self.keywords = ''
      # name is the name of the Queue, such as "Hall Health" 
      self.qname = ''
      self.managers = None
      self.admins = None
      self.blocked_users = None
      self.location = ''
      self.active = 1
      self.min_wait_rejoin = 0
      self.website = ''
      self.organization = ''
      self.disclaimer = ''
      self.prompt = ''

   @staticmethod
   def from_dict(settings):
      q_settings = QueueSettings()
      for key in settings.keys():
         if hasattr(q_settings, key):
            setattr(q_settings, key, settings[key])
      return q_settings

class QueueServer(object):
   """ This is a Queue Server object, which is responsible
   for keeping track of all the queues in the system. 
   The table field is a table of the Queues in the system, 
   and index is a reverse index that maps from uid to 
   a set of qid.
   Current behavior is to raise an exception when a client
   tries to modify a non-existent queue."""
   
   def __init__(self, sync_db = True):
      # the sync_db parameters is for testing purposes.
      #  By setting this parameter to False, you can create a QueueServer
      #  that does not try to talk to the database.
      
      # table from qid to Queue
      self.table = {}
      # reverse index from uid to a set of qids
      self.index = {}
      self.sync_db = sync_db
      if not sync_db:
         # If we don't want to recreate from the database, we can stop here
         self.id_gen = 500
         return

      def get_q_history(qid):
         # this method takes a qid, gets the info from the database
         #  and returns the q_history for it.
         #  (dict of list of tuples)
         time_rows = db_util.get_history(qid)
         if time_rows == None:
            return {}
         result = {}
         for row in time_rows:
            uid = row[uid]
            if uid not in result:
               result[uid] = []
            result[uid].append( (row['join_time'], row['leave_time']) )
         return result

      # read all the queues from the database, and put them into the tables
      # get_all_queues returns a list of tuples of qids to QueueSettings 
      #  objects
      (q_settings_rows, q_rows) = db_util.get_all_queues()
      print 'Loading queues from db...'
      i = 0
      for q_settings_row in q_settings_rows:
         q_settings = QueueSettings.from_dict(q_settings_row)
         qid = q_settings_row['qid']
         q = Queue(qid, q_settings)
         #reattach the time history to the queue
         q.wait_times = get_q_history(qid)
         self.table[qid] = q
         member_rows = db_util.get_queue_members(qid)
         if member_rows:
            j = 0
            for member_row in member_rows:
               # already ordered
               q_member = QueueMember.from_dict(member_row)
               q.add(q_member)
               if q_member.uid not in self.index:
                  self.index[q_member.uid] = set()
               self.index[q_member.uid].add(qid)
               print 'added', q_member.uname, 'to queue', q_settings.qname
               j = j + 1
            print 'Loaded', j, 'members into queue', q_settings.qname
         i = i + 1
      print 'Done loading. loaded', i, 'queues'

   def add(self, member, qid):
      """ Adds a new member to a specific queue."""
      if qid not in self.table:
         raise QueueNotFoundException('Queue not found')
      q = self.table[qid]
      q.add(member)
      #add member to the reverse index
      if member.uid not in self.index:
         self.index[member.uid] = set()
      self.index[member.uid].add(qid)
      if self.sync_db:
         db_util.add_to_queue(member.uid, qid, member.optional_data)

   def remove(self, member, qid):
      """ This could raise a KeyError, which we are currently
         passing on the to caller. """
      q = self.table[qid]
      self.index[member.uid].remove(qid)
      if self.sync_db:
         db_util.remove_by_uid_qid(member.uid, qid)
      return q.remove(member)

   def removeByID(self, uid, qid):
      """ This could raise a KeyError, which we are currently
         passing on the to caller. """
      q = self.table[qid]
      self.index[uid].remove(qid)
      if self.sync_db:
         db_util.remove_by_uid_qid(uid, qid)
      member = q.get_member(uid)
      return q.remove(member)


   def dequeue(self, qid):
      if qid not in self.table:
         raise QueueNotFoundException('Queue not found')
      q_member = self.table[qid].dequeue()
      if q_member is None:
         return None
      self.index[q_member.uid].remove(qid)
      if self.sync_db:
         db_util.remove_by_uid_qid(q_member.uid, qid)
      return q_member


   def search(self, search_string):
      """ Returns a list of  qids that match the parameters 
         passed in. Currently, search returns all the queues
         that match any of the keywords, with the ones that match
         the most at the top. Implementation is not that efficient. """
      def remove_duplicates(lst):
         return list(set(lst))
      def to_list(st):
         #split string on comma, space, or semicolon, and make everything lower case
         return [ s.lower() for s in re.split('[:;, ]+', st)]
      def match_score(str1, str2):
         words1 = remove_duplicates(to_list(str1))
         words2 = remove_duplicates(to_list(str2))
         score = 0
         for word1 in words1:
            for word2 in words2:
               if word1 == word2:
                  score += 1
         return score
      results = []
      for qid, queue in self.table.items():
         qset = queue.q_settings
         if qset == None:
            continue
         score = 0
         if qset.qname:
            score += match_score(search_string, qset.qname)
         if qset.location:
            score += match_score(search_string, qset.location)
         if qset.keywords:
            score += match_score(search_string, qset.keywords)
         if score > 0:
            results.append( (qid, score) )
      results = sorted(results, key=itemgetter(1), reverse=True)
      results = [item[0] for item in results]
      return results

   def get_popular(self):
         """ Returns a list of queues, sorted by their popularity """
         results = []
         for (qid, queue) in self.table.items():
            results.append( (qid, queue.get_popularity()) )
         results = sorted(results, key=itemgetter(1), reverse=True)
         results = [item[0] for item in results]
         return results

   def create(self, settings):
      """ Given a settings dictionary, or a QueueSettings object,
         creates a queue, adds to the database, and 
         returns the id of the queue created. """
      if self.sync_db:
         #save the queue to the database, get id
         qid = db_util.create_queue(settings)
      else:
         qid = self.id_gen
         self.id_gen += 1
      if not (type(settings) is QueueSettings):
         #convert from dict if necessary
         settings = QueueSettings.from_dict(settings)
      new_q = Queue(qid, settings)
      self.table[qid] = new_q
      return qid

   def get_members(self, qid):
      """ Returns a list of members of a specific queue 
      (not in UML)"""
      return self.table[qid].get_members()

   def get_member_queues(self, uid):
      """ Returns a set of queues that a member is in 
         (not in UML)"""
      return self.index[uid]
   
   def edit_queue(self, qid, qsettings):
      """ Updates the settings for the specified queue."""
      if qid not in self.table:
         raise QueueNotFoundException('Queue not found')
      else:
         q = self.table[qid]
         q.q_settings = qsettings
         db_settings = dict(q.q_settings.__dict__)
         db_settings['qid'] = qid
         if self.sync_db:
            db_util.modify_queue_settings(db_settings)
         
   def postpone(self, member, qid):
      if qid not in self.table:
         raise QueueNotFoundException('Queue not found')
      return self.table[qid].postpone(member, self.sync_db)

   def get_settings(self, member, qid):
      """ This method gets the settings associated with a queue."""
      q = self.table[qid]
      if qid not in self.table:
         raise QueueNotFoundException('Queue not found')
      return self.table[qid].q_settings

   def get_info(self, member, qid):
      """ This method gets the info associated with a queue."""
      q = self.table[qid]
      q_set = q.q_settings
      if q_set:
         qname = q_set.qname
      else:
         name = None
      size = len(q)
      avg_wait = q.get_avg_wait()
      ex_wait = q.get_expected_wait(member)
      #this is a zero-based index
      position = q.get_position(member)
      return QueueInfo(qname, qid, size, ex_wait, avg_wait, 
            position, q_set.organization, q_set.prompt, 
            q_set.disclaimer, q_set.website, q_set.location)

   def get_all_queues_info(self):
      """ (not in UML) """
      result = list()
      for queue in self.table.values():
         q_info = self.get_info(None, queue.id)
         result.append(q_info)
      return result

   def get_queue_info_list(self, userid):
      """ UML
      Args:
         q_member: a QueueMember object. QueueMembers are defined by uid, 
         so if uname and optional_data is not known, just create a 
         QueueMember and assign it the uid.

      Returns:
         a list of QueueInfo.
      """
      if not self.index.has_key(userid):
         return None
      queue_list = list()
      for qid in self.index[userid]:
         queue_list.append(self.get_info(QueueMember(uid=userid), qid))
      return queue_list

   def is_active(self, qid):
      if self.table.has_key(qid):
         q = self.table[qid]
         return q.q_settings.active
      return False

   def set_active(self, qid, active):
      """ Sets a specific queue as active or inactive."""
      if qid not in self.table:
         raise QueueNotFoundException('Queue not found')
      q = self.table[qid]
      q.q_settings.active = active
      db_settings = dict(q.q_settings.__dict__)
      db_settings['qid'] = qid
      if self.sync_db:
          db_util.modify_queue_settings(db_settings)

class QueueInfo(object):
   """ This is a class to store a number of pieces of information
      about a queue. This info will be sent back to the client
      as JSON, and rendered in the browser."""
   def __init__(self, qname, qid, size, expected_wait, avg_wait_time,
         member_position, organization, prompt, disclaimer, website, location):
      self.qname = qname
      self.qid = qid
      self.size = size
      self.expected_wait = expected_wait
      self.avg_wait_time = avg_wait_time
      self.member_position = member_position
      self.organization = organization
      self.prompt = prompt
      self.disclaimer = disclaimer
      self.website = website
      self.location = location

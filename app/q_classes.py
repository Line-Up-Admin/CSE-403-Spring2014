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

#Might use this in the future
import database_utilities as db_util

# Custom Exception
class QueueFullException(Exception):
   pass

class Queue(object):
   """ A Queue object stores the actual in-memory representation 
      of a Queue. """

   def __init__(self, qid, q_settings = None):
      # This is the actual Queue field of the object
      self.my_q = deque()

      # This q_settings object defaults to None if it is not
      # passed in to the constructor. A Queue with no
      # Queue settings is a 'default' queue, with no max size,
      # no admins, etc.
      self.q_settings = q_settings
      self.id = qid

      # Avg wait is initially undefined, and is not passed in.
      self.avg_wait = None

   def __len__(self):
      """ This allows the size of the queue object 'q' to be
         obtained by calling len(q) """
      return len(self.my_q)

   def add(self, member):
      """ Adds a Queue Member to a Queue. (If there is room.) """
      if self.q_settings and len(self.my_q) >= self.q_settings.max_size:
         raise QueueFullException("Queue is already at maximum size")
      else:
         self.my_q.append(member)

   def remove(self, member):
      """ Removes a Queue Member from a Queue """
      if member not in self.my_q:
         return False
      else:
         self.my_q.remove(member)
         return True

   def postpone(self, member):
      """ Postpones a Queue Member's position in a Queue.
         If a user attempt to postpone past the end of the line,
         the position is not affected."""
      pos = self.my_q.getPosition(member)
      if pos == None:
         raise Exception("Member is not in queue.")
      elif pos + 1 < len(self.my_q):
         #There is room to move the user back a position in the queue.
         temp = member
         self.my_q[pos] = self.my_q[pos + 1]
         self.my_q[pos + 1] = temp
      #else: member is already at the end of the queue

   def get_wait_time(self, member):
      """ Returns the estimated wait time of a user in a Queue, using
      intelligent heuristics based on their current position and 
      previous line information. """
      return "Not yet implemented"

   def dequeue(self):
      """ Dequeues the next QueueMember from the Queue. 
          Note: return type here differs from UML diagram """
      if len(self.my_q) > 0:
         return self.my_q.popleft()
      else:
         return None

   def get_position(self, member):
      """ Returns the current position in the queue of the Queue member
         being asked about. This is a 0-based index from the front
         of the line. """
      for i, j in enumerate(self.my_q):
         if j.uid == member.uid:
            return i
      return None

   def get_member(self, userid):
      """
      Returns:
         the saved QueueMember object associated with the uid."""
      q_member = QueueMember(uid=userid)
      for i, j in enumerate(self.my_q):
         if j == q_member:
            return j
      return None

   def get_members(self):
      members = list()
      for member in self.my_q:
         members.append(member)
      return members


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
      self.max_size = 0
      # keywords may be a list of strings in the future
      self.keywords = ''
      # name is the name of the Queue, such as "Hall Health" 
      self.qname = ''
      self.employees = None
      self.admins = None
      self.blockedUsers = None
      self.location = ''

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
         self.id_gen = 500
         return
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
         raise Exception('Queue not found')
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
      # TODO: update database state
      return q.remove(member)

   def dequeue(self, qid):
      """ Note -- parameter here differs from UML diagram. """
      if qid not in self.table:
         raise Exception('Queue not found')
      q_member = self.table[qid].dequeue()
      if q_member is None:
         return None
      self.index[q_member.uid].remove(qid)
      if self.sync_db:
         db_util.remove_by_uid_qid(q_member.uid, qid)
      return q_member

   def search(self, name, location):
      """ Returns a list of  qids that match the parameters 
         passed in.
      Implementation here is not very efficient. """
      results = []
      name = name.lower()
      #for qid, q in self.table:
      #   if 
      return "Not yet implemented"

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

   def postpone(self, member, qid):
      if qid not in self.table:
         raise Exception('Queue not found')
      return self.table[qid].postpone(member)

   def get_info(self, member, qid):
      """ This method gets the info associated with a queue.
         (Not currently in UML diagram.) """
      q = self.table[qid]
      q_set = q.q_settings
      if q_set:
         qname = q_set.qname
      else:
         name = None
      size = len(q)
      avg_wait = q.avg_wait
      #this is a zero-based index
      position = q.get_position(member)
      # the expected wait time here could be improved to be something
      #  more intelligent. Currently, it is average wait time of the queue
      #  times the proportion of the queue remaining.
      if avg_wait and position:
         ex_wait = avg_wait * (position + 0.5)/float(size) 
      else:
         ex_wait = 10
      return QueueInfo(qname, qid, size, ex_wait, avg_wait, position)

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

class QueueInfo(object):
   """ This is a class to store a number of pieces of information
      about a queue. This info will be sent back to the client
      as JSON, and rendered in the browser."""
   def __init__(self, qname, qid, size, expected_wait, avg_wait_time,
         member_position):
      self.qname = qname
      self.qid = qid
      self.size = size
      self.expected_wait = expected_wait
      self.avg_wait_time = avg_wait_time
      self.member_position = member_position

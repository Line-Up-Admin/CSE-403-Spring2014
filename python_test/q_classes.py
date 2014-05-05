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

class Queue(object):
   """ A Queue object stores the actual in-memory representation 
      of a Queue. """

   def __init__(self, id, q_settings = None):
      # This is the actual Queue field of the object
      self.my_q = deque()

      # This q_settings object defaults to None if it is not
      # passed in to the constructor. A Queue with no
      # Queue settings is a 'default' queue, with no max size,
      # no admins, etc.
      self.q_settings = q_settings

      # Avg wait is initially undefined, and is not passed in.
      self.avg_wait = None

   def __len__(self):
      """ This allows the size of the queue object 'q' to be
         obtained by calling len(q) """
      return len(self.my_q)

   def add(self, member):
      """ Adds a Queue Member to a Queue. (If there is room.) """
      if self.q_settings and len(self.my_q >= self.q_settings.max_size):
         raise Exception("Queue is already at maximum size")
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

   def getWaitTime(self, member):
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

   def getPosition(self, member):
      """ Returns the current position in the queue of the Queue member
         being asked about. """
      for i, j in enumerate(self.my_q):
         if j == member:
            return i
      return None


class QueueMember(object):
      """  This is a person / anonymous user in a queue. More
         fields may be added to this object to support more options
         such as party size. """
      def __init__(self, username, ID):
         self.username = username
         self.ID = ID

      def __eq__(self, other):
         """ Queue Members are defined to be equal only if they
            have the same ID. """
         if other == None:
            return False
         else:
            return self.ID == other.ID


class QueueServer(object):
   """ This is a Queue Server object, which is responsible
   for keeping track of all the queues in the system. 
   The table field is a table of the Queues in the system, 
   and index is a reverse index that maps from memberID to QID.
   Current behavior is to raise an exception when a client
   tries to modify a non-existent queue."""

   def __init__(self):
      self.table = {}
      self.index = {}

   def add(self, member, q_ID):
      """ Adds a new member to a specific queue."""
      if a_ID not in self.table:
         raise Exception('Queue not found')
      q = self.table[q_ID]
      q.add(member)

   def remove(self, member, q_ID):
      """ This could raise a KeyError, which we are currently
         passing on the to caller. """
      q = self.table[q_ID]
      return q.remove(member)

   def dequeue(self, q_ID):
      """ Note -- parameter here differs from UML diagram. """
      if a_ID not in self.table:
         raise Exception('Queue not found')
      return self.table[q_ID].dequeue()

   def search(self, name, location):
      """ Implementation here is not very efficient. """
      results = []
      name = name.lower()
      #for q_ID, q in self.table:
      #   if 

      return "Not yet implemented"

   def create(self, settings):
      return "Not yet implemented"

   def get(self, q_id):
      """ I'm not sure this method is necessary if all Queue 
         modification is done through the QueueServer object. """
      return self.table[q_id]

   def postpone(self, member, q_ID):
      if a_ID not in self.table:
         raise Exception('Queue not found')
      return self.table[q_ID].postpone(member)


class QueueSettings(object):
   """ This class is used to store all the settings that an administrator
      might want to set regarding a queue. """
   def __init__(self, max_size, keywords, name, employees, 
         admins, blockedUsers, location):
      self.max_size = max_size
      # keywords is a list of strings
      self.keywords = keywords
      # name is the name of the Queue, such as "Hall Health" 
      self.name = name
      self.employees = employees
      self.admins = admins
      self.blockedUsers = blockedUsers
      self.location = location




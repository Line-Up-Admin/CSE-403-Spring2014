""" 
The purpose of this file is to contain a number of Queue classes.
These classes will be used by the flask framework to handle the
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

   def __init__(self, id):
      # This is the actual Queue field of the object
      self.my_q = deque()

   def __len__(self):
      return len(self.my_q)

   def add(self, member):
      """ Adds a Queue Member to a Queue """
      self.my_q.append(member)

   def remove(self, member):
      """ Removes a Queue Member from a Queue """
      self.my_q.remove(member)

   def postpone(self, member):
      """ Postpones a Queue Member's position in a Queue.
         If a user attempt to postpone past the end of the line,
         the user is placed at the end of the line."""
      return "Not yet implemented"

   def getWaitTime(self, member):
      """ Returns the estimated wait time of a user in a Queue, using
      intelligent heuristics based on their current position and 
      previous line information. """
      return "Not yet implemented"

   def deq(self):
      """ Dequeues the next QueueMember from the Queue. """
      if len(self.my_q) > 0:
         return self.my_q.popleft()
      else:
         return None


   def getPosition(self, member):
      """ Returns the current position in the queue of the Queue member
         being asked about. """
      return "Not yet implemented"


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
   and index is a reverse index """
   table = {}
   index = {}

   def add(self, member, q_ID):
      if q_ID in self.table:
         # raise an exception here?
         return False
      self.table[q_ID] = member
      return True

   def remove(self, member, q_ID):
      return "Not yet implemented"
   def dequeue(self, member):
      return "Not yet implemented"
   def search(self, name, location):
      return "Not yet implemented"
   def create(self, settings):
      return "Not yet implemented"
   def get(self, q_id):
      return self.table[q_id]
   def postpone(self, member, q_ID):
      return "Not yet implemented"


class QueueSettings(object):
   """ This class is used to store all the settings that an administrator
      might want to set regarding a queue. """
   def __init__(self, max_size, keywords, name, employees, 
         admins, blockedUsers, location):
      self.max_size = max_size
      self.keywords = keywords
      self.name = name
      self.employees = employees
      self.admins = admins
      self.blockedUsers = blockedUsers
      self.location = location




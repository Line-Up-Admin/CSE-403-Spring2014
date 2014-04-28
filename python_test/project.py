# deque is Python's double ended queue implementation.
# append adds to the right, and popleft removes from the left.
# (similar methods are pop and appendleft if we wanted the queue to go
#   the other direction.)
from collections import deque

class Queue(object):
   """ A Queue object stores the actual in-memory representation 
      of a Queue. """
   #this is the actual Queue field of the object. This next line
   # is currently unnecessary, since the same thing happens in the 
   # constructor.
   my_q = deque()

   def __init__(self, id):
      # The queue is initially empty.
      self.my_q = deque()

   def add(member):
      my_q.append(member)

   def remove(member):
      my_q.remove(member)

   def postpone(member):
      return "Not yet implemented"

   def getWaitTime(member):
      return "Not yet implemented"

   def dequeue():
      if len(my_q) > 0:
         return my_q.popleft()
      else:
         return None

   def getPosition(member):
      return "Not yet implemented"


class QueueMember(object):
      """  This is a person / anonymous user in a queue. More
         fields may be added to this object to support more options
         such as party size. """
      def __init__(self, username, ID):
         self.username = username
         self.ID = ID

      def __cmp__(self, other):
         return cmp(self.ID, other.ID)


class QueueServer(object):
   """ This is a Queue Server object, which is responsible
   for keeping track of all the queues in the system. """
   tables = {}
   index = {}

   def add(member, q_ID):
      return "Not yet implemented"
   def remove(member, q_ID):
      return "Not yet implemented"
   def dequeue(member):
      return "Not yet implemented"
   def search(name, location):
      return "Not yet implemented"
   def create(settings):
      return "Not yet implemented"
   def get(q_id):
      return "Not yet implemented"
   def postpone(member, q_ID):
      return "Not yet implemented"


class QueueSettings(object):
   """ This class stores all the settings that an administrator
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




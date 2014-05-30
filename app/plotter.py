
import sys
import matplotlib.pyplot as plt
import time

class Plotter(object):
   def __init__(self, q):

      #currently plot fake data
      self.data = ([2,3,4,5],[4,7,9,6])
      return
      # turn the q into a series of x and y data points
      def wt_to_list(wt):
         res = []
         for q, waits in wt:
            res += waits
         return res
      time_list = wt_to_list(q.wait_times)

      in_times = []
      waits = []
      for tup in time_list:
         in_times.append(tup[0])
         waits.append(tup[1] - tup[0])
      self.data = (in_times, waits)

   def save_fig(self, filename):
      plt.plot(self.data[0], self.data[1], lw=2)
      plt.savefig(filename)






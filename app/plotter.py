
import sys
import matplotlib.pyplot as plt
import numpy
import time
import datetime
import math
import pylab

# "Constants" for units of Day, Month, etc. 
#   All units for variables are in seconds
MINUTE = 60
HOUR = 60 * MINUTE
DAY = 24 * HOUR
YEAR = 365 * DAY

class Plotter(object):

   def __init__(self, q):

      ####  fakery
      def ft(time_since_24, wait_time):
         #fake time function
         return (time.time() - DAY + time_since_24*HOUR,
             time.time() - DAY + time_since_24*HOUR + 
             wait_time*HOUR/2)
      fake_waits = {"b":[ft(2,2),ft(3.5,10),
                           ft(4,8),ft(5,11),ft(7.5,7),ft(9,8.5)]} 
      class A():
         wait_times = fake_waits
      q = A()
      ####  end fakery

      # turn the q into a series of x and y data points
      def wt_to_list(wt):
         res = []
         for q, waits in wt.items():
            res += waits
         return res
      time_list = wt_to_list(q.wait_times)

      in_times = []
      waits = []
      for tup in time_list:
         in_times.append(tup[0])
         waits.append(tup[1] - tup[0])
      #insert fake points to 
      # bring plot down to zero at the start and end
      f_time = in_times[0]
      in_times.insert(0, f_time - HOUR)
      waits.insert(0,0)
      l_time = in_times[-1]
      in_times.append(l_time + HOUR)
      waits.append(0)

      self.data = (in_times, waits)
      #precalculate some other useful things
      self.min_wait = min(waits)
      self.max_wait = max(waits)
      self.min_in_time = min(in_times)
      self.max_in_time = max(in_times)
      self.wait_range = max(waits) - min(waits)


   def save_fig(self, filename, st_time = 24):
      # Here we only plot the last 24 hours
      plt.plot(self.data[0], self.data[1], lw=2)
      # y axis always starts at 0
      # x axis units are seconds, but we overlay more
      # meaningful tick marks for the user#
      
      curr_time = time.time()
      curr_hour = datetime.datetime.now().hour
      #generate the x axis
      def time_label(i):
         #generate a string based on the hour i, on a 24hr clock
         while i < 0:
            i += 24
         if i >= 12 and i < 24:
            st = 'pm'
         else:
            st = 'am'
         i = i%12
         if i == 0:
            i = 12
         return str(i) + st
      xt = []
      x_labels = []
      for i in range(25):
         xt.append( curr_time - 24*HOUR + i*HOUR )
         x_labels.append(time_label(curr_hour-24 + i))

      #choose the units of the y axis
      #if y_max > ...
      #list of possible units on the y axis.
      #  each contains the string it would use for plotting
      def y_time_label(i):
         #given a integer value of seconds, returns a label
         i = int(i)
         display = True
         if i < MINUTE:
            st = " second"
         elif i < HOUR:
            st = " minute"
            if i % MINUTE != 0:
               display = False
            i = i // MINUTE
         elif i < DAY:
            st = " hour"
            if i % HOUR != 0:
               display = False
            i = i // HOUR
         else:
            st = " day"
            if i % DAY != 0:
               display = False
            i = i // DAY
         if i > 1:
            st += "s"
         return str(i) + st if display else ""

      #choose y axis display range
      y_max_display = math.ceil(self.max_wait*1.1)
      y_min_display = 0

      # Choose appropriate tick mark spacing for the vertical axis (in seconds)
      units = [10, 30, MINUTE, 10*MINUTE, 30*MINUTE, HOUR, DAY]
      i = 0
      # we don't want more than 20 tick marks on the vertical axis
      while i + 1 < len(units) and int(y_max_display) // units[i] > 20:
         i += 1
      unit = units[i]
      
      yt = []
      y_labels = []
      num_ticks = int(math.floor(y_max_display / unit)) + 1
      for i in range(1,num_ticks):
         yt.append( i*unit )
         y_labels.append( y_time_label(i*unit) )

      #set the ticks, labels, and axis range
      pylab.xticks(xt, x_labels, size=5)
      pylab.yticks(yt, y_labels, size=8)
      plt.axis(( curr_time - DAY, curr_time,
                 y_min_display,  y_max_display ))
      plt.savefig(filename)


# Example/test usage of this class. In actual use, you would
#  pass in an actual queue, rather than 'None'
p = Plotter(None)
p.save_fig("abc.png")




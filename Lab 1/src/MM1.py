import heapq
import random
import matplotlib.pyplot as plt
import numpy as np
from queue import Queue

# import matplotlib as mpl
# mpl.use('tkagg')
# import matplotlib.pyplot as plt

signalList = []
def send(signalType, evTime, destination, info):
    heapq.heappush(signalList, (evTime, signalType, destination, info))

GENERATE = 1
ARRIVAL = 2
MEASUREMENT = 3
DEPARTURE = 4

simTime = 0.0
stopTime = 1000.0

class larger():
    def __gt__(self, other):
        return False

class generator(larger):
    def __init__(self, sendTo,lmbda):
        self.sendTo = sendTo
        self.lmbda = lmbda
        self.arrivalTimes = []
    def arrivalTime(self):
        return simTime + random.expovariate(self.lmbda)
    def treatSignal(self, x, info):
        if x == GENERATE:
            send(ARRIVAL, simTime, self.sendTo, simTime)  #Send new cusomer to queue
            send(GENERATE, self.arrivalTime(), self, [])  #Schedule next arrival
            self.arrivalTimes.append(simTime)


class queue(larger):
    def __init__(self, mu, sendTo):
        self.numberInQueue = 0
        self.sumMeasurements = 0
        self.numberOfMeasurements = 0
        self.measuredValues = []
        self.buffer = Queue(maxsize=0)
        self.mu = mu 
        self.sendTo = sendTo
    def serviceTime(self):
        return simTime + random.expovariate(self.mu)    #this is where the serive time is decided
    def treatSignal(self, x, info):
        if x == ARRIVAL:
            if self.numberInQueue == 0:
                # this is where the service time is set for the task
                send(DEPARTURE,self.serviceTime() , self, []) #Schedule  a departure for the arrival customer if queue is empty
            self.numberInQueue = self.numberInQueue + 1
            self.buffer.put(info)
        elif x == DEPARTURE:
            self.numberInQueue = self.numberInQueue - 1
            if self.numberInQueue > 0:
                send(DEPARTURE, self.serviceTime(), self, [])  # Schedule  a departure for next customer in queue
            send(ARRIVAL, simTime, self.sendTo, self.buffer.get())
        elif x == MEASUREMENT:
            self.measuredValues.append(self.numberInQueue)
            self.sumMeasurements = self.sumMeasurements + self.numberInQueue
            self.numberOfMeasurements = self.numberOfMeasurements + 1
            send(MEASUREMENT, simTime + random.expovariate(1), self, [])



class sink(larger):
    def __init__(self):
        self.numberArrived = 0
        self.departureTimes = []
        self.totalTime = 0
        self.T = []
    def treatSignal(self, x, info):
        self.numberArrived = self.numberArrived + 1
        self.departureTimes.append(info)
        self.totalTime = self.totalTime + simTime - info
        self.T.append(simTime - info)

          
  ###################################################
  #
  # Add code to create a queuing system  here
  #
  ###################################################

sink = sink()
queue = queue(10, sink)
generator = generator(queue, 7)

send(GENERATE, 0, generator, [])
send(MEASUREMENT, 0.0, queue, [])

while simTime < stopTime:
    print(simTime) 
    [simTime, signalType, dest, info] = heapq.heappop(signalList)
    dest.treatSignal(signalType, info)


# Plot the number of customers in the system
plt.plot(queue.measuredValues)
plt.show()

# Questions
# how many servers are there?
# there is one server in the system. The queue class places the arrivals in
# the queue every time except for when the queue is empty and the server is free.

# how many places does the buffer have?
# The buffer has infinite places. 
#
# self.buffer = Queue(maxsize=0)
#
# when the maxsize in Queue is set to 0, the buffer has infinite places.

# what is the mean time between arrivals?
# answer: it is lambda

# What is the list arrivalTimes used for?
# answer: it is used to keep track of the arrival times of the customers.

# What does the list T contain after the simulation run?
# answer: The list T contains the time each customer spent in the system.

# What does the list measuredValues contain after the simulation run?
# answer: The list measuredValues contains the number of customers in the system at each measurement point.




  ###################################################
  #
  # Add code to print final result
  #
  ###################################################

import heapq
import random
import numpy as np
from queue import Queue
import time

#import matplotlib as mpl
#mpl.use('tkagg')
import matplotlib.pyplot as plt

signalList = []

def send(signalType, evTime, destination, info):
    heapq.heappush(signalList, (evTime, signalType, destination, info))

GENERATE = 1
ARRIVAL = 2
MEASUREMENT = 3
DEPARTURE = 4
        
class larger():
    def __gt__(self, other):
        return False


class generator(larger):
    def __init__(self, sendTo,lambda1):
        self.sendTo = sendTo
        self.lambda1 = lambda1
        self.arrivalTimes = []
    def arrivalTime(self):
        return simTime + random.expovariate(self.lambda1)
        # return simTime + 1.0
    def treatSignal(self, x, info):
        if x == GENERATE:
            send(ARRIVAL, simTime, self.sendTo, simTime)
            send(GENERATE, self.arrivalTime(), self, [])
            self.arrivalTimes.append(simTime)


class queue(larger):
    def __init__(self, mu, L, sendTo1,sendTo2,alpha,s):
        self.numberInQueue = 0
        self.sumMeasurements = 0
        self.numberOfMeasurements = 0
        self.measuredValues = []
        self.arrivalTimes = []
        self.Nq = []    # Number of customers in the queue
        self.Ts = []    # Service time
        self.buffer = Queue(maxsize=0)
        self.mu = mu 
        self.L = L
        self.alpha = alpha
        self.sendTo1 = sendTo1
        self.sendTo2 = sendTo2
        self.s = s

    def serviceTime(self):
        # return simTime + (1 / self.mu)
        # return simTime + random.expovariate(self.mu)
        mu1 = 2*self.mu
        mu2 = self.mu/2
        if random.random() < (1/1.5):
            return simTime + random.expovariate(mu1)
        else:
            return simTime + random.expovariate(mu2)
        # return simTime + 1.0
    def treatSignal(self, x, info):
        if x == ARRIVAL:
            if self.numberInQueue < self.L:
                if self.numberInQueue == 0:
                    send(DEPARTURE, self.serviceTime(), self, []) #Schedule  a departure for the arrival customer if queue is empty
                self.numberInQueue = self.numberInQueue + 1
                self.buffer.put(info)
                self.arrivalTimes.append(simTime)

        elif x == DEPARTURE:
            self.numberInQueue = self.numberInQueue - 1
            if self.numberInQueue > 0:
                time = self.serviceTime()
                #self.Ts.append(time - simTime)    # detta lade jag till för att mäta service tiden
                send(DEPARTURE,  time, self, [])  # Schedule  a departure for next customer
            tid = self.buffer.get()
            if random.uniform(0, 1) <= self.alpha :
               if self.sendTo1:
                  send(ARRIVAL, simTime, self.sendTo1, tid)
               send(ARRIVAL, simTime, self.s, tid)
            else : # rand >= self.alpha:
                if self.sendTo2:
                    send(ARRIVAL, simTime, self.sendTo2, tid) 
                # self.Ts.append(simTime - tid - (1 / self.mu))
                self.Ts.append(simTime - tid)
                send(ARRIVAL, simTime, self.s, tid)


        elif x == MEASUREMENT:
            self.measuredValues.append(self.numberInQueue)
            self.sumMeasurements = self.sumMeasurements + self.numberInQueue
            self.numberOfMeasurements = self.numberOfMeasurements + 1
            self.Nq.append(self.numberInQueue)      # lade till denna rad för att mäta antalet kunder i kön
            send(MEASUREMENT, simTime + random.expovariate(1), self, [])

            
class sink(larger):
    def __init__(self):
        self.numberArrived = 0
        self.departureTimes = []
        self.totalTime = 0
        self.T = [] # Total time since the customer arrived to queuing network
    def treatSignal(self, x, info):
        self.numberArrived = self.numberArrived + 1
        self.departureTimes.append(info)
        self.totalTime = self.totalTime + simTime - info
        self.T.append(simTime - info)






# Parameters are given values
[ lambda1,lambda2] = [7.5, 10]  #Arrival rate  
[mu1,mu2,mu3,mu4,mu5] = [10, 14, 22, 9, 11]     # Service rate
[L1,L2,L3,L4,L5] = [np.inf, np.inf, np.inf, np.inf, np.inf]    
# [L1,L2,L3,L4,L5] = [4, 10, 3, 20, 7] 
alpha = 0.4

simTime = 0.0
stopTime = 1000.0
bufferSize = 4
          
sink = sink()

queue4 = queue(mu4, alpha=alpha, L=L4, s=sink, sendTo1=None, sendTo2=None)
queue5 = queue(mu5, alpha=alpha, L=L5, s=sink, sendTo1=None, sendTo2=None)
queue3 = queue(mu3, alpha=alpha, L=L3, s=sink, sendTo1=queue4, sendTo2=queue5)
queue1 = queue(mu1, alpha=alpha, L=L1, s=queue3, sendTo1=None, sendTo2=None)
queue2 = queue(mu2, alpha=alpha, L=L2, s=queue3, sendTo1=None, sendTo2=None)
    

generatorA = generator(queue1, lambda1)
generatorB = generator(queue2, lambda2)

send(GENERATE, 0, generatorA, [])
send(GENERATE, 0, generatorB, [])

send(MEASUREMENT, 0.0, queue1, [])
send(MEASUREMENT, 0.0, queue2, [])
send(MEASUREMENT, 0.0, queue3, [])
send(MEASUREMENT, 0.0, queue4, [])
send(MEASUREMENT, 0.0, queue5, [])




while simTime < stopTime:
    [simTime, signalType, dest, info] = heapq.heappop(signalList)
    dest.treatSignal(signalType, info)


print("tid ", np.mean(queue5.Ts), "antal ", np.mean(queue5.Nq))
print("totaltime: ", np.mean(sink.T))
  ###################################################
  #
  # Add code to print final result
  #
  ###################################################
  
# Uncomment the code below to se histograms of the number of customers in all the
# queues in the queueing network
  
# ypoints1 = np.array(q1.measuredValues)
# ypoints2 = np.array(q2.measuredValues)
# ypoints3 = np.array(q3.measuredValues)
# ypoints4 = np.array(q4.measuredValues)
# ypoints5 = np.array(q5.measuredValues)


# end = int(np.min([np.max([L1,L2,L3,L4,L5])+5,100]))
# plt.figure()
# a = a_list = list(range(0, end))
# plt.subplot(231)
# plt.hist(ypoints1, bins = a, density = True)
# plt.title('Queue 1')
# plt.subplot(232)
# plt.hist(ypoints2, bins = a, density = True)
# plt.title('Queue 2')
# plt.subplot(233)
# plt.hist(ypoints3, bins = a, density = True)
# plt.title('Queue 3')
# plt.subplot(234)
# plt.hist(ypoints4, bins = a, density = True)
# plt.title('Queue 4')
# plt.subplot(235)
# plt.hist(ypoints5, bins = a, density = True)
# plt.title('Queue 5')
# plt.show()


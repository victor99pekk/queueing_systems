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
        self.totCounter = 0
        self.blockCounter = 0
    def serviceTime(self):
        return simTime + random.expovariate(self.mu)   #this is where the serive time is decided
    def treatSignal(self, x, info):
        self.totCounter +=1
        if x == ARRIVAL:
            if self.numberInQueue == 0:
                # this is where the service time is set for the task
                send(DEPARTURE,self.serviceTime() , self, []) #Schedule  a departure for the arrival customer if queue is empty
            if self.numberInQueue >= 6:
                self.blockCounter += 1
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


simTime = 0.0
stopTime = 1000.0

sink = sink()
queue = queue(10, sink)
generator = generator(queue, 11)

send(GENERATE, 0, generator, [])
send(MEASUREMENT, 0.0, queue, [])

while simTime < stopTime:
    [simTime, signalType, dest, info] = heapq.heappop(signalList)
    dest.treatSignal(signalType, info)


# Plot the number of customers in the system
# print("response: ", np.mean(sink.T),"\nmean queue length: ", np.mean(queue.measuredValues))
#plt.hist(sink.T, bins='auto')  # 'auto' automatically determines the number of bins
# x_values = [0.25, 0.5, 0.7, 0.9, 1, 1.1]
# y_values = [0.13, 0.19, 0.34, 0.84, 2.78, 58]

# plt.plot(x_values, y_values)
# plt.ylim(0, 30)

#plt.plot(sink.T[2:101],sink.T[1:100],'*')

# plt.plot(queue.measuredValues)
# plt.hist(queue.measuredValues, bins='auto')  # 'auto' automatically determines the number of bins

plt.hist(queue.measuredValues, bins='auto', density=True)  # 'auto' automatically determines the number of bins, density=True normalizes the histogram


# lambda1 = float(input('Arrival rate (lambda): '))
# mu = float(input('Service rate (mu): '))
# maxK = int(input('Maximum k value to plot: '))


# k =  np.array([i for i in range(0,maxK)])
# rho = lambda1/mu
# pk = pow(rho,k)*(1-rho)




# plt.plot(k,pk,'-') 



plt.show()

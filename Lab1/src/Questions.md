
# Questions, Laboration 1

### Q1: how many servers are there?
- there is one server in the system. The queue class places the arrivals in
the queue every time except for when the queue is empty and the server is free.

### Q2: how many places does the buffer have?
- The buffer has infinite places. when the maxsize in Queue is set to 0, the buffer has infinite places.

```py
self.buffer = Queue(maxsize=0)
```
### Q3: what is the mean time between arrivals?
- it is lambda

### Q4: What is the list arrivalTimes used for?
- it is used to keep track of the arrival times of the customers.

### Q5: What does the list T contain after the simulation run?
- The list T contains the time each customer spent in the system.

### Q6: What does the list measuredValues contain after the simulation run?
- The list measuredValues contains the number of customers in the system at each measurement point.

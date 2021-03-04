#!/usr/bin/python3
import sched
import time
from threading import Timer
from copy import deepcopy


class Frame:
    source = ''

    def __init__(self, deadline, priority, arrive_time, transmission_time, period, source):
        self.deadline = deadline
        self.priority = priority
        self.arrive_time = arrive_time
        self.window_time = transmission_time + 2  # time for guard band is 2 time unit
        self.transmission_time = transmission_time
        self.period = period
        self.source = source


def periodic_Generator(traffic, period, stream):
    traffic = deepcopy(traffic)
    traffic.arrive_time += period
    traffic.deadline = traffic.arrive_time + period
    stream.append(traffic)
    # print("arrive_time and deadline: ", stream[len(stream) - 1].source, stream[len(stream) - 1].arrive_time,
    #      stream[len(stream) - 1].deadline)
    if traffic.arrive_time < 100:
        periodic_Generator(traffic, period, stream)


if __name__ == "__main__":
    print("start traffic generation")
    ST1 = Frame(0, 0, 0, 1, 5, 'ECU1')
    stream1 = [ST1]
    periodic_Generator(ST1, ST1.period, stream1)

    for i in stream1:
        print(i.arrive_time, i.deadline, i.source)

    ST2 = Frame(0, 0, 0, 4, 8, 'ECU2')
    stream2 = [ST2]
    periodic_Generator(ST2, ST2.period, stream2)
    for i in stream2:
        print(i.arrive_time, i.deadline, i.source)

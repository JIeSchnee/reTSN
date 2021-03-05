#!/usr/bin/python3
import sched
import time
import numpy as np
from threading import Timer
from copy import deepcopy


class Frame:
    def __init__(self, frame_Id, deadline, priority, arrive_time, transmission_time, period, source):
        self.frame_id = frame_Id
        self.deadline = deadline
        self.priority = priority
        self.arrive_time = arrive_time
        self.window_time = transmission_time + 2  # time for guard band is 2 time unit
        self.transmission_time = transmission_time
        self.period = period
        self.source = source


def periodicFrame_Generator(traffic, stream):
    traffic = deepcopy(traffic)
    traffic.frame_id += 1
    traffic.arrive_time += traffic.period
    traffic.deadline = traffic.arrive_time + traffic.period
    stream.append(traffic)
    # print("arrive_time and deadline: ", stream[len(stream) - 1].source, stream[len(stream) - 1].arrive_time,
    #       stream[len(stream) - 1].deadline)
    if traffic.arrive_time < 100:
        periodicFrame_Generator(traffic, stream)


def system_periodic_streams_Generator(period, transmission_time):
    system_periodic_streams = []
    for i in range(len(period)):
        frame_id = 0
        frame_init = Frame(frame_id, 0, 0, 0, transmission_time[i], period[i], i)
        # print(frame_init.frame_id, frame_init.source, frame_init.transmission_time, frame_init.period)
        stream = [frame_init]
        periodicFrame_Generator(frame_init, stream)
        # for j in stream:
        #     print(j.frame_id, j.source, j.arrive_time, j.period)
        system_periodic_streams.append(stream)
    return system_periodic_streams


if __name__ == "__main__":
    print("start traffic generation")
    period = [4, 8, 16, 32]
    transmission_time = [1, 2, 4, 8]
    system_periodic_streams = system_periodic_streams_Generator(period, transmission_time)
    for j in range(len(system_periodic_streams)):
        print(len(system_periodic_streams[j]))
    for i in system_periodic_streams:
        for k in i:
            print(k.source, k.frame_id, k.arrive_time, k.deadline, k.period, k.transmission_time, k.window_time)


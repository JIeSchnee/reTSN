#!/usr/bin/python3

# import sched
# import time

# from threading import Timer
import numpy as np
import random
import math
from copy import deepcopy


class Frame:
    critical_level = ''

    def __init__(self, frame_Id, deadline, priority, arrive_time, transmission_time, period, source, critical_level):
        self.frame_id = frame_Id
        self.deadline = deadline
        self.priority = priority
        self.arrive_time = arrive_time
        self.window_time = transmission_time + 2  # time for guard band is 2 time unit
        self.transmission_time = transmission_time
        self.period = period
        self.source = source
        self.source = critical_level


def period_Generator(stream_number, generated_transmission_times):
    utilizations = uunifast(stream_number)
    # for j in range(len(utilizations)):
    #     print(utilizations[j])

    generated_period = []
    for j in range(stream_number):
        generated_period.append(math.ceil(generated_transmission_times[j] / utilizations[j]))

    # test the total utilization will not exist 1 after ceiling operation
    uti = []
    for i in range(stream_number):
        uti.append(generated_transmission_times[i] / generated_period[i])
    b = sum(uti)
    print(b)

    return generated_period


def uunifast(stream_number):
    sum_utilization = 1
    utilizations = []

    for i in range(1, stream_number):
        nextSumU = sum_utilization * random.uniform(0, 1) ** (1.0 / (stream_number - i))
        utilizations.append(sum_utilization - nextSumU)
        sum_utilization = nextSumU

    utilizations.append(sum_utilization)
    return utilizations


def periodicFrame_Generator(traffic, stream, time_duration):
    traffic = deepcopy(traffic)
    traffic.frame_id += 1
    traffic.arrive_time += traffic.period
    traffic.deadline = traffic.arrive_time + traffic.period
    stream.append(traffic)
    # print("arrive_time and deadline: ", stream[len(stream) - 1].source, stream[len(stream) - 1].arrive_time,
    #       stream[len(stream) - 1].deadline)

    if traffic.arrive_time < time_duration:
        periodicFrame_Generator(traffic, stream, time_duration)


def system_periodic_streams_Generator(period, transmission_time, offset, time_duration):
    system_periodic_streams = []
    critical_definition = []
    for i in range(len(period)):
        frame_id = 0
        frame_init = Frame(frame_id, offset[i] + period[i], 0, offset[i], transmission_time[i], period[i], i,
                           "not_identified")
        # print(frame_init.frame_id, frame_init.source, frame_init.transmission_time, frame_init.period)

        if period[i] <= 10:
            frame_init.critical_level = "safety_critical"
        if period[i] > 10 & period[i] <= 100:
            frame_init.critical_level = "critical"
        if period[i] > 100:
            frame_init.critical_level = "non_critical"

        stream = [frame_init]
        periodicFrame_Generator(frame_init, stream, time_duration)
        # for j in stream:
        #     print(j.frame_id, j.source, j.arrive_time, j.period)
        system_periodic_streams.append(stream)

    return system_periodic_streams


def sporadic_stream_Generator(time_duration):
    frame_id = 0
    arrive_time = random.randint(0, 100)
    transmission_time = random.randint(1, 8)
    period = random.randint(transmission_time, 32)
    deadline = arrive_time + period
    # print(arrive_time, transmission_time, period)
    frame_init = Frame(frame_id, deadline, 0, arrive_time, transmission_time, period, 256, "sporadic")
    # frame_Id, deadline, priority, arrive_time, transmission_time, period, source
    stream = [frame_init]
    periodicFrame_Generator(frame_init, stream, time_duration)
    return stream


def aperiodic_stream_Generator():
    aperiodic_stream = Frame(0, 1000, 1000, random.randint(0, 100), random.randint(1, 8), 0, 255, "aperiodic")
    # frame_Id, deadline, priority, arrive_time, transmission_time, period, source
    # print(aperiodic_stream.arrive_time, aperiodic_stream.transmission_time)
    return aperiodic_stream


def triggered_stream_Selection(triggerSignal, time_duration):
    global signal
    if triggerSignal == 1:
        signal = sporadic_stream_Generator(time_duration)
    elif triggerSignal == 0:
        signal = aperiodic_stream_Generator()
    return signal


if __name__ == "__main__":
    print("start traffic generation")

    # period generation
    stream_number = 10
    generated_transmission_times = np.random.randint(low=1, high=5, size=(stream_number))
    print(generated_transmission_times)
    generated_period = period_Generator(stream_number, generated_transmission_times)
    print(generated_period)
    # period = [4, 8, 16, 32]
    # transmission_time = [1, 2, 4, 8]

    # periodic streams generation
    period = generated_period
    transmission_time = generated_transmission_times
    offset = np.zeros(stream_number, dtype=int)
    time_duration = 200
    system_periodic_streams = system_periodic_streams_Generator(period, transmission_time, offset, time_duration)
    # for j in range(len(system_periodic_streams)):
    #     print(len(system_periodic_streams[j]))
    for i in system_periodic_streams:
        for k in i:
            print("system_periodic_streams:", "source", k.source, "frame_id", k.frame_id, "arrive_time", k.arrive_time,
                  "deadline", k.deadline, "period", k.period, "transmission_time", k.transmission_time, "window_time",
                  k.window_time, "critical_level:", k.critical_level)

    # aperiodic and sporadic traffic generation
    triggerSignal = 0  # 0: aperiodic traffic  1: sporadic traffic with minimal interval
    triggered_stream = triggered_stream_Selection(triggerSignal, time_duration)

    if triggerSignal == 0:
        print("aperiodic_traffic:", triggered_stream.source, triggered_stream.frame_id, triggered_stream.arrive_time,
              triggered_stream.deadline, triggered_stream.period, triggered_stream.transmission_time,
              triggered_stream.window_time, triggered_stream.critical_level)
    elif triggerSignal == 1:
        for k in triggered_stream:
            print("sporadic_traffic:", k.source, k.frame_id, k.arrive_time, k.deadline, k.period, k.transmission_time,
                  k.window_time, k.critical_level)

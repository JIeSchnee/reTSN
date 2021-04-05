#!/usr/bin/python3

import numpy as np
import random
import math
from copy import deepcopy


class Frame:
    critical_level = ''

    def __init__(self, frame_Id, fragment_Id, deadline, priority, arrive_time, window_times, period, source,
                 destination, critical_level):
        self.frame_id = frame_Id
        self.fragment_Id = fragment_Id
        self.deadline = deadline
        self.priority = priority
        self.arrive_time = arrive_time
        self.window_time = window_times
        self.transmission_time = window_times - 2  # time for guard band is 2 time unit
        self.period = period
        self.source = source
        self.destination = destination
        self.critical_level = critical_level


class schedule:
    def __init__(self, source, destination, frame_Id, fragment_Id, start_time, end_time):
        self.source = source
        self.destination = destination
        self.frame_Id = frame_Id
        self.fragment_Id = fragment_Id
        self.start_time = start_time
        self.end_time = end_time


def hyper_period_calculation(period):
    hyper_period = period[0]
    for i in range(1, len(period)):
        hyper_period = hyper_period * period[i] // math.gcd(hyper_period, period[i])

    return hyper_period


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


def window_time_Generator(stream_number, period):
    utilizations = uunifast(stream_number)

    # for j in range(len(utilizations)):
    #     print(utilizations[j])

    generated_window_times = np.multiply(np.array(utilizations), np.array(period)).astype(np.int)
    # print(generated_transmission_times)
    for i in range(len(generated_window_times)):
        if generated_window_times[i] < 1:
            generated_window_times[i] = 1
        elif generated_window_times[i] >= 1:
            generated_window_times[i] = round(generated_window_times[i])
    # print(generated_transmission_times)

    return generated_window_times


def uunifast(stream_number):
    sum_utilization = 0.5
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

    if traffic.deadline < time_duration:
        periodicFrame_Generator(traffic, stream, time_duration)


def system_periodic_streams_Generator(period, window_times, offset, time_duration):
    system_periodic_streams = []

    for i in range(len(period)):
        frame_id = 0
        # offset[i] = random.randint(0, period[i] - window_times[i])
        # print(offset[i])
        frame_init = Frame(frame_id, 0, offset[i] + period[i], 0, offset[i], window_times[i], period[i], i, 0,
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
    frame_init = Frame(frame_id, 0, deadline, 0, arrive_time, transmission_time, period, 256, 0, "sporadic")
    # frame_Id, fragment_Id, deadline, priority, arrive_time, window_times, period, source, destination, critical_level
    # for sporadic frames window_time = transmission_time
    stream = [frame_init]
    periodicFrame_Generator(frame_init, stream, time_duration)
    return stream


def aperiodic_stream_Generator():
    aperiodic_stream = Frame(0, 1000, 0, 1000, random.randint(0, 100), random.randint(1, 8), 0, 255, 0, "aperiodic")
    # frame_Id, fragment_Id, deadline, priority, arrive_time, window_times, period, source, destination, critical_level
    # for aperiodic frames window_time = transmission_time
    # print(aperiodic_stream.arrive_time, aperiodic_stream.transmission_time)
    return aperiodic_stream


def triggered_stream_Selection(triggerSignal, time_duration):
    global signal
    if triggerSignal == 1:
        signal = sporadic_stream_Generator(time_duration)
    elif triggerSignal == 0:
        signal = aperiodic_stream_Generator()
    return signal


def EDF_Scheduling(system_periodic_streams, period, window_times, hyper_period):
    global offline_schedule
    offline_schedule = []
    offset = []
    release_times = []
    current_period = []
    source = []
    destination = []
    frame_id = []
    fragment_id = []
    remain_time = []
    count = 0
    preemption_overhead = 2.3  # gard band and real preemption overhead
    for i in range(len(window_times)):
        remain_time.append(window_times[i])

    for i in system_periodic_streams:
        release = i[0].arrive_time
        offset.append(release)
        current_period.append(1)
        source.append(i[0].source)
        destination.append(i[0].destination)
        frame_id.append(0)
        fragment_id.append(0)
    # print("stream release time:", release_times)
    # print("stream period:", period)
    # print(source)
    # print(destination)

    for i in range(len(offset)):
        release_times.append(offset[i])

    current_time = min(release_times)
    # print("current_time:", current_time)

    # earliest_index = deadline.index(min(deadline))
    # print("index:", earliest_index)

    while current_time < hyper_period:
        print("-----------------------------------------------------------------------------------------------------")
        print("current time:", current_time)
        print("current period:", current_period)
        print("window:", window_times)
        print("remain:", remain_time)
        print("release time:", release_times)
        deadline = [a + b * c for a, b, c in zip(offset, period, current_period)]
        earliest_index = deadline.index(min(deadline))
        print("update deadlines:", deadline)

        if current_time < offset[earliest_index] + period[earliest_index] * (current_period[earliest_index] - 1):
            temp_list = [a + b * c for a, b, c in zip(offset, period, current_period)]
            current_period_p = offset[earliest_index] + period[earliest_index] * (
                    current_period[earliest_index] - 1)
            # print("current_p", current_period_p)

            k = True
            while k:
                #print("deadline need to be modified")
                temp_list[earliest_index] = 10000
                earliest_index = temp_list.index(min(temp_list))
                if current_time >= release_times[earliest_index]:
                    k = False

            if remain_time[earliest_index] <= current_period_p - current_time:
                print("schedule from part 1")
                running_time = remain_time[earliest_index]
                remain_time[earliest_index] -= running_time
                count += running_time
                # offline_schedule = offline_schedule.append(sche)
                # source, destination, frame_Id, fragment_Id, start_time, end_time

            else:
                print("schedule from part 2")
                running_time = current_period_p - current_time

                if remain_time[earliest_index] <= 2:
                    running_time = remain_time[earliest_index]
                    remain_time[earliest_index] -= running_time
                    count += running_time
                else:
                    running_time = current_period_p - current_time + 2
                    remain_time[earliest_index] = remain_time[earliest_index] - running_time + preemption_overhead
                    count += running_time
                    # print(current_period_p, round(remain_time[earliest_index], 2), round(running_time, 2),
                    #       preemption_overhead)
                    print("remain_fragment:", remain_time)

            sche = schedule(source[earliest_index], destination[earliest_index], frame_id[earliest_index],
                            fragment_id[earliest_index], current_time,
                            current_time + running_time)
            offline_schedule.append(sche)
            print("---- schedule--- source | frame_id | fragment_id | start time | end time")
            print(sche.source, sche.frame_Id, sche.fragment_Id, sche.start_time, sche.end_time)
            fragment_id[earliest_index] += 1
            current_time += running_time
            if remain_time[earliest_index] == 0:
                remain_time[earliest_index] = window_times[earliest_index]
                current_period[earliest_index] += 1
                release_times[earliest_index] += period[earliest_index]
                frame_id[earliest_index] += 1
                fragment_id[earliest_index] = 0
                # print("remain_update:", remain_time)
            if current_time < min(release_times):
                current_time = min(release_times)

        else:
            current_period_p = offset[earliest_index] + period[earliest_index] * current_period[earliest_index]
            print("current_p", current_period_p)
            if remain_time[earliest_index] <= current_period_p - current_time:
                print("schedule from part 3")
                running_time = remain_time[earliest_index]
                remain_time[earliest_index] -= running_time
                count += running_time
            else:
                print("schedule from part 4")
                running_time = current_period_p - current_time
                if remain_time[earliest_index] <= 2:
                    running_time = remain_time[earliest_index]
                    remain_time[earliest_index] -= running_time
                    count += running_time
                else:
                    running_time = current_period_p - current_time + 2
                    remain_time[earliest_index] = remain_time[earliest_index] - running_time + preemption_overhead
                    count += running_time
                    # print(current_period_p, round(remain_time[earliest_index], 2), round(running_time, 2),
                    #       preemption_overhead)
                    print("remain_fragment:", remain_time)

                # print("remain_update:", remain_time)
            sche = schedule(source[earliest_index], destination[earliest_index], frame_id[earliest_index],
                            fragment_id[earliest_index], current_time,
                            current_time + running_time)
            offline_schedule.append(sche)
            print("---- schedule--- source | frame_id | fragment_id | start time | end time")
            print(sche.source, sche.frame_Id, sche.fragment_Id, sche.start_time, sche.end_time)
            fragment_id[earliest_index] += 1
            current_time += running_time
            if remain_time[earliest_index] == 0:
                remain_time[earliest_index] = window_times[earliest_index]
                current_period[earliest_index] += 1
                release_times[earliest_index] += period[earliest_index]
                frame_id[earliest_index] += 1
                fragment_id[earliest_index] = 0
                # print("remain_update:", remain_time)

            if current_time < min(release_times):
                current_time = min(release_times)
            # print("frame id", frame_id)
            original_total_transmission_time = sum([b * c for b, c in zip(window_times, frame_id)])
            print("original_total_transmission_time and uti: ", original_total_transmission_time, "|", original_total_transmission_time / hyper_period)
            print("actual_total_transmission_time and uti:", count, "|", count / hyper_period)
            if count / hyper_period > 0.5:
                print("$______________warning________________$")
            if count / hyper_period > 1:
                print("$______________Error_______________$")
                exit()

    return offline_schedule


if __name__ == "__main__":
    print("start traffic generation")

    # period generation
    stream_number = 5

    # generated_transmission_times = np.random.randint(low=1, high=5, size=(stream_number))
    # print(generated_transmission_times)
    # generated_period = period_Generator(stream_number, generated_transmission_times)
    # print(generated_period)

    # period_set = [40, 80, 160, 320, 640, 1280, 2560]
    period_set = [50, 100, 200, 500, 1000]
    # period_set = [10, 20, 30, 60]
    idxs = np.random.randint(0, len(period_set), size=stream_number)
    # print(idxs)
    period = []
    for i in idxs:
        period.append(period_set[i])
    # print(period)
    # transmission_time = [1, 2, 4, 8]
    # periodic streams generation
    # period = generated_period
    k = True
    while k:
        window_times = window_time_Generator(stream_number, period)

        uti = []
        for i in range(stream_number):
            uti.append(window_times[i] / period[i])
        new_utilization = sum(uti)
        if new_utilization < 0.5 and min(window_times) >= 3:
            k = False

    print("window_time:", window_times)
    print("utilization:", new_utilization)
    hyper_period = hyper_period_calculation(period)
    print(hyper_period)
    time_duration = hyper_period

    offset = np.zeros(stream_number, dtype=int)

    system_periodic_streams = system_periodic_streams_Generator(period, window_times, offset, time_duration)
    # for j in range(len(system_periodic_streams)):
    #     print(len(system_periodic_streams[j]))
    # for i in system_periodic_streams:
    #     for k in i:
    #         print("system_periodic_streams:", "|source:", k.source, "|destination:", k.destination, "|frame_id:",
    #               k.frame_id, "|arrive_time:", k.arrive_time,
    #               "|deadline:", k.deadline, "|period:", k.period, "|transmission_time:", k.transmission_time,
    #               "|window_time:",
    #               k.window_time)
    # -------------------------------------------------------------------------#
    #                            EDF schedule generation                       #
    # -------------------------------------------------------------------------#

    offline_schedule = EDF_Scheduling(system_periodic_streams, period, window_times, hyper_period)
    # print("-------------------- summarize ---------------------------")
    # for i in range(len(offline_schedule)):
    #     print(" source | frame_id | fragment_id | start time | end time")
    #     print(offline_schedule[i].source, offline_schedule[i].frame_Id, offline_schedule[i].fragment_Id,
    #           offline_schedule[i].start_time, offline_schedule[i].end_time)

    # -------------------------------------------------------------------------#
    #               aperiodic and sporadic traffics generation                 #
    # -------------------------------------------------------------------------#
    # aperiodic and sporadic traffic generation
    triggerSignal = 1  # 0: aperiodic traffic  1: sporadic traffic with minimal interval
    triggered_stream = triggered_stream_Selection(triggerSignal, time_duration)

    # if triggerSignal == 0:
    #     print("aperiodic_traffic:", "source:", triggered_stream.source, "destination:", triggered_stream.destination,
    #           "frame_id:", triggered_stream.frame_id, "arrive_time:", triggered_stream.arrive_time,
    #           "deadline:", triggered_stream.deadline, "period:", triggered_stream.period, "transmission_time:",
    #           triggered_stream.transmission_time, "window_time:",
    #           triggered_stream.window_time)
    # elif triggerSignal == 1:
    #     for k in triggered_stream:
    #         print("sporadic_traffic:", "source:", k.source, "destination:", k.destination, "frame_id:", k.frame_id,
    #               "arrive_time:", k.arrive_time,
    #               "deadline:", k.deadline, "period:", k.period, "transmission_time:", k.transmission_time,
    #               "window_time:",
    #               k.window_time)

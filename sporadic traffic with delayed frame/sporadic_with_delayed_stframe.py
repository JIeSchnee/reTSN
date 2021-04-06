import numpy as np
import random
import math
from random import choice

import sys
from prettytable import PrettyTable


class schedule:
    def __init__(self, source, destination, frame_Id, fragment_Id, start_time, end_time, deadline):
        self.source = source
        self.destination = destination
        self.frame_Id = frame_Id
        self.fragment_Id = fragment_Id
        self.start_time = start_time
        self.end_time = end_time
        self.deadline = deadline


class sporadic_frame:
    def __init__(self, arrive_time, min_interval, transmission_time):
        self.arrive_time = arrive_time
        self.min_interval = min_interval
        self.transmission_time = transmission_time


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


def active_interference_delayed(offline_schedule, interference, release_time, transmission_time, deadline,
                                preemptable_flow, temp_retranse_frame, temp_retranse_deadline, temp_sched_check, delayed_sche_id):
    # print("------------ interference from active --------------")
    pure_preemption_overhead = 0.3
    for i in range(len(offline_schedule)):
        # interference of active periodic traffic
        if offline_schedule[i].start_time < release_time < offline_schedule[i].end_time:
            if i == delayed_sche_id:
                interference += 0
                # print("delayed frame is released within its offline scheduled time")
            else:
                if offline_schedule[i].source == preemptable_flow:
                    # need to check if the active frame belongs to preempable flow
                    if offline_schedule[i].deadline < deadline:
                        interference += offline_schedule[i].end_time - release_time
                    else:
                        if offline_schedule[i].end_time - release_time > 2:
                            if release_time + interference + transmission_time + offline_schedule[
                                i].end_time - release_time > offline_schedule[i].deadline:
                                interference += offline_schedule[i].end_time - release_time
                                print("the preemptable frame can not be preempted")
                            else:

                                interference += 1
                                print("blocked by preemptable one with lower priority and offline schedule will be updated",
                                      offline_schedule[i].start_time, offline_schedule[i].end_time, interference)
                                # TODO calculate the response time of offline_schedule[i]
                                temp_retranse_remain = (offline_schedule[i].end_time - release_time + 1) + 0.3

                                if abs(temp_retranse_remain - offline_schedule[i].end_time + offline_schedule[
                                    i].start_time) < 2:
                                    temp_retranse_remain = offline_schedule[i].end_time - offline_schedule[i].start_time - 2

                                # if temp_retranse_remain > offline_schedule[i].end_time - \
                                #         offline_schedule[i].start_time - 2:
                                #     temp_retranse_remain = offline_schedule[i].end_time - \
                                #                            offline_schedule[i].start_time - 2
                                temp_retranse_remain_deadline = offline_schedule[i].deadline

                                if temp_retranse_remain > 0:
                                    temp_retranse_frame.append(temp_retranse_remain)
                                    temp_retranse_deadline.append(temp_retranse_remain_deadline)
                                    temp_sched_check.append(i)

                        else:
                            interference += offline_schedule[i].end_time - release_time
                else:
                    # include the block by the st non preemptable frame.
                    interference += offline_schedule[i].end_time - release_time

                print("interference of active one:", offline_schedule[i].start_time,
                      offline_schedule[i].end_time, interference)

    return interference, temp_retranse_frame, temp_retranse_deadline, temp_sched_check


def future_interference_delayed(offline_schedule, interference, release_time, transmission_time, deadline,
                                preemptable_flow, temp_retranse_frame, temp_retranse_deadline, temp_sched_check, delayed_sche_id):
    # print("---------------- interference from future (accumulate) ----------------")
    pure_preemption_overhead = 0.3

    temp_compare = release_time + interference + transmission_time
    for i in range(len(offline_schedule)):
        # interference of the period traffic coming in the future
        if release_time <= offline_schedule[i].start_time < deadline:
            if i == delayed_sche_id:
                interference += 0
                # print("The frame is delayed frame, time slot assigned to sporadic:", offline_schedule[i].start_time,
                #       offline_schedule[i].end_time)
            else:
                if release_time + interference + transmission_time - offline_schedule[i].start_time <= 2:
                    interference += 0
                else:
                    if offline_schedule[i].source == preemptable_flow:

                        if offline_schedule[i].deadline < deadline:

                            if offline_schedule[i].start_time - temp_compare > 0:
                                if release_time + interference + transmission_time - offline_schedule[i].start_time <= 2:
                                    interference += 0
                                else:
                                    interference += offline_schedule[i].end_time - offline_schedule[i].start_time \
                                                    - 1 + pure_preemption_overhead
                                temp_compare = offline_schedule[i].end_time
                            else:
                                interference += offline_schedule[i].end_time - offline_schedule[i].start_time
                                temp_compare = offline_schedule[i].end_time
                            print("interference of future preemptable", offline_schedule[i].start_time,
                                  offline_schedule[i].end_time, interference)

                        else:
                            if release_time + interference + transmission_time + offline_schedule[i].end_time - \
                                    offline_schedule[
                                        i].start_time > offline_schedule[i].deadline:
                                interference += offline_schedule[i].end_time - offline_schedule[
                                    i].start_time
                                print("the preemptable frame can not be preempted")
                            else:
                                interference += 0
                                remain_transmission_time = offline_schedule[i].end_time - offline_schedule[i].start_time - 2
                                remain_transmission_deadline = offline_schedule[i].deadline
                                if remain_transmission_time > 0:
                                    temp_retranse_frame.append(remain_transmission_time)
                                    temp_retranse_deadline.append(remain_transmission_deadline)
                                    temp_sched_check.append(i)

                    else:
                        if offline_schedule[i].start_time - temp_compare > 0:
                            if release_time + interference + transmission_time - offline_schedule[i].start_time <= 2:
                                interference += 0
                            else:
                                if interference != 0:
                                    # if offline_schedule[i - 1].source == preemptable_flow:
                                    #     interference += offline_schedule[i].end_time - offline_schedule[
                                    #         i].start_time - 1 + pure_preemption_overhead
                                    # else:
                                    #     if offline_schedule[i].start_time - offline_schedule[i - 1].end_time < 1:
                                    #         interference += offline_schedule[i].end_time - offline_schedule[
                                    #             i].start_time
                                    #     else:
                                    #         interference += offline_schedule[i].end_time - offline_schedule[
                                    #             i].start_time - 1 + pure_preemption_overhead
                                    if offline_schedule[i].start_time - temp_compare < 1:
                                        interference += offline_schedule[i].end_time - offline_schedule[
                                            i].start_time
                                    else:
                                        interference += offline_schedule[i].end_time - offline_schedule[
                                            i].start_time - 1 + pure_preemption_overhead
                                else:
                                    interference += offline_schedule[i].end_time - offline_schedule[i].start_time \
                                                    - 1 + pure_preemption_overhead
                            temp_compare = offline_schedule[i].end_time
                        else:
                            interference += offline_schedule[i].end_time - offline_schedule[i].start_time
                            temp_compare = offline_schedule[i].end_time

                    print("interference of future ST", offline_schedule[i].start_time, offline_schedule[i].end_time, interference)

    return interference, temp_retranse_frame, temp_retranse_deadline, temp_sched_check


def active_frame_interference(j, offline_schedule, interference, release_time, transmission_time, deadline,
                              preemptable_flow, remain_transmission_time, remain_transmission_deadline,
                              retransmiss_st_preemptable_frames, retransmiss_st_deadline, retrans_sched_id,
                              sched_check, delayed_sche_id):
    pure_preemption_overhead = 0.3
    print("------------ interference from active --------------")
    # print(retrans_sched_id[j])
    print("interference", interference)
    for i in range(len(offline_schedule)):
        # interference of active periodic traffic
        if offline_schedule[i].start_time < release_time < offline_schedule[i].end_time:
            if i == delayed_sche_id:
                interference += 0
                print("The time slot belongs to the delayed frame in the GCL")
            else:
                if offline_schedule[i].source == preemptable_flow:
                    # need to check if the active frame belongs to preempable flow
                    if retrans_sched_id[j] == i:
                        # print("the frame is previous preempted one and is retransmitted")
                        interference += 0
                    else:
                        if offline_schedule[i].deadline < deadline:
                            interference += offline_schedule[i].end_time - release_time
                        else:
                            if offline_schedule[i].end_time - release_time > 2:
                                if release_time + interference + transmission_time + offline_schedule[i].end_time - release_time > offline_schedule[i].deadline:
                                    interference += offline_schedule[i].end_time - release_time
                                    print("the preemptable frame can not be preempted")
                                else:
                                # interference += 2
                                    interference += 1
                                    print(
                                        "blocked by preemptable one with lower priority and offline schedule will be updated")
                                    # TODO calculate the response time of offline_schedule[i]
                                    remain_transmission_time = (offline_schedule[i].end_time - offline_schedule[
                                        i].start_time)- (release_time - offline_schedule[i].start_time + 1) + 0.3

                                    if abs(remain_transmission_time - offline_schedule[i].end_time + offline_schedule[
                                        i].start_time) < 2:
                                        remain_transmission_time = offline_schedule[i].end_time - offline_schedule[
                                            i].start_time - 2

                                    # if remain_transmission_time > offline_schedule[i].end_time - \
                                    #         offline_schedule[i].start_time - 2:
                                    #     remain_transmission_time = offline_schedule[i].end_time - \
                                    #                                offline_schedule[i].start_time - 2

                                    remain_transmission_deadline = offline_schedule[i].deadline
                                    if remain_transmission_time > 0:
                                        if i not in retrans_sched_id:
                                            retransmiss_st_preemptable_frames.append(remain_transmission_time)
                                            retransmiss_st_deadline.append(remain_transmission_deadline)
                                            sched_check.append(i)

                            else:
                                interference += offline_schedule[i].end_time - release_time
                else:
                    # include the block by the st non preemptable frame.
                    interference += offline_schedule[i].end_time - release_time

            print("interference of active one with:", offline_schedule[i].start_time,
                  offline_schedule[i].end_time, interference)

    return interference, retransmiss_st_preemptable_frames, retransmiss_st_deadline, sched_check


def future_frame_interference(j, offline_schedule, interference, release_time, transmission_time, deadline,
                              preemptable_flow, remain_transmission_time, remain_transmission_deadline,
                              retransmiss_st_preemptable_frames, retransmiss_st_deadline, retrans_sched_id,
                              sched_check, delayed_sche_id):
    pure_preemption_overhead = 0.3

    print("---------------- interference from future (accumulate) ----------------")
    # print(release_time)
    # print(deadline)
    temp_compare = release_time + interference + transmission_time

    for i in range(len(offline_schedule)):
        # print("debug", interference)
        # interference of the period traffic coming in the future
        if release_time <= offline_schedule[i].start_time < deadline:
            # print("there exist future coming frame")
            if i == delayed_sche_id:
                interference += 0
                print("The frame is delayed frame, time slot assigned to sporadic:", offline_schedule[i].start_time,
                      offline_schedule[i].end_time)
            else:
                if release_time + interference + transmission_time - offline_schedule[i].start_time <= 2:
                    interference += 0
                else:
                    if offline_schedule[i].source == preemptable_flow:

                        if offline_schedule[i].deadline < deadline:

                            # if release_time - interference - transmission_time - offline_schedule[i].start_time <= 2:
                            #     interference += 0
                            # else:

                            if offline_schedule[i].start_time - temp_compare > 0:
                                if release_time + interference + transmission_time - offline_schedule[
                                    i].start_time <= 2:
                                    interference += 0
                                else:
                                    print("interference 1:", interference)
                                    interference += offline_schedule[i].end_time - offline_schedule[i].start_time \
                                                    - 1 + pure_preemption_overhead
                                temp_compare = offline_schedule[i].end_time
                            else:
                                interference += offline_schedule[i].end_time - offline_schedule[i].start_time
                                temp_compare = offline_schedule[i].end_time
                            print("interference of future preemptable", offline_schedule[i].start_time,
                                  offline_schedule[i].end_time, interference)

                        else:
                            if release_time + interference + transmission_time + offline_schedule[i].end_time - \
                                    offline_schedule[
                                        i].start_time > offline_schedule[i].deadline:
                                print("the preemptable frame can not be preempted")
                                interference += offline_schedule[i].end_time - offline_schedule[
                                    i].start_time
                            else:
                                interference += 0

                                if retrans_sched_id[j] != i:
                                    remain_transmission_time = offline_schedule[i].end_time - offline_schedule[
                                        i].start_time - 2
                                    remain_transmission_deadline = offline_schedule[i].deadline
                                    if remain_transmission_time > 0:
                                        if i not in retrans_sched_id:
                                            retransmiss_st_preemptable_frames.append(remain_transmission_time)
                                            retransmiss_st_deadline.append(remain_transmission_deadline)
                                            sched_check.append(i)

                    else:
                        if offline_schedule[i].start_time - temp_compare > 0:
                            if release_time + interference + transmission_time - offline_schedule[i].start_time <= 2:
                                interference += 0
                            else:
                                if interference != 0:
                                    # if offline_schedule[i - 1].source == preemptable_flow:
                                    #     interference += offline_schedule[i].end_time - offline_schedule[
                                    #         i].start_time - 1 + pure_preemption_overhead
                                    # else:
                                    #     if offline_schedule[i].start_time - temp_compare < 1:
                                    #         interference += offline_schedule[i].end_time - offline_schedule[
                                    #             i].start_time
                                    #     else:
                                    #         interference += offline_schedule[i].end_time - offline_schedule[
                                    #             i].start_time - 1 + pure_preemption_overhead
                                    if offline_schedule[i].start_time - temp_compare < 1:
                                        interference += offline_schedule[i].end_time - offline_schedule[
                                            i].start_time
                                    else:
                                        interference += offline_schedule[i].end_time - offline_schedule[
                                            i].start_time - 1 + pure_preemption_overhead

                                else:
                                    interference += offline_schedule[i].end_time - offline_schedule[i].start_time \
                                                    - 1 + pure_preemption_overhead

                            temp_compare = offline_schedule[i].end_time
                        else:
                            interference += offline_schedule[i].end_time - offline_schedule[i].start_time
                            temp_compare = offline_schedule[i].end_time

                        print("interference of future ST", offline_schedule[i].start_time, offline_schedule[i].end_time, interference)

    return interference, retransmiss_st_preemptable_frames, retransmiss_st_deadline, sched_check


def EDF_Scheduling(window_times, period, hyper_period):


    # window_times = [37, 48, 5, 35, 6]
    # period = [200, 200, 50, 200, 200]
    # hyper_period = 200
    current_time = 0

    current_period = []
    for i in range(len(window_times)):
        current_period.append(1)
    print("current period:", current_period)

    remain_time = []
    for i in range(len(window_times)):
        remain_time.append(window_times[i])
    print("remain_time:", remain_time)

    offset = []
    for i in range(len(window_times)):
        offset.append(0)
    print("offset:", offset)

    release_times = []
    for i in range(len(window_times)):
        release_times.append(0)
    print("release_times:", release_times)

    pure_preemption_overhead = 0.3
    preemption_overhead = 2.3

    frame_id = []
    for i in range(len(window_times)):
        frame_id.append(0)
    print("frame_id:", frame_id)

    fragment_id = []
    for i in range(len(window_times)):
        fragment_id.append(0)
    print("fragment_id:", fragment_id)

    source = []
    for i in range(len(window_times)):
        source.append(i)
    print("source:", source)

    destination = []
    for i in range(len(window_times)):
        destination.append(0)
    print("destination:", destination)

    offline_schedule = []
    count = 0




    # window_times = [23, 13, 48]
    # period = [200, 100, 200]
    # hyper_period = 200
    # current_time = 0
    # current_period = [1, 1, 1]
    # remain_time = [23, 13, 48]
    # offset = [0, 0, 0]
    # release_times = [0, 0, 0]
    # pure_preemption_overhead = 0.3
    # preemption_overhead = 2.3
    # frame_id = [0, 0, 0]
    # fragment_id = [0, 0, 0]
    # source = [0, 1, 2]
    # destination = [0, 0, 0]
    # offline_schedule = []
    # count = 0

    # 0.5
    # window_times = [4, 62, 6, 15]
    # period = [100, 200, 100, 200]
    # hyper_period = 200
    # current_time = 0
    # current_period = [1, 1, 1, 1]
    # remain_time = [4, 62, 6, 15]
    # offset = [0, 0, 0, 0]
    # release_times = [0, 0, 0, 0]
    # pure_preemption_overhead = 0.3
    # preemption_overhead = 2.3
    # frame_id = [0, 0, 0, 0]
    # fragment_id = [0, 0, 0, 0]
    # source = [0, 1, 2, 3]
    # destination = [0, 0, 0, 0]
    # offline_schedule = []
    # count = 0

    # 0.5
    # window_times = [17, 8, 8, 205, 40]
    # period = [200, 100, 100, 1000, 1000]
    # hyper_period = 1000
    # current_time = 0
    # current_period = [1, 1, 1, 1, 1]
    # remain_time = [17, 8, 8, 205, 40]
    # offset = [0, 0, 0, 0, 0]
    # release_times = [0, 0, 0, 0, 0]
    # pure_preemption_overhead = 0.3
    # preemption_overhead = 2.3
    # frame_id = [0, 0, 0, 0, 0]
    # fragment_id = [0, 0, 0, 0, 0]
    # source = [0, 1, 2, 3, 4]
    # destination = [0, 0, 0, 0, 0]
    # offline_schedule = []
    # count = 0

    # 0.75
    # window_times = [37, 48, 5, 35, 6]
    # period = [200, 200, 50, 200, 200]
    # hyper_period = 200
    # current_time = 0
    # current_period = [1, 1, 1, 1, 1]
    # remain_time = [37, 48, 5, 35, 6]
    # offset = [0, 0, 0, 0, 0]
    # release_times = [0, 0, 0, 0, 0]
    # pure_preemption_overhead = 0.3
    # preemption_overhead = 2.3
    # frame_id = [0, 0, 0, 0, 0]
    # fragment_id = [0, 0, 0, 0, 0]
    # source = [0, 1, 2, 3, 4]
    # destination = [0, 0, 0, 0, 0]
    # offline_schedule = []
    # count = 0




    # 0.8
    # window_times = [17, 101, 11, 44, 4]
    # period = [50, 1000, 100, 200, 500]
    # hyper_period = 1000
    # current_time = 0
    # current_period = [1, 1, 1, 1, 1]
    # remain_time = [17, 101, 11, 44, 4]
    # offset = [0, 0, 0, 0, 0]
    # release_times = [0, 0, 0, 0, 0]
    # pure_preemption_overhead = 0.3
    # preemption_overhead = 2.3
    # frame_id = [0, 0, 0, 0, 0]
    # fragment_id = [0, 0, 0, 0, 0]
    # source = [0, 1, 2, 3, 4]
    # destination = [0, 0, 0, 0, 0]
    # offline_schedule = []
    # count = 0


    # 0.9
    # window_times = [5, 35, 7, 41, 14]
    # period = [50, 100, 1000, 100, 1000]
    # hyper_period = 1000
    # current_time = 0
    # current_period = [1, 1, 1, 1, 1]
    # remain_time = [5, 35, 7, 41, 14]
    # offset = [0, 0, 0, 0, 0]
    # release_times = [0, 0, 0, 0, 0]
    # pure_preemption_overhead = 0.3
    # preemption_overhead = 2.3
    # frame_id = [0, 0, 0, 0, 0]
    # fragment_id = [0, 0, 0, 0, 0]
    # source = [0, 1, 2, 3, 4]
    # destination = [0, 0, 0, 0, 0]
    # offline_schedule = []
    # count = 0


    # frame_Id, fragment_Id, deadline, priority, arrive_time, window_times, period, source,destination, critical_level
    while current_time < 2 * hyper_period:
        # print("-----------------------------------------------------------------------------------------------------")
        # print("current time:", current_time)
        # print("current period:", current_period)
        # print("window:", window_times)
        # print("remain:", remain_time)
        # print("release time:", release_times)
        deadline = [a + b * c for a, b, c in zip(offset, period, current_period)]
        earliest_index = deadline.index(min(deadline))
        # print("update deadlines:", deadline)

        if current_time < offset[earliest_index] + period[earliest_index] * (current_period[earliest_index] - 1):
            temp_list = [a + b * c for a, b, c in zip(offset, period, current_period)]
            current_period_p = offset[earliest_index] + period[earliest_index] * (
                    current_period[earliest_index] - 1)
            # print("current_p", current_period_p)

            k = True
            while k:
                # print("deadline need to be modified")
                temp_list[earliest_index] = 10000
                earliest_index = temp_list.index(min(temp_list))
                if current_time >= release_times[earliest_index]:
                    k = False

            if remain_time[earliest_index] <= current_period_p - current_time:
                # print("schedule from part 1")
                running_time = remain_time[earliest_index]
                remain_time[earliest_index] -= running_time
                count += running_time
                # offline_schedule = offline_schedule.append(sche)
                # source, destination, frame_Id, fragment_Id, start_time, end_time

            else:
                # print("schedule from part 2")
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
                    # print("remain_fragment:", remain_time)

            sche = schedule(source[earliest_index], destination[earliest_index], frame_id[earliest_index],
                            fragment_id[earliest_index], current_time,
                            current_time + running_time, deadline[earliest_index])

            offline_schedule.append(sche)
            # print(sche.source, sche.frame_Id, sche.fragment_Id, sche.start_time, sche.end_time)
            fragment_id[earliest_index] += 1
            current_time += running_time
            if remain_time[earliest_index] == 0:
                remain_time[earliest_index] = window_times[earliest_index]
                current_period[earliest_index] += 1
                release_times[earliest_index] += offset[earliest_index] + period[earliest_index]
                frame_id[earliest_index] += 1
                fragment_id[earliest_index] = 0
                # print("remain_update:", remain_time)
            if current_time < min(release_times):
                current_time = min(release_times)

        else:
            current_period_p = offset[earliest_index] + period[earliest_index] * current_period[earliest_index]
            # print("current_p", current_period_p)
            if remain_time[earliest_index] <= current_period_p - current_time:
                # print("schedule from part 3")
                running_time = remain_time[earliest_index]
                remain_time[earliest_index] -= running_time
                count += running_time
            else:
                # print("schedule from part 4")
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
                    # print("remain_fragment:", remain_time)

                # print("remain_update:", remain_time)
            sche = schedule(source[earliest_index], destination[earliest_index], frame_id[earliest_index],
                            fragment_id[earliest_index], current_time,
                            current_time + running_time, deadline[earliest_index])
            offline_schedule.append(sche)
            # print(sche.source, sche.frame_Id, sche.fragment_Id, sche.start_time, sche.end_time)
            fragment_id[earliest_index] += 1
            current_time += running_time
            if remain_time[earliest_index] == 0:
                remain_time[earliest_index] = window_times[earliest_index]
                current_period[earliest_index] += 1
                release_times[earliest_index] += offset[earliest_index] + period[earliest_index]
                frame_id[earliest_index] += 1
                fragment_id[earliest_index] = 0
                # print("remain_update:", remain_time)

            if current_time < min(release_times):
                current_time = min(release_times)

            # print("frame id", frame_id)
            total_time = sum([b * c for b, c in zip(window_times, frame_id)])
            # print("total_time and uti", total_time, total_time/hyper_period)
            # print(count, count/hyper_period)
    print("-------------------- summarize ---------------------------")
    print(" start time | end time | source | frame_id | fragment_id | deadline")
    for i in range(len(offline_schedule)):
        print("------------------------------------------------------")
        print(offline_schedule[i].start_time, offline_schedule[i].end_time, offline_schedule[i].source,
              offline_schedule[i].frame_Id, offline_schedule[i].fragment_Id, offline_schedule[i].deadline)

    print("-------------------- utilization ---------------------------")
    print("original_total_transmission_time and uti: ", total_time, "|", total_time / (2 * hyper_period))
    print("actual_total_transmission_time and uti:", count, "|", count / (2 * hyper_period))

    return offline_schedule, source, hyper_period, window_times, period, destination, count


def pure_delayed_response_time(offline_schedule, delayed_release_time, C_delayed_frame, deadline_U_tbs,
                               preemptable_flow):
    inter_delayed = 0
    temp_retranse_deadline = []
    temp_retranse_frame = []
    temp_sched_check = []
    inter_delayed, temp_retranse_frame, temp_retranse_deadline, temp_sched_check = \
        active_interference_delayed(offline_schedule, inter_delayed, delayed_release_time, C_delayed_frame,
                                    deadline_U_tbs, preemptable_flow, temp_retranse_frame,
                                    temp_retranse_deadline,
                                    temp_sched_check, delayed_sche_id)

    inter_delayed, temp_retranse_frame, temp_retranse_deadline, temp_sched_check = \
        future_interference_delayed(offline_schedule, inter_delayed, delayed_release_time, C_delayed_frame,
                                    deadline_U_tbs, preemptable_flow, temp_retranse_frame,
                                    temp_retranse_deadline,
                                    temp_sched_check, delayed_sche_id)
    print("inter_delayed", inter_delayed)

    if delayed_flow_id == preemptable_flow:
        delayed_response_time = delayed_release_time + C_delayed_frame - 2 + inter_delayed
    else:
        delayed_response_time = delayed_release_time + C_delayed_frame + inter_delayed

    return delayed_response_time


def sporadic_frame_response_time(j, sporadic_c, sporadic_arrive_t, offline_schedule, deadline_U_CBS, C_CBS_remain,
                                 preemptable_flow, sporadic_response_time, mark, retrans_sched_id, sporadic_C,
                                 sporadic_arrive, delayed_release_time, delayed_response_time, deadline_U_tbs,
                                 delayed_flow_id, delayed_sche_id, count, error, delayed_error,
                                 retransmiss_st_preemptable_frames, retransmiss_st_deadline, sched_check):
    # interference_sporadic = 0
    # retransmiss_st_preemptable_frames = []
    # retransmiss_st_deadline = []
    # sched_check = []
    pure_preemption_overhead = 0.3


    deadline_U_CBS_backpack = deadline_U_CBS

    if mark[j] != 0:
        deadline_U_CBS = mark[j]
    print("actual assigned deadline:", deadline_U_CBS)

    # if there is frame preempted by sporadic frame is will be created as a new sporadic frame
    while sporadic_C[j] > 0:

        interference_sporadic = 0
        retransmiss_st_preemptable_frames = []
        retransmiss_st_deadline = []
        sched_check = []

        remain_transmission_time = 0
        remain_transmission_deadline = 0
        sporadic_c_backpack = sporadic_C[j]
        interference_sporadic, retransmiss_st_preemptable_frames, retransmiss_st_deadline, sched_check = \
            active_frame_interference(j, offline_schedule, interference_sporadic, sporadic_arrive[j],
                                      sporadic_C[j], deadline_U_CBS, preemptable_flow, remain_transmission_time,
                                      remain_transmission_deadline, retransmiss_st_preemptable_frames,
                                      retransmiss_st_deadline, retrans_sched_id, sched_check, delayed_sche_id)

        interference_sporadic, retransmiss_st_preemptable_frames, retransmiss_st_deadline, sched_check = \
            future_frame_interference(j, offline_schedule, interference_sporadic, sporadic_arrive[j],
                                      sporadic_C[j], deadline_U_CBS, preemptable_flow, remain_transmission_time,
                                      remain_transmission_deadline, retransmiss_st_preemptable_frames,
                                      retransmiss_st_deadline, retrans_sched_id, sched_check, delayed_sche_id)

        print("interference :", interference_sporadic)
        sporadic_response_time = sporadic_arrive[j] + interference_sporadic + sporadic_C[j]

        if count > 0:

            # if deadline_U_tbs == delayed_deadline:
            #     deadline_U_tbs = 0
            #     # the delayed frame is passed through slack calcultion can not be preempted anymore
            deadline_U_tbs = 1  # assign the highest priority
            print("deadline_U_tbs:", deadline_U_tbs)
            if delayed_release_time <= sporadic_arrive[j] <= delayed_response_time:
                count -= 1
                if delayed_response_time - sporadic_arrive[j] <= 2:
                    sporadic_arrive[j] += delayed_response_time - sporadic_arrive[j]
                else:
                    sporadic_arrive[j] = delayed_response_time

                print("the delayed frame will not be preempted by anyone else with response time",
                      delayed_response_time)
                print(sporadic_arrive)
                print(sporadic_C)
                print(mark)
                print(retrans_sched_id)
                # if deadline_U_tbs <= deadline_U_CBS:
                #     if delayed_response_time - sporadic_arrive[j] <= 2:
                #         sporadic_arrive[j] += delayed_response_time - sporadic_arrive[j]
                #     else:
                #         sporadic_arrive[j] = delayed_response_time
                #
                #     print("the delayed frame will not be preempted by anyone else with response time",
                #           delayed_response_time)
                #     print(sporadic_arrive)
                #     print(sporadic_C)
                #     print(mark)
                #     print(retrans_sched_id)
                # else:
                #     if delayed_response_time - sporadic_arrive[j] <= 2:
                #         sporadic_arrive[j] += delayed_response_time - sporadic_arrive[j]
                #         print(
                #             "the delayed frame will not be preempted by anyone else with response time but spo release changed",
                #             delayed_response_time)
                #         print(sporadic_arrive)
                #         print(sporadic_C)
                #         print(mark)
                #         print(retrans_sched_id)
                #     else:
                #         if delayed_release_time == sporadic_arrive[j]:
                #             delayed_remain = delayed_response_time - delayed_release_time - 1
                #         else:
                #             sporadic_arrive[j] += 0
                #             delayed_remain = delayed_response_time - sporadic_arrive[j]
                #
                #         delayed_release_time = sporadic_arrive[j] + interference_sporadic + sporadic_C[j]
                #
                #         sporadic_arrive.insert(j + 1, delayed_release_time)
                #         sporadic_C.insert(j + 1, delayed_remain)
                #         mark.insert(j + 1, deadline_U_tbs)
                #         retrans_sched_id.insert(j + 1, delayed_sche_id)
                #         print("!!!delayed frame will be preempted and insert into the table!!")
                #         print(sporadic_arrive)
                #         print(sporadic_C)
                #         print(mark)
                #         print(retrans_sched_id)

            elif sporadic_arrive[j] < delayed_release_time < sporadic_response_time:
                count -= 1

                if sporadic_response_time - delayed_release_time < 2:
                    print(" the delayed frame will be insert because it released after spo frame and with "
                          "higher priority ")
                    delayed_remain = delayed_response_time - delayed_release_time - 1
                    delayed_release_time = sporadic_response_time

                    sporadic_arrive.insert(j + 1, delayed_release_time)
                    sporadic_C.insert(j + 1, delayed_remain)
                    mark.insert(j + 1, deadline_U_tbs)
                    retrans_sched_id.insert(j + 1, delayed_sche_id)

                    print(sporadic_arrive)
                    print(sporadic_C)
                    print(mark)
                    print(retrans_sched_id)

                else:
                    print("release time of delayed frame", delayed_release_time)

                    temp_num = 0
                    for i in range(len(offline_schedule)):
                        if delayed_release_time == offline_schedule[i].start_time or delayed_release_time == \
                                offline_schedule[i].end_time:
                            delayed_release_time += 0
                        else:
                            temp_num += 1

                    if temp_num > 0:
                        delayed_release_time += 1

                    temp_back = sporadic_C[j]
                    print("parameters", sporadic_C[j], delayed_release_time, sporadic_arrive[j])
                    sporadic_C[j] = sporadic_C[j] - (delayed_release_time - sporadic_arrive[j]) + 0.3

                    if sporadic_C[j] < 0:
                        temp_inter1 = 0
                        for i in range(len(offline_schedule)):

                            if sporadic_arrive[j] <= offline_schedule[i].start_time <= delayed_release_time and offline_schedule[i].source != preemptable_flow and i != delayed_sche_id:
                                if offline_schedule[i].end_time <= delayed_release_time:
                                    temp_inter1 += offline_schedule[i].end_time - offline_schedule[i].start_time
                                elif offline_schedule[i].end_time > delayed_release_time:
                                    temp_inter1 += delayed_release_time - offline_schedule[i].start_time

                        print("parameters update", temp_back, delayed_release_time, sporadic_arrive[j], temp_inter1)
                        sporadic_C[j] = temp_back - (delayed_release_time - sporadic_arrive[j] - temp_inter1)

                    print("updated delayed_release_time", delayed_release_time)
                    delayed_response_time = pure_delayed_response_time(offline_schedule, delayed_release_time,
                                                                       C_delayed_frame, deadline_U_tbs,
                                                                       preemptable_flow)
                    if delayed_response_time > delayed_deadline:
                        print("!!!!!!!!the delayed traffic missed its deadline!!!!!!!!!!")
                        delayed_error += 1


                    sporadic_arrive[j] = delayed_response_time

                    print(" the delayed frame no need to be insert, with response time:", delayed_response_time)
                    print(" !!the remain sporadic frame will be undated!!")
                    print(sporadic_arrive)
                    print(sporadic_C)
                    print(mark)
                    print(retrans_sched_id)


        if mark[j] != 0:

            if retrans_sched_id[j] == delayed_sche_id:
                deadline_U_CBS = deadline_U_tbs

            # sporadic_response_time = sporadic_arrive[j] + sporadic_C[j] + interference_sporadic
            if mark[j + 1] == 0:

                if sporadic_arrive[j] <= sporadic_arrive[j + 1] < sporadic_response_time and deadline_U_CBS \
                        > deadline_U_CBS_backpack:
                    if sporadic_response_time - sporadic_arrive[j + 1] > 2:
                        print(" will be preempted by the sporadic frame")

                        # sporadic_c_backpack = sporadic_C[j]
                        if sporadic_arrive[j] == sporadic_arrive[j + 1]:
                            sporadic_C[j] -= 0
                        else:
                            sporadic_C[j] = sporadic_C[j] - (sporadic_arrive[j + 1] - sporadic_arrive[j] + 1) + 0.3

                        print(" temp remain preempted frame is: ", sporadic_C[j])

                        offsched_count = 0
                        for i in range(len(offline_schedule)):

                            if sporadic_arrive[j] <= offline_schedule[i].start_time <= sporadic_arrive[j + 1]:
                                offsched_count += 0

                            if offline_schedule[i].start_time <= sporadic_arrive[j] <= offline_schedule[i].end_time:

                                if offline_schedule[i].source != preemptable_flow and i != delayed_sche_id:

                                    sporadic_arrive[j] = offline_schedule[i].end_time
                                    sporadic_C[j] = sporadic_c_backpack
                                    print(" release during ST transmission 1")
                                    print(sporadic_C[j])
                                    print(sporadic_arrive[j])
                                    interference_sporadic = 0
                                    if offline_schedule[i].start_time <= sporadic_arrive[j + 1] \
                                            <= offline_schedule[i].end_time:
                                        # sporadic_C[j] = sporadic_c_backpack
                                        sporadic_arrive[j + 1] = offline_schedule[i].end_time
                                        print("555")
                                        break
                                elif offline_schedule[i].source == preemptable_flow and deadline_U_CBS < offline_schedule[i].deadline or i == delayed_sche_id:

                                    if sporadic_arrive[j] + sporadic_C[j] - offline_schedule[i].end_time > 2:
                                        sporadic_arrive[j] = offline_schedule[i].end_time
                                        sporadic_C[j] -= offline_schedule[i].end_time - sporadic_arrive[j]
                                        print(" release during preemptable ST transmission 2")
                                        print(sporadic_C[j])
                                        print(sporadic_arrive[j])
                                        interference_sporadic = 0
                                        break
                                    else:
                                        print(" release during preemptable ST transmission and can be finished")
                                        sporadic_C[j] -= 0
                                        sporadic_arrive[j] = offline_schedule[i].end_time
                                        interference_sporadic = 0
                                        break

                            elif sporadic_arrive[j] < offline_schedule[i].start_time < sporadic_response_time:

                                if offline_schedule[i].source != preemptable_flow and i != delayed_sche_id:

                                    if offline_schedule[i].start_time <= sporadic_arrive[j + 1] \
                                            <= offline_schedule[i].end_time:
                                        print(" release during ST transmission 3")
                                        sporadic_arrive[j + 1] = offline_schedule[i].end_time

                                        if sporadic_response_time - offline_schedule[i].start_time > 2:
                                            sporadic_C[j] = sporadic_c_backpack
                                            print("666")
                                            if offline_schedule[i].start_time - sporadic_arrive[j] > 0:
                                                print("AAA", sporadic_C[j], offline_schedule[i].start_time,
                                                      sporadic_arrive[j])
                                                sporadic_C[j] = sporadic_C[j] - (offline_schedule[i].start_time + 1
                                                                                 - sporadic_arrive[j]) + 0.3
                                                sporadic_arrive[j] = offline_schedule[i].end_time
                                                interference_sporadic = 0
                                                print(sporadic_C[j])
                                                print(sporadic_arrive[j])
                                                break
                                            else:
                                                print("bbb")
                                                sporadic_C[j] -= 0
                                                sporadic_arrive[j] = offline_schedule[i].end_time
                                                interference_sporadic = 0
                                                break



                        # if offsched_count == 0:
                        #     sporadic_arrive[j+1] += 1

                        newstart_time = 0
                        if sporadic_C[j] < 0:
                            temp = 0
                            for i in range(len(offline_schedule)):
                                if offline_schedule[i].start_time <= sporadic_arrive[j] <= offline_schedule[
                                    i].end_time and offline_schedule[
                                    i].source != preemptable_flow and i != delayed_sche_id:

                                    sporadic_C[j] = sporadic_c_backpack
                                    interference_sporadic = 0
                                    break
                                elif offline_schedule[i].start_time > sporadic_arrive[
                                    j] and offline_schedule[i].source != preemptable_flow and i != delayed_sche_id:
                                    temp = offline_schedule[i].start_time
                                    sporadic_C[j] = sporadic_c_backpack - (temp - sporadic_arrive[j] + 1) + 0.3
                                    if sporadic_C[j] <= 2:
                                        sporadic_response_time = sporadic_arrive[j] + sporadic_C[
                                            j] + interference_sporadic
                                        if retrans_sched_id[j] == delayed_sche_id:
                                            print("the response time of delayed frame", retrans_sched_id[j], "is: ",
                                                  sporadic_response_time)
                                            delayed_response_time = sporadic_response_time
                                        else:
                                            print("the response time of preempted frame", retrans_sched_id[j], "is: ",
                                                  sporadic_response_time)

                                        # deadline_U_CBS = deadline_U_CBS_backpack
                                        sporadic_C[j] = 0
                                        interference_sporadic = 1

                                        if sporadic_response_time > mark[j]:
                                            if retrans_sched_id[j] == delayed_sche_id:
                                                if sporadic_response_time > delayed_deadline:
                                                    print("!!!!!!!!!!!!!!!!!!!!warning!!!!!!!!!!!!!!!!!!!!!!!!!!!!")
                                                    print("the delayed ST frame miss deadline 1")
                                                    delayed_error += 1
                                            else:
                                                print("!!!!!!!!!!!!!!!!!!!!warning!!!!!!!!!!!!!!!!!!!!!!!!!!!!")
                                                print("the preempted ST frame miss deadline 1")
                                                error += 1
                                    else:
                                        newstart_time = offline_schedule[i].end_time
                                        interference_sporadic = 0
                                    break
                            if temp != 0:
                                sporadic_C[j] = sporadic_c_backpack - (temp - sporadic_arrive[j] + 1) + 0.3
                            else:
                                sporadic_C[j] = sporadic_c_backpack
                        else:
                            interference_sporadic = 0

                        print("offsched_count", offsched_count)
                        if offsched_count == 0:
                            sporadic_arrive[j + 1] += 1

                        print(" real remain preempted frame is: ", sporadic_C[j])
                        sporadic_C[j], sporadic_C[j + 1] = sporadic_C[j + 1], sporadic_C[j]
                        mark[j], mark[j + 1] = mark[j + 1], mark[j]
                        retrans_sched_id[j + 1] = retrans_sched_id[j]

                        if newstart_time:
                            sporadic_arrive[j] = newstart_time
                        else:
                            sporadic_arrive[j] = sporadic_arrive[j + 1]

                        deadline_U_CBS = deadline_U_CBS_backpack
                        print("update ")
                        print(sporadic_arrive)
                        print(sporadic_C)
                        print(mark)
                        print(retrans_sched_id)
                    else:
                        sporadic_response_time = sporadic_arrive[j] + sporadic_C[j] + interference_sporadic
                        sporadic_C[j] = 0

                        deadline_U_CBS = deadline_U_CBS_backpack

                        if retrans_sched_id[j] == delayed_sche_id:
                            print("the response time of delayed frame", retrans_sched_id[j], "is: ",
                                  sporadic_response_time)
                            delayed_response_time = sporadic_response_time
                        else:
                            print("the response time of preempted frame", retrans_sched_id[j], "is: ",
                                  sporadic_response_time)

                        if sporadic_response_time > mark[j]:
                            if retrans_sched_id[j] == delayed_sche_id:
                                if sporadic_response_time > delayed_deadline:
                                    print("!!!!!!!!!!!!!!!!!!!!warning!!!!!!!!!!!!!!!!!!!!!!!!!!!!")
                                    print("the delayed ST frame miss deadline 2")
                                    delayed_error += 1
                            else:
                                print("!!!!!!!!!!!!!!!!!!!!warning!!!!!!!!!!!!!!!!!!!!!!!!!!!!")
                                print("the preempted ST frame miss deadline 2")
                                error += 1
                else:
                    sporadic_response_time = sporadic_arrive[j] + sporadic_C[j] + interference_sporadic
                    sporadic_C[j] = 0
                    deadline_U_CBS = deadline_U_CBS_backpack

                    if retrans_sched_id[j] == delayed_sche_id:
                        print("the response time of delayed frame", retrans_sched_id[j], "is: ",
                              sporadic_response_time)
                        delayed_response_time = sporadic_response_time
                    else:
                        print("the response time of preempted frame", retrans_sched_id[j], "is: ",
                              sporadic_response_time)

                    if sporadic_response_time > mark[j]:
                        if retrans_sched_id[j] == delayed_sche_id:
                            if sporadic_response_time > delayed_deadline:
                                print("!!!!!!!!!!!!!!!!!!!!warning!!!!!!!!!!!!!!!!!!!!!!!!!!!!")
                                print("the delayed ST frame miss deadline 3")
                                delayed_error += 1
                        else:
                            print("!!!!!!!!!!!!!!!!!!!!warning!!!!!!!!!!!!!!!!!!!!!!!!!!!!")
                            print("the preempted ST frame miss deadline 3")
                            error += 1
            else:

                if deadline_U_CBS > deadline_U_CBS_backpack:
                    temp_check_flag = -2
                    temp_check_list = mark[j:]
                    for i in range(len(temp_check_list)):
                        if temp_check_list[i] == 0:
                            temp_check_flag = i
                            break

                    if temp_check_flag != -2:
                        prioritized_id = j + temp_check_flag
                        print("prioritized sporadic frame id", prioritized_id)

                        if sporadic_arrive[j] <= sporadic_arrive[prioritized_id] < sporadic_response_time:
                            if sporadic_response_time - sporadic_arrive[prioritized_id] > 2:
                                print(" will be preempted by the sporadic frame and being prioritized")

                                # sporadic_c_backpack = sporadic_C[j]
                                if sporadic_arrive[j] == sporadic_arrive[prioritized_id]:
                                    sporadic_C[j] -= 0
                                else:
                                    sporadic_C[j] = sporadic_C[j] - (sporadic_arrive[prioritized_id] - sporadic_arrive[j] + 1) + 0.3

                                print(" the remain preempted frame is updated: ", sporadic_C[j])

                                offsched_count = 0
                                for i in range(len(offline_schedule)):

                                    if sporadic_arrive[j] <= offline_schedule[i].start_time <= sporadic_arrive[prioritized_id]:
                                        offsched_count += 0

                                    if offline_schedule[i].start_time <= sporadic_arrive[j] <= offline_schedule[i].end_time \
                                            and offline_schedule[i].source != preemptable_flow and i != delayed_sche_id:

                                        sporadic_arrive[j] = offline_schedule[i].end_time
                                        sporadic_C[j] = sporadic_c_backpack
                                        print(" release during ST transmission and being suspended")
                                        print(sporadic_C[j])
                                        print(sporadic_arrive[j])
                                        interference_sporadic = 0
                                        if offline_schedule[i].start_time <= sporadic_arrive[prioritized_id] \
                                                <= offline_schedule[i].end_time:
                                            # sporadic_C[j] = sporadic_c_backpack
                                            sporadic_arrive[prioritized_id] = offline_schedule[i].end_time
                                            print("555ffff")
                                            break

                                    elif sporadic_arrive[j] < offline_schedule[i].start_time < sporadic_response_time \
                                            and offline_schedule[i].source != preemptable_flow and i != delayed_sche_id:

                                        if offline_schedule[i].start_time <= sporadic_arrive[prioritized_id] \
                                                <= offline_schedule[i].end_time:
                                            print(" release during ST transmission fafa")
                                            sporadic_arrive[prioritized_id] = offline_schedule[i].end_time

                                            if sporadic_response_time - offline_schedule[i].start_time > 2:
                                                sporadic_C[j] = sporadic_c_backpack
                                                print("666fff")
                                                if offline_schedule[i].start_time - sporadic_arrive[j] > 0:
                                                    print("AAA", sporadic_C[j], offline_schedule[i].start_time,
                                                          sporadic_arrive[j])
                                                    sporadic_C[j] = sporadic_C[j] - (offline_schedule[i].start_time + 1
                                                                                     - sporadic_arrive[j]) + 0.3
                                                    sporadic_arrive[j] = offline_schedule[i].end_time
                                                    interference_sporadic = 0
                                                    print(sporadic_C[j])
                                                    print(sporadic_arrive[j])
                                                    break
                                                else:
                                                    print("bbb")
                                                    sporadic_C[j] -= 0
                                                    sporadic_arrive[j] = offline_schedule[i].end_time
                                                    interference_sporadic = 0
                                                    break

                                # if offsched_count == 0:
                                #     sporadic_arrive[j+1] += 1

                                newstart_time = 0
                                if sporadic_C[j] < 0:
                                    temp = 0
                                    for i in range(len(offline_schedule)):
                                        if offline_schedule[i].start_time <= sporadic_arrive[j] <= offline_schedule[
                                            i].end_time and offline_schedule[
                                            i].source != preemptable_flow and i != delayed_sche_id:

                                            sporadic_C[j] = sporadic_c_backpack
                                            interference_sporadic = 0
                                            break
                                        elif offline_schedule[i].start_time > sporadic_arrive[
                                            j] and offline_schedule[i].source != preemptable_flow and i != delayed_sche_id:
                                            temp = offline_schedule[i].start_time
                                            sporadic_C[j] = sporadic_c_backpack - (temp - sporadic_arrive[j] + 1) + 0.3
                                            if sporadic_C[j] <= 2:
                                                sporadic_response_time = sporadic_arrive[j] + sporadic_C[
                                                    j] + interference_sporadic
                                                if retrans_sched_id[j] == delayed_sche_id:
                                                    print("the response time of delayed frame wwww", retrans_sched_id[j], "is: ",
                                                          sporadic_response_time)
                                                    delayed_response_time = sporadic_response_time
                                                else:
                                                    print("the response time of preempted frame www", retrans_sched_id[j],
                                                          "is: ",
                                                          sporadic_response_time)

                                                # deadline_U_CBS = deadline_U_CBS_backpack
                                                sporadic_C[j] = 0
                                                interference_sporadic = 1

                                                if sporadic_response_time > mark[j]:
                                                    if retrans_sched_id[j] == delayed_sche_id:
                                                        if sporadic_response_time > delayed_deadline:
                                                            print("!!!!!!!!!!!!!!!!!!!!warning!!!!!!!!!!!!!!!!!!!!!!!!!!!!")
                                                            print("the delayed ST frame miss deadline 1")
                                                            delayed_error += 1
                                                    else:
                                                        print("!!!!!!!!!!!!!!!!!!!!warning!!!!!!!!!!!!!!!!!!!!!!!!!!!!")
                                                        print("the preempted ST frame miss deadline 1")
                                                        error += 1
                                            else:
                                                newstart_time = offline_schedule[i].end_time
                                                interference_sporadic = 0
                                            break
                                    if temp != 0:
                                        sporadic_C[j] = sporadic_c_backpack - (temp - sporadic_arrive[j] + 1) + 0.3
                                    else:
                                        sporadic_C[j] = sporadic_c_backpack
                                else:
                                    interference_sporadic = 0

                                print("offsched_count", offsched_count)
                                if offsched_count == 0:
                                    sporadic_arrive[prioritized_id] += 1

                                print(" real remain preempted frame is: ", sporadic_C[j])

                                temp_arrive_time = sporadic_arrive[prioritized_id]
                                temp_sporadic_C = sporadic_C[prioritized_id]
                                temp_mark = mark[prioritized_id]
                                temp_retrans_sched_id = retrans_sched_id[prioritized_id]


                                sporadic_arrive.pop(prioritized_id)
                                sporadic_C.pop(prioritized_id)
                                mark.pop(prioritized_id)
                                retrans_sched_id.pop(prioritized_id)

                                sporadic_arrive.insert(j, temp_arrive_time)
                                sporadic_C.insert(j, temp_sporadic_C)
                                mark.insert(j, temp_mark)
                                retrans_sched_id.insert(j, temp_retrans_sched_id)


                                # sporadic_C[j], sporadic_C[j + 1] = sporadic_C[j + 1], sporadic_C[j]
                                # mark[j], mark[j + 1] = mark[j + 1], mark[j]
                                # retrans_sched_id[j + 1] = retrans_sched_id[j]

                                if newstart_time:
                                    sporadic_arrive[j] = newstart_time
                                else:
                                    sporadic_arrive[j] = sporadic_arrive[j + 1]

                                deadline_U_CBS = deadline_U_CBS_backpack
                                print("update ")
                                print(sporadic_arrive)
                                print(sporadic_C)
                                print(mark)
                                print(retrans_sched_id)
                            else:
                                sporadic_response_time = sporadic_arrive[j] + sporadic_C[j] + interference_sporadic
                                sporadic_C[j] = 0

                                deadline_U_CBS = deadline_U_CBS_backpack

                                if retrans_sched_id[j] == delayed_sche_id:
                                    print("the response time of delayed frame", retrans_sched_id[j], "is: ",
                                          sporadic_response_time)
                                    delayed_response_time = sporadic_response_time
                                else:
                                    print("the response time of preempted frame", retrans_sched_id[j], "is: ",
                                          sporadic_response_time)

                                if sporadic_response_time > mark[j]:
                                    if retrans_sched_id[j] == delayed_sche_id:
                                        if sporadic_response_time > delayed_deadline:
                                            print("!!!!!!!!!!!!!!!!!!!!warning!!!!!!!!!!!!!!!!!!!!!!!!!!!!")
                                            print("the delayed ST frame miss deadline 2")
                                            delayed_error += 1
                                    else:
                                        print("!!!!!!!!!!!!!!!!!!!!warning!!!!!!!!!!!!!!!!!!!!!!!!!!!!")
                                        print("the preempted ST frame miss deadline 2")
                                        error += 1
                        else:
                            sporadic_response_time = sporadic_arrive[j] + sporadic_C[j] + interference_sporadic
                            sporadic_C[j] = 0
                            deadline_U_CBS = deadline_U_CBS_backpack

                            if retrans_sched_id[j] == delayed_sche_id:
                                print("the response time of delayed frame", retrans_sched_id[j], "is: ",
                                      sporadic_response_time)
                                delayed_response_time = sporadic_response_time
                            else:
                                print("the response time of preempted frame", retrans_sched_id[j], "is: ",
                                      sporadic_response_time)

                            if sporadic_response_time > mark[j]:
                                if retrans_sched_id[j] == delayed_sche_id:
                                    if sporadic_response_time > delayed_deadline:
                                        print("!!!!!!!!!!!!!!!!!!!!warning!!!!!!!!!!!!!!!!!!!!!!!!!!!!")
                                        print("the delayed ST frame miss deadline 3")
                                        delayed_error += 1
                                else:
                                    print("!!!!!!!!!!!!!!!!!!!!warning!!!!!!!!!!!!!!!!!!!!!!!!!!!!")
                                    print("the preempted ST frame miss deadline 3")
                                    error += 1

                else:
                    if deadline_U_CBS > mark[j + 1]:

                        if sporadic_arrive[j] <= sporadic_arrive[j + 1] < sporadic_response_time:
                            if sporadic_response_time - sporadic_arrive[j + 1] > 2:
                                print(" preempted by the following frame tttt")
                                # sporadic_c_backpack = sporadic_C[j]
                                if sporadic_arrive[j] == sporadic_arrive[j + 1]:
                                    sporadic_C[j] -= 0
                                else:
                                    sporadic_C[j] = sporadic_C[j] - (sporadic_arrive[j + 1] - sporadic_arrive[j] + 1) + 0.3

                                print("temp remain preempted frame isttt: ", sporadic_C[j])

                                offsched_count = 0
                                for i in range(len(offline_schedule)):

                                    if sporadic_arrive[j] <= offline_schedule[i].start_time <= sporadic_arrive[j + 1]:
                                        offsched_count += 0

                                    if offline_schedule[i].start_time <= sporadic_arrive[j] <= offline_schedule[i].end_time \
                                            and offline_schedule[i].source != preemptable_flow and i != delayed_sche_id:

                                        sporadic_arrive[j] = offline_schedule[i].end_time
                                        sporadic_C[j] = sporadic_c_backpack
                                        print(" release during ST transmission 1ttt")
                                        interference_sporadic = 0
                                        if offline_schedule[i].start_time <= sporadic_arrive[j + 1] \
                                                <= offline_schedule[i].end_time:
                                            # sporadic_C[j] = sporadic_c_backpack
                                            sporadic_arrive[j + 1] = offline_schedule[i].end_time
                                            print("dfa555ttt")
                                            break

                                    elif sporadic_arrive[j] < offline_schedule[i].start_time < sporadic_response_time \
                                            and offline_schedule[i].source != preemptable_flow and i != delayed_sche_id:

                                        if offline_schedule[i].start_time <= sporadic_arrive[j + 1] \
                                                <= offline_schedule[i].end_time:
                                            print(" release during ST transmission 2ttt")
                                            sporadic_arrive[j + 1] = offline_schedule[i].end_time

                                            if sporadic_response_time - offline_schedule[i].start_time > 2:
                                                sporadic_C[j] = sporadic_c_backpack
                                                print("faaf666ttt")
                                                if offline_schedule[i].start_time - sporadic_arrive[j] > 0:
                                                    print("afasdfAAAttt")
                                                    sporadic_C[j] = sporadic_C[j] - (offline_schedule[i].start_time + 1
                                                                                     - sporadic_arrive[j]) + 0.3
                                                    sporadic_arrive[j] = offline_schedule[i].end_time
                                                    interference_sporadic = 0
                                                    print(sporadic_C[j])
                                                    print(sporadic_arrive[j])
                                                    break
                                                else:
                                                    print("fadfdbbbtttt")
                                                    sporadic_C[j] -= 0
                                                    sporadic_arrive[j] = offline_schedule[i].end_time
                                                    interference_sporadic = 0
                                                    break

                                newstart_time = 0
                                if sporadic_C[j] < 0:
                                    temp = 0
                                    for i in range(len(offline_schedule)):
                                        if offline_schedule[i].start_time <= sporadic_arrive[j] <= offline_schedule[
                                            i].end_time and offline_schedule[
                                            i].source != preemptable_flow and i != delayed_sche_id:
                                            sporadic_C[j] = sporadic_c_backpack
                                            interference_sporadic = 0
                                            break
                                        elif offline_schedule[i].start_time > sporadic_arrive[
                                            j] and offline_schedule[i].source != preemptable_flow and i != delayed_sche_id:
                                            temp = offline_schedule[i].start_time
                                            sporadic_C[j] = sporadic_c_backpack - (temp - sporadic_arrive[j] + 1) + 0.3
                                            if sporadic_C[j] <= 2:
                                                sporadic_response_time = sporadic_arrive[j] + sporadic_C[
                                                    j] + interference_sporadic
                                                if retrans_sched_id[j] == delayed_sche_id:
                                                    print("the response time of delayed framettt", retrans_sched_id[j], "is: ",
                                                          sporadic_response_time)
                                                    delayed_response_time = sporadic_response_time
                                                else:
                                                    print("the response time of preempted framettt", retrans_sched_id[j],
                                                          "is: ",
                                                          sporadic_response_time)

                                                # deadline_U_CBS = deadline_U_CBS_backpack
                                                sporadic_C[j] = 0
                                                interference_sporadic = 1

                                                if sporadic_response_time > mark[j]:
                                                    if retrans_sched_id[j] == delayed_sche_id:
                                                        if sporadic_response_time > delayed_deadline:
                                                            print("!!!!!!!!!!!!!!!!!!!!warning!!!!!!!!!!!!!!!!!!!!!!!!!!!!")
                                                            print("the delayed ST frame miss deadline 4ttt")
                                                            delayed_error += 1
                                                    else:
                                                        print("!!!!!!!!!!!!!!!!!!!!warning!!!!!!!!!!!!!!!!!!!!!!!!!!!!")
                                                        print("the preempted ST frame miss deadline 4ttt")
                                                        error += 1
                                            else:
                                                newstart_time = offline_schedule[i].end_time
                                                interference_sporadic = 0
                                            break
                                    if temp != 0:
                                        sporadic_C[j] = sporadic_c_backpack - (temp - sporadic_arrive[j] + 1) + 0.3
                                    else:
                                        sporadic_C[j] = sporadic_c_backpack
                                else:
                                    interference_sporadic = 1

                                print("222 offsched_countttt", offsched_count)
                                if offsched_count == 0:
                                    sporadic_arrive[j + 1] += 1

                                print(" real remain preempted frame is:ttt ", sporadic_C[j])
                                sporadic_C[j], sporadic_C[j + 1] = sporadic_C[j + 1], sporadic_C[j]
                                mark[j], mark[j + 1] = mark[j + 1], mark[j]
                                retrans_sched_id[j + 1] = retrans_sched_id[j]

                                if newstart_time:
                                    sporadic_arrive[j] = newstart_time
                                else:
                                    sporadic_arrive[j] = sporadic_arrive[j + 1]

                                deadline_U_CBS = deadline_U_CBS_backpack
                                print("update tt")
                                print(sporadic_arrive)
                                print(sporadic_C)
                                print(mark)
                                print(retrans_sched_id)
                            else:
                                sporadic_response_time = sporadic_arrive[j] + sporadic_C[j] + interference_sporadic
                                sporadic_C[j] = 0

                                deadline_U_CBS = deadline_U_CBS_backpack

                                if retrans_sched_id[j] == delayed_sche_id:
                                    print("the response time of delayed framettt", retrans_sched_id[j], "is: ",
                                          sporadic_response_time)
                                    delayed_response_time = sporadic_response_time
                                else:
                                    print("the response time of preempted framettt", retrans_sched_id[j], "is: ",
                                          sporadic_response_time)

                                if sporadic_response_time > mark[j]:
                                    if retrans_sched_id[j] == delayed_sche_id:
                                        if sporadic_response_time > delayed_deadline:
                                            print("!!!!!!!!!!!!!!!!!!!!warning!!!!!!!!!!!!!!!!!!!!!!!!!!!!")
                                            print("the delayed ST frame miss deadline 5ttt")
                                            delayed_error += 1
                                    else:
                                        print("!!!!!!!!!!!!!!!!!!!!warning!!!!!!!!!!!!!!!!!!!!!!!!!!!!")
                                        print("the preempted ST frame miss deadline 5ttt")
                                        error += 1
                        else:
                            sporadic_response_time = sporadic_arrive[j] + sporadic_C[j] + interference_sporadic
                            sporadic_C[j] = 0
                            deadline_U_CBS = deadline_U_CBS_backpack

                            if retrans_sched_id[j] == delayed_sche_id:
                                print("the response time of delayed framettt", retrans_sched_id[j], "is: ",
                                      sporadic_response_time)
                                delayed_response_time = sporadic_response_time
                            else:
                                print("the response time of preempted framettt", retrans_sched_id[j], "is: ",
                                      sporadic_response_time)

                            if sporadic_response_time > mark[j]:
                                if retrans_sched_id[j] == delayed_sche_id:
                                    if sporadic_response_time > delayed_deadline:
                                        print("!!!!!!!!!!!!!!!!!!!!warning!!!!!!!!!!!!!!!!!!!!!!!!!!!!")
                                        print("the delayed ST frame miss deadline 6ttt")
                                        delayed_error += 1
                                else:
                                    print("!!!!!!!!!!!!!!!!!!!!warning!!!!!!!!!!!!!!!!!!!!!!!!!!!!")
                                    print("the preempted ST frame miss deadline 6ttt")
                                    error += 1
                    else:
                        sporadic_response_time = sporadic_arrive[j] + sporadic_C[j] + interference_sporadic
                        sporadic_C[j] = 0
                        deadline_U_CBS = deadline_U_CBS_backpack

                        if retrans_sched_id[j] == delayed_sche_id:
                            print("the response time of delayed framettt", retrans_sched_id[j], "is: ",
                                  sporadic_response_time)
                            delayed_response_time = sporadic_response_time
                        else:
                            print("the response time of preempted framettt", retrans_sched_id[j], "is: ",
                                  sporadic_response_time)

                        if sporadic_response_time > mark[j]:
                            if retrans_sched_id[j] == delayed_sche_id:
                                if sporadic_response_time > delayed_deadline:
                                    print("!!!!!!!!!!!!!!!!!!!!warning!!!!!!!!!!!!!!!!!!!!!!!!!!!!")
                                    print("the delayed ST frame miss deadline 7ttt")
                                    delayed_error += 1
                            else:
                                print("!!!!!!!!!!!!!!!!!!!!warning!!!!!!!!!!!!!!!!!!!!!!!!!!!!")
                                print("the preempted ST frame miss deadline 7ttt")
                                error += 1

        else:
            if mark[j + 1] != 0 and deadline_U_CBS > mark[j + 1]:
                sporadic_arrive[j], sporadic_arrive[j+1] = sporadic_arrive[j+1], sporadic_arrive[j]
                sporadic_C[j], sporadic_C[j + 1] = sporadic_C[j + 1], sporadic_C[j]
                mark[j], mark[j + 1] = mark[j + 1], mark[j]
                retrans_sched_id[j], retrans_sched_id[j + 1] = retrans_sched_id[j], retrans_sched_id[j + 1]

                print("priority convert!")
                print(sporadic_arrive)
                print(sporadic_C)
                print(mark)
                print(retrans_sched_id)
            else:
                temp_int = 0
                temp_deadline_1 = deadline_U_CBS

                if C_CBS_remain > sporadic_C[j]:
                    print("the parameters", C_CBS_remain, sporadic_arrive[j], sporadic_C[j],
                          interference_sporadic)
                    sporadic_response_time = sporadic_arrive[j] + sporadic_C[j] + interference_sporadic

                    C_CBS_remain -= sporadic_C[j]
                    sporadic_C[j] = 0
                    print("remain capacity for following sporadic frame: ", C_CBS_remain)
                    print("response time of sporadic frame:", sporadic_response_time)
                    sporadic_Rt.append(sporadic_response_time)
                else:
                    sporadic_response_time = sporadic_arrive[j] + C_CBS_remain + interference_sporadic
                    print("response time check check and arrive time", sporadic_arrive[j])

                    # for i in range(len(offline_schedule)):
                    #
                    #     if offline_schedule[i].start_time <= sporadic_arrive[j] < offline_schedule[i].end_time:
                    #         print("@@@@@@@@@@@@@", offline_schedule[i].start_time, offline_schedule[i].end_time)
                    #         print()
                    #         break
                    #
                    #     elif sporadic_arrive[j] < offline_schedule[i].start_time:
                    #
                    #         print("################")
                    #
                    #         break

                    flag = 0

                    for i in range(len(offline_schedule)):

                        if offline_schedule[i].start_time <= sporadic_arrive[j] < offline_schedule[i].end_time:
                            print("@@@@@@@@@@@@@", offline_schedule[i].start_time, offline_schedule[i].end_time)
                            print("delayed id", delayed_sche_id)
                            flag = 1
                            flag_id = i
                            break

                        if sporadic_arrive[j] < offline_schedule[i].start_time and sporadic_arrive[j] + C_CBS_remain - \
                                offline_schedule[i].start_time > 2:
                            print("################", offline_schedule[i].start_time, offline_schedule[i].end_time)
                            flag = 2
                            flag_id = i
                            break

                        elif sporadic_arrive[j] == offline_schedule[i].end_time:
                            print("$$$$$$$$$$$$$$$", offline_schedule[i].start_time, offline_schedule[i].end_time)
                            flag = 3
                            flag_id = i
                            break

                    print("flag, flag_id", flag)

                    if flag == 1:
                        if offline_schedule[flag_id].source != preemptable_flow or offline_schedule[
                            flag_id].deadline < deadline_U_CBS:
                            if flag_id != delayed_sche_id:
                                print("the influence frame", offline_schedule[flag_id].start_time,
                                      offline_schedule[flag_id].end_time)

                                sporadic_arrive[j] = offline_schedule[flag_id].end_time
                                sporadic_C[j] -= 0
                                C_CBS_remain -= 0
                                interference_sporadic = 0
                                print("sporadic frame is delayed and keep in the current loop 1, ", sporadic_arrive[j])
                                print(sporadic_arrive)
                                print(sporadic_C)
                                print(mark)

                            else:
                                if sporadic_arrive[j] + C_CBS_remain - offline_schedule[flag_id].end_time > 2:
                                    sporadic_arrive[j] = offline_schedule[flag_id].end_time
                                    sporadic_C[j] -= (offline_schedule[flag_id].end_time - sporadic_arrive[j])
                                    C_CBS_remain -= (offline_schedule[flag_id].end_time - sporadic_arrive[j])
                                    print(sporadic_arrive)
                                    print(sporadic_C)
                                    print(mark)
                                else:
                                    exhaust_time = sporadic_arrive[j] + C_CBS_remain
                                    sporadic_arrive[j] = exhaust_time
                                    sporadic_C[j] -= C_CBS_remain
                                    deadline_U_CBS += T_CBS
                                    C_CBS_remain = C_CBS
                                    interference_sporadic = 0
                                    print("the capacity is exhausted at time point 1:", exhaust_time,
                                          sporadic_arrive[j],
                                          sporadic_C[j], deadline_U_CBS)
                                    print(sporadic_arrive)
                                    print(sporadic_C)
                                    print(mark)

                        else:
                            if flag_id == delayed_sche_id:

                                if sporadic_arrive[j] + C_CBS_remain - offline_schedule[flag_id].end_time > 2:
                                    sporadic_arrive[j] = offline_schedule[flag_id].end_time
                                    sporadic_C[j] -= (offline_schedule[flag_id].end_time - sporadic_arrive[j])
                                    C_CBS_remain -= (offline_schedule[flag_id].end_time - sporadic_arrive[j])
                                    print(sporadic_arrive)
                                    print(sporadic_C)
                                    print(mark)
                                else:
                                    exhaust_time = sporadic_arrive[j] + C_CBS_remain
                                    sporadic_arrive[j] = exhaust_time
                                    sporadic_C[j] -= C_CBS_remain
                                    deadline_U_CBS += T_CBS
                                    C_CBS_remain = C_CBS
                                    interference_sporadic = 0
                                    print("the capacity is exhausted at time point 1 from flag 1:", exhaust_time,
                                          sporadic_arrive[j],
                                          sporadic_C[j], deadline_U_CBS)
                                    print(sporadic_arrive)
                                    print(sporadic_C)
                                    print(mark)

                            else:
                                if offline_schedule[flag_id].deadline > deadline_U_CBS:

                                    if offline_schedule[flag_id].end_time - sporadic_arrive[j] > 2:

                                        remain_time = (offline_schedule[flag_id].end_time - offline_schedule[
                                            flag_id].start_time) - (sporadic_arrive[j] - offline_schedule[
                                            flag_id].start_time + 1) + 0.3

                                        print("the remain time of preemption candidate", remain_time)

                                        # 改成用utibound来确认是否能抢占

                                        if sporadic_response_time + remain_time > offline_schedule[flag_id].deadline:
                                            print("!!!!!!ATTENTION the preempt operation rejected frome flag 1!!!!!")
                                            sporadic_arrive[j] = offline_schedule[flag_id].end_time
                                            sporadic_C[j] -= 0
                                            C_CBS_remain -= 0
                                            interference_sporadic = 0
                                            print(
                                                "sporadic frame is delayed and keep in the current loop frome flag 1, ")
                                            print(sporadic_arrive)
                                            print(sporadic_C)
                                            print(mark)

                                        else:

                                            if abs(remain_time - offline_schedule[flag_id].end_time + offline_schedule[
                                                flag_id].start_time) < 2:
                                                remain_time = offline_schedule[flag_id].end_time - offline_schedule[
                                                    flag_id].start_time - 2

                                            if flag_id not in retrans_sched_id:

                                                # start_index = 0
                                                # for i in range(len(retrans_sched_id)):
                                                #     if retrans_sched_id[i] != -1:
                                                #         start_index = i
                                                #         break

                                                insert_mark = 1
                                                search_list = retrans_sched_id[j + 1:]
                                                print("reserch list", search_list)
                                                for i in range(len(search_list)):
                                                    if search_list[i] == -1:
                                                        insert_mark = 1 + i
                                                        break
                                                sporadic_arrive.insert(j + insert_mark,
                                                                       offline_schedule[flag_id].end_time)
                                                sporadic_C.insert(j + insert_mark, remain_time)
                                                mark.insert(j + insert_mark, offline_schedule[flag_id].deadline)
                                                retrans_sched_id.insert(j + insert_mark, flag_id)

                                                print("## ST frame insert from flag 1")
                                                print(sporadic_arrive)
                                                print(sporadic_C)
                                                print(mark)
                                                print(retrans_sched_id)

                                            if sporadic_arrive[j] + C_CBS_remain - offline_schedule[
                                                flag_id].end_time > 2:
                                                sporadic_arrive[j] = offline_schedule[flag_id].end_time
                                                sporadic_C[j] = sporadic_C[j] - (
                                                        offline_schedule[flag_id].end_time - sporadic_arrive[j]) + 0.3
                                                C_CBS_remain -= (
                                                            offline_schedule[flag_id].end_time - sporadic_arrive[j])
                                                print(
                                                    "sporadic frame is delayed and keep in the current loop 2.3 from flag 1, ")
                                                print(sporadic_arrive)
                                                print(sporadic_C)
                                                print(mark)

                                            else:
                                                exhaust_time = sporadic_arrive[j] + C_CBS_remain
                                                sporadic_arrive[j] = exhaust_time
                                                sporadic_C[j] -= C_CBS_remain
                                                deadline_U_CBS += T_CBS
                                                C_CBS_remain = C_CBS
                                                interference_sporadic = 0
                                                print("the capacity is exhausted at time point from flag 1:",
                                                      exhaust_time,
                                                      sporadic_arrive[j], sporadic_C[j], deadline_U_CBS)
                                                print(sporadic_arrive)
                                                print(sporadic_C)
                                                print(mark)

                                    else:
                                        sporadic_arrive[j] = offline_schedule[flag_id].end_time
                                        sporadic_C[j] -= 0
                                        C_CBS_remain -= 0
                                        interference_sporadic = 0
                                        print("sporadic frame is delayed and keep in the current loop from flag 1, ")
                                        print(sporadic_arrive)
                                        print(sporadic_C)
                                        print(mark)

                                else:
                                    print("the frame can not be preempted, because the assigned deadline greater than "
                                          "preempted ST")
                                    if sporadic_arrive[j] + C_CBS_remain - offline_schedule[flag_id].end_time > 2:
                                        sporadic_arrive[j] = offline_schedule[flag_id].end_time
                                        sporadic_C[j] -= (offline_schedule[flag_id].end_time - sporadic_arrive[j])
                                        C_CBS_remain -= (offline_schedule[flag_id].end_time - sporadic_arrive[j])
                                        print(sporadic_arrive)
                                        print(sporadic_C)
                                        print(mark)
                                    else:
                                        exhaust_time = sporadic_arrive[j] + C_CBS_remain
                                        sporadic_arrive[j] = exhaust_time
                                        sporadic_C[j] -= C_CBS_remain
                                        deadline_U_CBS += T_CBS
                                        C_CBS_remain = C_CBS
                                        interference_sporadic = 0
                                        print("the capacity is exhausted at time point ## :", exhaust_time,
                                              sporadic_arrive[j], sporadic_C[j], deadline_U_CBS)
                                        print(sporadic_arrive)
                                        print(sporadic_C)
                                        print(mark)

                    if flag == 2:

                        if flag_id != delayed_sche_id:

                            if offline_schedule[flag_id].source != preemptable_flow or offline_schedule[
                                flag_id].deadline < deadline_U_CBS:

                                sporadic_arrive[j] = offline_schedule[flag_id].end_time
                                sporadic_C[j] = sporadic_C[j] - (
                                        offline_schedule[flag_id].start_time - sporadic_arrive[j] + 1) + 0.3
                                C_CBS_remain -= (offline_schedule[flag_id].start_time - sporadic_arrive[j])
                                print("sporadic frame is delayed and keep in the current loop 2.5 from flag 2,")
                                print(sporadic_arrive)
                                print(sporadic_C)
                                print(mark)

                            else:

                                deadline_check = sporadic_arrive[j] + C_CBS_remain + (
                                        offline_schedule[flag_id].end_time - offline_schedule[flag_id].start_time)

                                if deadline_check > offline_schedule[flag_id].deadline:
                                    print("!!!!!!ATTENTION the preempt operation rejected 2 from flag 2!!!!!")
                                    sporadic_arrive[j] = offline_schedule[flag_id].end_time
                                    sporadic_C[j] = sporadic_C[j] - (
                                            offline_schedule[flag_id].start_time - sporadic_arrive[j] + 1) + 0.3
                                    C_CBS_remain -= (offline_schedule[flag_id].start_time - sporadic_arrive[j])
                                    print("sporadic frame is delayed and keep in the current loop 2.6 from flag 2,")
                                    print(sporadic_arrive)
                                    print(sporadic_C)
                                    print(mark)

                                else:

                                    if flag_id not in retrans_sched_id:

                                        # start_index = 0
                                        # for i in range(len(retrans_sched_id)):
                                        #     if retrans_sched_id[i] != -1:
                                        #         start_index = i
                                        #         break

                                        insert_mark = 1
                                        search_list = retrans_sched_id[j + 1:]
                                        print("reserch list", search_list)
                                        for i in range(len(search_list)):
                                            if search_list[i] == -1:
                                                insert_mark = 1 + i
                                                break
                                        sporadic_arrive.insert(j + insert_mark, sporadic_arrive[j] + C_CBS_remain)
                                        sporadic_C.insert(j + insert_mark,
                                                          offline_schedule[flag_id].end_time - offline_schedule[
                                                              flag_id].start_time)
                                        mark.insert(j + insert_mark, offline_schedule[flag_id].deadline)
                                        retrans_sched_id.insert(j + insert_mark, flag_id)

                                        print("## ST frame insert from flag 2")
                                        print(sporadic_arrive)
                                        print(sporadic_C)
                                        print(mark)
                                        print(retrans_sched_id)

                                    exhaust_time = sporadic_arrive[j] + C_CBS_remain
                                    sporadic_arrive[j] = exhaust_time
                                    sporadic_C[j] -= C_CBS_remain
                                    deadline_U_CBS += T_CBS
                                    C_CBS_remain = C_CBS
                                    interference_sporadic = 0
                                    print("the capacity is exhausted at time point 2 from flag 2:", exhaust_time,
                                          sporadic_arrive[j], sporadic_C[j], deadline_U_CBS)
                                    print(sporadic_arrive)
                                    print(sporadic_C)
                                    print(mark)

                        else:
                            if sporadic_arrive[j] + C_CBS_remain - offline_schedule[flag_id].end_time > 2:
                                sporadic_arrive[j] = offline_schedule[flag_id].end_time
                                sporadic_C[j] -= (offline_schedule[flag_id].end_time - sporadic_arrive[j])
                                C_CBS_remain -= (offline_schedule[flag_id].end_time - sporadic_arrive[j])
                                print("sporadic frame is delayed and keep in the current loop 2.7 from flag 2,")
                                print(sporadic_arrive)
                                print(sporadic_C)
                                print(mark)

                            else:
                                exhaust_time = sporadic_arrive[j] + C_CBS_remain
                                sporadic_arrive[j] = exhaust_time
                                sporadic_C[j] -= C_CBS_remain
                                deadline_U_CBS += T_CBS
                                C_CBS_remain = C_CBS
                                interference_sporadic = 0
                                print("the capacity is exhausted at time point 3 from flag 2:", exhaust_time,
                                      sporadic_arrive[j],
                                      sporadic_C[j], deadline_U_CBS)
                                print(sporadic_arrive)
                                print(sporadic_C)
                                print(mark)

                    if flag == 3:
                        if flag_id + 1 < len(offline_schedule):
                            print("offline_schedule[flag_id + 1].start_time, sporadic_arrive[j]",
                                  offline_schedule[flag_id + 1].start_time, sporadic_arrive[j])

                            if offline_schedule[flag_id + 1].start_time - sporadic_arrive[j] == 0:
                                if flag_id + 1 != delayed_sche_id:

                                    if offline_schedule[flag_id + 1].source != preemptable_flow or offline_schedule[
                                        flag_id + 1].deadline < deadline_U_CBS:
                                        sporadic_arrive[j] = offline_schedule[flag_id + 1].end_time
                                        print("sporadic frame is delayed and keep in the current loop 2.8 from flag 3,")
                                        print(sporadic_arrive)
                                        print(sporadic_C)
                                        print(mark)
                                    else:
                                        deadline_check = sporadic_arrive[j] + C_CBS_remain + (
                                                offline_schedule[flag_id + 1].end_time - offline_schedule[
                                            flag_id + 1].start_time)

                                        if deadline_check > offline_schedule[flag_id + 1].deadline:
                                            print("!!!!!!ATTENTION the preempt operation rejected 3 from flag 3!!!!!")
                                            sporadic_arrive[j] = offline_schedule[flag_id + 1].end_time
                                            print(sporadic_arrive)
                                            print(sporadic_C)
                                            print(mark)

                                        else:
                                            if flag_id + 1 not in retrans_sched_id:

                                                # start_index = 0
                                                # for i in range(len(retrans_sched_id)):
                                                #     if retrans_sched_id[i] != -1:
                                                #         start_index = i
                                                #         break

                                                insert_mark = 1
                                                search_list = retrans_sched_id[j + 1:]
                                                print("reserch list", search_list)
                                                for i in range(len(search_list)):
                                                    if search_list[i] == -1:
                                                        insert_mark = 1 + i
                                                        break

                                                sporadic_arrive.insert(j + insert_mark,
                                                                       sporadic_arrive[j] + C_CBS_remain)
                                                sporadic_C.insert(j + insert_mark,
                                                                  offline_schedule[flag_id + 1].end_time -
                                                                  offline_schedule[
                                                                      flag_id + 1].start_time)
                                                mark.insert(j + insert_mark, offline_schedule[flag_id + 1].deadline)
                                                retrans_sched_id.insert(j + insert_mark, flag_id + 1)
                                                print("## ST frame insert 3 from flag 3")
                                                print(sporadic_arrive)
                                                print(sporadic_C)
                                                print(mark)
                                                print(retrans_sched_id)

                                            exhaust_time = sporadic_arrive[j] + C_CBS_remain
                                            sporadic_arrive[j] = exhaust_time
                                            sporadic_C[j] -= C_CBS_remain
                                            deadline_U_CBS += T_CBS
                                            C_CBS_remain = C_CBS
                                            interference_sporadic = 0
                                            print("the capacity is exhausted at time point 4 from flag 3:",
                                                  exhaust_time,
                                                  sporadic_arrive[j], sporadic_C[j], deadline_U_CBS)
                                            print(sporadic_arrive)
                                            print(sporadic_C)
                                            print(mark)

                                else:
                                    if sporadic_arrive[j] + C_CBS_remain - offline_schedule[flag_id + 1].end_time > 2:
                                        sporadic_arrive[j] = offline_schedule[flag_id + 1].end_time
                                        sporadic_C[j] -= (offline_schedule[flag_id + 1].end_time - sporadic_arrive[j])
                                        C_CBS_remain -= (offline_schedule[flag_id + 1].end_time - sporadic_arrive[j])
                                        print(
                                            "sporadic frame is delayed and keep in the current loop 2.9 frome flag 3,")
                                        print(sporadic_arrive)
                                        print(sporadic_C)
                                        print(mark)

                                    else:
                                        exhaust_time = sporadic_arrive[j] + C_CBS_remain
                                        sporadic_arrive[j] = exhaust_time
                                        sporadic_C[j] -= C_CBS_remain
                                        deadline_U_CBS += T_CBS
                                        C_CBS_remain = C_CBS
                                        interference_sporadic = 0
                                        print("the capacity is exhausted at time point 4 from flag 3:", exhaust_time,
                                              sporadic_arrive[j], sporadic_C[j], deadline_U_CBS)
                                        print(sporadic_arrive)
                                        print(sporadic_C)
                                        print(mark)

                            else:
                                if sporadic_arrive[j] + C_CBS_remain - offline_schedule[flag_id + 1].start_time < 2:
                                    exhaust_time = sporadic_arrive[j] + C_CBS_remain
                                    sporadic_arrive[j] = exhaust_time
                                    sporadic_C[j] -= C_CBS_remain
                                    deadline_U_CBS += T_CBS
                                    C_CBS_remain = C_CBS
                                    interference_sporadic = 0
                                    print("the capacity is exhausted at time point 5 from flag 3:", exhaust_time,
                                          sporadic_arrive[j], sporadic_C[j], deadline_U_CBS)
                                    print(sporadic_arrive)
                                    print(sporadic_C)
                                    print(mark)

                                else:
                                    sporadic_arrive[j] = offline_schedule[flag_id + 1].start_time
                                    sporadic_C[j] = sporadic_C[j] - (
                                            offline_schedule[flag_id + 1].start_time - sporadic_arrive[j] + 1) + 0.3
                                    C_CBS_remain -= (offline_schedule[flag_id + 1].start_time - sporadic_arrive[j])
                                    print("sporadic frame is delayed and keep in the current loop 2.9 from flag 3,")
                                    print(sporadic_arrive)
                                    print(sporadic_C)
                                    print(mark)

                        else:
                            exhaust_time = sporadic_arrive[j] + C_CBS_remain
                            sporadic_arrive[j] = exhaust_time
                            sporadic_C[j] -= C_CBS_remain
                            deadline_U_CBS += T_CBS
                            C_CBS_remain = C_CBS
                            interference_sporadic = 0
                            print("the capacity is exhausted at time point 5 from flag 3:", exhaust_time,
                                  sporadic_arrive[j], sporadic_C[j], deadline_U_CBS)
                            print(sporadic_arrive)
                            print(sporadic_C)
                            print(mark)

                    if flag == 0:
                        exhaust_time = sporadic_arrive[j] + C_CBS_remain
                        sporadic_arrive[j] = exhaust_time
                        sporadic_C[j] -= C_CBS_remain
                        deadline_U_CBS += T_CBS
                        C_CBS_remain = C_CBS
                        interference_sporadic = 0
                        print("the capacity is exhausted at time point 6 from flag 0:", exhaust_time,
                              sporadic_arrive[j], sporadic_C[j], deadline_U_CBS)
                        print(sporadic_arrive)
                        print(sporadic_C)
                        print(mark)






    return sporadic_response_time, retransmiss_st_preemptable_frames, retransmiss_st_deadline, \
           C_CBS_remain, deadline_U_CBS, sched_check, delayed_response_time, error, delayed_error


def window_time_Generator(stream_number, period, target_utilization):

    utilizations = uunifast(stream_number, target_utilization)

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


def uunifast(stream_number, target_utilization):
    sum_utilization = target_utilization
    utilizations = []

    for i in range(1, stream_number):
        nextSumU = sum_utilization * random.uniform(0, 1) ** (1.0 / (stream_number - i))
        utilizations.append(sum_utilization - nextSumU)
        sum_utilization = nextSumU

    utilizations.append(sum_utilization)
    return utilizations


def hyper_period_calculation(period):
    hyper_period = period[0]
    for i in range(1, len(period)):
        hyper_period = hyper_period * period[i] // math.gcd(hyper_period, period[i])

    return hyper_period

if __name__ == "__main__":

    delayed_error = 0
    error = 0
    guaranteed_sporadic = 0
    accepted_delayed_traffic = 0
    sporadic_frame_number = []
    sporadic_response_time_list = []
    round_number = 1
    unscheduleable_count = 0

    for k in range(round_number):


        reselect = True
        while reselect:

            stream_number = 5
            target_utilization = 0.75
            period_set = [50, 100, 200, 500, 1000]
            generated_window_times = []
            window_times = []
            actual_utilization = 0
            idxs = np.random.randint(0, len(period_set), size=stream_number)
            period = []
            for i in idxs:
                period.append(period_set[i])

            k = True
            while k:
                generated_window_times = window_time_Generator(stream_number, period, target_utilization)
                uti = []
                for i in range(stream_number):
                    uti.append(generated_window_times[i] / period[i])
                actual_utilization = sum(uti)
                if actual_utilization < target_utilization and min(generated_window_times) >= 3:
                    k = False
            for i in range(len(generated_window_times)):
                window_times.append(generated_window_times[i])

            print("window_times:", window_times)
            print("actual utilization:", actual_utilization)
            print("period:", period)
            hyper_period = hyper_period_calculation(period)
            print(hyper_period)

            temp_window = []
            for i in range(len(period)):
                if period[i] == max(period):
                    temp_window.append(window_times[i])
            # print(temp_window)

            offline_schedule, source, hyper_period, window_times, period, destination, count = EDF_Scheduling(window_times,
                                                                                                              period,
                                                                                                              hyper_period)

            proportion = []
            for i in range(len(period)):
                proportion.append(window_times[i] / period[i])

            print(temp_window)
            print(window_times)

            preemptable_flow = window_times.index(max(temp_window))

            if offline_schedule[0].source != preemptable_flow:
                reselect = False
            print("The preemptable flow is", preemptable_flow)

        # preemptable_flow = 1
        pure_preemption_overhead = 0.3
        preemption_overhead = 2.3

        Uti_server_up_bound = 1 - count / (2 * hyper_period)


        print("-------------------- delayed frame generator ---------------------------")

        delayed_flow_id = random.randint(0, max(source))
        temp = []
        frame_id_check = []
        fragment_check = []
        emergency_queue = []
        deadline_U_tbs = 0
        delayed_response_time = 0
        for i in range(len(offline_schedule)):
            if offline_schedule[i].source == delayed_flow_id:
                temp.append(i)
                frame_id_check.append(offline_schedule[i].frame_Id)
                fragment_check.append(offline_schedule[i].fragment_Id)
        print("delayed_flow_id", delayed_flow_id)
        # print("candidate sche id", temp)
        # print("frame_id of candidate flow", frame_id_check)
        # print("the fragment check", fragment_check)
        delayed_sche_id = choice(temp)
        start_time = offline_schedule[delayed_sche_id].start_time
        end_time = offline_schedule[delayed_sche_id].end_time
        delayed_fragment_id = offline_schedule[delayed_sche_id].fragment_Id

        print("delayed_sche_id", delayed_sche_id)
        time_duration = end_time - start_time
        if delayed_flow_id == preemptable_flow:
            C_delayed_frame = time_duration
        else:
            C_delayed_frame = time_duration - 2
            if C_delayed_frame < 0:
                C_delayed_frame = 1
            C_delayed_frame = time_duration - 2

        # if delayed_sche_id == preemptable_flow:
        #     C_delayed_frame = time_duration

        utilization_delayed = window_times[delayed_flow_id] / (2 * hyper_period)
        # print(int(math.ceil(start_time)), offline_schedule[delayed_frame_id].deadline - time_duration,
        #      offline_schedule[delayed_frame_id].deadline, window_times[delayed_flow_id])
        delayed_release_time = random.randint(int(math.ceil(start_time)),
                                              offline_schedule[delayed_sche_id].deadline - math.ceil(time_duration))
        delayed_deadline = offline_schedule[delayed_sche_id].deadline

        delayed_frame = Frame(offline_schedule[delayed_sche_id].frame_Id, offline_schedule[delayed_sche_id].fragment_Id,
                              delayed_deadline, 0, delayed_release_time,
                              time_duration, period[delayed_flow_id], source[delayed_flow_id], destination[delayed_flow_id],
                              "safety_critical")
        delayed_count = 1
        # print(delayed_frame.source, delayed_frame.arrive_time, delayed_frame.window_time+delayed_frame.arrive_time,
        # delayed_frame.window_time) frame_Id, fragment_Id, deadline, priority, arrive_time, window_times, period,

        # source, destination, critical_level

        print("utilization_delayed :", utilization_delayed)
        print("frame base Uti", sum(emergency_queue) / (2 * hyper_period))
        print("original start time, end time ans frame size: ", start_time, end_time, C_delayed_frame)
        print("release time of delayed frame:", delayed_release_time)
        print("deadline of delayed frame:", delayed_deadline)

        # ---------------------------------------------------------------------------------------- #
        #        sporadic traffic can be transmitted according to the CBS assigned deadline        #
        #                                        CBS                                               #
        # ---------------------------------------------------------------------------------------- #
        print("")
        print("-----------------------sporadic generator----------------------------------")
        sporadic_flow = Frame(0, 0, 0, 0, random.randint(0, 100), random.randint(1, math.ceil(np.mean(window_times))),
                                                                                 np.mean(period), 0, 0, "sporadic")
        sporadic_offset = sporadic_flow.arrive_time
        # print("sporadic offset:", sporadic_offset)
        C_sporadic = sporadic_flow.window_time
        sporadic_interval = sporadic_flow.period

        sporadic_queue = []
        print("sporadic traffic parameters:", sporadic_offset, C_sporadic, sporadic_interval)

        sporadic_arrive = []
        sporadic_time_stamp = sporadic_offset
        while sporadic_time_stamp < 2 * hyper_period:
            sporadic_arrive.append(sporadic_time_stamp)
            sporadic_time_stamp += sporadic_interval
        sporadic_arrive.append(0)
        print(sporadic_arrive)

        sporadic_deadline = []
        sporadic_step = sporadic_offset + sporadic_interval
        for i in range(len(sporadic_arrive)):
            sporadic_deadline.append(sporadic_step)
            sporadic_step += sporadic_interval

        sporadic_deadline.append(1000000)
        print(sporadic_deadline)


        sporadic_C = []
        for i in range(len(sporadic_arrive)):
            sporadic_C.append(C_sporadic)
        sporadic_C.append(0)
        print(sporadic_C)


        mark = []
        for i in range(len(sporadic_arrive)):
            mark.append(0)
        mark.append(1000000)
        print(mark)

        retrans_sched_id = []
        for i in range(len(sporadic_arrive)):
            retrans_sched_id.append(-1)
        retrans_sched_id.append(-1)
        print(retrans_sched_id)

        print("")
        print("-----------------------CBS parameter setup----------------------------------")

        # C_sporadic_avg = math.floor(np.median(window_times))
        C_sporadic_avg = 10
        max_preemption_times = math.floor(C_sporadic_avg / 2)
        max_preemption_overhead = max_preemption_times * pure_preemption_overhead
        # print(max_preemption_overhead)

        # Uti_CBS = Uti_server_up_bound + utilization_delayed - \
        #           sum(emergency_queue) / (2 * hyper_period)

        # Uti_preempted_ST = window_times[preemptable_flow]/period[preemptable_flow]
        Uti_preempted_ST = window_times[preemptable_flow] / (2 * hyper_period)

        print("para:", Uti_server_up_bound, utilization_delayed, Uti_preempted_ST)

        Uti_CBS = Uti_server_up_bound + utilization_delayed - Uti_preempted_ST
        if Uti_CBS < 0:
            print("!!!!system is unschedulable!!!")
            unscheduleable_count += 1
            break


        print("the utilization allocate to sporadic traffic:", Uti_CBS)

        T_CBS = math.floor(
            1 / Uti_CBS * (
                    max_preemption_overhead + math.sqrt((max_preemption_times * C_sporadic_avg) / (1 - Uti_CBS))))
        C_CBS = math.floor(T_CBS * Uti_CBS)
        C_CBS_remain = C_CBS

        print("the parameters of CBS periodic time | capacity | actual utilization: ", T_CBS, C_CBS, C_CBS / T_CBS)
        deadline_U_CBS = 0
        # deadline_U_CBS = sporadic_offset + T_CBS  # initiation
        print("original deadline: ", deadline_U_CBS)
        sporadic_response_time = 0
        sporadic_release_time = sporadic_arrive[0]

        sporadic_Rt = []
        count = 1

        Uti_TBS = Uti_server_up_bound - sum(emergency_queue) / (2 * hyper_period)
        print("utilization for TBS:", Uti_TBS)

        pst_mark = 0
        for i in range(len(offline_schedule)):

            if offline_schedule[i].start_time <= delayed_release_time < offline_schedule[i].end_time:
                if offline_schedule[i].source == preemptable_flow:
                    preemptable_flow_instance = i
                    pst_mark = 1
                    break

            if delayed_release_time <= offline_schedule[i].start_time < delayed_deadline:
                if offline_schedule[i].source == preemptable_flow:
                    preemptable_flow_instance = i
                    pst_mark = 1
                    break

        decay = 1
        Uti_TBS = Uti_server_up_bound - sum(emergency_queue) / (2 * hyper_period)
        if pst_mark != 0:
            C_preempted_ST = offline_schedule[preemptable_flow_instance].end_time - offline_schedule[
                preemptable_flow_instance].start_time
            Uti_TBS_test = Uti_TBS * decay - C_preempted_ST / (
                        offline_schedule[preemptable_flow_instance].deadline - delayed_release_time - C_delayed_frame)
        else:
            Uti_TBS_test = Uti_TBS

        sporadic_frame_number.append(len(sporadic_arrive))


        original_length_sporadic = len(sporadic_arrive)


        for j in range(1000000):

            if j < len(sporadic_arrive) - 1:

                if delayed_count >= 1:
                    if C_delayed_frame <= (delayed_deadline - delayed_release_time) * Uti_TBS_test:
                        # acceptance_state1 = True
                        acceptance_state = True
                        # accepted_count += 1
                        deadline_U_tbs = max(delayed_release_time, deadline_U_tbs) + C_delayed_frame / Uti_TBS_test
                        print("********* Acceptance test passed from uti 1 ***********:")
                        # print("TBS assigned deadline:", deadline_U_tbs)
                        if pst_mark != 0:
                            Uti_preempted_test = Uti_TBS_test - utilization_delayed
                            if C_preempted_ST > (offline_schedule[preemptable_flow_instance].deadline - delayed_release_time - C_delayed_frame)*Uti_preempted_test:
                                acceptance_state = False
                                # rejected_count += 1
                                print("reject from ST_test")

                        if delayed_deadline - delayed_release_time <= hyper_period * 0.3:

                            inter_block = 0
                            for i in range(len(offline_schedule)):

                                if offline_schedule[i].start_time < delayed_release_time < offline_schedule[i].end_time:
                                    if i == delayed_sche_id:
                                        inter_block += 0
                                        # print("delayed frame is released within its offline scheduled time")

                                    else:
                                        inter_block += offline_schedule[i].end_time - delayed_release_time

                                if delayed_release_time <= offline_schedule[i].start_time < delayed_deadline:
                                    inter_block += offline_schedule[i].end_time - offline_schedule[i].start_time

                            if delayed_release_time + inter_block + C_delayed_frame > delayed_deadline:
                                acceptance_state = False
                                # rejected_count += 1
                                print(
                                    "!$$$WARNING: The delayed traffic can not be transmitted within its deadline and emergency "
                                    "action should be triggered ! reject from Uti")
                            else:
                                print("********* Acceptance test passed from uti 2 ***********:")

                    else:
                        emergency_action = True
                        # acceptance_state2 = False
                        acceptance_state = False
                        # rejected_count += 1
                        print(
                            "!$$$WARNING: The delayed traffic can not be transmitted within its deadline and emergency "
                            "action should be triggered ! ")

                    if acceptance_state:

                        inter_delayed = 0
                        temp_retranse_deadline = []
                        temp_retranse_frame = []
                        temp_sched_check = []
                        inter_delayed, temp_retranse_frame, temp_retranse_deadline, temp_sched_check = \
                            active_interference_delayed(offline_schedule, inter_delayed, delayed_release_time, C_delayed_frame,
                                                        deadline_U_tbs, preemptable_flow, temp_retranse_frame,
                                                        temp_retranse_deadline,
                                                        temp_sched_check, delayed_sche_id)

                        inter_delayed, temp_retranse_frame, temp_retranse_deadline, temp_sched_check = \
                            future_interference_delayed(offline_schedule, inter_delayed, delayed_release_time, C_delayed_frame,
                                                        deadline_U_tbs, preemptable_flow, temp_retranse_frame,
                                                        temp_retranse_deadline,
                                                        temp_sched_check, delayed_sche_id)

                        if delayed_flow_id == preemptable_flow:
                            delayed_response_time = delayed_release_time + C_delayed_frame - 2 + inter_delayed
                        else:
                            delayed_response_time = delayed_release_time + C_delayed_frame + inter_delayed

                        temp_inter = 0
                        temp_deadline_0 = deadline_U_tbs
                        while delayed_response_time > temp_deadline_0:
                            # print("updated response time of delayed frame")
                            temp_compare = delayed_release_time
                            for i in range(len(offline_schedule)):
                                if temp_deadline_0 < offline_schedule[i].start_time < delayed_response_time:

                                    if delayed_response_time - offline_schedule[i].start_time <= 2:
                                        temp_inter += 0
                                    else:
                                        if offline_schedule[i].source == preemptable_flow:

                                            if offline_schedule[i].deadline < deadline_U_tbs:

                                                if offline_schedule[i].start_time - temp_compare > 0:

                                                    if delayed_response_time - offline_schedule[i].start_time <= 2:
                                                        temp_inter += 0
                                                    else:
                                                        temp_inter += offline_schedule[i].end_time - offline_schedule[
                                                            i].start_time \
                                                                      - 1 + pure_preemption_overhead
                                                    temp_compare = offline_schedule[i].end_time

                                                else:
                                                    temp_inter += offline_schedule[i].end_time - offline_schedule[i].start_time \
                                                                  - 1 + pure_preemption_overhead
                                                    temp_compare = offline_schedule[i].end_time
                                                # print("interference of preemptable frame coming after response time",
                                                #       offline_schedule[i].start_time, offline_schedule[i].end_time)
                                            else:
                                                temp_inter += 0
                                                temp_retranse_remain = (offline_schedule[i].end_time - offline_schedule[
                                                    i].start_time)
                                                temp_retranse_remain_deadline = offline_schedule[i].deadline

                                                if temp_retranse_remain > 0:
                                                    temp_retranse_frame.append(temp_retranse_remain)
                                                    temp_retranse_deadline.append(temp_retranse_remain_deadline)
                                                    temp_sched_check.append(i)

                                        else:
                                            if offline_schedule[i].start_time - temp_compare > 0:

                                                if delayed_response_time - offline_schedule[i].start_time <= 2:
                                                    temp_inter += 0
                                                else:
                                                    temp_inter += offline_schedule[i].end_time - offline_schedule[i].start_time \
                                                                  - 1 + pure_preemption_overhead
                                                    # print("interference of ST frame coming after response time",
                                                    #       offline_schedule[i].start_time, offline_schedule[i].end_time)
                                                    temp_compare = offline_schedule[i].end_time
                                            else:
                                                temp_inter += offline_schedule[i].end_time - offline_schedule[i].start_time
                                                temp_compare = offline_schedule[i].end_time
                                                # print("interference of ST frame coming after response time",
                                                #       offline_schedule[i].start_time, offline_schedule[i].end_time)

                            delayed_response_time += temp_inter
                            temp_deadline_0 = delayed_response_time

                    if acceptance_state:
                        accepted_delayed_traffic += 1
                        delayed_count -= 1
                    else:
                        delayed_count -= 1
                        count -= 1

                print("-----------------------------SPRADIC START-------------------------------")
                print(j)
                print("delayed frame check state: delayed_count, count", delayed_count, count)
                if count == 0:
                    print("there is no delayed frame or the already rejected")

                # print("the size of sporadic array", len(sporadic_arrive))
                print("sporadic frame arrive time", sporadic_arrive[j])
                if sporadic_response_time > sporadic_arrive[j]:
                    sporadic_arrive[j] = sporadic_response_time

                print("updated sporadic arrive time: ", sporadic_arrive[j])
                print(sporadic_arrive)
                print(sporadic_C)
                print(mark)
                print(retrans_sched_id)

                if Uti_CBS <= 0:
                    deadline_U_CBS = 1000000000000000
                    C_CBS_remain = C_CBS
                    print("sporadic deadline stay unchanged: ", deadline_U_CBS)
                    print("C_remain is enough for the next frame: ", C_CBS_remain)
                else:
                    if C_CBS_remain >= (deadline_U_CBS - sporadic_arrive[j]) * Uti_CBS:
                        deadline_U_CBS = sporadic_arrive[j] + T_CBS
                        C_CBS_remain = C_CBS
                        print("full capacity and deadline updated: ", deadline_U_CBS)
                    else:
                        print("sporadic deadline stay unchanged: ", deadline_U_CBS)
                        print("C_remain is enough for the next frame: ", C_CBS_remain)


                retransmiss_st_preemptable_frames = []
                retransmiss_st_deadline = []
                sched_check = []

                sporadic_response_time, retransmiss_st_preemptable_frames, retransmiss_st_deadline, C_CBS_remain, \
                deadline_U_CBS, sched_check, delayed_response_time, error, delayed_error = \
                    sporadic_frame_response_time(j, sporadic_C[j], sporadic_arrive[j], offline_schedule, deadline_U_CBS,
                                                 C_CBS_remain, preemptable_flow, sporadic_response_time, mark,
                                                 retrans_sched_id, sporadic_C, sporadic_arrive, delayed_release_time,
                                                 delayed_response_time, deadline_U_tbs, delayed_flow_id, delayed_sche_id, count,
                                                 error, delayed_error, retransmiss_st_preemptable_frames, retransmiss_st_deadline,
                                                 sched_check)

                print(" The response time of ", j, "th sporadic frame is :", sporadic_response_time)

                if delayed_response_time <= delayed_deadline:
                    print("the final delayed response time is:", delayed_response_time)
                else:
                    print(" !!! WARNING delayed frame miss deadline")
                    delayed_error += 1


                if retrans_sched_id[j] == -1:
                    sporadic_response_time_list.append(sporadic_response_time)


                # for i in range(len(retransmiss_st_preemptable_frames)):
                #     count_sporadic += 1
                #     # if retrans_sched_id[j+1] == -1
                #     sporadic_arrive.insert(j + i + 1, sporadic_response_time)
                #
                # for i in range(len(retransmiss_st_preemptable_frames)):
                #     sporadic_C.insert(j + i + 1, retransmiss_st_preemptable_frames[i])
                #
                # for i in range(len(retransmiss_st_deadline)):
                #     mark.insert(j + i + 1, retransmiss_st_deadline[i])
                #
                # for i in range(len(sched_check)):
                #     retrans_sched_id.insert(j + i + 1, sched_check[i])

                print("---------------------results----------------------------")
                print(sporadic_arrive)
                print(sporadic_C)
                print(mark)
                print(retrans_sched_id)
                print(sporadic_deadline)


            else:
                break
        print("---------------------error----------------------------")
        print("the number of delayed frame error", delayed_error)
        print("the preempted ST frame error", error)
        # print("the sporadic response time", sporadic_response_time_list)
        print("round number:", round_number)
        print("accepted delayed frame:", accepted_delayed_traffic)

        # print("original length:", original_length_sporadic)
        print("sporadic frame for each round", sporadic_frame_number)
        print("unscheduable count", unscheduleable_count)

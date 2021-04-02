import numpy as np
import random
import math
import matplotlib.pyplot as plt
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
                                preemptable_flow, temp_retranse_frame, temp_retranse_deadline, temp_sched_check,
                                delayed_sche_id):
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
                            interference += 1
                            print("blocked by preemptable one with lower priority and offline schedule will be updated",
                                  offline_schedule[i].start_time, offline_schedule[i].end_time, interference)
                            # TODO calculate the response time of offline_schedule[i]
                            temp_retranse_remain = (offline_schedule[i].end_time - offline_schedule[i].start_time) \
                                                   - (release_time - offline_schedule[i].start_time + 1) + 0.3

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
                                preemptable_flow, temp_retranse_frame, temp_retranse_deadline, temp_sched_check,
                                delayed_sche_id):
    # print("---------------- interference from future (accumulate) ----------------")
    pure_preemption_overhead = 0.3

    temp_compare = release_time
    for i in range(len(offline_schedule)):
        # interference of the period traffic coming in the future
        if release_time <= offline_schedule[i].start_time < deadline:
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
                              offline_schedule[i].end_time)

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

                print("interference of future ST", offline_schedule[i].start_time, offline_schedule[i].end_time)

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
                                # interference += 2
                                interference += 1
                                print(
                                    "blocked by preemptable one with lower priority and offline schedule will be updated")
                                # TODO calculate the response time of offline_schedule[i]
                                remain_transmission_time = (offline_schedule[i].end_time - offline_schedule[
                                    i].start_time) \
                                                           - (release_time - offline_schedule[i].start_time + 1) + 0.3

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
    temp_compare = release_time

    for i in range(len(offline_schedule)):
        # print("debug", interference)
        # interference of the period traffic coming in the future
        if release_time <= offline_schedule[i].start_time < deadline:
            print("there exist future coming frame")
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
                                  offline_schedule[i].end_time)

                        else:
                            interference += 0

                            if retrans_sched_id[j] != i:
                                remain_transmission_time = offline_schedule[i].end_time - offline_schedule[
                                    i].start_time - 2
                                remain_transmission_deadline = offline_schedule[i].deadline
                                if remain_transmission_time > 0:
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

                        print("interference of future ST", offline_schedule[i].start_time, offline_schedule[i].end_time)

    return interference, retransmiss_st_preemptable_frames, retransmiss_st_deadline, sched_check


def EDF_Scheduling():
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

    window_times = [37, 48, 5, 35, 6]
    period = [200, 200, 50, 200, 200]
    hyper_period = 200
    current_time = 0
    current_period = [1, 1, 1, 1, 1]
    remain_time = [37, 48, 5, 35, 6]
    offset = [0, 0, 0, 0, 0]
    release_times = [0, 0, 0, 0, 0]
    pure_preemption_overhead = 0.3
    preemption_overhead = 2.3
    frame_id = [0, 0, 0, 0, 0]
    fragment_id = [0, 0, 0, 0, 0]
    source = [0, 1, 2, 3, 4]
    destination = [0, 0, 0, 0, 0]
    offline_schedule = []
    count = 0


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


def sporadic_frame_response_time(j, sporadic_c, sporadic_arrive_t, offline_schedule,
                                 preemptable_flow, sporadic_response_time, mark, retrans_sched_id, sporadic_C,
                                 sporadic_arrive, delayed_release_time, delayed_response_time, deadline_U_tbs,
                                 delayed_flow_id, delayed_sche_id, count):
    interference_sporadic = 0
    retransmiss_st_preemptable_frames = []
    retransmiss_st_deadline = []
    sched_check = []
    pure_preemption_overhead = 0.3
    deadline_U_CBS = 0

    if mark[j] != 0:
        deadline_U_CBS = mark[j]
    print("actual assigned deadline:", deadline_U_CBS)

    # if there is frame preempted by sporadic frame is will be created as a new sporadic frame

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

    return sporadic_response_time, retransmiss_st_preemptable_frames, retransmiss_st_deadline, \
           deadline_U_CBS, sched_check, delayed_response_time


def conventional_response_time(delayed_release_time, delayed_deadline, C_delayed_frame, offline_schedule,
                               conven_delayed_response_time):
    interference = 0
    pure_preemption_overhead = 0.3

    for i in range(len(offline_schedule)):
        if offline_schedule[i].start_time < delayed_release_time < offline_schedule[i].end_time:
            # if i == delayed_sche_id:
            #     interference += 0
            # else:
            #     interference += offline_schedule[i].end_time - delayed_release_time
            interference += offline_schedule[i].end_time - delayed_release_time

    temp = delayed_release_time
    for i in range(len(offline_schedule)):
        if delayed_release_time <= offline_schedule[i].start_time < delayed_deadline:
            if delayed_release_time + interference + C_delayed_frame - offline_schedule[i].start_time <= 2:
                interference += 0
            else:
                if offline_schedule[i].start_time - temp > 0:
                    if delayed_release_time + interference + C_delayed_frame - offline_schedule[i].start_time <= 2:
                        interference += 0
                    else:
                        if interference != 0:
                            if offline_schedule[i].start_time - temp < 1:
                                interference += offline_schedule[i].end_time - offline_schedule[
                                    i].start_time
                            else:
                                interference += offline_schedule[i].end_time - offline_schedule[
                                    i].start_time - 1 + pure_preemption_overhead
                        else:
                            interference += offline_schedule[i].end_time - offline_schedule[i].start_time \
                                            - 1 + pure_preemption_overhead
                    temp = offline_schedule[i].end_time
                else:
                    interference += offline_schedule[i].end_time - offline_schedule[i].start_time
                    temp = offline_schedule[i].end_time

        conven_delayed_response_time = delayed_release_time + C_delayed_frame + interference

    return conven_delayed_response_time


if __name__ == "__main__":

    offline_schedule, source, hyper_period, window_times, period, destination, count = EDF_Scheduling()

    preemptable_flow = 1
    pure_preemption_overhead = 0.3
    preemption_overhead = 2.3

    Uti_server_up_bound = 1 - count / (2 * hyper_period)
    sporadic_flow = Frame(0, 0, 0, 0, random.randint(0, 100), 7, 20, 0, 0, "sporadic")

    sporadic_arrive = []
    sporadic_C = []
    mark = []
    retrans_sched_id = []

    delayed_frame_release_time_list = []
    delayed_frame_size_list = []
    delayed_frame_deadline_list = []
    delayed_frame_response_time_list = []
    delayed_id_list = []

    preempted_sched_list = []
    pre_variation = []
    preempted_origi_response_time = []
    preempted_sched_response_time = []


    acceptance_test_state = []
    rejected_count = 0
    accepted_count = 0
    delayed_miss_deadline_count = 0

    conven_deadline_miss = 0
    conven_response_time_list = []
    conven_id_list = []

    variation = []

    round_number = 1000
    preempted_frame_ontime = 0
    preempted_frame_misstime = 0

    for j in range(round_number):

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

        # if delayed_sche_id == preemptable_flow:
        #     C_delayed_frame = time_duration

        utilization_delayed = window_times[delayed_flow_id] / (2 * hyper_period)
        # print(int(math.ceil(start_time)), offline_schedule[delayed_frame_id].deadline - time_duration,
        #      offline_schedule[delayed_frame_id].deadline, window_times[delayed_flow_id])
        delayed_release_time = random.randint(int(math.ceil(start_time)),
                                              offline_schedule[delayed_sche_id].deadline)
        delayed_deadline = offline_schedule[delayed_sche_id].deadline

        delayed_frame = Frame(offline_schedule[delayed_sche_id].frame_Id, offline_schedule[delayed_sche_id].fragment_Id,
                              delayed_deadline, 0, delayed_release_time,
                              time_duration, period[delayed_flow_id], source[delayed_flow_id],
                              destination[delayed_flow_id],
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
        # delayed_frame_release_time_list.append(delayed_release_time)
        # delayed_frame_deadline_list.append(delayed_deadline)
        # delayed_frame_size_list.append(C_delayed_frame)

        conven_delayed_response_time = 0
        conven_delayed_response_time = conventional_response_time(delayed_release_time, delayed_deadline,
                                                                  C_delayed_frame, offline_schedule,
                                                                  conven_delayed_response_time)
        print("conventinal response time:", conven_delayed_response_time)
        #conven_response_time_list.append(conven_delayed_response_time)

        if conven_delayed_response_time > delayed_deadline:
            conven_deadline_miss += 1
        else:
            conven_response_time_list.append(conven_delayed_response_time)
            conven_id_list.append(j)

        Uti_TBS = Uti_server_up_bound - sum(emergency_queue) / (2 * hyper_period)
        print("utilization for TBS:", Uti_TBS)
        if C_delayed_frame <= (delayed_deadline - delayed_release_time) * Uti_TBS:
            acceptance_state = True
            accepted_count += 1
            deadline_U_tbs = max(delayed_release_time, deadline_U_tbs) + C_delayed_frame / Uti_TBS
            print("********* Acceptance test passed from uti ***********:")
            print("TBS assigned deadline:", deadline_U_tbs)
        else:
            # temp_start = delayed_deadline - C_delayed_frame - 2
            temp_in = 0
            for i in range(len(offline_schedule)):
                if offline_schedule[i].start_time < delayed_release_time < offline_schedule[i].end_time:
                    print(offline_schedule[i].start_time, offline_schedule[i].end_time)
                    if i == delayed_sche_id:
                        temp_in += 0
                        print("delayed frame is released within its offline scheduled time")
                    else:
                        if offline_schedule[i].source == preemptable_flow:
                            if offline_schedule[i].deadline < delayed_deadline:
                                temp_in += offline_schedule[i].end_time - delayed_release_time
                            else:
                                if offline_schedule[i].end_time - delayed_release_time > 2:
                                    temp_in += 1
                                else:
                                    temp_in += offline_schedule[i].end_time - delayed_release_time
                            print("##", temp_in)
                        else:
                            temp_in += offline_schedule[i].end_time - delayed_release_time
                            print("@@", temp_in)

            for i in range(len(offline_schedule)):
                if delayed_release_time <= offline_schedule[i].start_time < delayed_deadline:
                    if delayed_release_time + C_delayed_frame + temp_in - offline_schedule[i].start_time <= 2:
                        temp_in += 0
                        print("$$", temp_in)
                    else:
                        if offline_schedule[i].source == preemptable_flow:
                            if offline_schedule[i].deadline < delayed_deadline:
                                temp_in += offline_schedule[i].end_time - offline_schedule[i].start_time
                                print("&&", temp_in)
                            else:
                                temp_in += 0
                        else:
                            temp_in += offline_schedule[i].end_time - offline_schedule[i].start_time
                            print("@#$", temp_in)

            slack = delayed_deadline - delayed_release_time - temp_in

            if slack >= C_delayed_frame:
                acceptance_state = True
                accepted_count += 1
                deadline_U_tbs = delayed_deadline
                print("******** Acceptance test  passed with slack time *********:", slack)
                print("assigned deadline:", deadline_U_tbs)
            else:
                emergency_action = True
                acceptance_state = False
                rejected_count += 1
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
                print("updated response time of delayed frame")
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

            if delayed_response_time <= delayed_deadline:

                acceptance_test_state.append(1)
                emergency_queue.append(C_delayed_frame)
                print(" the Response time of delayed frame is: ", delayed_response_time)
                delayed_frame_response_time_list.append(delayed_response_time)
                delayed_frame_release_time_list.append(delayed_release_time)
                delayed_frame_deadline_list.append(delayed_deadline)
                delayed_frame_size_list.append(C_delayed_frame)
                delayed_id_list.append(j)

                if temp_retranse_frame:
                    print("There is preempted ST frame", temp_retranse_frame)
                    for i in range(len(temp_retranse_frame)):
                        sporadic_arrive.append(delayed_response_time)
                        sporadic_C.append(temp_retranse_frame[i])
                        mark.append(temp_retranse_deadline[i])
                        retrans_sched_id.append(temp_sched_check[i])

            else:
                delayed_miss_deadline_count += 1
                acceptance_test_state.append(0)
                #delayed_frame_response_time_list.append(delayed_response_time)
                print(
                    "!!! @@@#### WARNING  acceptance test 2 failed. The delayed st frame can not be handled before its "
                    "deadline")

            while sporadic_arrive:
                print(sporadic_arrive)
                print(sporadic_C)
                print(mark)
                print(retrans_sched_id)

                for j in range(len(sporadic_arrive)):

                    print("-----------------------------Preempted ST frame-------------------------------")
                    print(j)
                    # print("the size of sporadic array", len(sporadic_arrive))
                    print("the preempted ST frame release time", sporadic_arrive[j])

                    print(sporadic_arrive)
                    print(sporadic_C)
                    print(mark)
                    print(retrans_sched_id)

                    sporadic_response_time = 0
                    sporadic_response_time, retransmiss_st_preemptable_frames, retransmiss_st_deadline, \
                    deadline_U_CBS, sched_check, delayed_response_time = \
                        sporadic_frame_response_time(j, sporadic_C[j], sporadic_arrive[j], offline_schedule,
                                                     preemptable_flow, sporadic_response_time, mark,
                                                     retrans_sched_id, sporadic_C, sporadic_arrive, delayed_release_time,
                                                     delayed_response_time, deadline_U_tbs, delayed_flow_id,
                                                     delayed_sche_id, count)

                    if sporadic_response_time <= mark[j]:
                        preempted_frame_ontime += 1

                        print("the preempted response time is:", sporadic_response_time)
                        print("it's original response time:", offline_schedule[retrans_sched_id[j]].end_time)
                        print("variation", sporadic_response_time - offline_schedule[retrans_sched_id[j]].end_time)

                        preempted_sched_list.append(retrans_sched_id[j])
                        preempted_origi_response_time.append(offline_schedule[retrans_sched_id[j]].end_time)
                        preempted_sched_response_time.append(sporadic_response_time)
                        sporadic_arrive.pop(0)
                        sporadic_C.pop(0)
                        mark.pop(0)
                        retrans_sched_id.pop(0)

                    else:
                        print(" !!! WARNING preempted ST frame miss deadline")
                        preempted_frame_misstime += 1

                    if retransmiss_st_preemptable_frames:
                        print("There is another preempted ST frame", retransmiss_st_preemptable_frames)
                        for i in range(len(retransmiss_st_preemptable_frames)):
                            sporadic_arrive.append(sporadic_response_time)
                            sporadic_C.append(retransmiss_st_preemptable_frames[i])
                            mark.append(retransmiss_st_deadline[i])
                            retrans_sched_id.append(sched_check[i])

                        print(sporadic_arrive)
                        print(sporadic_C)
                        print(mark)
                        print(retrans_sched_id)

    print("")
    print("-----------------------Results-------------------------------")
    # print("release time:", delayed_frame_release_time_list)
    # print("frame size:", delayed_frame_size_list)
    # print("response time:", delayed_frame_response_time_list)
    # print("deadline:", delayed_frame_deadline_list)
    # print("acceptance state:", acceptance_test_state)
    print("conventional deadline missing number: ", conven_deadline_miss)
    print("average response time of conventional method: ", np.mean(conven_response_time_list))

    # print("the accepted round of conventional method:", conven_id_list)
    print("----------------------With emergency queue-------------------------------")
    print("accepted num: ", accepted_count)
    print("rejected num: ", rejected_count)
    print("accepted delayed frame deadline missing:", delayed_miss_deadline_count)
    print("average response time of proposed method:", np.mean(delayed_frame_response_time_list))
    # print("the accepted round of proposed mothod:", delayed_id_list)

    a = [x for x in conven_id_list if x in delayed_id_list]
    b = [y for y in (conven_id_list + delayed_id_list) if y not in a]
    print("the difference of accepted delayed frame:", len(b))

    if len(b) == 0:
        for i in range(len(delayed_frame_response_time_list)):
            variation_value = conven_response_time_list[i] - delayed_frame_response_time_list[i]
            if variation_value < 0.001:
                variation_value = 0
            variation.append(variation_value)

        # print("variation:", variation)
        print("average reduce time:", np.mean(variation))
        print("maximum reduce time:", max(variation))
        print("minimum reduce time:", min(variation))
        # plt.scatter(delayed_frame_release_time_list, variation)
        # plt.show()



    print("----------------------Interference to preemptable ST frame----------------------")
    # print("the preempted ST sched_id:", preempted_sched_list)
    # print("the response time of preempted sched_id:", preempted_sched_response_time)
    # print("the original response time of preempted sched_id:", preempted_origi_response_time)
    print("the number of ontime preempted ST frame:", preempted_frame_ontime)
    print("the number of mistime preempted ST frame:", preempted_frame_misstime)
    if preempted_frame_ontime:
        for i in range(len(preempted_sched_response_time)):
            pre_variation_value = preempted_sched_response_time[i] - preempted_origi_response_time[i]
            if -2 <= pre_variation_value <= 0:
                pre_variation_value = 0
            pre_variation.append(pre_variation_value)
            # print("Jitter of preempted ST frame:", pre_variation)
        print("average jitter:", np.mean(pre_variation))
        print("maximum jitter:", max(pre_variation))
        print("minimum jitter:", min(pre_variation))

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
                                preemptable_flow, temp_retranse_frame, temp_retranse_deadline, temp_sched_check):
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

                            if abs(temp_retranse_remain - offline_schedule[i].end_time + offline_schedule[i].start_time) < 2:
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
                                preemptable_flow, temp_retranse_frame, temp_retranse_deadline, temp_sched_check):
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
                            retransmiss_st_preemptable_frames.append(remain_transmission_time)
                            retransmiss_st_deadline.append(remain_transmission_deadline)
                            sched_check.append(i)

                else:
                    if offline_schedule[i].start_time - temp_compare > 0:
                        if release_time + interference + transmission_time - offline_schedule[i].start_time <= 2:
                            interference += 0
                        else:
                            if interference != 0:
                                if offline_schedule[i - 1].source == preemptable_flow:
                                    interference += offline_schedule[i].end_time - offline_schedule[
                                        i].start_time - 1 + pure_preemption_overhead
                                else:
                                    if offline_schedule[i].start_time - offline_schedule[i - 1].end_time < 1:
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
                              sched_check):
    pure_preemption_overhead = 0.3
    print("------------ interference from active --------------")
    # print(retrans_sched_id[j])
    print("interference", interference)
    for i in range(len(offline_schedule)):
        # interference of active periodic traffic
        if offline_schedule[i].start_time < release_time < offline_schedule[i].end_time:
            if i == delayed_sche_id:
                interference += 0
                print("delayed frame is released within its offline scheduled time")
            else:
                if offline_schedule[i].source == preemptable_flow:
                    # need to check if the active frame belongs to preempable flow
                    if retrans_sched_id[j] == i:
                        print("the frame is previous preempted one and is retransmitted")
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
                              sched_check):
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
                                    if offline_schedule[i - 1].source == preemptable_flow:
                                        interference += offline_schedule[i].end_time - offline_schedule[
                                            i].start_time - 1 + pure_preemption_overhead
                                    else:
                                        if offline_schedule[i].start_time - offline_schedule[i - 1].end_time < 1:
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

    window_times = [4, 62, 6, 15]
    period = [100, 200, 100, 200]
    hyper_period = 200
    current_time = 0
    current_period = [1, 1, 1, 1]
    remain_time = [4, 62, 6, 15]
    offset = [0, 0, 0, 0]
    release_times = [0, 0, 0, 0]
    pure_preemption_overhead = 0.3
    preemption_overhead = 2.3
    frame_id = [0, 0, 0, 0]
    fragment_id = [0, 0, 0, 0]
    source = [0, 1, 2, 3]
    destination = [0, 0, 0, 0]
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


def sporadic_frame_response_time(j, sporadic_c, sporadic_arrive_t, offline_schedule, deadline_U_CBS, C_CBS_remain,
                                 preemptable_flow, sporadic_response_time, mark, retrans_sched_id, sporadic_C,
                                 sporadic_arrive, delayed_release_time, delayed_response_time):
    interference_sporadic = 0
    retransmiss_st_preemptable_frames = []
    retransmiss_st_deadline = []
    sched_check = []
    pure_preemption_overhead = 0.3

    deadline_U_CBS_backpack = deadline_U_CBS

    if mark[j] != 0:
        deadline_U_CBS = mark[j]
    print("actual assigned deadline:", deadline_U_CBS)

    # if there is frame preempted by sporadic frame is will be created as a new sporadic frame
    while sporadic_C[j] > 0:

        remain_transmission_time = 0
        remain_transmission_deadline = 0
        sporadic_c_backpack = sporadic_C[j]
        interference_sporadic, retransmiss_st_preemptable_frames, retransmiss_st_deadline, sched_check = \
            active_frame_interference(j, offline_schedule, interference_sporadic, sporadic_arrive[j],
                                      sporadic_C[j], deadline_U_CBS, preemptable_flow, remain_transmission_time,
                                      remain_transmission_deadline, retransmiss_st_preemptable_frames,
                                      retransmiss_st_deadline, retrans_sched_id, sched_check)

        interference_sporadic, retransmiss_st_preemptable_frames, retransmiss_st_deadline, sched_check = \
            future_frame_interference(j, offline_schedule, interference_sporadic, sporadic_arrive[j],
                                      sporadic_C[j], deadline_U_CBS, preemptable_flow, remain_transmission_time,
                                      remain_transmission_deadline, retransmiss_st_preemptable_frames,
                                      retransmiss_st_deadline, retrans_sched_id, sched_check)

        print("interference :", interference_sporadic)
        # if mark[j] != 0:
        #     deadline_U_CBS = deadline_U_CBS_backpack
        #     sporadic_response_time = sporadic_arrive_t + sporadic_c + interference_sporadic
        #     sporadic_c = 0
        #     print("handling preempted ST frame, the response time is:", sporadic_response_time)
        #     if sporadic_response_time > mark[j]:
        #         print("!!!!!!!!!!!!!!!!!!!!warning!!!!!!!!!!!!!!!!!!!!!!!!!!!!")
        #         print(" warning the ST frame missing deadline, previous sporadic frame will be dropped ")
        #
        if sporadic_arrive[j] <= delayed_release_time < sporadic_response_time:
            print("interrupted by delayed frame")
            if sporadic_response_time - delayed_release_time < 2:
                delayed_response_time += sporadic_response_time - delayed_release_time
                print("the delayed response time is updated:", delayed_response_time)
            else:
                sporadic_C[j] -= delayed_release_time - sporadic_arrive[j] + 1
                delayed_response_time += 1
                sporadic_arrive[j] = delayed_response_time

            if sporadic_arrive[j + 1] < delayed_response_time:
                sporadic_arrive[j + 1] = delayed_response_time

        if mark[j] != 0:

            sporadic_response_time = sporadic_arrive[j] + sporadic_C[j] + interference_sporadic
            if mark[j + 1] == 0:

                if sporadic_arrive[j] <= sporadic_arrive[j + 1] < sporadic_response_time and deadline_U_CBS \
                        > deadline_U_CBS_backpack:
                    if sporadic_response_time - sporadic_arrive[j + 1] > 2:
                        print(" preempted by the sporadic frame")
                        # sporadic_c_backpack = sporadic_C[j]
                        if sporadic_arrive[j] == sporadic_arrive[j + 1]:
                            sporadic_C[j] -= 0
                        else:
                            sporadic_C[j] = sporadic_C[j] - (sporadic_arrive[j + 1] - sporadic_arrive[j] + 1) + 0.3

                        print("remain preempted frame is: ", sporadic_C[j])

                        if sporadic_C[j] < 0:
                            temp = 0
                            for i in range(len(offline_schedule)):
                                if offline_schedule[i].start_time <= sporadic_arrive[j] <= offline_schedule[
                                    i].end_time and i != preemptable_flow and i != delayed_sche_id:
                                    sporadic_C[j] = sporadic_c_backpack
                                    interference_sporadic = 0
                                    break
                                elif offline_schedule[i].start_time > sporadic_arrive[j] and i != preemptable_flow and i != delayed_sche_id:
                                    temp = offline_schedule[i].start_time
                                    sporadic_C[j] = sporadic_c_backpack - (temp - sporadic_arrive[j] + 1) + 0.3
                                    if sporadic_C[j] <= 2:
                                        sporadic_response_time = sporadic_arrive[j] + sporadic_C[
                                            j] + interference_sporadic
                                        print("the response time of preempted frame", retrans_sched_id[j], "is: ",
                                              sporadic_response_time)
                                        deadline_U_CBS = deadline_U_CBS_backpack
                                        sporadic_C[j] = 0
                                        interference_sporadic = 1
                                        if sporadic_response_time > mark[j]:
                                            print("!!!!!!!!!!!!!!!!!!!!warning!!!!!!!!!!!!!!!!!!!!!!!!!!!!")
                                            print(
                                                "warning the ST frame missing deadline, previous sporadic frame will "
                                                "be dropped ")
                                    break
                            if temp != 0:
                                sporadic_C[j] = sporadic_c_backpack - (temp - sporadic_arrive[j] + 1) + 0.3
                            else:
                                sporadic_C[j] = sporadic_c_backpack
                        else:
                            interference_sporadic = 1

                        sporadic_C[j], sporadic_C[j + 1] = sporadic_C[j + 1], sporadic_C[j]
                        mark[j], mark[j + 1] = mark[j + 1], mark[j]
                        retrans_sched_id[j + 1] = retrans_sched_id[j]
                        sporadic_arrive[j] = sporadic_arrive[j + 1]

                        deadline_U_CBS = deadline_U_CBS_backpack
                        print("ATTENTION ")
                        print(sporadic_arrive)
                        print(sporadic_C)
                        print(mark)
                        print(retrans_sched_id)
                    else:
                        sporadic_response_time = sporadic_arrive[j] + sporadic_C[j] + interference_sporadic
                        sporadic_C[j] = 0
                        print("the response time of preempted frame", retrans_sched_id[j], "is: ",
                              sporadic_response_time)
                        deadline_U_CBS = deadline_U_CBS_backpack
                        if sporadic_response_time > mark[j]:
                            print("!!!!!!!!!!!!!!!!!!!!warning!!!!!!!!!!!!!!!!!!!!!!!!!!!!")
                            print(" warning the ST frame missing deadline, previous sporadic frame will be dropped ")
                else:
                    sporadic_response_time = sporadic_arrive[j] + sporadic_C[j] + interference_sporadic
                    sporadic_C[j] = 0
                    print("the response time of preempted frame", retrans_sched_id[j], "is: ", sporadic_response_time)
                    deadline_U_CBS = deadline_U_CBS_backpack
                    if sporadic_response_time > mark[j]:
                        print("!!!!!!!!!!!!!!!!!!!!warning!!!!!!!!!!!!!!!!!!!!!!!!!!!!")
                        print(" warning the ST frame missing deadline, previous sporadic frame will be dropped ")
            else:

                sporadic_response_time = sporadic_arrive[j] + sporadic_C[j] + interference_sporadic
                sporadic_C[j] = 0
                print("the response time of preempted frame", retrans_sched_id[j], "is: ", sporadic_response_time)
                deadline_U_CBS = deadline_U_CBS_backpack
                if sporadic_response_time > mark[j]:
                    print("!!!!!!!!!!!!!!!!!!!!warning!!!!!!!!!!!!!!!!!!!!!!!!!!!!")
                    print(" warning the ST frame missing deadline, previous sporadic frame will be dropped ")

        else:
            temp_int = 0
            temp_deadline_1 = deadline_U_CBS

            if C_CBS_remain > sporadic_C[j]:
                print("the parameters", C_CBS_remain, sporadic_arrive[j], sporadic_C[j],
                      interference_sporadic)
                sporadic_response_time = sporadic_arrive[j] + sporadic_C[j] + interference_sporadic
                while sporadic_response_time > temp_deadline_1:
                    print("updated response time of delayed frame")
                    compare_para = sporadic_response_time
                    for i in range(len(offline_schedule)):
                        if temp_deadline_1 < offline_schedule[i].start_time < sporadic_response_time:
                            if sporadic_response_time - offline_schedule[i].start_time <= 2:
                                temp_int += 0
                            else:
                                if offline_schedule[i].source == preemptable_flow:

                                    if offline_schedule[i].deadline < deadline_U_CBS:
                                        if offline_schedule[i].start_time - compare_para > 0:
                                            if sporadic_response_time - offline_schedule[i].start_time <= 2:
                                                temp_int += 0
                                            else:
                                                temp_int += offline_schedule[i].end_time - \
                                                            offline_schedule[i].start_time - 1 + \
                                                            pure_preemption_overhead
                                            compare_para = offline_schedule[i].end_time
                                        else:
                                            temp_int += offline_schedule[i].end_time - offline_schedule[i].start_time
                                            compare_para = offline_schedule[i].end_time
                                    else:
                                        temp_int += 0
                                        remain_transmission_time = (offline_schedule[i].end_time - offline_schedule[
                                            i].start_time)
                                        remain_transmission_deadline = offline_schedule[i].deadline
                                        if remain_transmission_time > 0:
                                            retransmiss_st_preemptable_frames.append(remain_transmission_time)
                                            retransmiss_st_deadline.append(remain_transmission_deadline)
                                            sched_check.append(i)

                                else:
                                    if offline_schedule[i].start_time - compare_para > 0:
                                        if sporadic_response_time - offline_schedule[i].start_time <= 2:
                                            temp_int += 0
                                        else:
                                            temp_int += offline_schedule[i].end_time - \
                                                        offline_schedule[i].start_time - 1 + \
                                                        pure_preemption_overhead
                                        compare_para = offline_schedule[i].end_time
                                    else:
                                        temp_int += offline_schedule[i].end_time - offline_schedule[i].start_time
                                        compare_para = offline_schedule[i].end_time

                                        print("interference of preemptable frame coming after response time",
                                              offline_schedule[i].start_time, offline_schedule[i].end_time)
                    print("temp_int", temp_int)
                    sporadic_response_time += temp_int
                    temp_deadline_1 = sporadic_response_time


                C_CBS_remain -= sporadic_C[j]
                sporadic_C[j] = 0
                print("remain capacity for following sporadic frame: ", C_CBS_remain)
                print("response time of sporadic frame:", sporadic_response_time)
                sporadic_Rt.append(sporadic_response_time)
            else:
                sporadic_response_time = sporadic_arrive[j] + C_CBS_remain + interference_sporadic
                print("restart because of the server capacity exhausted temporary sporadic response time: ",
                      sporadic_response_time)
                sporadic_arrive[j] = sporadic_response_time
                interference_sporadic = 0
                sporadic_C[j] = sporadic_C[j] - C_CBS_remain

                deadline_U_CBS += T_CBS
                C_CBS_remain = C_CBS
                print("sporadic frame is fragmented and keep in the current loop, "
                      "capacity replenishment and update deadline",
                      C_CBS_remain, deadline_U_CBS)\

        # if sporadic_arrive[j] <= delayed_release_time < sporadic_response_time:
        #     print("!! delayed traffic released during the sporadic transmission !!")
        #     if 0 < sporadic_c_backpack - (delayed_release_time - sporadic_arrive[j]) <= 2:
        #         sporadic_response_time += 0
        #         delayed_response_time += sporadic_c_backpack - (delayed_release_time - sporadic_arrive[j])
        #     else:
        #         sporadic_response_time = sporadic_response_time + C_delayed_frame - 1
        #         delayed_response_time += 1


    return sporadic_response_time, retransmiss_st_preemptable_frames, retransmiss_st_deadline, \
           C_CBS_remain, deadline_U_CBS, sched_check, delayed_response_time


if __name__ == "__main__":

    offline_schedule, source, hyper_period, window_times, period, destination, count = EDF_Scheduling()

    preemptable_flow = 1
    pure_preemption_overhead = 0.3
    preemption_overhead = 2.3

    Uti_server_up_bound = 1 - count / (2 * hyper_period)
    sporadic_flow = Frame(0, 0, 0, 0, random.randint(0, 100), 7, 20, 0, 0, "sporadic")

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
                                          offline_schedule[delayed_sche_id].deadline - time_duration)
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
    print(sporadic_arrive)

    sporadic_C = []
    for i in range(len(sporadic_arrive)):
        sporadic_C.append(C_sporadic)
    print(sporadic_C)

    mark = []
    for i in range(len(sporadic_arrive)):
        mark.append(0)
    print(mark)

    retrans_sched_id = []
    for i in range(len(sporadic_arrive)):
        retrans_sched_id.append(-1)
    print(retrans_sched_id)

    print("")
    print("-----------------------CBS parameter setup----------------------------------")

    # C_sporadic_avg = math.floor(np.median(window_times))
    C_sporadic_avg = 10
    max_preemption_times = math.floor(C_sporadic_avg / 2)
    max_preemption_overhead = max_preemption_times * pure_preemption_overhead
    # print(max_preemption_overhead)

    Uti_CBS = Uti_server_up_bound + utilization_delayed - \
              sum(emergency_queue) / (2 * hyper_period)

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

    # 如果有多个delay 需要再加一个循环
    Uti_TBS = Uti_server_up_bound - sum(emergency_queue) / (2 * hyper_period)
    print("utilization for TBS:", Uti_TBS)
    for j in range(len(sporadic_arrive)):

        # 此处做接受测试 其结果会对Uti_cbs进行更改。只有在通过测试之后 delayed frame 才能入queue


        if delayed_count >= 1:
            if C_delayed_frame <= (delayed_deadline - delayed_release_time) * Uti_TBS:
                acceptance_state = True
                deadline_U_tbs = max(delayed_release_time, deadline_U_tbs) + C_delayed_frame / Uti_TBS
                print("*********acceptance test 1 passed from uti***********:")
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
                print("Slack for delayed traffic", slack)
                if slack >= C_delayed_frame:
                    acceptance_state_1 = True
                    deadline_U_tbs = delayed_deadline
                    print("********acceptance test 1 passed with slack time *********:", slack)
                    print("assigned deadline:", deadline_U_tbs)
                else:
                    emergency_action = True
                    acceptance_state_1 = False
                    print(
                        "!$$$WARNING: The delayed traffic can not be transmitted within its deadline and emergency "
                        "action should be triggered ! ")

            inter_delayed = 0
            temp_retranse_deadline = []
            temp_retranse_frame = []
            temp_sched_check = []
            inter_delayed, temp_retranse_frame, temp_retranse_deadline, temp_sched_check = \
                active_interference_delayed(offline_schedule, inter_delayed, delayed_release_time, C_delayed_frame,
                                            deadline_U_tbs, preemptable_flow, temp_retranse_frame,
                                            temp_retranse_deadline,
                                            temp_sched_check)

            if inter_delayed == 0:
                if sporadic_arrive[j] <= delayed_release_time < sporadic_arrive[j] + sporadic_C[j]:
                    if sporadic_arrive[j] + sporadic_C[j] - delayed_release_time > 2:
                        inter_delayed += 1
                    else:
                        inter_delayed += sporadic_arrive[j] + sporadic_C[j] - delayed_release_time

            inter_delayed, temp_retranse_frame, temp_retranse_deadline, temp_sched_check = \
                future_interference_delayed(offline_schedule, inter_delayed, delayed_release_time, C_delayed_frame,
                                            deadline_U_tbs, preemptable_flow, temp_retranse_frame,
                                            temp_retranse_deadline,
                                            temp_sched_check)

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
                acceptance_state = True
                emergency_queue.append(C_delayed_frame)
                delayed_count -= 1
                print("acceptance test 2 passed:", acceptance_state)
                print(" the response time of delayed frame is: ", delayed_response_time)

                if delayed_release_time < sporadic_arrive[j] < delayed_response_time:
                    sporadic_arrive[j] = delayed_response_time

            else:
                acceptance_state = False
                print(
                    "!!! @@@#### WARNING  acceptance test 2 failed. The delayed st frame can not be handled before its "
                    "deadline")

        print("-----------------------------SPRADIC START-------------------------------")
        print(j)

        print("sporadic frame arrive time", sporadic_arrive[j])
        if sporadic_response_time > sporadic_arrive[j]:
            sporadic_arrive[j] = sporadic_response_time

        print("updated sporadic arrive time: ", sporadic_arrive[j])
        if C_CBS_remain >= (deadline_U_CBS - sporadic_arrive[j]) * Uti_CBS:
            deadline_U_CBS = sporadic_arrive[j] + T_CBS
            C_CBS_remain = C_CBS
            print("full capacity and deadline updated: ", deadline_U_CBS)
        else:
            print("sporadic deadline stay unchanged: ", deadline_U_CBS)
            print("C_remain is enough for the next frame: ", C_CBS_remain)

        sporadic_response_time, retransmiss_st_preemptable_frames, retransmiss_st_deadline, C_CBS_remain, \
        deadline_U_CBS, sched_check, delayed_response_time = \
            sporadic_frame_response_time(j, sporadic_C[j], sporadic_arrive[j], offline_schedule, deadline_U_CBS,
                                         C_CBS_remain, preemptable_flow, sporadic_response_time, mark,
                                         retrans_sched_id, sporadic_C, sporadic_arrive, delayed_release_time,
                                         delayed_response_time)

        print(" The response time of ", j, "th sporadic frame is :", sporadic_response_time)

        if delayed_response_time <= delayed_deadline:
            print("the final delayed response time is:", delayed_response_time)
        else:
            print(" !!! WARNING delayed frame miss deadline")

        for i in range(len(retransmiss_st_preemptable_frames)):
            sporadic_arrive.insert(j + i + 1, sporadic_response_time)

        for i in range(len(retransmiss_st_preemptable_frames)):
            sporadic_C.insert(j + i + 1, retransmiss_st_preemptable_frames[i])

        for i in range(len(retransmiss_st_deadline)):
            mark.insert(j + i + 1, retransmiss_st_deadline[i])

        for i in range(len(sched_check)):
            retrans_sched_id.insert(j + i + 1, sched_check[i])

        print(sporadic_arrive)
        print(sporadic_C)
        print(mark)
        print(retrans_sched_id)

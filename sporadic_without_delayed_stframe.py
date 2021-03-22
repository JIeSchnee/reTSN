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


def active_frame_interference(j, offline_schedule, interference, release_time, transmission_time, deadline,
                              preemptable_flow, remain_transmission_time, remain_transmission_deadline,
                              retransmiss_st_preemptable_frames, retransmiss_st_deadline, retrans_sched_id,
                              sched_check):
    print("------------ interference from active --------------")
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
                                if remain_transmission_time > offline_schedule[i].end_time - \
                                        offline_schedule[i].start_time - 2:
                                    remain_transmission_time = offline_schedule[i].end_time - \
                                                               offline_schedule[i].start_time - 2

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

            print("interference of active one with higher priority:", offline_schedule[i].start_time,
                  offline_schedule[i].end_time, interference)

    return interference, retransmiss_st_preemptable_frames, retransmiss_st_deadline, sched_check


def future_frame_interference(j, offline_schedule, interference, release_time, transmission_time, deadline,
                              preemptable_flow, remain_transmission_time, remain_transmission_deadline,
                              retransmiss_st_preemptable_frames, retransmiss_st_deadline, retrans_sched_id,
                              sched_check):
    print("---------------- interference from future (accumulate) ----------------")
    #print(release_time)
    #print(deadline)
    temp_compare = release_time
    for i in range(len(offline_schedule)):
        #print("debug", interference)
        # interference of the period traffic coming in the future
        if release_time <= offline_schedule[i].start_time < deadline:
            print("there exist future coming frame")
            if release_time + interference + transmission_time - offline_schedule[i].start_time <= 2:
                interference += 0
            else:
                if offline_schedule[i].source == preemptable_flow:

                    if offline_schedule[i].deadline < deadline:

                        # if release_time - interference - transmission_time - offline_schedule[i].start_time <= 2:
                        #     interference += 0
                        # else:

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
                        remain_transmission_time = offline_schedule[i].end_time - offline_schedule[i].start_time
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
                                 preemptable_flow, sporadic_response_time, mark, retrans_sched_id):
    interference_sporadic = 0
    retransmiss_st_preemptable_frames = []
    retransmiss_st_deadline = []
    sched_check = []

    deadline_U_CBS_backpack = deadline_U_CBS

    if mark[j] != 0:
        deadline_U_CBS = mark[j]

    print("actual assigned deadline:", deadline_U_CBS)

    deadline_U_CBS = deadline_U_CBS_backpack

    # if there is frame preempted by sporadic frame is will be created as a new sporadic frame
    while sporadic_c > 0:

        remain_transmission_time = 0
        remain_transmission_deadline = 0
        interference_sporadic, retransmiss_st_preemptable_frames, retransmiss_st_deadline, sched_check = \
            active_frame_interference(j, offline_schedule, interference_sporadic, sporadic_arrive_t,
                                      sporadic_c, deadline_U_CBS, preemptable_flow, remain_transmission_time,
                                      remain_transmission_deadline, retransmiss_st_preemptable_frames,
                                      retransmiss_st_deadline, retrans_sched_id, sched_check)

        interference_sporadic, retransmiss_st_preemptable_frames, retransmiss_st_deadline, sched_check = \
            future_frame_interference(j, offline_schedule, interference_sporadic, sporadic_arrive_t,
                                      sporadic_c, deadline_U_CBS, preemptable_flow, remain_transmission_time,
                                      remain_transmission_deadline, retransmiss_st_preemptable_frames,
                                      retransmiss_st_deadline, retrans_sched_id, sched_check)

        print("interference :", interference_sporadic)

        if mark[j] != 0:
            print("#########################################################")
            sporadic_response_time = sporadic_arrive_t + sporadic_c + interference_sporadic
            sporadic_c = 0
            print("handling preempted ST frame, the response time is:", sporadic_response_time)
            if sporadic_response_time > deadline_U_CBS:
                print(" warning the ST frame missing deadline, previous sporadic frame will be dropped ")

        # if response time larger than assigned deadline, the interference coming after assigned deadline need
        # to be calculated
        else:
            temp_int = 0
            temp_deadline_1 = deadline_U_CBS
            if C_CBS_remain > sporadic_c:
                sporadic_response_time = sporadic_arrive_t + sporadic_c + interference_sporadic
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

                    sporadic_response_time += temp_int
                    temp_deadline_1 = sporadic_response_time

                C_CBS_remain = C_CBS_remain - sporadic_c
                sporadic_c = 0
                print("remain capacity for following sporadic frame: ", C_CBS_remain)
                print("response time of sporadic frame:", sporadic_response_time)
                sporadic_Rt.append(sporadic_response_time)
            else:
                sporadic_response_time = sporadic_arrive_t + sporadic_c + interference_sporadic
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

                    sporadic_response_time += temp_int
                    temp_deadline_1 = sporadic_response_time

                C_CBS_remain = C_CBS
                sporadic_c = sporadic_c - C_CBS_remain
                deadline_U_CBS += T_CBS
                print("sporadic frame is fragmented and keep in the current loop, "
                      "capacity replenishment and update deadline",
                      C_CBS_remain, deadline_U_CBS)



    return sporadic_response_time, retransmiss_st_preemptable_frames, retransmiss_st_deadline, \
           C_CBS_remain, deadline_U_CBS, sched_check


if __name__ == "__main__":

    offline_schedule, source, hyper_period, window_times, period, destination, count = EDF_Scheduling()

    preemptable_flow = 1
    pure_preemption_overhead = 0.3
    preemption_overhead = 2.3

    Uti_server_up_bound = 1 - count / (2 * hyper_period)
    sporadic_flow = Frame(0, 0, 0, 0, random.randint(0, 100), 7, 20, 0, 0, "sporadic")

    print("-----------------------------------------------------------------------------------")
    print("                   Assume no delayed ST frame                                      ")
    emergency_queue = []
    utilization_delayed = 0
    delayed_sche_id = 10000000000000000
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
              sum(emergency_queue[i].transmission_time for i in range(len(emergency_queue))) / (2 * hyper_period)

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
    sim_time = 0
    while sim_time < 2 * hyper_period:
        for j in range(len(sporadic_arrive)):
            print("---------------------------------------------------------------------------")
            print(j)
            print("sporadic frame arrive time", sporadic_arrive[j])
            if sporadic_response_time > sporadic_arrive[j]:
                sporadic_arrive[j] = sporadic_response_time

            print("updated sporadic arrive time: ", sporadic_arrive[j])
            if C_CBS_remain >= (deadline_U_CBS - sporadic_arrive[j]) * Uti_CBS:
                deadline_U_CBS = sporadic_arrive[j] + T_CBS
                C_CBS_remain = C_CBS
                print("full capacity and deadline: ", deadline_U_CBS)
            else:
                print("sporadic deadline stay unchanged: ", deadline_U_CBS)
                print("C_remain is enough for the next frame: ", C_CBS_remain)

            sporadic_response_time, retransmiss_st_preemptable_frames, retransmiss_st_deadline, C_CBS_remain, \
            deadline_U_CBS, sched_check = \
                sporadic_frame_response_time(j, sporadic_C[j], sporadic_arrive[j], offline_schedule, deadline_U_CBS,
                                             C_CBS_remain, preemptable_flow, sporadic_response_time, mark,
                                             retrans_sched_id)

            # 此处进行剩下的被抢占帧的处理
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

            sim_time += sporadic_response_time
            # if sim_time > 2*hyper_period:
            #     break

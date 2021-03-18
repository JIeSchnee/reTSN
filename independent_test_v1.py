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


if __name__ == "__main__":
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

    preemptable_flow = 1

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

    sporadic_flow = Frame(0, 0, 0, 0, random.randint(0, 100), 4, 20, 0, 0, "sporadic")

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

    print("-------------------- simulation ---------------------------")
    delayed_flow_id = random.randint(0, max(source))
    temp = []
    frame_id_check = []
    fragment_check = []
    deadline_U_tbs = 0
    for i in range(len(offline_schedule)):
        if offline_schedule[i].source == delayed_flow_id:
            temp.append(i)
            frame_id_check.append(offline_schedule[i].frame_Id)
            fragment_check.append(offline_schedule[i].fragment_Id)
    print("delayed_flow_id", delayed_flow_id)
    print("candidate sche id", temp)
    print("frame_id of candidate flow", frame_id_check)
    print("the fragment check", fragment_check)
    delayed_sche_id = choice(temp)
    start_time = offline_schedule[delayed_sche_id].start_time
    end_time = offline_schedule[delayed_sche_id].end_time
    delayed_fragment_id = offline_schedule[delayed_sche_id].fragment_Id

    print("delayed_sche_id", delayed_sche_id)
    time_duration = end_time - start_time
    C_delayed_frame = time_duration - 2
    utilization_delayed = window_times[delayed_flow_id] / (2 * hyper_period)
    # print(int(math.ceil(start_time)), offline_schedule[delayed_frame_id].deadline - time_duration,
    #      offline_schedule[delayed_frame_id].deadline, window_times[delayed_flow_id])
    delayed_release_time = random.randint(int(math.ceil(start_time)),
                                          offline_schedule[delayed_sche_id].deadline - time_duration)
    delayed_deadline = offline_schedule[delayed_sche_id].deadline

    delayed_frame = Frame(offline_schedule[delayed_sche_id].frame_Id, offline_schedule[delayed_sche_id].fragment_Id,
                          delayed_deadline, 0, start_time,
                          time_duration, period[delayed_flow_id], source[delayed_flow_id], destination[delayed_flow_id],
                          "safety_critical")
    # print(delayed_frame.source, delayed_frame.arrive_time, delayed_frame.window_time+delayed_frame.arrive_time,
    # delayed_frame.window_time) frame_Id, fragment_Id, deadline, priority, arrive_time, window_times, period,
    # source, destination, critical_level
    print("start time | end time | time_duration | utilization_delayed :", start_time, end_time, time_duration,
          utilization_delayed)
    print("release time of delayed frame:", delayed_release_time)
    print("deadline of delayed frame:", delayed_deadline)

    print("----------------Delayed frame acceptance test 1--------------------")
    emergency_queue = []
    delayed_response_time = 0
    interference_same_queue = 0
    acceptance_state_1 = False
    acceptance_state_2 = False
    emergency_action = False
    Uti_server_up_bound = 1 - count / (2 * hyper_period)
    print("server up bound:", Uti_server_up_bound)
    # Uti_TBS = Uti_server_up_bound + utilization_delayed - sum(emergency_queue) / (2 * hyper_period)

    # server up bound without utilization reclaim

    Uti_TBS = Uti_server_up_bound - sum(emergency_queue[i].transmission_time for i in range(len(emergency_queue))) / (
            2 * hyper_period)

    print("utilization for TBS:", Uti_TBS)

    if C_delayed_frame <= (delayed_deadline - delayed_release_time) * Uti_TBS:
        acceptance_state_1 = True
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

                if offline_schedule[i].source == preemptable_flow:
                    if offline_schedule[i].deadline < delayed_deadline:
                        temp_in += offline_schedule[i].end_time - delayed_release_time
                    else:
                        if offline_schedule[i].end_time - delayed_release_time > 2:
                            temp_in += 2
                        else:
                            temp_in += offline_schedule[i].end_time - delayed_release_time
                    print("##", temp_in)
                else:
                    temp_in += offline_schedule[i].end_time - delayed_release_time
                    print("@@", temp_in)

        for i in range(len(offline_schedule)):
            if delayed_release_time <= offline_schedule[i].start_time < delayed_deadline:
                if offline_schedule[i].start_time - delayed_release_time - temp_in > C_delayed_frame:
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
        print("%%%", slack)
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
    print("")
    # ---------------------------------------------------------------------- #
    #           response time analysis for delayed traffic                   #
    # ---------------------------------------------------------------------- #

    print("----------------Delayed frame acceptance test 2 response time analysis--------------------")
    if not acceptance_state_1:
        emergency_action = True
        print("***************"
              "! WARNING: The delayed traffic can not be transmitted within its deadline and emergency action "
              "should be triggered ! ")
        pass
    # !!! ATTENTION----flow 1 is preemptable -----!!!!#
    else:
        iteration = True
        while iteration:
            interference = 0
            delayed_response_time = 0
            for i in range(len(offline_schedule)):
                # interference of active periodic traffic
                if offline_schedule[i].start_time < delayed_release_time < offline_schedule[i].end_time:
                    if i == delayed_sche_id:
                        interference += 0
                        print("delayed frame is released within its offline scheduled time")
                    else:
                        if offline_schedule[i].source == preemptable_flow:
                            # need to check if the active frame belongs to preempable flow
                            if offline_schedule[i].deadline < deadline_U_tbs:
                                interference += offline_schedule[i].end_time - delayed_release_time
                            else:
                                if offline_schedule[i].end_time - delayed_release_time > 2:
                                    interference += 2
                                    # time_for_delayed_frame = offline_schedule[i].end_time - delayed_release_time + 2
                                    # C_delayed_frame -= time_for_delayed_frame
                                    # !!! attention the time can be used to transmit delayed frame !!!#
                                    ## TODO calculate the response time of offline_schedule[i]
                                    print("blocked by preemptable one with lower priority:",
                                          offline_schedule[i].start_time,
                                          offline_schedule[i].end_time, interference)
                                else:
                                    interference += offline_schedule[i].end_time - delayed_release_time
                        else:
                            # include the block by the st non preemptable frame.
                            interference += offline_schedule[i].end_time - delayed_release_time
                            print("interference of active one with higher priority:", offline_schedule[i].start_time,
                                  offline_schedule[i].end_time, interference)
            preemption = 0
            for i in range(len(offline_schedule)):
                # interference of the period traffic coming in the future
                if delayed_release_time <= offline_schedule[i].start_time < deadline_U_tbs:
                    if offline_schedule[i].start_time - delayed_release_time - interference > C_delayed_frame:
                        interference += 0
                    else:
                        if offline_schedule[i].source == preemptable_flow:
                            if offline_schedule[i].deadline < delayed_deadline:
                                interference += offline_schedule[i].end_time - offline_schedule[i].start_time
                                preemption += pure_preemption_overhead
                                print("future higher priority", offline_schedule[i].end_time - offline_schedule[i].start_time)
                            else:
                                interference += 0
                        else:
                            interference += offline_schedule[i].end_time - offline_schedule[i].start_time
                            # preemption += pure_preemption_overhead
                            print("future ST", offline_schedule[i].end_time - offline_schedule[i].start_time)
                            ## TODO calculate the response time of offline_schedule[i]
            # interference += preemption
            print("interference :", interference)



            # # interference of active sporadic traffic
            # if interference_active == 0:
            #     latest_sporadic_release = (math.ceil(
            #         (delayed_release_time - sporadic_flow.arrive_time) / sporadic_flow.period) - 1) * sporadic_flow.period
            #     print("the latest arrive time of sporadic frame", latest_sporadic_release)
            #     if latest_sporadic_release <= delayed_release_time < latest_sporadic_release + sporadic_flow.window_time:
            #         if latest_sporadic_release + sporadic_flow.window_time - delayed_release_time > 2:
            #             interference_active += 2
            #         else:
            #             interference_active = latest_sporadic_release + sporadic_flow.window_time - delayed_release_time
            #             print("blocked by actuve sporadic frame:", interference_active)

            # interference of the frame in the same queue
            if delayed_response_time - delayed_release_time > 0:
                interference_same_queue = delayed_response_time - delayed_release_time
                print("interference of the same queue:", interference_same_queue)

            delayed_response_time += delayed_release_time + C_delayed_frame + interference + interference_same_queue
            print("TBS assigned deadline:", deadline_U_tbs)
            print("deadline of delayed frame:", delayed_deadline)
            print("the response time of delayed frame:", delayed_response_time)

            if delayed_response_time >= deadline_U_tbs:
                iteration = False

            temp_inter = 0
            temp_deadline_0 = deadline_U_tbs

            while delayed_response_time > temp_deadline_0:
                print("updated response time of delayed frame")
                for i in range(len(offline_schedule)):
                    if temp_deadline_0 < offline_schedule[i].start_time < delayed_response_time:
                        if offline_schedule[i].source == preemptable_flow:
                            if offline_schedule[i].deadline < delayed_deadline:
                                temp_inter += offline_schedule[i].end_time - offline_schedule[i].start_time
                            else:
                                temp_inter += 0
                                ## TODO calculate the response time of offline_schedule[i]
                        else:
                            temp_inter += offline_schedule[i].end_time - offline_schedule[i].start_time
                delayed_response_time += temp_inter
                temp_deadline_0 = delayed_response_time

            if delayed_response_time < deadline_U_tbs:
                temp_deadline = deadline_U_tbs
                deadline_U_tbs = delayed_response_time
                if deadline_U_tbs == temp_deadline:
                    iteration = False
        # interference of the current active period traffic with deadline smaller than the assigned deadline and
        # blocked by preemptable frame with greater deadline and blocked by st non-preemptable frame with lower priority

        if delayed_response_time <= delayed_deadline:
            acceptance_state_2 = True
            emergency_queue.append(delayed_frame)
            print("acceptance test 2 passed:", acceptance_state_1)
        else:
            acceptance_state_2 = False
            print("!!! @@@#### WARNING  acceptance test 2 failed. The delayed st frame can not be handled before its "
                  "deadline")

    # print("-----------------------CBS based sporadic traffic transmission----------------------------------")
    # sporadic_queue = []
    #
    # sporadic_response_time = 0
    # print("sporadic traffic parameters:", sporadic_flow.arrive_time, sporadic_flow.window_time, sporadic_flow.period)
    # if sporadic_flow.arrive_time > delayed_response_time:
    #     emergency_queue.pop(0)
    #
    # # C_sporadic_avg = math.floor(np.median(window_times))
    # C_sporadic_avg = 10
    # max_preemption_times = math.floor(C_sporadic_avg / 2)
    # max_preemption_overhead = max_preemption_times * pure_preemption_overhead
    # # print(max_preemption_overhead)
    # sim_time = 0
    # sporadic_frame_id = 0
    # Uti_CBS = Uti_server_up_bound + utilization_delayed - \
    #           sum(emergency_queue[i].transmission_time for i in range(len(emergency_queue))) / (2 * hyper_period)
    # sporadic_queue.append(sporadic_flow)
    #
    # print("the utilization allocate to sporadic traffic:", Uti_CBS)

    # # ----------------CBS parameters definition-----------------------------#
    # T_CBS = math.floor(
    #     1 / Uti_CBS * (
    #             max_preemption_overhead + math.sqrt((max_preemption_times * C_sporadic_avg) / (1 - Uti_CBS))))
    # C_CBS = math.floor(T_CBS * Uti_CBS)
    # C_remain = C_CBS
    # print("the parameters of CBS periodic time | capacity | actual utilization: ", T_CBS, C_CBS, C_CBS / T_CBS)
    # offset = sporadic_flow.arrive_time
    # sporadic_deadline = offset + T_CBS
    # while sim_time < 2 * hyper_period:
    #     print("------------------------------------------------------------------")
    #     print("sporadic frame info: ", sporadic_queue[sporadic_frame_id].frame_id,
    #           sporadic_queue[sporadic_frame_id].arrive_time, sporadic_queue[sporadic_frame_id].window_time)
    #     print("sporadic deadline: ", sporadic_deadline)
    #     print("capacity:", C_remain)
    #
    #     # if len(sporadic_queue) == 1:
    #     #     print("the server is idle")
    #     #     if C_remain >= (sporadic_deadline - sporadic_queue[sporadic_frame_id].arrive_time) * Uti_CBS:
    #     #         sporadic_deadline += sporadic_queue[sporadic_frame_id].arrive_time + T_CBS
    #     #         C_remain = C_CBS
    #     #     else:
    #     #         print("sporadic deadline stay unchanged: ", sporadic_deadline)
    #     #         print("C_remain is enough for the next frame: ", C_remain)
    #
    #     # interference of active periodic traffic
    #     interference_active = 0
    #     for i in range(len(offline_schedule)):
    #         if offline_schedule[i].start_time <= sporadic_queue[sporadic_frame_id].arrive_time < offline_schedule[
    #             i].end_time:
    #             if offline_schedule[i].source == 1:  # need to check if the active frame belongs to preempable flow
    #                 if offline_schedule[i].deadline < sporadic_deadline:
    #                     interference_active += offline_schedule[i].end_time - sporadic_queue[
    #                         sporadic_frame_id].arrive_time
    #                 else:
    #                     if offline_schedule[i].end_time - sporadic_queue[sporadic_frame_id].arrive_time > 2:
    #                         interference_active += 2
    #                         # time_for_delayed_frame = offline_schedule[i].end_time - delayed_release_time + 2
    #                         # C_delayed_frame -= time_for_delayed_frame
    #                         # !!! attention the time can be used to transmit delayed frame !!!#
    #                         print("blocked by preemptable one with lower priority:",
    #                               offline_schedule[i].start_time,
    #                               offline_schedule[i].end_time, interference_active)
    #                     else:
    #                         interference_active += offline_schedule[i].end_time - sporadic_queue[
    #                             sporadic_frame_id].arrive_time
    #             else:
    #                 # include the block by the st non preemptable frame.
    #                 interference_active += offline_schedule[i].end_time - sporadic_queue[sporadic_frame_id].arrive_time
    #                 print("interference of active one with higher priority:", offline_schedule[i].start_time,
    #                       offline_schedule[i].end_time, interference_active)
    #
    #     # interference of the period traffic coming in the future
    #     interference_future = 0
    #     for i in range(len(offline_schedule)):
    #         if sporadic_queue[sporadic_frame_id].arrive_time < offline_schedule[i].start_time < sporadic_deadline:
    #             if offline_schedule[i].source == 1:
    #                 if offline_schedule[i].deadline < sporadic_deadline:
    #                     interference_future += offline_schedule[i].end_time - offline_schedule[i].start_time
    #                 else:
    #                     interference_future += 0
    #             else:
    #                 interference_future += offline_schedule[i].end_time - offline_schedule[i].start_time
    #
    #             print("interference of the period traffic coming in the future:", offline_schedule[i].start_time,
    #                   offline_schedule[i].end_time, interference_future)
    #
    #     # interference of the frame in the same queue
    #     interference_same_queue = 0
    #     if sporadic_response_time - sporadic_queue[sporadic_frame_id].arrive_time > 0:
    #         interference_same_queue = sporadic_response_time - sporadic_queue[sporadic_frame_id].arrive_time
    #         print("interference if the frames in the same queue: ", interference_same_queue)
    #
    #     if C_remain > sporadic_queue[sporadic_frame_id].window_time:
    #         sporadic_response_time = sporadic_queue[sporadic_frame_id].arrive_time + interference_same_queue \
    #                                   + interference_active + interference_future + sporadic_queue[
    #                                       sporadic_frame_id].window_time
    #
    #         if sporadic_response_time > sporadic_deadline:
    #             for i in range(len(offline_schedule)):
    #                 if sporadic_deadline < offline_schedule[i].start_time < sporadic_response_time:
    #                     if offline_schedule[i].source == 1:
    #                         if offline_schedule[i].deadline < sporadic_deadline:
    #                             interference_future += offline_schedule[i].end_time - offline_schedule[i].start_time
    #                         else:
    #                             interference_future += 0
    #                     else:
    #                         sporadic_response_time += offline_schedule[i].end_time - offline_schedule[i].start_time
    #             sporadic_response_time += pure_preemption_overhead
    #             print("!! updated response time of delayed frame:", sporadic_response_time)
    #
    #         C_remain = C_remain - sporadic_queue[sporadic_frame_id].window_time
    #         print("response time:", sporadic_response_time)
    #         sporadic_queue.pop(0)
    #         sporadic_flow.frame_id += 1
    #         sporadic_flow.arrive_time = 7 + sporadic_flow.frame_id * sporadic_flow.period
    #         sporadic_queue.append(sporadic_flow)
    #     else:
    #         sporadic_response_time = sporadic_queue[sporadic_frame_id].arrive_time + interference_same_queue \
    #                                   + interference_active + interference_future + C_CBS
    #         if sporadic_response_time > sporadic_deadline:
    #             for i in range(len(offline_schedule)):
    #                 if sporadic_deadline < offline_schedule[i].start_time < sporadic_response_time:
    #                     if offline_schedule[i].source == 1:
    #                         if offline_schedule[i].deadline < sporadic_deadline:
    #                             interference_future += offline_schedule[i].end_time - offline_schedule[i].start_time
    #                         else:
    #                             interference_future += 0
    #                     else:
    #                         sporadic_response_time += offline_schedule[i].end_time - offline_schedule[i].start_time
    #             sporadic_response_time += pure_preemption_overhead
    #             print("!! updated response time of delayed frame:", sporadic_response_time)
    #         sporadic_queue[sporadic_frame_id].window_time = sporadic_queue[sporadic_frame_id].window_time - C_CBS
    #         C_remain = C_CBS
    #         sporadic_queue[sporadic_frame_id].arrive_time = sporadic_response_time
    #         sporadic_deadline += T_CBS
    #         print("sporadic frame is fragmented")
    #     print("remain capacity:", C_remain)
    #     if C_remain >= (sporadic_deadline - sporadic_queue[sporadic_frame_id].arrive_time) * Uti_CBS:
    #         sporadic_deadline = sporadic_queue[sporadic_frame_id].arrive_time + T_CBS
    #         C_remain = C_CBS
    #         print("replenishment")
    #     else:
    #         print("sporadic deadline stay unchanged: ", sporadic_deadline)
    #         print("C_remain is enough for the next frame: ", C_remain)
    #     sim_time = sporadic_response_time

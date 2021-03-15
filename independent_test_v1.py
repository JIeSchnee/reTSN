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


if __name__ == "__main__":
    # window_times = [23, 13, 48]
    # period = [200, 100, 200]
    # hyper_period = 200
    # current_time = 0
    # current_period = [1, 1, 1]
    # remain_time = [23, 13, 48]
    # offset = [0, 0, 0]
    # release_times = [0, 0, 0]
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
    utilization_delayed = window_times[delayed_flow_id] / (2 * hyper_period)
    # print(int(math.ceil(start_time)), offline_schedule[delayed_frame_id].deadline - time_duration,
    #      offline_schedule[delayed_frame_id].deadline, window_times[delayed_flow_id])
    delayed_release_time = random.randint(int(math.ceil(start_time)),
                                          offline_schedule[delayed_sche_id].deadline - time_duration)
    delayed_deadline = offline_schedule[delayed_sche_id].deadline

    print("start time | end time | time_duration | utilization_delayed :", start_time, end_time, time_duration,
          utilization_delayed)
    print("release time of delayed frame:", delayed_release_time)
    print("deadline of delayed frame:", delayed_deadline)

    print("----------------Delayed frame acceptance test 1--------------------")
    emergency_queue = [0]
    acceptance_state_1 = False
    acceptance_state_2 = False
    emergency_action = False
    Uti_server_up_bound = 1 - count / (2 * hyper_period)
    print("server up bound:", Uti_server_up_bound)
    # Uti_TBS = Uti_server_up_bound + utilization_delayed - sum(emergency_queue) / (2 * hyper_period)

    # server up bound without utilization reclaim
    Uti_TBS = Uti_server_up_bound - sum(emergency_queue) / (2 * hyper_period)
    C_delayed_frame = time_duration - 2
    print("utilization for TBS:", Uti_TBS)

    if C_delayed_frame <= (delayed_deadline - delayed_release_time) * Uti_TBS:
        acceptance_state_1 = True
        deadline_U_tbs = max(delayed_release_time, deadline_U_tbs) + C_delayed_frame / Uti_TBS
        print("acceptance test 1 passed:", acceptance_state_1)
    else:
        temp_start = delayed_deadline - C_delayed_frame
        for i in range(len(offline_schedule)):

            if offline_schedule[i].start_time < delayed_deadline and offline_schedule[i].end_time > temp_start:
                # check if the frame belongs to preemptable flow, which without GB. With following test part we can #
                # relax the release time of delayed frame for more prices verification                              #
                if i == 1:
                    emergency_action = True
                    acceptance_state_1 = False
                    print(offline_schedule[i].start_time, offline_schedule[i].end_time)
                    print("!@@@WARNING: The delayed traffic can not be transmitted within its deadline and emergency "
                          "action should be triggered ! ", acceptance_state_1)
                else:
                    gb_tolerate_time = offline_schedule[i].start_time - delayed_deadline
                    if gb_tolerate_time <= 1:
                        acceptance_state_1 = True
                        deadline_U_tbs = delayed_deadline
                        print("acceptance test 1 passed:", acceptance_state_1)
                    else:
                        emergency_action = True
                        acceptance_state_1 = False
                        print(offline_schedule[i].start_time, offline_schedule[i].end_time)
                        print(
                            "!$$$WARNING: The delayed traffic can not be transmitted within its deadline and emergency "
                            "action should be triggered ! ", acceptance_state_1)
            else:
                acceptance_state_1 = True
        print("acceptance test 1 passed:", acceptance_state_1)

    print("----------------Delayed frame acceptance test 2 response time analysis--------------------")
    if not acceptance_state_1:
        emergency_action = True
        print("***************"
              "! WARNING: The delayed traffic can not be transmitted within its deadline and emergency action "
              "should be triggered ! ", acceptance_state_2)
        pass
    # !!! ATTENTION----flow 1 is preemptable -----!!!!#
    else:
        print("TBS assigned deadline:", deadline_U_tbs)
        print("## flow 1 belongs to preemptable category ##")

        # interference of the current active period traffic with deadline smaller than the assigned deadline and
        # blocked by preemptable frame with greater deadline
        remain_higher_priority = 0
        preemptable_block = 0
        for i in range(len(offline_schedule)):
            if offline_schedule[i].start_time <= delayed_release_time < offline_schedule[i].end_time:
                if i == 1:  # need to check if the active frame belongs to preempable flow
                    if offline_schedule[i].deadline < delayed_deadline:
                        remain_higher_priority += offline_schedule[i].end_time - delayed_release_time
                    else:
                        if offline_schedule[i].end_time - delayed_release_time > 2:
                            preemptable_block += 2
                            print("blocked by preemptable one with lower priority:", offline_schedule[i].start_time,
                                  offline_schedule[i].end_time, preemptable_block)
                        else:
                            remain_higher_priority += offline_schedule[i].end_time - delayed_release_time
                else:
                    remain_higher_priority += offline_schedule[i].end_time - delayed_release_time
                print("active one with higher priority:", offline_schedule[i].start_time, offline_schedule[i].end_time,
                      remain_higher_priority)

        # interference of the period traffic coming in the future

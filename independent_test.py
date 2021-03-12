class schedule:
    def __init__(self, source, destination, frame_Id, fragment_Id, start_time, end_time):
        self.source = source
        self.destination = destination
        self.frame_Id = frame_Id
        self.fragment_Id = fragment_Id
        self.start_time = start_time
        self.end_time = end_time


if __name__ == "__main__":
    window_times = [8, 5, 289, 69]
    period = [100, 100, 1000, 1000]
    hyper_period = 1000
    current_time = 0
    current_period = [1, 1, 1, 1]
    remain_time = [8, 5, 289, 69]
    offset = [0, 0, 0, 0]
    release_times = [0, 0, 0, 0]
    preemption_overhead = 2.3
    frame_id = [0, 0, 0, 0]
    fragment_id = [0, 0, 0, 0]
    source = [0, 1, 2, 3]
    destination = [0, 0, 0, 0]
    offline_schedule = []
    count = 0

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
            print("current_p", current_period_p)

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
            print(sche.source, sche.frame_Id, sche.fragment_Id, sche.start_time, sche.end_time)
            fragment_id[earliest_index] += 1
            current_time += running_time
            if remain_time[earliest_index] == 0:
                remain_time[earliest_index] = window_times[earliest_index]
                current_period[earliest_index] += 1
                release_times[earliest_index] += period[earliest_index]
                frame_id[earliest_index] += 1
                fragment_id[earliest_index] = 0
                #print("remain_update:", remain_time)
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

                #print("remain_update:", remain_time)
            sche = schedule(source[earliest_index], destination[earliest_index], frame_id[earliest_index],
                            fragment_id[earliest_index], current_time,
                            current_time + running_time)
            offline_schedule.append(sche)
            print(sche.source, sche.frame_Id, sche.fragment_Id, sche.start_time, sche.end_time)
            fragment_id[earliest_index] += 1
            current_time += running_time
            if remain_time[earliest_index] == 0:
                remain_time[earliest_index] = window_times[earliest_index]
                current_period[earliest_index] += 1
                release_times[earliest_index] += period[earliest_index]
                frame_id[earliest_index] += 1
                fragment_id[earliest_index] = 0
                #print("remain_update:", remain_time)

            if current_time < min(release_times):
                current_time = min(release_times)

            print("frame id", frame_id)
            total_time = sum([b * c for b, c in zip(window_times, frame_id)])
            print("total_time and uti", total_time, total_time/hyper_period)
            print(count, count/hyper_period)
    # print("-------------------- summarize ---------------------------")
    # for i in range(len(offline_schedule)):
    #     print(" source | frame_id | fragment_id | start time | end time")
    #     print(offline_schedule[i].source, offline_schedule[i].frame_Id, offline_schedule[i].fragment_Id, offline_schedule[i].start_time, offline_schedule[i].end_time)
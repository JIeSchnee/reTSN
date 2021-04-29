import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import pickle
import seaborn as sns
# delayed frame

with open('/home/jiezou/EMSOFT\'21_Flex-TSN/Scheduling_without_guarantee/uti_0.8_10ST/round 1000_delay/difference_CBS_AVB_delayed_frame.pickle', 'rb') as handle:
    U08_difference_CBS_AVB_delayed_frame = pickle.load(handle)

with open('/home/jiezou/EMSOFT\'21_Flex-TSN/Scheduling_without_guarantee/uti_0.6_10ST/round 1000_delay/difference_CBS_AVB_delayed_frame.pickle', 'rb') as handle:
    U06_difference_CBS_AVB_delayed_frame = pickle.load(handle)

with open('/home/jiezou/EMSOFT\'21_Flex-TSN/Scheduling_without_guarantee/uti_0.5_10ST/round 1000_delay/difference_CBS_AVB_delayed_frame.pickle', 'rb') as handle:
    U05_difference_CBS_AVB_delayed_frame = pickle.load(handle)

with open('/home/jiezou/EMSOFT\'21_Flex-TSN/Scheduling_without_guarantee/uti_0.3_10ST/round 1000_delay/difference_CBS_AVB_delayed_frame.pickle', 'rb') as handle:
    U03_difference_CBS_AVB_delayed_frame = pickle.load(handle)

grid = plt.GridSpec(nrows=4, ncols=1)

plt.subplot(grid[0, 0])
x = range(len(U08_difference_CBS_AVB_delayed_frame))
plt.plot(x, U08_difference_CBS_AVB_delayed_frame, label='Uti 0.8', marker='o', color='orange', linewidth=2)
plt.legend(prop={'size': 20})
plt.tick_params(labelsize=18)

plt.subplot(grid[1, 0])
x = range(len(U06_difference_CBS_AVB_delayed_frame))
plt.plot(x, U06_difference_CBS_AVB_delayed_frame, label='Uti 0.6', marker='o', color='orange', linewidth=2)
plt.ylabel("Response time reduction", fontsize=24)
plt.legend(prop={'size': 20})
plt.tick_params(labelsize=18)

plt.subplot(grid[2, 0])
x = range(len(U05_difference_CBS_AVB_delayed_frame))
plt.plot(x, U05_difference_CBS_AVB_delayed_frame, label='Uti 0.5', marker='o', color='orange', linewidth=2)
plt.legend(prop={'size': 20})
plt.tick_params(labelsize=18)

plt.subplot(grid[3, 0])
x = range(len(U03_difference_CBS_AVB_delayed_frame))
plt.plot(x, U03_difference_CBS_AVB_delayed_frame, label='Uti 0.3', marker='o', color='orange', linewidth=2)
plt.legend(prop={'size': 20})
plt.tick_params(labelsize=18)
plt.suptitle('The response time reduction of delayed SF frame between CBServer and AVB (raw data)',  fontsize=24)
plt.xlabel(" Delayed ST frame", fontsize=24)
plt.show()





# ----------- 柱状图 ------------#
# accepted number comparison

name_list = ['Uti 0.8', 'Uti 0.6', 'Uti 0.5', 'Uti 0.3']
total_width, n = 0.5, 2
width = total_width / n

cbs = [692, 858, 912, 987]
avb = [84, 662, 864, 982]
x = list(range(len(cbs)))


plt.bar(x, cbs, width=width, label='CBServer', tick_label=name_list, fc='orange', edgecolor='0', linewidth=2)
for i in range(len(x)):
    x[i] = x[i] + width
plt.bar(x, avb, width=width, label='AVB', fc='g', edgecolor='0', linewidth=2)
plt.ylabel("Counts", fontsize=24)
plt.title("The number of handled delayed ST frame (1000 round)", fontsize=24, pad=24)
plt.legend(loc='best', prop={'size': 22})
plt.tick_params(labelsize=24)
plt.show()

# for i in range(len(U08_difference_CBS_AVB_delayed_frame)):
#     U08_difference_CBS_AVB_delayed_frame[i] = \
#         (U08_difference_CBS_AVB_delayed_frame[i] - min(U08_difference_CBS_AVB_delayed_frame))/\
#         (max(U08_difference_CBS_AVB_delayed_frame)- min(U08_difference_CBS_AVB_delayed_frame))
#
# for i in range(len(U06_difference_CBS_AVB_delayed_frame)):
#     U06_difference_CBS_AVB_delayed_frame[i] = \
#         (U06_difference_CBS_AVB_delayed_frame[i] - min(U06_difference_CBS_AVB_delayed_frame))/\
#         (max(U06_difference_CBS_AVB_delayed_frame)- min(U06_difference_CBS_AVB_delayed_frame))
#
# for i in range(len(U05_difference_CBS_AVB_delayed_frame)):
#     U05_difference_CBS_AVB_delayed_frame[i] = \
#         (U05_difference_CBS_AVB_delayed_frame[i] - min(U05_difference_CBS_AVB_delayed_frame))/\
#         (max(U05_difference_CBS_AVB_delayed_frame)- min(U05_difference_CBS_AVB_delayed_frame))
#
# for i in range(len(U03_difference_CBS_AVB_delayed_frame)):
#     U03_difference_CBS_AVB_delayed_frame[i] = \
#         (U03_difference_CBS_AVB_delayed_frame[i] - min(U03_difference_CBS_AVB_delayed_frame))/\
#         (max(U03_difference_CBS_AVB_delayed_frame)- min(U03_difference_CBS_AVB_delayed_frame))

# s1 = pd.Series(U08_difference_CBS_AVB_delayed_frame)
# s2 = pd.Series(U06_difference_CBS_AVB_delayed_frame)
# s3 = pd.Series(U05_difference_CBS_AVB_delayed_frame)
# s4 = pd.Series(U03_difference_CBS_AVB_delayed_frame)
# thred08 = 0.05*abs(max(U08_difference_CBS_AVB_delayed_frame) - min(U08_difference_CBS_AVB_delayed_frame))
thred08 = 2
U08_difference_CBS_AVB_delayed_frame = list(filter(lambda x:x>thred08 or x<-thred08 , U08_difference_CBS_AVB_delayed_frame))
# x = range(len(U08_difference_CBS_AVB_delayed_frame))
# plt.plot(x, U08_difference_CBS_AVB_delayed_frame, label='Uti 0.8', marker='o', color='orange', linewidth=2)
# plt.show()
#
# thred06 = 0.05*abs(max(U06_difference_CBS_AVB_delayed_frame) - min(U06_difference_CBS_AVB_delayed_frame))
thred06 = 2
U06_difference_CBS_AVB_delayed_frame = list(filter(lambda x:x>thred06 or x<-thred06, U06_difference_CBS_AVB_delayed_frame))
# x = range(len(U06_difference_CBS_AVB_delayed_frame))
# plt.plot(x, U06_difference_CBS_AVB_delayed_frame, label='Uti 0.8', marker='o', color='orange', linewidth=2)
# plt.show()
# thred05 = 0.05*abs(max(U05_difference_CBS_AVB_delayed_frame) - min(U05_difference_CBS_AVB_delayed_frame))
thred05 = 2
U05_difference_CBS_AVB_delayed_frame = list(filter(lambda x:x>thred05 or x<-thred05, U05_difference_CBS_AVB_delayed_frame))
# x = range(len(U05_difference_CBS_AVB_delayed_frame))
# plt.plot(x, U05_difference_CBS_AVB_delayed_frame, label='Uti 0.8', marker='o', color='orange', linewidth=2)
# plt.show()
# thred03 = 0.05*abs(max(U03_difference_CBS_AVB_delayed_frame) - min(U03_difference_CBS_AVB_delayed_frame))
thred03 = 2
U03_difference_CBS_AVB_delayed_frame = list(filter(lambda x:x>thred03 or x<-thred03, U03_difference_CBS_AVB_delayed_frame))
# x = range(len(U03_difference_CBS_AVB_delayed_frame))
# plt.plot(x, U03_difference_CBS_AVB_delayed_frame, label='Uti 0.8', marker='o', color='orange', linewidth=2)
# plt.show()
#
s1 = pd.Series(U08_difference_CBS_AVB_delayed_frame)
s2 = pd.Series(U06_difference_CBS_AVB_delayed_frame)
s3 = pd.Series(U05_difference_CBS_AVB_delayed_frame)
s4 = pd.Series(U03_difference_CBS_AVB_delayed_frame)

data = pd.DataFrame({'Uti 0.8': s1, 'Uti 0.6': s2, 'Uti 0.5': s3, 'Uti 0.3': s4})
data.boxplot(whis =1.5, meanline=True, showmeans=True, meanprops={'linestyle':'--','color':'green', 'linewidth': 2}, capprops = {'linewidth': 2},
             medianprops={'linestyle':'--','color':'orange', 'linewidth': 2}, boxprops={'linewidth': 2},
             whiskerprops={'linewidth': 2})
plt.grid(linestyle="--", alpha=0.5)
plt.ylabel("Response time difference", fontsize=24)
plt.title("The response time difference of delayed SF frame", fontsize=24, pad=24)
plt.tick_params(labelsize=24)
plt.show()
#

#
#

s1.plot.hist(grid=True, bins=100, rwidth=0.9,
                   color='#607c8e')
plt.title("The response time reduction of delayed SF frame, Uti 0.8", fontsize=24, pad=24)
plt.xlabel('Response time reduction ', fontsize=24)
plt.ylabel('Counts', fontsize=24)
plt.grid(linestyle="--", alpha=0.5)
plt.tick_params(labelsize=24)
plt.show()

s2.plot.hist(grid=True, bins=100, rwidth=0.9,
                   color='#607c8e')
plt.title("The response time reduction of delayed SF frame, Uti 0.6", fontsize=24, pad=24)
plt.xlabel('Response time reduction ', fontsize=24)
plt.ylabel('Counts', fontsize=24)
plt.grid(linestyle="--", alpha=0.5)
plt.tick_params(labelsize=24)
plt.show()

s3.plot.hist(grid=True, bins=100, rwidth=0.9,
                   color='#607c8e')
plt.title("The response time reduction of delayed SF frame, Uti 0.5", fontsize=24, pad=24)
plt.xlabel('Response time reduction ', fontsize=24)
plt.ylabel('Counts', fontsize=24)
plt.grid(linestyle="--", alpha=0.5)
plt.tick_params(labelsize=24)
plt.show()

s4.plot.hist(grid=True, bins=100, rwidth=0.9,
                   color='#607c8e')
plt.title("The response time reduction of delayed SF frame, Uti 0.3", fontsize=24, pad=24)
plt.xlabel('Response time reduction ', fontsize=24)
plt.ylabel('Counts', fontsize=24)
plt.grid(linestyle="--", alpha=0.5)
plt.tick_params(labelsize=24)
plt.show()

#
# # with open('/home/jiezou/EMSOFT\'21_Flex-TSN/Scheduling_without_guarantee/uti_0.8_10ST/AVB_max_response_time_classA.pickle', 'rb') as handle:
# #     AVB_max_response_time_classA = pickle.load(handle)
# #
# # x = range(len(AVB_max_response_time_classA))
# # plt.plot(x, AVB_max_response_time_classA, marker='o', color='orange', linewidth=2)
# # plt.show()
#
#

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import pickle
import seaborn as sns
# delayed frame




with open('/home/.../uti_0.8_10ST/round 1000_delay/CBS_delayed_response.pickle', 'rb') as handle:
    CBS_delayed_response08 = pickle.load(handle)
# print(len(CBS_delayed_response08))
with open('/home/.../uti_0.8_10ST/round 1000_delay/AVB_delayed_response.pickle', 'rb') as handle:
    AVB_delayed_response08 = pickle.load(handle)
# print(len(AVB_delayed_response08))

with open('/home/.../uti_0.6_10ST/round 1000_delay/CBS_delayed_response.pickle', 'rb') as handle:
    CBS_delayed_response06 = pickle.load(handle)
# print(len(CBS_delayed_response06))
with open('/home/.../uti_0.6_10ST/round 1000_delay/AVB_delayed_response.pickle', 'rb') as handle:
    AVB_delayed_response06 = pickle.load(handle)
# print(len(AVB_delayed_response06))

with open('/home/.../uti_0.5_10ST/round 1000_delay/CBS_delayed_response.pickle', 'rb') as handle:
    CBS_delayed_response05 = pickle.load(handle)
# print(len(CBS_delayed_response05))
with open('/home/.../uti_0.5_10ST/round 1000_delay/AVB_delayed_response.pickle', 'rb') as handle:
    AVB_delayed_response05 = pickle.load(handle)
# print(len(AVB_delayed_response05))

with open('/home/.../uti_0.3_10ST/round 1000_delay/CBS_delayed_response.pickle', 'rb') as handle:
    CBS_delayed_response03 = pickle.load(handle)
# print(len(CBS_delayed_response03))
with open('/home/.../uti_0.3_10ST/round 1000_delay/AVB_delayed_response.pickle', 'rb') as handle:
    AVB_delayed_response03 = pickle.load(handle)
# print(len(AVB_delayed_response03))



with open('/home/.../uti_0.8_10ST/round 1000_delay/difference_CBS_AVB_delayed_frame.pickle', 'rb') as handle:
    U08_difference_CBS_AVB_delayed_frame = pickle.load(handle)

u08_rela = []
for i in range(len(U08_difference_CBS_AVB_delayed_frame)):
    u08_rela.append(U08_difference_CBS_AVB_delayed_frame[i]/AVB_delayed_response08[i])
# print(len(U08_difference_CBS_AVB_delayed_frame))

with open('/home/.../uti_0.6_10ST/round 1000_delay/difference_CBS_AVB_delayed_frame.pickle', 'rb') as handle:
    U06_difference_CBS_AVB_delayed_frame = pickle.load(handle)
u06_rela = []
for i in range(len(U06_difference_CBS_AVB_delayed_frame)):
    u06_rela.append(U06_difference_CBS_AVB_delayed_frame[i]/AVB_delayed_response06[i])
# print(len(U06_difference_CBS_AVB_delayed_frame))

with open('/home/.../uti_0.5_10ST/round 1000_delay/difference_CBS_AVB_delayed_frame.pickle', 'rb') as handle:
    U05_difference_CBS_AVB_delayed_frame = pickle.load(handle)
# print(len(U05_difference_CBS_AVB_delayed_frame))
u05_rela = []
for i in range(len(U05_difference_CBS_AVB_delayed_frame)):
    u05_rela.append(U05_difference_CBS_AVB_delayed_frame[i]/AVB_delayed_response05[i])

with open('/home/.../uti_0.3_10ST/round 1000_delay/difference_CBS_AVB_delayed_frame.pickle', 'rb') as handle:
    U03_difference_CBS_AVB_delayed_frame = pickle.load(handle)
# print(len(U03_difference_CBS_AVB_delayed_frame))

u03_rela = []
for i in range(len(U03_difference_CBS_AVB_delayed_frame)):
    u03_rela.append(U03_difference_CBS_AVB_delayed_frame[i]/AVB_delayed_response03[i])
# grid = plt.GridSpec(nrows=4, ncols=1)
#
# plt.subplot(grid[0, 0])
# x = range(len(U08_difference_CBS_AVB_delayed_frame))
# plt.plot(x, U08_difference_CBS_AVB_delayed_frame, label='Uti 0.8', marker='o', color='orange', linewidth=2)
# plt.legend(prop={'size': 20})
# plt.tick_params(labelsize=18)
#
# plt.subplot(grid[1, 0])
# x = range(len(U06_difference_CBS_AVB_delayed_frame))
# plt.plot(x, U06_difference_CBS_AVB_delayed_frame, label='Uti 0.6', marker='o', color='orange', linewidth=2)
# plt.ylabel("Response time reduction", fontsize=24)
# plt.legend(prop={'size': 20})
# plt.tick_params(labelsize=18)
#
# plt.subplot(grid[2, 0])
# x = range(len(U05_difference_CBS_AVB_delayed_frame))
# plt.plot(x, U05_difference_CBS_AVB_delayed_frame, label='Uti 0.5', marker='o', color='orange', linewidth=2)
# plt.legend(prop={'size': 20})
# plt.tick_params(labelsize=18)
#
# plt.subplot(grid[3, 0])
# x = range(len(U03_difference_CBS_AVB_delayed_frame))
# plt.plot(x, U03_difference_CBS_AVB_delayed_frame, label='Uti 0.3', marker='o', color='orange', linewidth=2)
# plt.legend(prop={'size': 20})
# plt.tick_params(labelsize=18)
# plt.suptitle('The response time reduction of delayed SF frame between CBServer and AVB (raw data)',  fontsize=24)
# plt.xlabel(" Delayed ST frame", fontsize=24)
# plt.show()


# accepted number comparison

name_list = ['Uti 0.3', 'Uti 0.5', 'Uti 0.6', 'Uti 0.8']
total_width, n = 0.5, 2
width = total_width / n

cbs = [9864, 9182, 8740, 6683]
avb = [9824, 8756, 7030, 1460]

x = np.arange(len(name_list))
fig, ax = plt.subplots()

ax.bar(x-width/2, cbs, width=width, label='CBServer', fc='orange', edgecolor='0', linewidth=3)
ax.bar(x+width/2, avb, width=width, label='AVB', fc='g', edgecolor='0', linewidth=3)
plt.ylabel("Counts", fontsize=26)
plt.title("The number of handled delayed ST frame (10000 round)", fontsize=26, pad=26)
ax.set_xticks(x)
ax.set_xticklabels(name_list)

plt.legend(loc='best', prop={'size': 26})
plt.tick_params(labelsize=26)
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
thred08 = 0
U08_difference_CBS_AVB_delayed_frame = list(filter(lambda x:x != 0 , U08_difference_CBS_AVB_delayed_frame))
# x = range(len(U08_difference_CBS_AVB_delayed_frame))
# plt.plot(x, U08_difference_CBS_AVB_delayed_frame, label='Uti 0.8', marker='o', color='orange', linewidth=2)
# plt.show()
#
# thred06 = 0.05*abs(max(U06_difference_CBS_AVB_delayed_frame) - min(U06_difference_CBS_AVB_delayed_frame))
thred06 = 0
U06_difference_CBS_AVB_delayed_frame = list(filter(lambda x:x != 0, U06_difference_CBS_AVB_delayed_frame))
# x = range(len(U06_difference_CBS_AVB_delayed_frame))
# plt.plot(x, U06_difference_CBS_AVB_delayed_frame, label='Uti 0.8', marker='o', color='orange', linewidth=2)
# plt.show()
# thred05 = 0.05*abs(max(U05_difference_CBS_AVB_delayed_frame) - min(U05_difference_CBS_AVB_delayed_frame))
thred05 = 0
U05_difference_CBS_AVB_delayed_frame = list(filter(lambda x:x != 0, U05_difference_CBS_AVB_delayed_frame))
# x = range(len(U05_difference_CBS_AVB_delayed_frame))
# plt.plot(x, U05_difference_CBS_AVB_delayed_frame, label='Uti 0.8', marker='o', color='orange', linewidth=2)
# plt.show()
# thred03 = 0.05*abs(max(U03_difference_CBS_AVB_delayed_frame) - min(U03_difference_CBS_AVB_delayed_frame))
thred03 = 0
U03_difference_CBS_AVB_delayed_frame = list(filter(lambda x:x != 0, U03_difference_CBS_AVB_delayed_frame))
# x = range(len(U03_difference_CBS_AVB_delayed_frame))
# plt.plot(x, U03_difference_CBS_AVB_delayed_frame, label='Uti 0.8', marker='o', color='orange', linewidth=2)
# plt.show()
#

count03 = 0
count03_d = 0
for i in range(len(u03_rela)):
    if u03_rela[i]<0:
        count03 += 1
    elif u03_rela[i] > 0:
        count03_d += 1
print('percent of reduction 03 $ better , worse, unchanged:', count03/len(u03_rela),
      count03_d/len(u03_rela), 1-count03/len(u03_rela)-count03_d/len(u03_rela))


count05 = 0
count05_d = 0
for i in range(len(u05_rela)):
    if u05_rela[i]<0:
        count05 += 1
    elif u05_rela[i] > 0:
        count05_d += 1
print('percent of reduction 05 $ better , worse, unchanged:', count05/len(u05_rela),
      count05_d/len(u05_rela), 1-count05/len(u05_rela)-count05_d/len(u05_rela))


count06 = 0
count06_d = 0
for i in range(len(u06_rela)):
    if u06_rela[i]<0:
        count06 += 1
    elif u06_rela[i] > 0:
        count06_d += 1
print('percent of reduction 06 $ better , worse, unchanged:', count06/len(u06_rela),
      count06_d/len(u06_rela), 1-count06/len(u06_rela)-count06_d/len(u06_rela))


count08 = 0
count08_d = 0
print(len(u08_rela))
for i in range(len(u08_rela)):
    if u08_rela[i]<0:
        count08 += 1
    elif u08_rela[i] > 0:
        count08_d += 1
print('percent of reduction 08 $ better , worse, unchanged:', count08/len(u08_rela),
      count08_d/len(u08_rela), 1-count08/len(u08_rela)-count08_d/len(u08_rela))


u03_rela = list(filter(lambda x:x != 0, u03_rela))
print("max mean median 0.3:", min(u03_rela), np.mean(u03_rela), np.median(u03_rela))
u05_rela = list(filter(lambda x:x != 0, u05_rela))
print("max mean median 0.5:", min(u05_rela), np.mean(u05_rela), np.median(u05_rela))
u06_rela = list(filter(lambda x:x != 0, u06_rela))
print("max mean median 0.6:", min(u06_rela), np.mean(u06_rela), np.median(u06_rela))
u08_rela = list(filter(lambda x:x != 0, u08_rela))
print("max mean median 0.8:", min(u08_rela), np.mean(u08_rela), np.median(u08_rela))

# s4 = pd.Series(u03_rela)
# s3 = pd.Series(u05_rela)
# s2 = pd.Series(u06_rela)
# s1 = pd.Series(u08_rela)
# #
# for i in range(len(s1)):
#     if s1[i] == 0:
#         print("!!!!!!!!!!!!!!!!!!")

s1 = pd.Series(U08_difference_CBS_AVB_delayed_frame)
# s1test = list(filter(lambda x:x >0, s1))
# print(s1test)
s2 = pd.Series(U06_difference_CBS_AVB_delayed_frame)
s3 = pd.Series(U05_difference_CBS_AVB_delayed_frame)
s4 = pd.Series(U03_difference_CBS_AVB_delayed_frame)

data = pd.DataFrame({'Uti 0.3': s4, 'Uti 0.5': s3, 'Uti 0.6': s2, 'Uti 0.8': s1})
data.boxplot(whis =3, meanline=True, showmeans=True, meanprops={'linestyle':'--','color':'green', 'linewidth': 3}, capprops = {'linewidth': 3},
             medianprops={'linestyle':'--','color':'orange', 'linewidth': 3}, boxprops={'linewidth': 3},
             whiskerprops={'linewidth': 3})
plt.grid(linestyle="--", alpha=0.5)
plt.ylabel("Finish time difference", fontsize=26)
plt.title("The distribution of finish time difference of delayed SF frames", fontsize=26, pad=24)
plt.tick_params(labelsize=24)
plt.show()
#
# def set_title(ax, title):
#     ax.set_title(title)
#


# grid = plt.GridSpec(nrows=2, ncols=2)

# plt.suptitle('The finish time reduction of delayed SF frames', fontsize=26)

p1 = plt.subplot(221)
plt.title('The finish time reduction of delayed ST frame, Uti 0.3', fontsize=12, pad=10)
# plt.tick_params(labelsize=18)
s4.plot.hist(grid=True, bins=300, rwidth=0.9, color='#607c8e')
plt.xlabel("reduced time", fontsize=12)
plt.ylabel("counts", fontsize=12)
plt.grid(linestyle="--", alpha=0.5)

p2 = plt.subplot(222)
plt.title('The finish time reduction of delayed ST frame, Uti 0.5', fontsize=12, pad=10)
# plt.tick_params(labelsize=18)
s3.plot.hist(grid=True, bins=300, rwidth=0.9, color='#607c8e')
plt.xlabel("reduced time", fontsize=12)
plt.ylabel("counts", fontsize=12)
plt.grid(linestyle="--", alpha=0.5)

p3 = plt.subplot(223)
plt.title('The finish time reduction of delayed ST frame, Uti 0.6', fontsize=12, pad=10)
# plt.tick_params(labelsize=18)
s2.plot.hist(grid=True, bins=300, rwidth=0.9, color='#607c8e')
plt.xlabel("reduced time", fontsize=12)
plt.ylabel("counts", fontsize=12)
plt.grid(linestyle="--", alpha=0.5)

p4 = plt.subplot(224)
plt.title('The finish time reduction of delayed ST frame, Uti 0.8', fontsize=12, pad=10)
# plt.tick_params(labelsize=18)
s1.plot.hist(grid=True, bins=300, rwidth=0.9, color='#607c8e')
plt.xlabel("reduced time", fontsize=12)
plt.ylabel("counts", fontsize=12)
plt.grid(linestyle="--", alpha=0.5)
#
#

plt.show()



#
# #
#
# s1.plot.hist(grid=True, bins=100, rwidth=0.9,
#                    color='#607c8e')
# plt.title("The response time reduction of delayed SF frame, Uti 0.8", fontsize=24, pad=24)
# plt.xlabel('Response time reduction ', fontsize=24)
# plt.ylabel('Counts', fontsize=24)
# plt.grid(linestyle="--", alpha=0.5)
# plt.tick_params(labelsize=24)
# plt.show()
#
# s2.plot.hist(grid=True, bins=100, rwidth=0.9,
#                    color='#607c8e')
# plt.title("The response time reduction of delayed SF frame, Uti 0.6", fontsize=24, pad=24)
# plt.xlabel('Response time reduction ', fontsize=24)
# plt.ylabel('Counts', fontsize=24)
# plt.grid(linestyle="--", alpha=0.5)
# plt.tick_params(labelsize=24)
# plt.show()
#
# s3.plot.hist(grid=True, bins=100, rwidth=0.9,
#                    color='#607c8e')
# plt.title("The response time reduction of delayed SF frame, Uti 0.5", fontsize=24, pad=24)
# plt.xlabel('Response time reduction ', fontsize=24)
# plt.ylabel('Counts', fontsize=24)
# plt.grid(linestyle="--", alpha=0.5)
# plt.tick_params(labelsize=24)
# plt.show()
#
# s4.plot.hist(grid=True, bins=100, rwidth=0.9,
#                    color='#607c8e')
# plt.title("The response time reduction of delayed SF frame, Uti 0.3", fontsize=24, pad=24)
# plt.xlabel('Response time reduction ', fontsize=24)
# plt.ylabel('Counts', fontsize=24)
# plt.grid(linestyle="--", alpha=0.5)
# plt.tick_params(labelsize=24)
# plt.show()



import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import pickle
import seaborn as sns
# delayed frame
thred = 0.0
# uti 0.3
with open('/home/jiezou/EMSOFT\'21_Flex-TSN/Scheduling_without_guarantee/uti_0.3_10ST/difference_CBS_AVB_max_response_time_classA.pickle', 'rb') as handle:
    difference_CBS_AVB_max_response_time_classA03 = pickle.load(handle)
difference_CBS_AVB_max_response_time_classA03 = list(filter(lambda x: x > thred or x < -thred, difference_CBS_AVB_max_response_time_classA03))

with open('/home/jiezou/EMSOFT\'21_Flex-TSN/Scheduling_without_guarantee/uti_0.3_10ST/difference_CBS_AVB_max_response_time_classB.pickle', 'rb') as handle:
    difference_CBS_AVB_max_response_time_classB03 = pickle.load(handle)
difference_CBS_AVB_max_response_time_classB03 = list(filter(lambda x: x > thred or x < -thred, difference_CBS_AVB_max_response_time_classB03))

with open('/home/jiezou/EMSOFT\'21_Flex-TSN/Scheduling_without_guarantee/uti_0.3_10ST/AVB_classA_response_time.pickle', 'rb') as handle:
    AVB_response_A = pickle.load(handle)

with open('/home/jiezou/EMSOFT\'21_Flex-TSN/Scheduling_without_guarantee/uti_0.3_10ST/CBS_based_classA_response_time.pickle', 'rb') as handle:
    CBS_response_A = pickle.load(handle)

with open('/home/jiezou/EMSOFT\'21_Flex-TSN/Scheduling_without_guarantee/uti_0.3_10ST/AVB_classB_response_time.pickle', 'rb') as handle:
    AVB_response_B = pickle.load(handle)

with open('/home/jiezou/EMSOFT\'21_Flex-TSN/Scheduling_without_guarantee/uti_0.3_10ST/CBS_based_classB_response_time.pickle', 'rb') as handle:
    CBS_response_B = pickle.load(handle)
# x = range(len(AVB_response))
# plt.plot(x, AVB_response, label='Uti 0.8', marker='o', color='orange', linewidth=2)
# plt.plot(x, CBS_response, label='Uti 0.8', marker='o', color='blue', linewidth=2)
# plt.show()

response_diff_A = []
for i in range(len(AVB_response_A)):
    response_diff_A.append((CBS_response_A[i] - AVB_response_A[i])/ AVB_response_A[i])
response_diff_A = list(filter(lambda x: x > thred or x < -thred, response_diff_A))

ref_A = pd.Series(response_diff_A)
ref_A.plot.hist(grid=True, bins=100, rwidth=0.9,
                   color='#607c8e')
plt.title("The response time reduction for class A, Uti 0.3", fontsize=24, pad=24)
plt.xlabel('Response time reduction ', fontsize=24)
plt.ylabel('Counts', fontsize=24)
plt.grid(linestyle="--", alpha=0.5)
plt.tick_params(labelsize=24)
plt.show()



response_diff_B = []
for i in range(len(AVB_response_B)):
    response_diff_B.append((CBS_response_B[i] - AVB_response_B[i])/AVB_response_B[i])

response_diff_B = list(filter(lambda x: x > thred or x < -thred, response_diff_B))

ref_B = pd.Series(response_diff_B)
ref_B.plot.hist(grid=True, bins=100, rwidth=0.9,
                   color='#607c8e')
plt.title("The response time reduction for class B, Uti 0.3", fontsize=24, pad=24)
plt.xlabel('Response time reduction ', fontsize=24)
plt.ylabel('Counts', fontsize=24)
plt.grid(linestyle="--", alpha=0.5)
plt.tick_params(labelsize=24)
plt.show()





classA03 = pd.Series(difference_CBS_AVB_max_response_time_classA03)
classB03 = pd.Series(difference_CBS_AVB_max_response_time_classB03)


classA03.plot.hist(grid=True, bins=100, rwidth=0.9,
                   color='#607c8e')
plt.title("The maximum response time reduction for class A, Uti 0.3", fontsize=24, pad=24)
plt.xlabel('Response time reduction ', fontsize=24)
plt.ylabel('Counts', fontsize=24)
plt.grid(linestyle="--", alpha=0.5)
plt.tick_params(labelsize=24)
plt.show()

classB03.plot.hist(grid=True, bins=100, rwidth=0.9,
                   color='#607c8e')
plt.title("The maximum response time reduction for class B, Uti 0.3", fontsize=24, pad=24)
plt.xlabel('Response time reduction ', fontsize=24)
plt.ylabel('Counts', fontsize=24)
plt.grid(linestyle="--", alpha=0.5)
plt.tick_params(labelsize=24)
plt.show()





# uti 0.5
with open('/home/jiezou/EMSOFT\'21_Flex-TSN/Scheduling_without_guarantee/uti_0.5_10ST/difference_CBS_AVB_max_response_time_classA.pickle', 'rb') as handle:
    difference_CBS_AVB_max_response_time_classA05 = pickle.load(handle)
difference_CBS_AVB_max_response_time_classA05 = list(filter(lambda x: x > thred or x < -thred, difference_CBS_AVB_max_response_time_classA05))

with open('/home/jiezou/EMSOFT\'21_Flex-TSN/Scheduling_without_guarantee/uti_0.5_10ST/difference_CBS_AVB_max_response_time_classB.pickle', 'rb') as handle:
    difference_CBS_AVB_max_response_time_classB05 = pickle.load(handle)
difference_CBS_AVB_max_response_time_classB05 = list(filter(lambda x: x > thred or x < -thred, difference_CBS_AVB_max_response_time_classB05))

with open('/home/jiezou/EMSOFT\'21_Flex-TSN/Scheduling_without_guarantee/uti_0.5_10ST/AVB_classA_response_time.pickle', 'rb') as handle:
    AVB_response_A05 = pickle.load(handle)

with open('/home/jiezou/EMSOFT\'21_Flex-TSN/Scheduling_without_guarantee/uti_0.5_10ST/CBS_based_classA_response_time.pickle', 'rb') as handle:
    CBS_response_A05 = pickle.load(handle)

with open('/home/jiezou/EMSOFT\'21_Flex-TSN/Scheduling_without_guarantee/uti_0.5_10ST/AVB_classB_response_time.pickle', 'rb') as handle:
    AVB_response_B05 = pickle.load(handle)

with open('/home/jiezou/EMSOFT\'21_Flex-TSN/Scheduling_without_guarantee/uti_0.5_10ST/CBS_based_classB_response_time.pickle', 'rb') as handle:
    CBS_response_B05 = pickle.load(handle)
# x = range(len(AVB_response))
# plt.plot(x, AVB_response, label='Uti 0.8', marker='o', color='orange', linewidth=2)
# plt.plot(x, CBS_response, label='Uti 0.8', marker='o', color='blue', linewidth=2)
# plt.show()

response_diff_A05 = []
for i in range(len(AVB_response_A05)):
    response_diff_A05.append((CBS_response_A05[i] - AVB_response_A05[i])/AVB_response_A05[i])
response_diff_A05 = list(filter(lambda x: x > thred or x < -thred, response_diff_A05))

ref_A05 = pd.Series(response_diff_A05)
ref_A05.plot.hist(grid=True, bins=100, rwidth=0.9,
                   color='#607c8e')
plt.title("The response time reduction for class A, Uti 0.5", fontsize=24, pad=24)
plt.xlabel('Response time reduction ', fontsize=24)
plt.ylabel('Counts', fontsize=24)
plt.grid(linestyle="--", alpha=0.5)
plt.tick_params(labelsize=24)
plt.show()



response_diff_B05 = []
for i in range(len(AVB_response_B05)):
    response_diff_B05.append((CBS_response_B05[i] - AVB_response_B05[i])/ AVB_response_B05[i])
response_diff_B05 = list(filter(lambda x: x > thred or x < -thred, response_diff_B05))

ref_B05 = pd.Series(response_diff_B05)
ref_B05.plot.hist(grid=True, bins=100, rwidth=0.9,
                   color='#607c8e')
plt.title("The response time reduction for class B, Uti 0.5", fontsize=24, pad=24)
plt.xlabel('Response time reduction ', fontsize=24)
plt.ylabel('Counts', fontsize=24)
plt.grid(linestyle="--", alpha=0.5)
plt.tick_params(labelsize=24)
plt.show()





classA05 = pd.Series(difference_CBS_AVB_max_response_time_classA05)
classB05 = pd.Series(difference_CBS_AVB_max_response_time_classB05)


classA05.plot.hist(grid=True, bins=100, rwidth=0.9,
                   color='#607c8e')
plt.title("The maximum response time reduction for class A, Uti 0.5", fontsize=24, pad=24)
plt.xlabel('Response time reduction ', fontsize=24)
plt.ylabel('Counts', fontsize=24)
plt.grid(linestyle="--", alpha=0.5)
plt.tick_params(labelsize=24)
plt.show()

classB05.plot.hist(grid=True, bins=100, rwidth=0.9,
                   color='#607c8e')
plt.title("The maximum response time reduction for class B, Uti 0.5", fontsize=24, pad=24)
plt.xlabel('Response time reduction ', fontsize=24)
plt.ylabel('Counts', fontsize=24)
plt.grid(linestyle="--", alpha=0.5)
plt.tick_params(labelsize=24)
plt.show()




# uti 0.6
with open('/home/jiezou/EMSOFT\'21_Flex-TSN/Scheduling_without_guarantee/uti_0.6_10ST/difference_CBS_AVB_max_response_time_classA.pickle', 'rb') as handle:
    difference_CBS_AVB_max_response_time_classA06 = pickle.load(handle)

difference_CBS_AVB_max_response_time_classA06 = list(filter(lambda x: x > thred or x < -thred, difference_CBS_AVB_max_response_time_classA06))

with open('/home/jiezou/EMSOFT\'21_Flex-TSN/Scheduling_without_guarantee/uti_0.6_10ST/difference_CBS_AVB_max_response_time_classB.pickle', 'rb') as handle:
    difference_CBS_AVB_max_response_time_classB06 = pickle.load(handle)
difference_CBS_AVB_max_response_time_classB06 = list(filter(lambda x: x > thred or x < -thred, difference_CBS_AVB_max_response_time_classB06))

with open('/home/jiezou/EMSOFT\'21_Flex-TSN/Scheduling_without_guarantee/uti_0.6_10ST/AVB_classA_response_time.pickle', 'rb') as handle:
    AVB_response_A06 = pickle.load(handle)

with open('/home/jiezou/EMSOFT\'21_Flex-TSN/Scheduling_without_guarantee/uti_0.6_10ST/CBS_based_classA_response_time.pickle', 'rb') as handle:
    CBS_response_A06 = pickle.load(handle)

with open('/home/jiezou/EMSOFT\'21_Flex-TSN/Scheduling_without_guarantee/uti_0.6_10ST/AVB_classB_response_time.pickle', 'rb') as handle:
    AVB_response_B06 = pickle.load(handle)

with open('/home/jiezou/EMSOFT\'21_Flex-TSN/Scheduling_without_guarantee/uti_0.6_10ST/CBS_based_classB_response_time.pickle', 'rb') as handle:
    CBS_response_B06 = pickle.load(handle)
# x = range(len(AVB_response))
# plt.plot(x, AVB_response, label='Uti 0.8', marker='o', color='orange', linewidth=2)
# plt.plot(x, CBS_response, label='Uti 0.8', marker='o', color='blue', linewidth=2)
# plt.show()

response_diff_A06 = []
for i in range(len(AVB_response_A06)):
    response_diff_A06.append((CBS_response_A06[i] - AVB_response_A06[i])/ AVB_response_A06[i])

response_diff_A06 = list(filter(lambda x: x > thred or x < -thred, response_diff_A06))

ref_A06 = pd.Series(response_diff_A06)
ref_A06.plot.hist(grid=True, bins=100, rwidth=0.9,
                   color='#607c8e')
plt.title("The response time reduction for class A, Uti 0.6", fontsize=24, pad=24)
plt.xlabel('Response time reduction ', fontsize=24)
plt.ylabel('Counts', fontsize=24)
plt.grid(linestyle="--", alpha=0.5)
plt.tick_params(labelsize=24)
plt.show()



response_diff_B06 = []
for i in range(len(AVB_response_B06)):
    response_diff_B06.append((CBS_response_B06[i] - AVB_response_B06[i]) / AVB_response_B06[i])

response_diff_B06 = list(filter(lambda x: x > thred or x < -thred, response_diff_B06))

ref_B06 = pd.Series(response_diff_B06)
ref_B06.plot.hist(grid=True, bins=100, rwidth=0.9,
                   color='#607c8e')
plt.title("The response time reduction for class B, Uti 0.6", fontsize=24, pad=24)
plt.xlabel('Response time reduction ', fontsize=24)
plt.ylabel('Counts', fontsize=24)
plt.grid(linestyle="--", alpha=0.5)
plt.tick_params(labelsize=24)
plt.show()





classA06 = pd.Series(difference_CBS_AVB_max_response_time_classA06)
classB06 = pd.Series(difference_CBS_AVB_max_response_time_classB06)


classA06.plot.hist(grid=True, bins=100, rwidth=0.9,
                   color='#607c8e')
plt.title("The maximum response time reduction for class A, Uti 0.6", fontsize=24, pad=24)
plt.xlabel('Response time reduction ', fontsize=24)
plt.ylabel('Counts', fontsize=24)
plt.grid(linestyle="--", alpha=0.5)
plt.tick_params(labelsize=24)
plt.show()

classB06.plot.hist(grid=True, bins=100, rwidth=0.9,
                   color='#607c8e')
plt.title("The maximum response time reduction for class B, Uti 0.6", fontsize=24, pad=24)
plt.xlabel('Response time reduction ', fontsize=24)
plt.ylabel('Counts', fontsize=24)
plt.grid(linestyle="--", alpha=0.5)
plt.tick_params(labelsize=24)
plt.show()




# uti 0.8


with open('/home/jiezou/EMSOFT\'21_Flex-TSN/Scheduling_without_guarantee/uti_0.8_10ST/difference_CBS_AVB_max_response_time_classA.pickle', 'rb') as handle:
    difference_CBS_AVB_max_response_time_classA08 = pickle.load(handle)

difference_CBS_AVB_max_response_time_classA08 = list(filter(lambda x: x > thred or x < -thred, difference_CBS_AVB_max_response_time_classA08))

with open('/home/jiezou/EMSOFT\'21_Flex-TSN/Scheduling_without_guarantee/uti_0.8_10ST/difference_CBS_AVB_max_response_time_classB.pickle', 'rb') as handle:
    difference_CBS_AVB_max_response_time_classB08 = pickle.load(handle)

difference_CBS_AVB_max_response_time_classB08 = list(filter(lambda x: x > thred or x < -thred, difference_CBS_AVB_max_response_time_classB08))


with open('/home/jiezou/EMSOFT\'21_Flex-TSN/Scheduling_without_guarantee/uti_0.8_10ST/AVB_classA_response_time.pickle', 'rb') as handle:
    AVB_response_A08 = pickle.load(handle)

with open('/home/jiezou/EMSOFT\'21_Flex-TSN/Scheduling_without_guarantee/uti_0.8_10ST/CBS_based_classA_response_time.pickle', 'rb') as handle:
    CBS_response_A08 = pickle.load(handle)

with open('/home/jiezou/EMSOFT\'21_Flex-TSN/Scheduling_without_guarantee/uti_0.8_10ST/AVB_classB_response_time.pickle', 'rb') as handle:
    AVB_response_B08 = pickle.load(handle)

with open('/home/jiezou/EMSOFT\'21_Flex-TSN/Scheduling_without_guarantee/uti_0.8_10ST/CBS_based_classB_response_time.pickle', 'rb') as handle:
    CBS_response_B08 = pickle.load(handle)
# x = range(len(AVB_response))
# plt.plot(x, AVB_response, label='Uti 0.8', marker='o', color='orange', linewidth=2)
# plt.plot(x, CBS_response, label='Uti 0.8', marker='o', color='blue', linewidth=2)
# plt.show()

response_diff_A08 = []
for i in range(len(AVB_response_A08)):
    response_diff_A08.append((CBS_response_A08[i] - AVB_response_A08[i])/AVB_response_A08[i])

response_diff_A08 = list(filter(lambda x: x > thred or x < -thred, response_diff_A08))

ref_A08 = pd.Series(response_diff_A08)
ref_A08.plot.hist(grid=True, bins=100, rwidth=0.9,
                   color='#607c8e')
plt.title("The response time reduction for class A, Uti 0.8", fontsize=24, pad=24)
plt.xlabel('Response time reduction ', fontsize=24)
plt.ylabel('Counts', fontsize=24)
plt.grid(linestyle="--", alpha=0.5)
plt.tick_params(labelsize=24)
plt.show()



response_diff_B08 = []
for i in range(len(AVB_response_B08)):
    response_diff_B08.append((CBS_response_B08[i] - AVB_response_B08[i])/AVB_response_B08[i])

response_diff_B08 = list(filter(lambda x: x > thred or x < -thred, response_diff_B08))

ref_B08 = pd.Series(response_diff_B08)
ref_B08.plot.hist(grid=True, bins=100, rwidth=0.9,
                   color='#607c8e')
plt.title("The response time reduction for class B, Uti 0.8", fontsize=24, pad=24)
plt.xlabel('Response time reduction ', fontsize=24)
plt.ylabel('Counts', fontsize=24)
plt.grid(linestyle="--", alpha=0.5)
plt.tick_params(labelsize=24)
plt.show()





classA08 = pd.Series(difference_CBS_AVB_max_response_time_classA08)
classB08 = pd.Series(difference_CBS_AVB_max_response_time_classB08)


classA08.plot.hist(grid=True, bins=100, rwidth=0.9,
                   color='#607c8e')
plt.title("The maximum response time reduction for class A, Uti 0.8", fontsize=24, pad=24)
plt.xlabel('Response time reduction ', fontsize=24)
plt.ylabel('Counts', fontsize=24)
plt.grid(linestyle="--", alpha=0.5)
plt.tick_params(labelsize=24)
plt.show()

classB08.plot.hist(grid=True, bins=100, rwidth=0.9,
                   color='#607c8e')
plt.title("The maximum response time reduction for class B, Uti 0.8", fontsize=24, pad=24)
plt.xlabel('Response time reduction ', fontsize=24)
plt.ylabel('Counts', fontsize=24)
plt.grid(linestyle="--", alpha=0.5)
plt.tick_params(labelsize=24)
plt.show()
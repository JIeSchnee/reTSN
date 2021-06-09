import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import scipy
from scipy import stats
import pickle
import seaborn as sns
# delayed frame
thred = 0.00


def convert(CBS_A, AVB_A, CBS_B, AVB_B):

    CBSA = []
    AVBA = []
    moreA = 0
    for i in range(len(CBS_A)):
        if CBS_A[i] <= 2000 and AVB_A[i] <= 2000:
            CBSA.append(CBS_A[i])
            AVBA.append(AVB_A[i])
        elif CBS_A[i] <= 2000 and AVB_A[i] > 2000:
            moreA += 1

    CBSB = []
    AVBB = []
    moreB = 0
    for i in range(len(CBS_B)):
        if CBS_B[i] <= 2000 and AVB_B[i] <= 2000:
            CBSB.append(CBS_B[i])
            AVBB.append(AVB_B[i])
        elif CBS_B[i] <= 2000 and AVB_B[i] > 2000:
            moreB += 1
    return CBSA, AVBA, CBSB, AVBB, moreA, moreB


print("---------------------------0.3-----------------------------------")
# uti 0.3
with open('/home/.../uti_0.3_10ST/difference_CBS_AVB_max_response_time_classA.pickle', 'rb') as handle:
    difference_CBS_AVB_max_response_time_classA03 = pickle.load(handle)
difference_CBS_AVB_max_response_time_classA03 = list(filter(lambda x: x != 0, difference_CBS_AVB_max_response_time_classA03))
# print("mean, median", np.mean(difference_CBS_AVB_max_response_time_classA03), np.median(difference_CBS_AVB_max_response_time_classA03))

with open('/home/.../uti_0.3_10ST/difference_CBS_AVB_max_response_time_classB.pickle', 'rb') as handle:
    difference_CBS_AVB_max_response_time_classB03 = pickle.load(handle)
difference_CBS_AVB_max_response_time_classB03 = list(filter(lambda x: x != 0, difference_CBS_AVB_max_response_time_classB03))
# print("mean, median", np.mean(difference_CBS_AVB_max_response_time_classB03), np.median(difference_CBS_AVB_max_response_time_classB03))


with open('/home/.../uti_0.3_10ST/AVB_classA_response_time.pickle', 'rb') as handle:
    AVB_response_A = pickle.load(handle)

with open('/home/.../uti_0.3_10ST/CBS_based_classA_response_time.pickle', 'rb') as handle:
    CBS_response_A = pickle.load(handle)

with open('/home/.../uti_0.3_10ST/AVB_classB_response_time.pickle', 'rb') as handle:
    AVB_response_B = pickle.load(handle)

with open('/home/.../uti_0.3_10ST/CBS_based_classB_response_time.pickle', 'rb') as handle:
    CBS_response_B = pickle.load(handle)
# x = range(len(AVB_response))
# plt.plot(x, AVB_response, label='Uti 0.8', marker='o', color='orange', linewidth=2)
# plt.plot(x, CBS_response, label='Uti 0.8', marker='o', color='blue', linewidth=2)
# plt.show()
CBSA03 = []
AVBA03 = []
more03A = 0

for i in range(len(CBS_response_A)):
    if CBS_response_A[i] <= 2000 and AVB_response_A[i] <= 2000:
        CBSA03.append(CBS_response_A[i])
        AVBA03.append(AVB_response_A[i])
    elif CBS_response_A[i] <= 2000 and AVB_response_A[i] > 2000:
        more03A +=1

CBSB03 = []
AVBB03 = []
more03B = 0

for i in range(len(CBS_response_B)):
    if CBS_response_B[i] <= 2000 and AVB_response_B[i] <= 2000:
        CBSB03.append(CBS_response_B[i])
        AVBB03.append(AVB_response_B[i])
    elif CBS_response_B[i] <= 2000 and AVB_response_B[i] > 2000:
        more03B += 1

print("more transmitted frames", more03A, more03B)

# CBS_based_classA = []
# CBS_based_classB = []
# if len(CBS_response_A) >= len(AVB_response_A):
#     CBS_based_classA = CBS_response_A[:len(AVB_response_A)]
# if len(CBS_response_B) >= len(AVB_response_B):
#     CBS_based_classB = CBS_response_B[:len(AVB_response_B)]



response_diffpo_A = []
response_diff_A = []
for i in range(len(CBSA03)):
    response_diffpo_A.append((CBSA03[i] - AVBA03[i])/AVBA03[i])
    response_diff_A.append((CBSA03[i] - AVBA03[i]))
countA03 = 0
countA03_d = 0
for i in range(len(response_diff_A)):
    if response_diff_A[i]<0:
        countA03 += 1
    elif response_diff_A[i]>0:
        countA03_d += 1

print('percent of reduction classA 03 $ better , worse, unchanged:', countA03/len(response_diff_A),
      countA03_d/len(response_diff_A), 1-countA03/len(response_diff_A)-countA03_d/len(response_diff_A))

response_diff_A = list(filter(lambda x: x != 0, response_diff_A))
response_diffpo_A = list(filter(lambda x: x != 0, response_diffpo_A))

ref_A_max03 = min(response_diffpo_A)
ref_A_mean03 = np.mean(response_diffpo_A)
ref_A_median03 = np.median(response_diffpo_A)
print('ref_A03', ref_A_mean03, ref_A_median03)



response_diff_B = []
response_diffpo_B = []
for i in range(len(AVB_response_B)):
    response_diffpo_B.append((CBSB03[i] - AVBB03[i])/AVBB03[i])
    response_diff_B.append((CBSB03[i] - AVBB03[i]))
countB03 = 0
countB03_d =0
for i in range(len(response_diff_B)):
    if response_diff_B[i]<0:
        countB03 += 1
    elif response_diff_B[i] > 0:
        countB03_d +=1

print('percent of reduction classB 03 $ better , worse, unchanged:', countB03/len(response_diff_B),
      countB03_d/len(response_diff_B), 1-countB03/len(response_diff_B)-countB03_d/len(response_diff_B))

response_diff_B = list(filter(lambda x: x != 0, response_diff_B))
response_diffpo_B = list(filter(lambda x: x != 0, response_diffpo_B))
ref_B_max03 = min(response_diffpo_B)
ref_B_mean03 = np.mean(response_diffpo_B)
ref_B_median03 = np.median(response_diffpo_B)

print('ref_B03', ref_B_mean03, ref_B_median03)


# response_diff_A = list(filter(lambda x: x != 0, response_diff_A))
plt.subplot(211)

ref_A = pd.Series(response_diff_A)
ref_A.plot.hist(grid=True, bins=100, rwidth=0.9,
                   color='#607c8e')
plt.title("The finish time decreasing  time for class A, Uti 0.3", fontsize=12, pad=10)
plt.xlabel('decreasing  time',fontsize=12)
plt.ylabel('counts', fontsize=12)
plt.grid(linestyle="--", alpha=0.5)
# plt.tick_params(labelsize=16)
# plt.show()


# response_diff_B = list(filter(lambda x: x != 0, response_diff_B))
plt.subplot(212)

ref_B = pd.Series(response_diff_B)
ref_B.plot.hist(grid=True, bins=100, rwidth=0.9,
                   color='#607c8e')
plt.title("The finish time decreasing  time for class B, Uti 0.3", fontsize=12, pad=10)
plt.xlabel('decreasing  time', fontsize=12)
plt.ylabel('counts', fontsize=12)
plt.grid(linestyle="--", alpha=0.5)
# plt.tick_params(labelsize=10)
plt.show()


# norm_cdf03A = scipy.stats.norm.cdf(ref_A)
# sns.lineplot(x=ref_A, y=norm_cdf03A)
# plt.show()
#
# norm_cdf03B = scipy.stats.norm.cdf(ref_B)
# sns.lineplot(x=ref_B, y=norm_cdf03B)
# plt.show()

# plt.subplot(223)
# classA03 = pd.Series(difference_CBS_AVB_max_response_time_classA03)
# classB03 = pd.Series(difference_CBS_AVB_max_response_time_classB03)
#
# # countA03max = 0
# # countA03max_d = 0
# # for i in range(len(classA03)):
# #     if classA03[i]<0:
# #         countA03max += 1
# #     elif classA03[i] >0:
# #         countA03max_d +=1
# #
# # print('percent of max reduction classA 03  $ better , worse, unchanged:', countA03max/len(classA03),
# #       countA03max_d/len(classA03), 1-countA03max/len(classA03)-countA03max_d/len(classA03))
# #
# #
# # countB03max = 0
# # countB03max_d = 0
# # for i in range(len(classB03)):
# #     if classB03[i]<0:
# #         countB03max += 1
# #     elif classB03[i] >0:
# #         countB03max_d += 1
# #
# # print('percent of max reduction classB 03 $ better , worse, unchanged:', countB03max/len(classB03),
# #       countB03max_d/len(classB03), 1-countB03max/len(classB03)-countB03max_d/len(classB03))
#
#
#
# classA03.plot.hist(grid=True, bins=100, rwidth=0.9,
#                    color='#607c8e')
# plt.title("The maximum finish time decreasing  time for class A, Uti 0.3", fontsize=12, pad=10)
# plt.xlabel('decreasing  time', fontsize=12)
# plt.ylabel('counts', fontsize=12)
# plt.grid(linestyle="--", alpha=0.5)
# # plt.tick_params(labelsize=16)
# # plt.show()
#
# plt.subplot(224)
# classB03.plot.hist(grid=True, bins=100, rwidth=0.9,
#                    color='#607c8e')
# plt.title("The maximum finish time decreasing  time for class B, Uti 0.3", fontsize=12, pad=10)
# plt.xlabel('decreasing  time', fontsize=12)
# plt.ylabel('counts', fontsize=12)
# plt.grid(linestyle="--", alpha=0.5)
# # plt.tick_params(labelsize=16)
# plt.show()

# norm_cdf03A_max = scipy.stats.norm.cdf(classA03)
# sns.lineplot(x=classA03, y=norm_cdf03A_max)
# plt.show()
#
# norm_cdf03B_max = scipy.stats.norm.cdf(classB03)
# sns.lineplot(x=classB03, y=norm_cdf03B_max)
# plt.show()


print("---------------------------0.5-----------------------------------")
# uti 0.5
with open('/home/.../uti_0.5_10ST/difference_CBS_AVB_max_response_time_classA.pickle', 'rb') as handle:
    difference_CBS_AVB_max_response_time_classA05 = pickle.load(handle)
difference_CBS_AVB_max_response_time_classA05 = list(filter(lambda x: x != 0, difference_CBS_AVB_max_response_time_classA05))
# print("mean, median", np.mean(difference_CBS_AVB_max_response_time_classA05), np.median(difference_CBS_AVB_max_response_time_classA05))
with open('/home/.../uti_0.5_10ST/difference_CBS_AVB_max_response_time_classB.pickle', 'rb') as handle:
    difference_CBS_AVB_max_response_time_classB05 = pickle.load(handle)
difference_CBS_AVB_max_response_time_classB05 = list(filter(lambda x: x != 0, difference_CBS_AVB_max_response_time_classB05))
# print("mean, median", np.mean(difference_CBS_AVB_max_response_time_classB05), np.median(difference_CBS_AVB_max_response_time_classB05))

with open('/home/.../uti_0.5_10ST/AVB_classA_response_time.pickle', 'rb') as handle:
    AVB_response_A05 = pickle.load(handle)



with open('/home/.../uti_0.5_10ST/CBS_based_classA_response_time.pickle', 'rb') as handle:
    CBS_response_A05 = pickle.load(handle)

with open('/home/.../uti_0.5_10ST/AVB_classB_response_time.pickle', 'rb') as handle:
    AVB_response_B05 = pickle.load(handle)

with open('/home/.../uti_0.5_10ST/CBS_based_classB_response_time.pickle', 'rb') as handle:
    CBS_response_B05 = pickle.load(handle)

with open('/home/.../uti_0.5_10ST/classA_arrive_time.pickle',
          'rb') as handle:
    classA_arrive_time = pickle.load(handle)
classA_arrive_time = list(filter(lambda x: x !=100000000, classA_arrive_time))
with open(
        '/home/.../uti_0.5_10ST/classB_arrive_time.pickle',
        'rb') as handle:
    classB_arrive_time = pickle.load(handle)

# for i in range(len(difference_CBS_AVB_max_response_time_classB05)):
#     difference_CBS_AVB_max_response_time_classB05[i] = (difference_CBS_AVB_max_response_time_classB05[i]/ AVB_response_B05[i])




# print(len(classA_arrive_time), len(AVB_response_A05), len(CBS_response_A05))
# responseA_cbs = []
# responseA_avb = []
#
# for i in range(len(AVB_response_B05)):
#     responseA_avb.append(AVB_response_A05[i] - classA_arrive_time[i])
#     responseA_cbs.append(CBS_response_A05[i] - classA_arrive_time[i])
#
# ditest = []
# for i in range(len(responseA_avb)):
#     ditest.append(responseA_avb[i] - responseA_cbs[i])
# #
# # x = range(len(ditest))
# # plt.plot(x, ditest, label='Uti 0.8', marker='o', color='orange', linewidth=2)
# # plt.show()
#
# ditest = pd.Series(ditest)
# ditest.plot.hist(grid=True, bins=100, rwidth=0.9,
#                    color='#607c8e')
# plt.title("The finish time decreasing  time for class A, Uti 0.5", fontsize=12, pad=10)
# plt.xlabel('decreasing  time', fontsize=12)
# plt.ylabel('counts', fontsize=12)
# plt.grid(linestyle="--", alpha=0.5)
# plt.show()


CBS_classA05, AVB_classA05, CBS_classB05, AVB_classB05, moreA05, moreB05 = convert(CBS_response_A05, AVB_response_A05, CBS_response_B05, AVB_response_B05)

print("more transmitted frame", moreA05, moreB05)

response_diff_A05 = []
response_diffpo_A05 = []
for i in range(len(CBS_classA05)):
    response_diffpo_A05.append((CBS_classA05[i] - AVB_classA05[i])/AVB_classA05[i])
    response_diff_A05.append((CBS_classA05[i] - AVB_classA05[i]))
countA05 = 0
countA05_d = 0
for i in range(len(response_diff_A05)):
    if response_diff_A05[i]<0:
        countA05 += 1
    elif response_diff_A05[i] > 0:
        countA05_d += 1
print('percent of reduction classA 05 $ better , worse, unchanged:', countA05/len(response_diff_A05),
      countA05_d/len(response_diff_A05), 1-countA05/len(response_diff_A05)-countA05_d/len(response_diff_A05))

response_diff_A05 = list(filter(lambda x: x != 0, response_diff_A05))
response_diffpo_A05 = list(filter(lambda x: x != 0, response_diffpo_A05))


ref_A_mean05 = np.mean(response_diffpo_A05)
ref_A_median05 = np.median(response_diffpo_A05)

print('ref_A05', ref_A_mean05, ref_A_median05)


plt.subplot(211)
ref_A05 = pd.Series(response_diff_A05)
ref_A05.plot.hist(grid=True, bins=100, rwidth=0.9,
                   color='#607c8e')
plt.title("The finish time decreasing  time for class A, Uti 0.5", fontsize=12, pad=10)
plt.xlabel('decreasing  time', fontsize=12)
plt.ylabel('counts', fontsize=12)
plt.grid(linestyle="--", alpha=0.5)
# plt.tick_params(labelsize=16)
# plt.show()


response_diff_B05 = []
response_diffpo_B05 = []
for i in range(len(CBS_classB05)):
    response_diffpo_B05.append((CBS_classB05[i] - AVB_classB05[i])/AVB_classB05[i])
    response_diff_B05.append((CBS_classB05[i] - AVB_classB05[i]))

countB05 = 0
countB05_d = 0
for i in range(len(response_diff_B05)):
    if response_diff_B05[i]<0:
        countB05 += 1
    elif response_diff_B05[i] > 0:
        countB05_d += 1
print('percent of reduction classB 05 $ better , worse, unchanged:', countB05/len(response_diff_B05),
      countB05_d/len(response_diff_B05), 1-countB05/len(response_diff_B05)-countB05_d/len(response_diff_B05))

response_diff_B05 = list(filter(lambda x: x != 0, response_diff_B05))
response_diffpo_B05 = list(filter(lambda x: x != 0, response_diffpo_B05))


ref_B_mean05 = np.mean(response_diffpo_B05)
ref_B_median05 = np.median(response_diffpo_B05)

print('ref_B05', ref_B_mean05, ref_B_median05)

plt.subplot(212)
ref_B05 = pd.Series(response_diff_B05)
ref_B05.plot.hist(grid=True, bins=100, rwidth=0.9,
                   color='#607c8e')
plt.title("The finish time decreasing  time for class B, Uti 0.5", fontsize=12, pad=10)
plt.xlabel('decreasing  time', fontsize=12)
plt.ylabel('counts', fontsize=12)
plt.grid(linestyle="--", alpha=0.5)
# plt.tick_params(labelsize=16)
plt.show()



# norm_cdf05A = scipy.stats.norm.cdf(ref_A05)
# sns.lineplot(x=ref_A05, y=norm_cdf05A)
# plt.show()
#
# norm_cdf05B = scipy.stats.norm.cdf(ref_B05)
# sns.lineplot(x=ref_B05, y=norm_cdf05B)
# plt.show()



# plt.subplot(223)
#
# classA05 = pd.Series(difference_CBS_AVB_max_response_time_classA05)
# classB05 = pd.Series(difference_CBS_AVB_max_response_time_classB05)
#
# countA05max = 0
# countA05max_d = 0
# for i in range(len(classA05)):
#     if classA05[i]<0:
#         countA05max += 1
#     elif classA05[i] > 0:
#         countA05max_d += 1
# # print('percent of max reduction classA 05 $ better , worse, unchanged:', countA05max/len(classA05),
# #       countA05max_d/len(classA05), 1-countA05max/len(classA05)-countA05max_d/len(classA05))
#
# countB05max = 0
# countB05max_d = 0
# for i in range(len(classB05)):
#     if classB05[i]<0:
#         countB05max += 1
#     elif classB05[i] > 0:
#         countB05max_d += 1
# # print('percent of max reduction classB 05 $ better , worse, unchanged', countB05max/len(classB05),
# #       countB05max_d/len(classB05), 1-countB05max/len(classB05)-countB05max_d/len(classB05))
#
#
#
# classA05.plot.hist(grid=True, bins=100, rwidth=0.9,
#                    color='#607c8e')
# plt.title("The maximum finish time decreasing  time for class A, Uti 0.5", fontsize=12, pad=10)
# plt.xlabel('decreasing  time', fontsize=12)
# plt.ylabel('counts', fontsize=12)
# plt.grid(linestyle="--", alpha=0.5)
# # plt.tick_params(labelsize=16)
# # plt.show()
# plt.subplot(224)
# classB05.plot.hist(grid=True, bins=100, rwidth=0.9,
#                    color='#607c8e')
# plt.title("The maximum finish time decreasing  time for class B, Uti 0.5", fontsize=12, pad=10)
# plt.xlabel('decreasing  time', fontsize=12)
# plt.ylabel('counts', fontsize=12)
# plt.grid(linestyle="--", alpha=0.5)
# # plt.tick_params(labelsize=16)
# plt.show()
# #
# norm_cdf05A_max = scipy.stats.norm.cdf(classA05)
# sns.lineplot(x=classA05, y=norm_cdf05A_max)
# plt.show()
#
# norm_cdf05B_max = scipy.stats.norm.cdf(classB05)
# sns.lineplot(x=classB05, y=norm_cdf05B_max)
# plt.show()



print("---------------------------0.6-----------------------------------")
# uti 0.6
with open('/home/.../uti_0.6_10ST/difference_CBS_AVB_max_response_time_classA.pickle', 'rb') as handle:
    difference_CBS_AVB_max_response_time_classA06 = pickle.load(handle)

difference_CBS_AVB_max_response_time_classA06 = list(filter(lambda x: x != 0, difference_CBS_AVB_max_response_time_classA06))
# print("mean, median", np.mean(difference_CBS_AVB_max_response_time_classA06), np.median(difference_CBS_AVB_max_response_time_classA06))

with open('/home/.../uti_0.6_10ST/difference_CBS_AVB_max_response_time_classB.pickle', 'rb') as handle:
    difference_CBS_AVB_max_response_time_classB06 = pickle.load(handle)
difference_CBS_AVB_max_response_time_classB06 = list(filter(lambda x: x != 0, difference_CBS_AVB_max_response_time_classB06))
# print("mean, median", np.mean(difference_CBS_AVB_max_response_time_classB06), np.median(difference_CBS_AVB_max_response_time_classB06))

with open('/home/.../uti_0.6_10ST/AVB_classA_response_time.pickle', 'rb') as handle:
    AVB_response_A06 = pickle.load(handle)

with open('/home/.../uti_0.6_10ST/CBS_based_classA_response_time.pickle', 'rb') as handle:
    CBS_response_A06 = pickle.load(handle)

with open('/home/.../uti_0.6_10ST/AVB_classB_response_time.pickle', 'rb') as handle:
    AVB_response_B06 = pickle.load(handle)

with open('/home/.../uti_0.6_10ST/CBS_based_classB_response_time.pickle', 'rb') as handle:
    CBS_response_B06 = pickle.load(handle)


# r06AA = pd.Series(AVB_response_A06)
# r06AC = pd.Series(CBS_response_A06)
# r06BA = pd.Series(AVB_response_B06)
# r06BC = pd.Series(CBS_response_B06)
# plt.subplot(221)
# r06AA.plot.hist(grid=True, bins=100, rwidth=0.9, color='#607c8e')
# plt.subplot(222)
# r06BA.plot.hist(grid=True, bins=100, rwidth=0.9, color='#607c8e')
# plt.subplot(223)
# r06AC.plot.hist(grid=True, bins=100, rwidth=0.9, color='#607c8e')
# plt.subplot(224)
# r06BC.plot.hist(grid=True, bins=100, rwidth=0.9, color='#607c8e')
# plt.show()

# x = range(len(AVB_response))
# plt.plot(x, AVB_response, label='Uti 0.8', marker='o', color='orange', linewidth=2)
# plt.plot(x, CBS_response, label='Uti 0.8', marker='o', color='blue', linewidth=2)
# plt.show()


CBS_classA06, AVB_classA06, CBS_classB06, AVB_classB06, moreA06, moreB06 = convert(CBS_response_A06, AVB_response_A06, CBS_response_B06,
                                                                 AVB_response_B06)
print("more transmitted frame", moreA06, moreB06)

response_diff_A06 = []
response_diffpo_A06 = []
for i in range(len(CBS_classA06)):
    response_diffpo_A06.append((CBS_classA06[i] - AVB_classA06[i])/AVB_classA06[i])
    response_diff_A06.append((CBS_classA06[i] - AVB_classA06[i]))

countA06 = 0
countA06_d = 0
for i in range(len(response_diff_A06)):
    if response_diff_A06[i]<0:
        countA06 += 1
    elif response_diff_A06[i] >0:
        countA06_d += 1
print('percent of reduction classA 06 $ better , worse, unchanged:', countA06/len(response_diff_A06),
      countA06_d/len(response_diff_A06), 1-countA06/len(response_diff_A06)-countA06_d/len(response_diff_A06))

response_diff_A06 = list(filter(lambda x: x != 0, response_diff_A06))
response_diffpo_A06 = list(filter(lambda x: x != 0, response_diffpo_A06))


ref_A_mean06 = np.mean(response_diffpo_A06)
ref_A_median06 = np.median(response_diffpo_A06)

print('ref_A06', ref_A_mean06, ref_A_median06)

plt.subplot(211)

ref_A06 = pd.Series(response_diff_A06)
ref_A06.plot.hist(grid=True, bins=100, rwidth=0.9,
                   color='#607c8e')
plt.title("The finish time decreasing  time for class A, Uti 0.6", fontsize=12, pad=10)
plt.xlabel('decreasing  time', fontsize=12)
plt.ylabel('counts', fontsize=12)
plt.grid(linestyle="--", alpha=0.5)
# plt.tick_params(labelsize=16)
# plt.show()


response_diff_B06 = []
response_diffpo_B06 = []
for i in range(len(CBS_classB06)):
    response_diffpo_B06.append((CBS_classB06[i] - AVB_classB06[i])/AVB_classB06[i])
    response_diff_B06.append((CBS_classB06[i] - AVB_classB06[i]))

countB06 = 0
countB06_d =0
for i in range(len(response_diff_B06)):
    if response_diff_B06[i]<0:
        countB06 += 1
    elif response_diff_B06[i] >0:
        countB06_d +=1
print('percent of reduction classB 06 $ better , worse, unchanged:', countB06/len(response_diff_B06),
      countB06_d/len(response_diff_B06), 1- countB06/len(response_diff_B06) - countB06_d/len(response_diff_B06))

response_diff_B06 = list(filter(lambda x: x != 0, response_diff_B06))
response_diffpo_B06 = list(filter(lambda x: x != 0, response_diffpo_B06))


ref_B_mean06 = np.mean(response_diffpo_B06)
ref_B_median06 = np.median(response_diffpo_B06)

print('ref_B06', ref_B_mean06, ref_B_median06)

plt.subplot(212)
ref_B06 = pd.Series(response_diff_B06)
ref_B06.plot.hist(grid=True, bins=100, rwidth=0.9,
                   color='#607c8e')
plt.title("The finish time decreasing  time for class B, Uti 0.6",  fontsize=12, pad=10)
plt.xlabel('decreasing  time',  fontsize=12)
plt.ylabel('counts',  fontsize=12)
plt.grid(linestyle="--", alpha=0.5)
# plt.tick_params(labelsize=16)
plt.show()



# norm_cdf06A = scipy.stats.norm.cdf(ref_A06)
# sns.lineplot(x=ref_A06, y=norm_cdf06A)
# plt.show()
#
# norm_cdf06B = scipy.stats.norm.cdf(ref_B06)
# sns.lineplot(x=ref_B06, y=norm_cdf06B)
# plt.show()


# plt.subplot(223)
#
# classA06 = pd.Series(difference_CBS_AVB_max_response_time_classA06)
# classB06 = pd.Series(difference_CBS_AVB_max_response_time_classB06)
#
# countA06max = 0
# countA06max_d = 0
# for i in range(len(classA06)):
#     if classA06[i]<0:
#         countA06max += 1
#     elif classA06[i] >0:
#         countA06max_d += 1
# # print('percent of max reduction classA 06 $ better , worse, unchanged:', countA06max/len(classA06),
# #       countA06max_d/len(classA06), 1 - countA06max/len(classA06) - countA06max_d/len(classA06))
#
# countB06max = 0
# countB06max_d = 0
# for i in range(len(classB06)):
#     if classB06[i]<0:
#         countB06max += 1
#     elif classB06[i]>0:
#         countB06max_d +=1
# # print('percent of max reduction classB 06 $ better , worse, unchanged:', countB06max/len(classB06),
# #       countB06max_d/len(classB06), 1- countB06max/len(classB06) - countB06max_d/len(classB06))
#
#
#
#
# classA06.plot.hist(grid=True, bins=100, rwidth=0.9,
#                    color='#607c8e')
# plt.title("The maximum finish time decreasing  time for class A, Uti 0.6",  fontsize=12, pad=10)
# plt.xlabel('decreasing  time',  fontsize=12)
# plt.ylabel('counts',  fontsize=12)
# plt.grid(linestyle="--", alpha=0.5)
# # plt.tick_params(labelsize=16)
# # plt.show()
#
# plt.subplot(224)
# classB06.plot.hist(grid=True, bins=100, rwidth=0.9,
#                    color='#607c8e')
# plt.title("The maximum finish time decreasing  time for class B, Uti 0.6",  fontsize=12, pad=10)
# plt.xlabel('decreasing  time',  fontsize=12)
# plt.ylabel('counts',  fontsize=12)
# plt.grid(linestyle="--", alpha=0.5)
# # plt.tick_params(labelsize=16)
# plt.show()

# norm_cdf06A_max = scipy.stats.norm.cdf(classA06)
# sns.lineplot(x=classA06, y=norm_cdf06A_max)
# plt.show()
#
# norm_cdf06B_max = scipy.stats.norm.cdf(classB06)
# sns.lineplot(x=classB06, y=norm_cdf06B_max)
# plt.show()

print("---------------------------0.8-----------------------------------")
# uti 0.8


with open('/home/.../uti_0.8_10ST/difference_CBS_AVB_max_response_time_classA.pickle', 'rb') as handle:
    difference_CBS_AVB_max_response_time_classA08 = pickle.load(handle)
difference_CBS_AVB_max_response_time_classA08 = list(filter(lambda x: x != 0, difference_CBS_AVB_max_response_time_classA08))
# print("mean, median", np.mean(difference_CBS_AVB_max_response_time_classA08), np.median(difference_CBS_AVB_max_response_time_classA08))


with open('/home/.../uti_0.8_10ST/difference_CBS_AVB_max_response_time_classB.pickle', 'rb') as handle:
    difference_CBS_AVB_max_response_time_classB08 = pickle.load(handle)

difference_CBS_AVB_max_response_time_classB08 = list(filter(lambda x: x != 0, difference_CBS_AVB_max_response_time_classB08))
# print("mean, median", np.mean(difference_CBS_AVB_max_response_time_classB08), np.median(difference_CBS_AVB_max_response_time_classB08))

with open('/home/.../uti_0.8_10ST/AVB_classA_response_time.pickle', 'rb') as handle:
    AVB_response_A08 = pickle.load(handle)

with open('/home/.../uti_0.8_10ST/CBS_based_classA_response_time.pickle', 'rb') as handle:
    CBS_response_A08 = pickle.load(handle)

with open('/home/.../uti_0.8_10ST/AVB_classB_response_time.pickle', 'rb') as handle:
    AVB_response_B08 = pickle.load(handle)

with open('/home/.../uti_0.8_10ST/CBS_based_classB_response_time.pickle', 'rb') as handle:
    CBS_response_B08 = pickle.load(handle)
# x = range(len(AVB_response))
# plt.plot(x, AVB_response, label='Uti 0.8', marker='o', color='orange', linewidth=2)
# plt.plot(x, CBS_response, label='Uti 0.8', marker='o', color='blue', linewidth=2)
# plt.show()


CBS_classA08, AVB_classA08, CBS_classB08, AVB_classB08, moreA08, moreB08 = convert(CBS_response_A08, AVB_response_A08, CBS_response_B08,
                                                                 AVB_response_B08)

print("more transmitted frame", moreA08, moreB08)



response_diff_A08 = []
response_diffpo_A08 =[]
for i in range(len(CBS_classA08)):
    response_diffpo_A08.append((CBS_classA08[i] - AVB_classA08[i])/AVB_classA08[i])
    response_diff_A08.append((CBS_classA08[i] - AVB_classA08[i]))

countA08 = 0
countA08_d = 0
for i in range(len(response_diff_A08)):
    if response_diff_A08[i]<0:
        countA08 += 1
    elif response_diff_A08[i] >0:
        countA08_d +=1
print('percent of reduction classA 08 $ better , worse, unchanged:', countA08/len(response_diff_A08), countA08_d/len(response_diff_A08),
      1-countA08/len(response_diff_A08)-countA08_d/len(response_diff_A08))

response_diff_A08 = list(filter(lambda x: x != 0, response_diff_A08))
response_diffpo_A08 = list(filter(lambda x: x != 0, response_diffpo_A08))


ref_A_mean08 = np.mean(response_diffpo_A08)
ref_A_median08 = np.median(response_diffpo_A08)

print('ref_A08', ref_A_mean08, ref_A_median08)


plt.subplot(211)
ref_A08 = pd.Series(response_diff_A08)
ref_A08.plot.hist(grid=True, bins=100, rwidth=0.9,
                   color='#607c8e')
plt.title("The finish time decreasing  time for class A, Uti 0.8",  fontsize=12, pad=10)
plt.xlabel('decreasing  time',fontsize=12)
plt.ylabel('counts', fontsize=12)
plt.grid(linestyle="--", alpha=0.5)
# plt.tick_params(labelsize=12)
# plt.show()



response_diff_B08 = []
response_diffpo_B08 = []
for i in range(len(CBS_classB08)):
    response_diffpo_B08.append((CBS_classB08[i] - AVB_classB08[i])/AVB_classB08[i])
    response_diff_B08.append((CBS_classB08[i] - AVB_classB08[i]))

countB08 = 0
countB08_d = 0
for i in range(len(response_diff_B08)):
    if response_diff_B08[i]<0:
        countB08 += 1
    elif response_diff_B08[i] >0:
        countB08_d +=1
print('percent of reduction classB 08 $ better , worse, unchanged:', countB08/len(response_diff_B08), countB08_d/len(response_diff_B08),
      1 - countB08/len(response_diff_B08) - countB08_d/len(response_diff_B08))

response_diff_B08 = list(filter(lambda x: x != 0, response_diff_B08))
response_diffpo_B08 = list(filter(lambda x: abs(x) > 0.01, response_diffpo_B08))

ref_B_mean08 = np.mean(response_diffpo_B08)
ref_B_median08 = np.median(response_diffpo_B08)

print('ref_B08', ref_B_mean08, ref_B_median08)

plt.subplot(212)
ref_B08 = pd.Series(response_diff_B08)
ref_B08.plot.hist(grid=True, bins=100, rwidth=0.9,
                   color='#607c8e')
plt.title("The finish time decreasing  time for class B, Uti 0.8",  fontsize=12, pad=10)
plt.xlabel('decreasing  time',  fontsize=12)
plt.ylabel('counts',  fontsize=12)
plt.grid(linestyle="--", alpha=0.5)
# plt.tick_params(labelsize=12)
plt.show()


# norm_cdf08A = scipy.stats.norm.cdf(ref_A08)
# sns.lineplot(x=ref_A08, y=norm_cdf08A)
# plt.show()
#
# norm_cdf08B = scipy.stats.norm.cdf(ref_B08)
# sns.lineplot(x=ref_B08, y=norm_cdf08B)
# plt.show()
#

#
# plt.subplot(223)
#
# classA08 = pd.Series(difference_CBS_AVB_max_response_time_classA08)
# classB08 = pd.Series(difference_CBS_AVB_max_response_time_classB08)
#
# countA08max = 0
# countA08max_d = 0
# for i in range(len(classA08)):
#     if classA08[i]<0:
#         countA08max += 1
#     elif classA08[i] >0:
#         countA08max_d +=1
# # print('percent of max reduction classA 08 $ better , worse, unchanged:', countA08max/len(classA08), countA08max_d/len(classA08),
# #       1 - countA08max/len(classA08) -countA08max_d/len(classA08))
#
# countB08max = 0
# countB08max_d = 0
# for i in range(len(classB08)):
#     if classB08[i]<0:
#         countB08max += 1
#     elif classB08[i] >0:
#         countB08max_d +=1
# # print('percent of max reduction classB 08 $ better , worse, unchanged:', countB08max/len(classB08), countB08max_d/len(classB08),
# #       1 - countB08max/len(classB08)-countB08max_d/len(classB08))
#
#
#
# classA08.plot.hist(grid=True, bins=100, rwidth=0.9,
#                    color='#607c8e')
# plt.title("The maximum finish time decreasing  time for class A, Uti 0.8",  fontsize=12, pad=10)
# plt.xlabel('decreasing  time',  fontsize=12)
# plt.ylabel('counts',  fontsize=12)
# plt.grid(linestyle="--", alpha=0.5)
# # plt.tick_params(labelsize=12)
# # plt.show()
#
# plt.subplot(224)
# classB08.plot.hist(grid=True, bins=100, rwidth=0.9,
#                    color='#607c8e')
# plt.title("The maximum finish time decreasing  time for class B, Uti 0.8",  fontsize=12, pad=10)
# plt.xlabel('decreasing  time',  fontsize=12)
# plt.ylabel('counts',  fontsize=12)
# plt.grid(linestyle="--", alpha=0.5)
# # plt.tick_params(labelsize=12)
# plt.show()

# norm_cdf08A_max = scipy.stats.norm.cdf(classA08)
# sns.lineplot(x=classA08, y=norm_cdf08A_max)
# plt.show()
#
# norm_cdf08B_max = scipy.stats.norm.cdf(classB08)
# sns.lineplot(x=classB08, y=norm_cdf08B_max)
# plt.show()

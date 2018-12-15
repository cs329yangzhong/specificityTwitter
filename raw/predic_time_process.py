import datetime
from datetime import datetime, timedelta
from dateutil import tz
from matplotlib import pyplot as plt
from scipy.stats import spearmanr, pearsonr, wilcoxon, tstd
import scipy.stats


output_low_bdi = []
output_hi_bdi = []
a = [0,1,2,3,4,5,6]
b = ['Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat', 'Sun']
idx_to_weekday = dict(zip(a, b))

user = []
scores = []
hours = []
lines = []

with open('users-bdi') as in_file:
    in_file.readline()
    for line in in_file:
        lines.append(line.strip().split())
user_bdi = {}
user_score = {}
for line in lines:
    score = int(line[-1])

    if score <= 13:
        score = 1
    elif score <= 19:
        score = 2
    elif score <= 28:
        score = 3
    else:
        score = 4
    user_bdi[line[0]] = score

all_bdi = []
user_count = []
with open('predicted_with_time', encoding='utf-8') as in_file:
    in_file.readline()
    for line in in_file:

        l = line.strip().split('\t')
        if l[-1] == 'None':
            continue
        current_user = l[0]
        score = float(l[2])
        scores.append(score)
        timestamp = l[3]
        # print(timestamp)

        user.append(current_user)
        all_bdi.append(user_bdi[current_user])

        if current_user not in user_score:
            user_score[current_user] = [score]
        else:
            user_score[current_user].append(score)

        utc_offset = int(l[-1])
        tzlocal = tz.tzoffset('IST', utc_offset)
        # print(timestamp)
        utc_time = datetime.strptime(str(timestamp), "%a %b %d %H:%M:%S %z %Y")
        utc_time = utc_time.replace(second=0, microsecond=0, minute=0, hour=utc_time.hour) + timedelta(
            hours=utc_time.minute // 30)
        local = str(utc_time.replace(tzinfo=tz.tzutc()).astimezone(tzlocal))
        # print(utc_time.replace(tzinfo=tz.tzutc()).astimezone(tzlocal).weekday())
        # print(local[11:13])
        if user_bdi[current_user] <= 1:
            user_count.append(current_user)
            output_low_bdi.append([score, idx_to_weekday[utc_time.replace(tzinfo=tz.tzutc()).astimezone(tzlocal).weekday()], str(int(local[11:13]))])
        elif user_bdi[current_user] > 2:

            output_hi_bdi.append(
                [score, idx_to_weekday[utc_time.replace(tzinfo=tz.tzutc()).astimezone(tzlocal).weekday()],
                 str(int(local[11:13]))])


        hours.append(int(str(int(local[11:13]))))
print(len(set(user_count)))
print(len(scores))
print(spearmanr(scores, all_bdi))
print(pearsonr(scores, all_bdi))
for key in user_score:
    user_score[key] = sum(user_score[key]) / len(user_score[key])
scores = []
all_bdi = []
for key in user_score:
    scores.append(user_score[key])
    all_bdi.append(user_bdi[key])
print(len(scores))
print(spearmanr(scores, all_bdi))
print(pearsonr(scores, all_bdi))

print(len(set(user)))

print(len(output_low_bdi))
weekend = []
weekend_score = []
weekend_time_dict = {}
weekday_score = []
weekday_time_dict = {}
weekday_count = 0
weekend_count = 0

with open('predicted_time_local', 'w', encoding='utf-8') as out:
    for i in ['score', 'weekday', 'hour']:
        out.write(i)
        out.write('\t')
    out.write('\n')
    for idx, info in enumerate(output_low_bdi):
        for i in info:
            out.write(str(i))
            out.write('\t')
        out.write('\n')
        if info[1] in weekend:
            weekend_count += 1
            if info[-1] not in weekend_time_dict:
                weekend_time_dict[info[-1]] = [info[0]]
            else:
                weekend_time_dict[info[-1]].append(info[0])
        else:
            weekday_count += 1
            if info[-1] not in weekday_time_dict:
                weekday_time_dict[info[-1]] = [info[0]]
            else:
                weekday_time_dict[info[-1]].append(info[0])
print(weekend_count)
print(weekday_count)

weekend_time_dict_count = {}
weekday_time_dict_count = {}

for i in weekend_time_dict.keys():
    weekend_time_dict_count[i] = len(weekend_time_dict[i])
    weekend_time_dict[i] = sum(weekend_time_dict[i]) / len(weekend_time_dict[i])

for i in weekday_time_dict.keys():
    weekday_time_dict_count[i] = len(weekday_time_dict[i])
    weekday_time_dict[i] = sum(weekday_time_dict[i]) / len(weekday_time_dict[i])

print(weekend_time_dict)
print(weekday_time_dict)

score_for_plot_weekend = []
count_for_plot_weekend = []
score_for_plot_weekday = []
count_for_plot_weekday = []

'''
for i in range(24):
    score_for_plot_weekend.append(weekend_time_dict[str(i)])
    count_for_plot_weekend.append(weekend_time_dict_count[str(i)])
'''
for i in range(24):
    score_for_plot_weekday.append(weekday_time_dict[str(i)])
    count_for_plot_weekday.append(weekday_time_dict_count[str(i)])

print(len(score_for_plot_weekend))
print(len(count_for_plot_weekday))

plt.figure(1)

ax1 = plt.subplot(111)
ax1.plot(range(24), score_for_plot_weekday, label='Not Depressed')
# ax2.plot(range(24), score_for_plot_weekend,  label='Not Depressed')
n_depressed_weekday = [i for i in score_for_plot_weekday]
n_depressed_weekend = [i for i in score_for_plot_weekend]

weekend_score = []
weekend_time_dict = {}
weekday_score = []
weekday_time_dict = {}
weekday_count = 0
weekend_count = 0

with open('predicted_time_local', 'w', encoding='utf-8') as out:
    for i in ['score', 'weekday', 'hour']:
        out.write(i)
        out.write('\t')
    out.write('\n')
    for idx, info in enumerate(output_hi_bdi):
        for i in info:
            out.write(str(i))
            out.write('\t')
        out.write('\n')
        if info[1] in weekend:
            weekend_count += 1
            if info[-1] not in weekend_time_dict:
                weekend_time_dict[info[-1]] = [info[0]]
            else:
                weekend_time_dict[info[-1]].append(info[0])
        else:
            weekday_count += 1
            if info[-1] not in weekday_time_dict:
                weekday_time_dict[info[-1]] = [info[0]]
            else:
                weekday_time_dict[info[-1]].append(info[0])
print(weekend_count)
print(weekday_count)

weekend_time_dict_count = {}
weekday_time_dict_count = {}

for i in weekend_time_dict.keys():
    weekend_time_dict_count[i] = len(weekend_time_dict[i])
    weekend_time_dict[i] = sum(weekend_time_dict[i]) / len(weekend_time_dict[i])

for i in weekday_time_dict.keys():
    weekday_time_dict_count[i] = len(weekday_time_dict[i])
    weekday_time_dict[i] = sum(weekday_time_dict[i]) / len(weekday_time_dict[i])

print(weekend_time_dict)
print(weekday_time_dict)

score_for_plot_weekend = []
count_for_plot_weekend = []
score_for_plot_weekday = []
count_for_plot_weekday = []
'''
for i in range(24):
    score_for_plot_weekend.append(weekend_time_dict[str(i)])
    count_for_plot_weekend.append(weekend_time_dict_count[str(i)])
'''
for i in range(24):
    score_for_plot_weekday.append(weekday_time_dict[str(i)])
    count_for_plot_weekday.append(weekday_time_dict_count[str(i)])

print(len(count_for_plot_weekday))
print(wilcoxon(n_depressed_weekday, score_for_plot_weekday))
print(scipy.stats.tstd(n_depressed_weekday))
print(scipy.stats.tstd(score_for_plot_weekday))
ax1.plot(range(24), score_for_plot_weekday, 'r--', label='Depressed')
# ax2.plot(range(24), score_for_plot_weekend, 'r--',  label='Depressed')

ax1.set_xlabel('time')
ax1.set_ylabel('score')
ax1.set_ylim(2.1, 2.9)
ax1.legend()

plt.show()


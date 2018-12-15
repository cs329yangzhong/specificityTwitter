import pandas as pd
import datetime
from matplotlib import pyplot as plt
'''
df = pd.read_csv('new_time_hour_round.csv')
df.to_csv('new_time.tsv', encoding='utf-8', sep='\t')
'''

year = []
weekdate = []
hour = []
score = []
with open('new_time.tsv', encoding='utf-8') as in_file:
    in_file.readline()
    for line in in_file:
        l = line.strip().split('\t')
        year.append(l[7])
        weekdate.append(l[-4])
        hour.append(l[-3])
        score.append(float(l[-7]))
print(year)
print(weekdate)
print(hour)

weekend = ['Sun', 'Sat']
weekend_score = []
weekend_hour_dict = {}
for idx, day in enumerate(weekdate):
    if day not in weekend:
        if hour[idx] not in weekend_hour_dict:
            weekend_hour_dict[hour[idx]] = [score[idx]]
        else:
            weekend_hour_dict[hour[idx]].append(score[idx])
print(weekend_score)
print(weekend_hour_dict)

weekend_hour_dict_count = {}
for i in weekend_hour_dict.keys():
    weekend_hour_dict_count[i] = len(weekend_hour_dict[i])
    weekend_hour_dict[i] = sum(weekend_hour_dict[i]) / len(weekend_hour_dict[i])

print(len(weekend_hour_dict))
print(weekend_hour_dict_count)

score_for_plot_weekend = []
count_for_plot_weekend = []
for i in range(24):
    score_for_plot_weekend.append(weekend_hour_dict[str(i)])
    count_for_plot_weekend.append(weekend_hour_dict_count[str(i)])
print(score_for_plot_weekend)
print(count_for_plot_weekend)

plt.bar(range(24), count_for_plot_weekend)
plt.xlabel('time')
plt.ylabel('count')
# plt.ylim(2.1, 2.9)
# plt.grid(True)

plt.show()


plt.plot(range(24), score_for_plot_weekend)
plt.xlabel('time')
plt.ylabel('score')
plt.ylim(2.1, 2.9)
# plt.grid(True)

plt.show()
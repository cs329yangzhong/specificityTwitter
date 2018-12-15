import pandas as pd
import json
import datetime

df = pd.read_csv('LIWC2015 Results (1000_tweets_per_user.csv).csv')
user_id = list(set(list(df['userID'])))
all_tweet_id = list(df['tweet_id'])
scores = list(df['Score'])
tweet_to_score = dict(zip(all_tweet_id, scores))
print(df['Score'])

result = []

path = 'C:\\Users\\Yuan\\Desktop\\twitter-demographics\\twitter-demographics\\Dec-2017\\12-22-17\\output\\'

result = []
user_count = 0
for user in user_id:
    user_count += 1
    count = 0
    with open(path + str(user), encoding='utf-8') as in_file:
        for line in in_file:
            if count == -1:
                break
            a_tweet = json.loads(line)
            time_zone = a_tweet['user']['utc_offset']
            tweet_id = a_tweet['id']
            if tweet_id in all_tweet_id:
                print('%d %d found time_zone %d / %d finished' % (user, tweet_id, user_count - 1, len(user_id)))
                utc_time = a_tweet['created_at']
                count += 1
                result.append([user, tweet_id, tweet_to_score[tweet_id], utc_time, time_zone])

print(result)
print(len(result))

with open('predicted_with_time', 'w', encoding='utf-8') as out_file:
    for title in ['user_id', 'tweet_id', 'score', 'utc_time', 'time_zone']:
        out_file.write(title)
        out_file.write('\t')
    for line in result:
        for item in line:
            out_file.write(str(item))
            out_file.write('\t')
        out_file.write('\n')

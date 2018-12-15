import pandas as pd

raw = pd.read_csv('LIWC2015 Results (1000_tweets_per_user.csv).csv', encoding='utf-8')
print(raw)
raw.to_csv('LIWC2015 Results 100', sep='\t', encoding='utf-8', index=False)

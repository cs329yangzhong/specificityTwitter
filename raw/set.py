import pandas as pd

'''
df_train = pd.read_csv('8_15_trainingSet', sep='\t', skip_blank_lines=True)
df_test = df_train.dropna()[-1000:]
print(df_test)
index = df_test.index.tolist()
df_train = df_train.drop(index, axis='rows')
df_valid = df_train.dropna()[-500:]
index = df_valid.index.tolist()
df_train = df_train.drop(index, axis='rows')
print(df_train)

df_train.to_csv('training.tsv', sep='\t', encoding='utf-8')
df_test.to_csv('test.tsv', sep='\t', encoding='utf-8', index=False)
df_valid.to_csv('validation.tsv', sep='\t', encoding='utf-8', index=False)
'''

df = pd.read_csv('training', sep='\t', skip_blank_lines=True)
score = list(df['Score'])
print(sum(score)/len(score))
print(min(score))
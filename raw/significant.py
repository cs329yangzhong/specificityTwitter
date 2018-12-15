from scipy.stats import wilcoxon
from scipy.stats import ttest_rel
from scipy.stats import mannwhitneyu
from scipy.stats import spearmanr, pearsonr

path = '.\\result\\'
feature_a = []
with open(path + 'RBF_ALL_noEmotion_output') as in_file:
    in_file.readline()
    in_file.readline()
    for line in in_file:
        feature_a.append(float(line.strip()))

feature_b = []
with open(path + 'RBF_All_TEMP_output') as in_file:
    in_file.readline()
    in_file.readline()
    for line in in_file:
        feature_b.append(float(line.strip()))

feature_t = []
with open(path + 'testing_target') as in_file:
    for line in in_file:
        feature_t.append(float(line.strip()))

print(pearsonr(feature_a, feature_t))
feature_a = [abs(feature_a[i] - feature_t[i]) for i in range(1000)]
feature_b = [abs(feature_b[i] - feature_t[i]) for i in range(1000)]

print(sum(feature_a)/1000)
print(sum(feature_b)/1000)
print(wilcoxon(feature_a, feature_b))
print(ttest_rel(feature_a, feature_b))
print(mannwhitneyu(feature_a, feature_b))

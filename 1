from sklearn.linear_model import LogisticRegression
from sklearn.linear_model import LinearRegression
from sklearn.svm import SVR, LinearSVR
import numpy as np
from scipy.stats import pearsonr


if __name__ == '__main__':
    lines = []
    with open('users-bdi') as in_file:
        in_file.readline()
        for line in in_file:
            lines.append(line.strip().split())
    user_bdi = {}
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
    print(user_bdi)
    print(len(user_bdi))
    speci = {}

    with open('LIWC2015 Results annotated') as in_file:
        in_file.readline()

        for line in in_file:
            if len(line.strip()) < 2:
                continue
            l = line.strip().split('\t')
            if l[1] in user_bdi:
                if l[1] not in speci:
                    speci[l[1]] = [user_bdi[l[1]], float(l[4])]
                else:
                    speci[l[1]][1] = (float(l[4]) + speci[l[1]][1]) / 2

    print(speci)
    print(len(speci))

    validation_speci = {}
    with open('validation') as in_file:
        in_file.readline()
        for line in in_file:
            l = line.strip().split()
            if l[1] in user_bdi:
                if l[1] not in speci:
                    speci[l[1]] = [user_bdi[l[1]], float(l[3])]
                else:
                    speci[l[1]][1] = (float(l[3]) + speci[l[1]][1]) / 2

    print(validation_speci)
    print(len(validation_speci))

    testing_speci = {}
    with open('testing', encoding='Windows-1252') as in_file:
        in_file.readline()
        for line in in_file:
            l = line.strip().split('\t')
            if l[1] in user_bdi:
                speci[l[1]] = [user_bdi[l[1]],float(l[3])]

    print(testing_speci)
    print(len(testing_speci))

    print(speci)
    print(len(speci))
    bdi = []
    sp = []
    for item in speci.keys():
        print(speci[item])
        bdi.append(speci[item][0])
        sp.append(speci[item][1])

    print(pearsonr(bdi, sp))

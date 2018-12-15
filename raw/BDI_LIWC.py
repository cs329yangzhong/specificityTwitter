from scipy.stats import pearsonr
from matplotlib import pyplot as plt
import matplotlib.mlab as mlab

if __name__ == '__main__':
    lines = []
    with open('users-bdi') as in_file:
        in_file.readline()
        for line in in_file:
            lines.append(line.strip().split())
    user_bdi = {}
    for line in lines:
        score = int(line[-1])
        '''
        if score <= 13:
            score = 1
        elif score <= 19:
            score = 2
        elif score <= 28:
            score = 3
        else:
            score = 4'''
        user_bdi[line[0]] = score
    # print(user_bdi)
    print(len(user_bdi))
    output = []

    bdi = []
    sp_score = []
    past = []
    present = []
    future = []
    age = []
    gender = []
    user = []

    with open('final_all') as in_file:
        in_file.readline()
        for ind, line in enumerate(in_file):
            l = line.strip().split('\t')
            if l[1] in user_bdi:
                if l[-9] == '' or l[-8] == '':
                    continue
                user.append(l[1])
                #print(ind)
                bdi.append(float(user_bdi[l[1]]))
                sp_score.append(float(l[4]))
                past.append(float(l[-3]))
                present.append(float(l[-2]))
                future.append(float(l[-1]))
                age.append(float(l[-8]))
                gender.append(float(l[-9]))
                output.append([float(user_bdi[l[1]]), float(l[4]), float(l[9])])

    print(len(set(user)))
    '''
    print(bdi)
    print(sp_score)
    print(len(bdi), len(sp_score), len(past))
    print(len(age))
    print(pearsonr(bdi, sp_score))'''
    with open('annotated_result_for_R all', 'w', encoding='utf-8') as out_file:
        for title in ['BDI', 'SPECIFICITY', 'PAST', 'PRESENT', 'FUTURE', 'AGE', 'GENDER']:
            out_file.write(title)
            out_file.write(',')
        out_file.write('\n')
        for i in range(len(past)):
            for cat in [bdi, sp_score, past, present, future, age, gender]:
                out_file.write(str(cat[i]))
                out_file.write(',')
            out_file.write('\n')



    '''560 560
(-0.07097197336600126, 0.09337307176151578)'''

    score_plot = []
    score_plot_co = []
    with open('training2_revise_score (2).csv', encoding='utf-8') as in_file:
        in_file.readline()
        for ind, line in enumerate(in_file):
            l = line.strip().split(',')
            score_plot.append(float(l[-1]))
    with open('LIWC2015 Results annotated', encoding='utf-8') as in_file:
        in_file.readline()
        for ind, line in enumerate(in_file):
            l = line.strip().split('\t')
            score_plot_co.append(float(l[4]))
    print([score_plot_co[i] - score_plot[i] for i in range(7267)])
    print(sum([score_plot_co[i] - score_plot[i] for i in range(7267)]))
    print(min(score_plot))
    print(len(score_plot))
    n, bins, patches = plt.hist(score_plot, 30, edgecolor='black', linewidth=0.5)
    plt.xlabel('score')
    plt.ylabel('count')
    plt.axis([0.9, 5.1, 0, 650])
    # plt.grid(True)

    plt.show()
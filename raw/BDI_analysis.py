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
    print(user_bdi)
    print(len(user_bdi))
    speci = {}

    with open('LIWC2015 Results 100') as in_file:
        in_file.readline()
        for line in in_file:
            l = line.strip().split('\t')
            if l[1] in user_bdi:
                if l[1] not in speci:
                    speci[l[1]] = [[float(l[4])], [float(l[11])]]
                else:
                    speci[l[1]][0].append(float(l[4]))
                    speci[l[1]][1].append(float(l[11]))

    bdi = []
    sp_score = []
    temp = []
    for key in speci.keys():
        sp_score.append(sum(speci[key][0]) / len(speci[key][0]))
        temp.append(sum(speci[key][1]) / len(speci[key][1]))
        bdi.append(user_bdi[key])

    print(speci)
    print(len(speci))

    print(bdi)
    print(sp_score)
    print(len(bdi), len(sp_score), len(temp))

    print(pearsonr(bdi, sp_score))
    with open('100_result_for_R', 'w', encoding='utf-8') as out_file:
        for title in ['BDI', 'SPECIFICITY', 'PAST']:
            out_file.write(title)
            out_file.write(',')
        out_file.write('\n')
        for i in range(len(temp)):
            for cat in [bdi, sp_score, temp]:
                out_file.write(str(cat[i]))
                out_file.write(',')
            out_file.write('\n')



    '''560 560
(-0.07097197336600126, 0.09337307176151578)'''
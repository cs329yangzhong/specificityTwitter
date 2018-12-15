users ={}
with open('final_all') as in_file:
    in_file.readline()
    for line in in_file:
        l = line.strip().split('\t')
        if l[1] in users:
            pass
        else:
            users[l[1]] = [l[-9], l[-8]]

print(users)

lines = []
with open('users-bdi') as in_file:
    in_file.readline()
    for line in in_file:
        lines.append(line.strip().split())
user_bdi = {}
user_score = {}
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

lines = []
with open('predicted_with_time') as in_file:
    titles = in_file.readline().strip().split('\t')
    titles.append('gender')
    titles.append('age')
    titles.append('bdi')
    for line in in_file:
        l = line.strip().split('\t')
        if l[0] in users:
            lines.append(l)
print(titles)
user_count = []
with open('bdi_age_gender', 'w', encoding='utf-8') as out_put:
    for title in titles:
        out_put.write(title)
        out_put.write('\t')
    out_put.write('\n')
    for line in lines:
        user_count.append(line[0])
        if users[line[0]][0] == '' or users[line[0]][1] == '':
            continue
        for item in line:
            out_put.write(item)
            out_put.write('\t')
        for item in users[line[0]]:
            out_put.write(item)
            out_put.write('\t')
        out_put.write(str(user_bdi[line[0]]))
        out_put.write('\n')

print(len(set(user_count)))
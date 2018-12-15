import re
import os
import random
import json

valid_token = re.compile('[\'\"_0-9a-zA-Z].+')
newline = re.compile('[\n\r]')
user = re.compile('@[a-zA-Z_0-9]+')
url = re.compile(r'(http(s)?://|www\.)[a-zA-Z_0-9/.=?]+')
RT = re.compile('\s?RT ')


# input_path
path = 'C:\\Users\\Yuan\\Desktop\\twitter-demographics\\twitter-demographics\\Dec-2017\\12-22-17\\output'


def sample(lines, quant=100, min_len=3):
    """
    randomly select tweet with given minimum length

    :param lines: string representation of input file
    :param quant: number of tweets from each user
    :param min_len: minimum unique tokens
    :return: None
    """

    random.shuffle(lines)
    count = 0
    output = []
    while len(output) < quant:
        if count == len(lines):
            break
        a_tweet = json.loads(lines[count])
        count += 1
        # print('pass')
        content = url.sub("<URL>", user.sub('<USER>', newline.sub(' ', a_tweet['text'])))
        if RT.search(content):
            continue
        tweet = a_tweet['id']
        time = a_tweet['created_at']
        token = set([item for item in content.split() if valid_token.match(item)])
        if not len(token) >= min_len:
            continue

        output.append((tweet, content, time))
        # print(output)
    if len(output) > 1:
        # print(output)
        return output
    else:
        return []


def parse(path, dic):
    """
    parse tweets from a given path
    this parser only works with DEC parts where each user has a unique file
    :param path: path where all input files are stored
    :return: None
    """
    quant = []
    failed = []
    with open('raw_output', 'w', encoding='utf-8') as out_file:
        out_file.write('tweet_id')
        out_file.write('\t')
        out_file.write('user_id')
        out_file.write('\t')
        out_file.write('text')
        out_file.write('\t')
        out_file.write('time')
        out_file.write('\n')
        dirs = os.listdir(path)
        print(dirs)

        user_count = 0
        for user_f in dirs:
            if user_f not in dic:
                continue
            # print(user_f)
            user_count += 1
            print(user_count)
            with open(path + '\\' + user_f, encoding='UTF-8') as in_file:
                count = 0
                lines = in_file.readlines()

                # minimum tweets = 4
                if len(lines) < 1:
                    continue

                tweets = sample(lines)
                if len(tweets) == 0:
                    continue
                quant.append(len(tweets))
                for item in tweets:
                    # print(item)

                    # print(user_count, end='   ')
                    # print(user_f, count, end='  ')
                    # print(item)
                    out_file.write(str(item[0]) + '\t')
                    out_file.write(str(user_f) + '\t')

                    out_file.write('\"' + item[1] + '\"\t')
                    out_file.write(str(item[2]) + '\n')
                    count += 1
                # if no enough qualified tweets
                '''
                except TypeError:
                    tweets = sample(lines)
                    print(user_f)
                    failed.append(user_f)
                    print('******************')
                    continue'''
    print(quant)
    print(sum(quant))
    print(len(quant))

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
    parse(path, user_bdi)


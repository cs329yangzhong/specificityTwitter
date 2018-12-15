import re
from nltk.tokenize import TweetTokenizer
html_and = re.compile(r'&amp;')
html_gt = re.compile(r'&gt;')
html_lt = re.compile(r'&lt;')
punctuation = re.compile(r'[?,.!()";\'\\]')

tok = TweetTokenizer()
with open('raw_out_text_only', encoding='utf-8') as in_file:
    with open('raw_out_text_html', 'w', encoding='utf-8') as out_file:
        out_file.write('Tweet')
        out_file.write('\n')
        for line in in_file:
            l = line.strip()
            l = html_and.sub('&', l)
            l = html_gt.sub('>', l)
            l = html_lt.sub('<', l)
            out_file.write(' '.join(tok.tokenize(l)))
            out_file.write('\n')

            print(punctuation.sub('', l))




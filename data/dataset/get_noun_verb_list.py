import spacy
import os, glob, json
from collections import Counter, OrderedDict
from pprint import pprint

# python -m spacy download en_core_web_md

nlp = spacy.load('en_core_web_md')
'''text = 'Yuh-jung Youn won the Oscar for best supporting actress for her performance in "Minari" on Sunday and made history by becoming the first Korean actor to win an Academy Award.'
doc = nlp(text)

# for noun_chunk in doc.noun_chunks:
#     print(noun_chunk.text)

str_format = "{:>10}"*8
print(str_format.format('Text', 'Lemma', 'POS', 'Tag', 'Dep', 'Shape', 'is alpha', 'is stop'))
print("=="*40)

for token in doc:
    print(str_format.format(token.text, token.lemma_, token.pos_, token.tag_,
                            token.dep_, token.shape_, str(token.is_alpha), str(token.is_stop)))
'''
# --------------------------------------------------------------------------------------------------

datasets = ['activitynet', 'charades', 'tacos']

nouns = {
    'activitynet': Counter(),
    'charades': Counter(),
    'tacos': Counter()
}

verbs = {
    'activitynet': Counter(),
    'charades': Counter(),
    'tacos': Counter()
}

def count(text):
    doc = nlp(text)

    for token in doc:
        pos = token.pos_
        lemma = token.lemma_

        if pos == 'NOUN':
            nouns[dataset][lemma] += 1
        elif pos == 'VERB':
            verbs[dataset][lemma] += 1

for dataset in datasets:
    filenames = list(glob.glob(dataset + ('/*.txt' if dataset == 'charades' else '/*.json')))

    for filename in filenames:
        print('filename:', filename)

        if dataset == 'activitynet' or dataset == 'tacos':
            with open(filename, encoding='utf8') as f:
                data = json.load(f)
                print('json len:', len(data))

            for vid, annotation in data.items():
                sentences = annotation['sentences']
                text = ' '.join(sentences)

                count(text)


        elif dataset == 'charades':
            with open(filename, encoding='utf8') as f:
                data = f.readlines()
                print('line len:', len(data))

            for line in data:
                text = line.split('##')[-1]
                count(text)


for k, v in nouns.items():
    nouns[k] = OrderedDict(v.most_common())
for k, v in verbs.items():
    verbs[k] = OrderedDict(v.most_common())

# pprint(nouns)
# pprint(verbs)

with open("nouns.json", "w") as json_file:
    json.dump(nouns, json_file)
with open("verbs.json", "w") as json_file:
    json.dump(verbs, json_file)

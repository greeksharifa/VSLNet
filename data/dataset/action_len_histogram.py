import json
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import glob
import re

"""
바꿀 부분:
DATASET # 1
filenames(경로) # 2
"""

datasets = ['activitynet', 'charades', 'tacos']

durations = {
    'activitynet': [],
    'charades': [],
    'tacos': []
}

for dataset in datasets:
    filenames = list(glob.glob(dataset + '/*.txt' if dataset == 'charades' else '/*.json'))

    for filename in filenames:

        def get_duration():

            if dataset == 'activitynet':
                with open(filename, encoding='utf8') as f:
                    data = json.load(f)

                for vid, annotation in data.items():
                    timestamps = annotation['timestamps']
                    for t in timestamps:
                        durations[dataset].append(float(t[1])-float(t[0]))
            elif dataset == 'charades':
                with open(filename, encoding='utf8') as f:
                    data = f.readlines()

                result = []
                for line in data:
                    if len(line) < 2:
                        continue
                    t = line.split('##')[0].split()[1:]
                    durations[dataset].append(float(t[1])-float(t[0]))
            elif dataset == 'tacos':
                pass

            return result


        durations[dataset].extend(get_duration())


    print('durations:', len(durations))
    avg_len = sum(durations) / len(durations)
    print('avg_len:', avg_len)

# colors = ["windows blue", "amber", "greyish", "faded green", "dusty purple"]
# sns.palplot(sns.xkcd_palette(colors))
# sns.set(rc={'figure.figsize':(15,10)})
# plt.xlim(0, 500)
# sns.histplot(data=durations, binwidth=5, kde=True)#, palette=['red', 'blue'])
sns.histplot(data=durations, binwidth=2, element='poly')#, palette=['red', 'blue'])

plt.title(DATASET + ' vid_ans_len(avg={:.1f}s)'.format(avg_len), fontsize=15)
plt.xlabel('len(sec)', fontsize=10)
plt.ylabel('count', fontsize=15)

fig = plt.gcf()
fig.savefig(DATASET + ' vid_ans_len.png', dpi=300, format='png', bbox_inches="tight", facecolor="white")
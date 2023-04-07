import json
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import os, glob
import re


# datasets = ['activitynet', 'charades', 'tacos']
datasets = ['charades']

durations = {
    # 'activitynet': [],
    'charades': [],
    # 'tacos': []
}



for dataset in datasets:
    filenames = list(glob.glob(dataset + ('/*.txt' if dataset == 'charades' else '/*.json')))

    vid_set = set()
    num_timestamps = 0

    max_vid = ''
    max_len = 0.0
    for filename in filenames:
        print('filename:', filename)

        if dataset == 'activitynet':
            with open(filename, encoding='utf8') as f:
                data = json.load(f)
                print('json len:', len(data))

            for vid, annotation in data.items():
                if 'train' in filename:
                    vid_set.add(vid)
                timestamps = annotation['timestamps']
                for t in timestamps:

                    if 'train' in filename:
                        num_timestamps += 1
                    durations[dataset].append(float(t[1])-float(t[0]))

                    l = float(t[1])-float(t[0])
                    if l > max_len:
                        max_len = l
                        max_vid = vid

        elif dataset == 'charades':
            with open(filename, encoding='utf8') as f:
                data = f.readlines()
                print('line len:', len(data))

            result = []
            for line in data:
                if len(line) < 2:
                    continue
                vid = line.split()[0]

                if 'train' in filename:
                    vid_set.add(vid)
                    num_timestamps += 1

                t = line.split('##')[0].split()[1:]

                l = float(t[1])-float(t[0])
                if l > max_len:
                    max_len = l
                    max_vid = vid

                durations[dataset].append(float(t[1])-float(t[0]))

        elif dataset == 'tacos':
            with open(filename, encoding='utf8') as f:
                data = json.load(f)
                print('json len:', len(data))

            for vid, annotation in data.items():
                if 'train' in filename:
                    vid_set.add(vid)

                timestamps = annotation['timestamps']
                fps = annotation['fps']
                for t in timestamps:

                    if 'train' in filename:
                        num_timestamps += 1

                    l = float(t[1]-t[0]) / fps
                    if l > max_len:
                        max_len = l
                        max_vid = vid

                    durations[dataset].append(float(t[1]-t[0]) / fps)


    print('number of video in trainset:', len(vid_set))
    print('number of timestamps in trainset:', num_timestamps)
    print('len of durations:', len(durations[dataset]))
    avg_len = sum(durations[dataset]) / len(durations[dataset])
    print('avg_len: {:.2f}'.format(avg_len))
    max_len = max(durations[dataset])
    print('max_len: {:.2f}'.format(max_len))
    print('max_vid:', max_vid)

# durations['charades'].extend(list(map(lambda x: x+0.1, range(0, 81))))

# colors = ["windows blue", "amber", "greyish", "faded green", "dusty purple"]
# sns.palplot(sns.xkcd_palette(colors))
# sns.set(rc={'figure.figsize':(15,10)})
LIMIT = 81
plt.xlim(0, LIMIT)
# sns.histplot(data=durations, binwidth=5, kde=True)#, palette=['red', 'blue'])
sns.histplot(data=durations, binwidth=1, element='poly')#, palette=['red', 'blue'])

plt.title('action_len: lim_{}'.format(LIMIT), fontsize=15)
plt.xlabel('len(sec)', fontsize=10)
plt.ylabel('count', fontsize=15)
# plt.yscale('log')
plt.yscale('log')

fig = plt.gcf()
fig.savefig('action_len-lim_{}_log.png'.format(LIMIT), dpi=300, format='png', bbox_inches="tight", facecolor="white")
plt.show()
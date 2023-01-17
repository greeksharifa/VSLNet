import json
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import os, glob
import re

ONLY_AUG = False
AUG = False
LIMIT = 250


datasets = ['activitynet', 'charades', 'tacos']

durations = {
    'activitynet': [],
    'charades': [],
    'tacos': []
}


for dataset in datasets:
    filenames = list(glob.glob(dataset + '/*.json'))

    vid_set = set()
    num_timestamps = 0

    max_vid = ''
    max_len = 0.0
    for filename in filenames:
        print('filename:', filename)
        if ONLY_AUG and 'aug' not in filename:
            print('not aug file passed')
            continue
        if not ONLY_AUG and not AUG and 'aug' in filename:
            print('aug file passed')
            continue

        if dataset == 'activitynet' or dataset == 'charades':
            with open(filename, encoding='utf8') as f:
                data = json.load(f)
                print('json len:', len(data))

            for vid, annotation in data.items():
                if 'train' in filename:
                    vid_set.add(vid)

                duration = annotation['duration']
                durations[dataset].append(duration)

                if 'train' in filename:
                    num_timestamps += 1
                l = duration

                if l > max_len:
                    max_len = l
                    max_vid = vid

        elif dataset == 'tacos':
            with open(filename, encoding='utf8') as f:
                data = json.load(f)
                print('json len:', len(data))

            for vid, annotation in data.items():
                if 'train' in filename:
                    vid_set.add(vid)

                num_frames = annotation['num_frames']
                fps = annotation['fps']
                l = num_frames / fps
                durations[dataset].append(l)

                if 'train' in filename:
                    num_timestamps += 1

                if l > max_len:
                    max_len = l
                    max_vid = vid



    print('\nnumber of video in trainset:', len(vid_set))
    print('number of timestamps in trainset:', num_timestamps)
    print('len of durations:', len(durations[dataset]))
    avg_len = sum(durations[dataset]) / len(durations[dataset])
    print('avg_len: {:.2f}'.format(avg_len))
    max_len = max(durations[dataset])
    print('max_len: {:.2f}'.format(max_len))
    print('max_vid:', max_vid, '\n\n')

# colors = ["windows blue", "amber", "greyish", "faded green", "dusty purple"]
# sns.palplot(sns.xkcd_palette(colors))
# sns.set(rc={'figure.figsize':(15,10)})
plt.xlim(0, LIMIT)
# sns.histplot(data=durations, binwidth=5, kde=True)#, palette=['red', 'blue'])
sns.histplot(data=durations, binwidth=2, element='poly')#, palette=['red', 'blue'])

title = 'vid_len'
if ONLY_AUG:
    title += '-only_aug'
elif AUG:
    title += '-contain_aug'
title += '-lim_{}'.format(LIMIT)

plt.title(title, fontsize=15)
plt.xlabel('len(sec)', fontsize=10)
plt.ylabel('count', fontsize=15)

fig = plt.gcf()
fig.savefig(title + '.png', dpi=300, format='png', bbox_inches="tight", facecolor="white")
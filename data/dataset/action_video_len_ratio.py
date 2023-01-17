import json
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import os, glob
import re


ONLY_AUG = False
AUG = False


datasets = ['activitynet', 'charades', 'tacos']

durations = {
    'activitynet': {'S': [], 'E': []},
    'charades': {'S': [], 'E': []},
    'tacos': {'S': [], 'E': []},
}


with open('charades/charades.json', encoding='utf8') as f:
    charades_duration = json.load(f)



for dataset in datasets:
    filenames = list(glob.glob(dataset + ('/*.txt' if dataset == 'charades' else '/*.json')))

    for filename in filenames:
        print('filename:', filename)
        if ONLY_AUG and 'aug' not in filename:
            print('not aug file passed')
            continue
        if not ONLY_AUG and not AUG and 'aug' in filename:
            print('aug file passed')
            continue
        # if 'train' in filename:
        #     continue

        if dataset == 'activitynet':
            with open(filename, encoding='utf8') as f:
                data = json.load(f)
                print('json len:', len(data))

            for vid, annotation in data.items():
                timestamps = annotation['timestamps']
                duration = float(annotation['duration'])

                for t in timestamps:
                    S = t[0] / duration
                    E = t[1] / duration
                    durations[dataset]['S'].append(S)
                    durations[dataset]['E'].append(E)

                    if S >= E:
                        print(vid, S, E)
                    if E >1.01:
                        print(vid, S, E)

        elif dataset == 'charades':
            with open(filename, encoding='utf8') as f:
                data = f.readlines()
                print('line len:', len(data))

            result = []
            for line in data:
                if len(line) < 2:
                    continue

                t = line.split('##')[0].split()[1:]
                vid = line.split()[0]
                duration = float(charades_duration[vid]['duration'])
                S = float(t[0]) / duration
                E = float(t[1]) / duration
                durations[dataset]['S'].append(S)
                durations[dataset]['E'].append(E)
                if S >= E:
                    print(vid, S, E)
                if E >1.01:
                    print(vid, S, E)

        elif dataset == 'tacos':
            with open(filename, encoding='utf8') as f:
                data = json.load(f)
                print('json len:', len(data))

            for vid, annotation in data.items():
                timestamps = annotation['timestamps']
                num_frames = float(annotation['num_frames'])
                for t in timestamps:
                    S = t[0] / num_frames
                    E = t[1] / num_frames
                    durations[dataset]['S'].append(S)
                    durations[dataset]['E'].append(E)
                    if S >= E:
                        print(vid, S, E)
                    if E >1.01:
                        print(vid, S, E)


    print('len of durations:', len(durations[dataset]))

    # colors = ["windows blue", "amber", "greyish", "faded green", "dusty purple"]
    # sns.palplot(sns.xkcd_palette(colors))
    # sns.set(rc={'figure.figsize':(15,10)})
    plt.xlim(0, 1)

    sns.scatterplot(x='S', y='E', data=durations[dataset], s=1)

    title = 'act_vid_len_ratio'
    if ONLY_AUG:
        title += '-only_aug'
    elif AUG:
        title += '-contain_aug'
    title += '-{}'.format(dataset)

    plt.title(title, fontsize=15)
    plt.xlabel('S', fontsize=15)
    plt.ylabel('E', fontsize=15)

    fig = plt.gcf()
    fig.savefig(title + '.png', dpi=300, format='png',
                bbox_inches="tight", facecolor="white")
    plt.show()
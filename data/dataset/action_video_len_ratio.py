import json
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import os, glob
import re
import argparse

from utils import *


args = get_args()
    
# datasets = ['activitynet', 'charades', 'tacos']
datasets = ['charades']

durations = {
    # 'activitynet': {'S': [], 'E': []},
    'charades': {'S': [], 'E': []},
    # 'tacos': {'S': [], 'E': []},
}


# with open('charades/charades_aug.json', encoding='utf8') as f:
with open('charades/charades.json', encoding='utf8') as f:
    charades_duration = json.load(f)


for dataset in datasets:
    filenames = list(glob.glob(dataset + ('/*.txt' if dataset == 'charades' else '/*.json')))

    for filename in filenames:
        if not check_filename(args, filename):
            continue

        if dataset == 'activitynet':
            with open(filename, encoding='utf8') as f:
                data = json.load(f)
                print('json len:', len(data))

            for vid, annotation in data.items():
                if args.ONLY_AUG and 'aug' not in vid:
                    continue
                    
                timestamps = annotation['timestamps']
                duration = float(annotation['duration'])

                for t in timestamps:
                    S = t[0] / duration
                    E = t[1] / duration
                    durations[dataset]['S'].append(S)
                    durations[dataset]['E'].append(E)
                    checkSE(vid, S, E)

        elif dataset == 'charades':
            with open(filename, encoding='utf8') as f:
                data = f.readlines()
                print('line len:', len(data))

            for line in data:
                if len(line) < 2:
                    continue

                t = line.split('##')[0].split()[1:]
                vid = line.split()[0]
                if args.ONLY_AUG and 'aug' not in vid:
                    continue
                duration = float(charades_duration[vid]['duration'])
                # if duration > 10:
                if duration <= 10 or duration >= 30:
                # if duration < 30:
                    continue
                S = float(t[0]) / duration
                E = float(t[1]) / duration
                durations[dataset]['S'].append(S)
                durations[dataset]['E'].append(E)
                checkSE(vid, S, E)
                print('{} : {:5.3f}~{:5.3f} / {:5.3f}'.format(vid, duration, S*duration, E*duration))

        elif dataset == 'tacos':
            with open(filename, encoding='utf8') as f:
                data = json.load(f)
                print('json len:', len(data))

            for vid, annotation in data.items():
                if args.ONLY_AUG and 'aug' not in vid:
                    continue
                timestamps = annotation['timestamps']
                num_frames = float(annotation['num_frames'])
                fps = annotation['fps']
                for t in timestamps:
                    S = t[0] / num_frames
                    E = t[1] / num_frames
                    if 'aug' in vid:
                        S *= fps
                        E *= fps
                    # print(num_frames, t[0], S, t[1], E)
                    durations[dataset]['S'].append(S)
                    durations[dataset]['E'].append(E)
                    checkSE(vid, S, E)


    print('len of durations:', len(durations[dataset]['S']))

    # colors = ["windows blue", "amber", "greyish", "faded green", "dusty purple"]
    # sns.palplot(sns.xkcd_palette(colors))
    # sns.set(rc={'figure.figsize':(15,10)})
    plt.xlim(0, 1)

    sns.scatterplot(x='S', y='E', data=durations[dataset], s=1)

    title = get_title(args, dataset, 'act_vid_len_ratio_10_to_30_secs')

    plt.title(title, fontsize=15)
    plt.xlabel('S', fontsize=15)
    plt.ylabel('E', fontsize=15)
    plt.xlim(-0.1, 1.1)

    fig = plt.gcf()
    save_filename = 'png_ratio/' + title + '.png'
    print('save_filename:', save_filename)
    fig.savefig(save_filename, dpi=300, format='png',
                bbox_inches="tight", facecolor="white")
    plt.show()
    

    print('\n' + '-' * 80 + '\n')
import json
from collections import Counter

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



action_number = {}

for dataset in datasets:
    filenames = list(glob.glob(dataset + ('/*.txt' if dataset == 'charades' else '/*.json')))

    for filename in filenames:
        if not check_filename(args, filename):
            continue

        with open(filename, encoding='utf8') as f:
            data = f.readlines()
            print('line len:', len(data))

        for line in data:
            if len(line) < 2:
                continue

            t = line.split('##')[0].split()[1:]
            s, e = t[0], t[1]
            
            vid = line.split()[0]
            if args.ONLY_AUG and 'aug' not in vid:
                continue
            
            if vid not in action_number:
                action_number[vid] = set()
            action_number[vid].add((s,e))

    print('len(action_number):', len(action_number))
    
    
    counter = Counter()
    
    for key, value in action_number.items():
        counter[len(value)] += 1
    
    print(counter)
    print(counter.keys())
    print(counter.values())
    
    
    sns.barplot(x=list(counter.keys()), y=list(counter.values()))

    title = get_title(args, dataset, 'unique_action_number_in_video')

    plt.title(title, fontsize=15)
    plt.xlabel('action_number', fontsize=15)
    plt.ylabel('count', fontsize=15)

    fig = plt.gcf()
    save_filename = title + '.png'
    print('save_filename:', save_filename)
    fig.savefig(save_filename, dpi=300, format='png',
                bbox_inches="tight", facecolor="white")
    plt.show()
    

    print('\n' + '-' * 80 + '\n')
import os, glob, json


video_dir = '/data/video_datasets/activitynet/'
dataset_dir = '../data/dataset/activitynet/'


with open(os.path.join(dataset_dir, "train.json"), mode="r", encoding="utf-8") as f:
    train_ids = list(json.load(f).keys())
    train_ids = [vid[2:] if len(vid) == 13 else vid for vid in train_ids]

with open(os.path.join(dataset_dir, "val_1.json"), mode="r", encoding="utf-8") as f:
    val_ids = list(json.load(f).keys())
    val_ids = [vid[2:] if len(vid) == 13 else vid for vid in val_ids]

with open(os.path.join(dataset_dir, "val_2.json"), mode="r", encoding="utf-8") as f:
    test_ids = list(json.load(f).keys())
    test_ids = [vid[2:] if len(vid) == 13 else vid for vid in test_ids]

all_video_ids = list(set(train_ids + val_ids + test_ids))
print("train_video_ids", len(train_ids))
print("val_1_video_ids", len(val_ids))
print("val_2_video_ids", len(test_ids))
print("all_video_ids", len(all_video_ids))

print(train_ids[0])

video_ids = []

for i, path in enumerate(glob.glob(video_dir + '*')):
    video_ids.append(path.split('/')[-1][2:-4])

# print(video_ids[:5])

train_ids = set(train_ids)
val_ids = set(val_ids)
test_ids = set(test_ids)
video_ids = set(video_ids)

result = {
    'train': {
        'exists' : list(train_ids.intersection(video_ids)),
        'missing': list(train_ids.difference(video_ids))
    },
    'val': {
        'exists' : list(val_ids.intersection(video_ids)),
        'missing': list(val_ids.difference(video_ids))
    },
    'test': {
        'exists' : list(test_ids.intersection(video_ids)),
        'missing': list(test_ids.difference(video_ids))
    },
}

for s in ['train', 'val', 'test']:
    print('{}\t: exists={}\t, missing={}'.format(s, len(result[s]['exists']), len(result[s]['missing'])))


w_name = dataset_dir + 'downloaded_vids.json'
print('downloaded vid lists are stored in ', w_name)

with open(w_name, 'w', encoding='utf8') as f:
    json.dump(result, f)
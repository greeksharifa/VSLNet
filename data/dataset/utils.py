

def get_title(args, dataset):
    title = 'act_vid_len_ratio'
    if args.ONLY_AUG:
        title += '-only_aug'
    elif args.ONLY_AUG_FILE:
        title += '-only_aug_file'
    elif args.ONLY_TRAIN:
        title += '-only_train'
    elif args.AUG:
        title += '-contain_aug'
    title += '-{}'.format(dataset)


def checkSE(vid, S, E):
    if S >= E:
        print(vid, S, E)
    # if E >1.01:
    #     print(vid, S, E)
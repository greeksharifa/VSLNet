import argparse

def get_args():
    
    parser = argparse.ArgumentParser(description='act_vid_len_ratio')
    
    parser.add_argument('--ONLY_AUG', action='store_true')
    parser.add_argument('--ONLY_TRAIN', action='store_true')
    parser.add_argument('--TRAIN_AUG', action='store_true')
    parser.add_argument('--AUG', action='store_true')
    
    args = parser.parse_args()
    
    return args


def check_filename(args, filename):
    if (args.ONLY_AUG or args.TRAIN_AUG) and 'aug' not in filename:
        # print('not aug file passed')
        return False
    if 'aug' in filename and (not args.ONLY_AUG and not args.TRAIN_AUG and not args.AUG):
        # print('aug file passed')
        return False
    if args.ONLY_TRAIN and ('train' not in filename or 'aug' in filename):
        return False

    print('filename:', filename)
    return True


def get_title(args, dataset, basename):
    title = basename
    if args.ONLY_AUG:
        title += '-only_aug'
    elif args.TRAIN_AUG:
        title += '-train_aug'
    elif args.ONLY_TRAIN:
        title += '-only_train'
    elif args.AUG:
        title += '-contain_aug'
    title += '-{}'.format(dataset)

    return title


def checkSE(vid, S, E):
    if S >= E:
        print(vid, S, E)
    # if E >1.01:
    #     print(vid, S, E)
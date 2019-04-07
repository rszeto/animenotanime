import argparse
import os
import random
import shutil


def main(val_percentage, seed):
    random.seed(seed)

    create_train_val_split('not_anime', '0', val_percentage)
    create_train_val_split('anime', '1', val_percentage)


def create_train_val_split(human_label, numeric_label, val_percentage):
    dir = os.path.join('data', 'images', human_label)
    full_dir = os.path.abspath(dir)
    image_file_names = os.listdir(full_dir)
    random.shuffle(image_file_names)
    train_dir = os.path.join('data', 'train', numeric_label)
    val_dir = os.path.join('data', 'val', numeric_label)
    if os.path.isdir(train_dir):
        shutil.rmtree(train_dir)
    os.makedirs(train_dir)
    if os.path.isdir(val_dir):
        shutil.rmtree(val_dir)
    os.makedirs(val_dir)
    for i, file_name in enumerate(image_file_names):
        if i < int(val_percentage * len(image_file_names)):
            os.symlink(os.path.join(full_dir, file_name), os.path.join(val_dir, file_name))
        else:
            os.symlink(os.path.join(full_dir, file_name), os.path.join(train_dir, file_name))


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--val_percentage', type=float, default=0.1,
                        help='Percentage of images from each class that should be in the validation set')
    parser.add_argument('--seed', type=int, default=123, help='RNG seed used to create the split')
    args = parser.parse_args()

    main(**vars(args))
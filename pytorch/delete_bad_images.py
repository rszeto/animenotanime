import argparse
import os

from PIL import Image

def main(images_root):
    delete_count = 0
    image_file_names = os.listdir(images_root)
    for i, image_file_name in enumerate(image_file_names):
        image_file_path = os.path.join(images_root, image_file_name)
        if i % 100 == 0:
            print('Processing {} (file {}/{})'.format(image_file_path, i+1, len(image_file_names)))
        try:
            image = Image.open(image_file_path)
            image_rgb = image.convert('RGB')
        except OSError:
            print('Deleting {}'.format(image_file_path))
            os.remove(image_file_path)
            delete_count += 1
    print('Removed {} images'.format(delete_count))


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('images_root', type=str)
    args = parser.parse_args()

    main(**vars(args))
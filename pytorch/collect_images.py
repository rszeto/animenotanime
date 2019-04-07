import argparse
import os
import sys
from urllib.request import urlretrieve

import requests
from imgurpython import ImgurClient


ALLOWED_EXTS = ['.png', '.jpg', '.jpeg']


def download_not_anime_images(client_id, client_secret, num_pages, subreddits):

    client = ImgurClient(client_id, client_secret)
    not_anime_dir = os.path.join('data', 'images', 'not_anime')
    if not os.path.isdir(not_anime_dir):
        os.makedirs(not_anime_dir)

    numItems = 0
    for subreddit in subreddits:
        cycleFound = False
        for page in range(num_pages):
            items = client.subreddit_gallery(subreddit, window='all', page=page)
            for item in items:
                _, ext = os.path.splitext(item.link)
                if ext in ALLOWED_EXTS:
                    url = item.link
                    basename = os.path.basename(url)
                    dest = os.path.join(not_anime_dir, basename)
                    if not os.path.exists(dest):
                        print('Downloading %s' % url)
                        try:
                            urlretrieve(url, dest)
                            numItems += 1
                        except:
                            print("Unexpected error:", sys.exec_info()[0])
                            continue
                    else:
                        print('File %s exists, Imgur API is likely cycling images. Stopping' % basename)
                        cycleFound = True
                        break
            if cycleFound:
                break

    print('Downloaded %d images over %d gallery pages x %d galleries' % (numItems, num_pages, len(subreddits)))


def download_anime_images(num_pages):

    anime_dir = os.path.join('data', 'images', 'anime')
    if not os.path.exists(anime_dir):
        os.mkdir(anime_dir)

    numItems = 0
    for page in range(num_pages):
        url = 'http://konachan.net/post.json?limit=100&page=%d' % page
        response = requests.get(url)
        data = response.json()

        # Iterate through all returned posts
        for imageData in data:
            # Extract image url from the data
            imageUrl = imageData['file_url']
            # Make sure image is supported before downloading
            _, ext = os.path.splitext(imageUrl)
            # Make sure it is SFW
            sfw = (imageData['rating'] == 's')
            if ext in ALLOWED_EXTS and sfw:
                # Prepare for local download
                dest = os.path.join(anime_dir, '%06d%s' % (numItems, ext))
                print('Downloading %s' % imageUrl)
                try:
                    urlretrieve(imageUrl, dest)
                    numItems += 1
                except Exception as e:
                    print('Error downloading %s: %s' % (imageUrl, str(e)))
                    continue
    print('Saved %d images' % numItems)


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    subparsers = parser.add_subparsers(dest='cmd')

    parser_not_anime = subparsers.add_parser('notanime')
    parser_not_anime.add_argument('client_id', type=str)
    parser_not_anime.add_argument('client_secret', type=str)
    parser_not_anime.add_argument('--num_pages', type=int, default=1)
    parser_not_anime.add_argument('--subreddits', type=str, nargs='+', default=[
        'art', 'comics', 'comicbooks', 'mapporn', 'marvel', 'dccomics'
    ])

    parser_anime = subparsers.add_parser('anime')
    parser_anime = parser_anime.add_argument('--num_pages', type=int, default=1)

    args = parser.parse_args()

    if args.cmd == 'notanime':
        download_not_anime_images(args.client_id, args.client_secret, args.num_pages, args.subreddits)
    else:
        download_anime_images(args.num_pages)
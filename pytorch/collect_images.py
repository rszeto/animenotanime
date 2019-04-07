import argparse
import os
import sys
from urllib.request import urlretrieve

import requests
from imgurpython import ImgurClient


ALLOWED_EXTS = ['.png', '.jpg', '.jpeg']


def download_list(url_dest_pairs):
    num_downloads = 0
    for url, dest in url_dest_pairs:
        print('Downloading %s to %s' % (url, dest))
        try:
            urlretrieve(url, dest)
        except:
            print("Unexpected error:", sys.exec_info()[0])
            continue
        num_downloads += 1
    return num_downloads


def download_not_anime_images(client_id, client_secret, num_pages, subreddits):

    client = ImgurClient(client_id, client_secret)
    not_anime_dir = os.path.join('data', 'images', 'not_anime')
    if not os.path.isdir(not_anime_dir):
        os.makedirs(not_anime_dir)

    urls = []
    for subreddit in subreddits:
        for page in range(num_pages):
            items = client.subreddit_gallery(subreddit, window='all', page=page)
            urls += [item.link for item in items]

    # Create a set of urls, which filters out duplicates
    urls = set(urls)
    # Only keep valid image URLs, i.e. ones that end with an allowed extension
    urls = filter(lambda url: os.path.splitext(url)[1] in ALLOWED_EXTS, urls)
    # Construct url-destination pairs
    url_dest_pairs = [(url, (os.path.join(not_anime_dir, os.path.basename(url)))) for url in urls]

    # Download the images
    num_downloads = download_list(url_dest_pairs)
    print('Downloaded %d images over %d gallery pages x %d galleries' % (num_downloads, num_pages, len(subreddits)))


def download_anime_images(num_pages):

    anime_dir = os.path.join('data', 'images', 'anime')
    if not os.path.exists(anime_dir):
        os.mkdir(anime_dir)

    url_dest_pairs = []
    for page in range(num_pages):
        url = 'http://konachan.net/post.json?limit=100&page=%d' % page
        response = requests.get(url)
        data = response.json()

        # Iterate through all returned posts
        for imageData in data:
            url = imageData['file_url']  # Image URL
            _, ext = os.path.splitext(url)  # File extension
            id = imageData['id']  # Post ID
            sfw = (imageData['rating'] == 's')  # Safe for work flag
            if ext in ALLOWED_EXTS and sfw:
                dest = os.path.join(anime_dir, '%08d%s' % (id, ext))
                url_dest_pairs.append((url, dest))

    num_downloads = download_list(url_dest_pairs)
    print('Downloaded %d images over %d pages' % (num_downloads, num_pages))


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
import argparse
import os
import sys
from queue import Queue
from threading import Lock, Thread
from urllib.request import urlretrieve

import requests
from imgurpython import ImgurClient


ALLOWED_EXTS = ['.png', '.jpg', '.jpeg']


class StopWorkToken:
    pass


def download_url(url, dest):
    if os.path.isfile(dest):
        print('Destination %s exists, skipping' % dest)
        return 0
    else:
        print('Downloading %s to %s' % (url, dest))
        try:
            urlretrieve(url, dest)
        except Exception as e:
            print(e)
            return 0
        return 1


def download_list(url_dest_pairs, num_workers):
    q = Queue()
    num_downloads_counter = [0]
    num_downloads_lock = Lock()

    def download_list_worker():
        while True:
            # Get item (either (url, dest) or StopWorkToken)
            item = q.get()
            # Kill thread if StopWorkToken is received
            if isinstance(item, StopWorkToken):
                break
            # Try to download from the URL
            num_downloads = download_url(*item)
            # Decrement task count
            q.task_done()
            # Update download counter
            with num_downloads_lock:
                num_downloads_counter[0] += num_downloads

    # Create threads
    threads = []
    for _ in range(num_workers):
        t = Thread(target=download_list_worker)
        t.start()
        threads.append(t)

    # Put jobs into queue
    for pair in url_dest_pairs:
        q.put(pair)

    # Wait for tasks to finish
    q.join()

    # Put in a StopWorkToken for each worker
    for _ in range(num_workers):
        q.put(StopWorkToken())
    # Wait for all workers to terminate (i.e. each one receives a StopWorkToken)
    for t in threads:
        t.join()

    return num_downloads_counter[0]


def download_not_anime_images(client_id, client_secret, num_pages, subreddits, num_workers):

    client = ImgurClient(client_id, client_secret)
    not_anime_dir = os.path.join('data', 'images', 'not_anime')
    if not os.path.isdir(not_anime_dir):
        os.makedirs(not_anime_dir)

    urls = set()  # unique urls across all subreddits
    for subreddit in subreddits:
        subreddit_urls = set()  # unique urls for this subreddit
        for page in range(num_pages):
            items = client.subreddit_gallery(subreddit, window='all', page=page)
            if len(items) == 0:
                # No more urls for this subreddit
                break
            new_subreddit_urls = set([item.link for item in items])
            if len(new_subreddit_urls.difference(subreddit_urls)) == 0:
                # All urls are duplicates
                break
            subreddit_urls = subreddit_urls.union(new_subreddit_urls)
        urls = urls.union(subreddit_urls)

    # Only keep valid image URLs, i.e. ones that end with an allowed extension
    urls = filter(lambda url: os.path.splitext(url)[1] in ALLOWED_EXTS, urls)
    # Construct url-destination pairs
    url_dest_pairs = [(url, (os.path.join(not_anime_dir, os.path.basename(url)))) for url in urls]

    # Download the images
    num_downloads = download_list(url_dest_pairs, num_workers)
    print('Downloaded %d images over %d gallery pages x %d galleries' % (num_downloads, num_pages, len(subreddits)))


def download_anime_images(num_pages, num_workers):

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

    num_downloads = download_list(url_dest_pairs, num_workers)
    print('Downloaded %d images over %d pages' % (num_downloads, num_pages))


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    subparsers = parser.add_subparsers(dest='cmd')

    parser_not_anime = subparsers.add_parser('notanime')
    parser_not_anime.add_argument('client_id', type=str)
    parser_not_anime.add_argument('client_secret', type=str)
    parser_not_anime.add_argument('--num_pages', type=int, default=1)
    parser_not_anime.add_argument('--subreddits', type=str, nargs='+', default=[
        'abandonedporn', 'aww', 'cozyplaces', 'earthporn', 'eyebleach', 'happy', 'itookapicture', 'oldschoolcool',
        'pic', 'pics'
    ])
    parser_not_anime.add_argument('--num_workers', type=int, default=4, help='Number of download threads/workers')

    parser_anime = subparsers.add_parser('anime')
    parser_anime.add_argument('--num_pages', type=int, default=1)
    parser_anime.add_argument('--num_workers', type=int, default=4, help='Number of download threads/workers')

    args = parser.parse_args()

    if args.cmd == 'notanime':
        download_not_anime_images(args.client_id, args.client_secret, args.num_pages, args.subreddits, args.num_workers)
    else:
        download_anime_images(args.num_pages, args.num_workers)
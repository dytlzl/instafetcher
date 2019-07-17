import requests
import re
import json
import os
from datetime import datetime


class Post:
    URL = 'https://www.instagram.com/p/%s/'

    def __init__(self, shortcode, mode='di', sub_directory=None):
        self.headers = {
            "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_3) "
                          "AppleWebKit/537.36 (KHTML, like Gecko) "
                          "Chrome/73.0.3683.75 "
                          "Safari/537.36"
        }
        self.timestamp = None
        self.url = self.URL % shortcode
        self.json_key = ['PostPage', 'shortcode_media']
        self.mode = mode
        if sub_directory is None:
            sub_directory = 'posts/' + shortcode
        self.download_directory = './instagram_download/' + sub_directory

    def fetch(self):
        res = requests.get(self.url, headers=self.headers)
        html = res.text
        match = re.search(
            r'<script type="text/javascript">window\._sharedData = (.*?);</script>', html)
        if not match:
            print('Could not find "sharedData".')
            return
        json_text = match.groups()[0]
        dic = json.loads(json_text)
        dic_main = dic['entry_data'][self.json_key[0]
                                     ][0]['graphql'][self.json_key[1]]
        self.timestamp = dic_main['taken_at_timestamp']
        if 'i' in self.mode:
            list_to_print = []
            list_to_print.append(self.url)
            list_to_print += [dic_main[i] for i in (
                '__typename',
                'display_url')]
            list_to_print.append(str(datetime.fromtimestamp(self.timestamp)))
            print('\n'.join(list_to_print))
        if 'd' in self.mode:
            os.makedirs(self.download_directory, exist_ok=True)
            self.parse_media(dic_main)
        if 'i' in self.mode:
            print('\n')

    def parse_media(self, dic):
        typename = dic['__typename']
        if typename == 'GraphImage':
            self.download_media(dic['display_url'])
        elif typename == 'GraphVideo':
            self.download_media(dic['display_url'])
            self.download_media(dic['video_url'])
        elif typename == 'GraphSidecar':
            for i in dic['edge_sidecar_to_children']['edges']:
                self.parse_media(i['node'])

    def download_media(self, url):
        basename = url.split('/')[-1].split('?')[0]
        filepath = self.download_directory
        if filepath[-1] != '/':
            filepath += '/'
        filepath += basename
        if os.path.exists(filepath):
            print('\r"%s" taken at %s Already Exists.' %
                  (basename, datetime.fromtimestamp(self.timestamp)), end='')
        else:
            print('\rDownload "%s" taken at %s ...' %
                  (basename, datetime.fromtimestamp(self.timestamp)), end='')
            res = requests.get(url, timeout=10)
            with open(filepath, mode='wb') as f:
                f.write(res.content)
            os.utime(filepath, (self.timestamp, self.timestamp))

    def create_dir(self):
        if not os.path.exists(self.download_directory):
            os.mkdir(self.download_directory)

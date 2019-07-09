import requests
import re
import json
import os


class Post:
    URL = 'https://www.instagram.com/p/%s/'

    def __init__(self, shortcode, sub_directory = ''):
        self.headers = {
            "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_3) "
                          "AppleWebKit/537.36 (KHTML, like Gecko) "
                          "Chrome/73.0.3683.75 "
                          "Safari/537.36"
        }
        self.timestamp = None
        self.url = self.URL % shortcode
        self.json_key = ['PostPage', 'shortcode_media']
        self.download_directory = './instagram_download/'
        self.create_dir()
        self.download_directory += sub_directory + '/'
        self.create_dir()

    def fetch(self):
        res = requests.get(self.url, headers=self.headers)
        html = res.text
        match = re.search(r'<script type="text/javascript">window._sharedData = (.*?);</script>', html)
        if not match:
            return None
        json_text = match.groups()[0]
        dic = json.loads(json_text)
        dic_main = dic['entry_data'][self.json_key[0]][0]['graphql'][self.json_key[1]]
        self.timestamp = dic_main['taken_at_timestamp']
        self.parse_media(dic_main)

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
        filepath = self.download_directory + url.split('/')[-1].split('?')[0]
        if os.path.exists(filepath):
            print('\r"%s" Already Exists.' % (filepath), end='')
        else:
            print('\rDownload "%s" to "%s" ...' % (url, filepath), end='')
            res = requests.get(url, timeout=10)
            with open(filepath, mode='wb') as f:
                f.write(res.content)
            os.utime(filepath, (self.timestamp, self.timestamp))

    def create_dir(self):
        if not os.path.exists(self.download_directory):
            os.mkdir(self.download_directory)

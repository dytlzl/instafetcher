import requests
import re
import json
import os


class Post:
    URL = 'https://www.instagram.com/p/%s/'

    def __init__(self, shortcode, mode, sub_directory):
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
        self.sub_directory = sub_directory

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
        if 'd' in self.mode:
            self.download_directory = './instagram_download/'
            self.create_dir()
            if self.sub_directory is None:
                self.sub_directory = 'inbox'
            self.download_directory += self.sub_directory + '/'
            self.create_dir()
            self.parse_media(dic_main)
        if 'i' in self.mode:
            info_list = [dic_main[i] for i in [
                '__typename',
                'shortcode',
                'display_url', 
                'taken_at_timestamp']]
            print(info_list)

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
        filepath = self.download_directory + basename
        if os.path.exists(filepath):
            print('\r"%s" Already Exists.' % (basename), end='')
        else:
            print('\rDownload to "%s" ...' % (basename), end='')
            res = requests.get(url, timeout=10)
            with open(filepath, mode='wb') as f:
                f.write(res.content)
            os.utime(filepath, (self.timestamp, self.timestamp))

    def create_dir(self):
        if not os.path.exists(self.download_directory):
            os.mkdir(self.download_directory)

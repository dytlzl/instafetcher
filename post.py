import requests
import re
import json


class Post:
    URL = 'https://www.instagram.com/p/%s/'

    def __init__(self, shortcode):
        super().__init__()
        self.headers = {
            "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_3) "
                          "AppleWebKit/537.36 (KHTML, like Gecko) "
                          "Chrome/73.0.3683.75 "
                          "Safari/537.36"
        }
        self.timestamp = None
        self.url = self.URL % shortcode
        self.json_key = ['PostPage', 'shortcode_media']

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
            print(dic['display_url'])
        elif typename == 'GraphVideo':
            print(dic['video_url'])
        elif typename == 'GraphSidecar':
            for i in dic['edge_sidecar_to_children']['edges']:
                self.parse_media(i['node'])

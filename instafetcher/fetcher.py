import requests
import re
import json
import time
from .post import Post


class Fetcher:
    URL = 'https://www.instagram.com/explore/tags/%s/'

    def __init__(self, mode, time_interval):
        self.headers = {
            "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_3) "
                          "AppleWebKit/537.36 (KHTML, like Gecko) "
                          "Chrome/73.0.3683.75 "
                          "Safari/537.36"
        }
        self.params = None
        self.first = 12
        self.after = None
        self.json_key = []
        self.user_id = None
        self.url = None
        self.sub_directory = None
        self.mode = mode
        self.time_interval = time_interval

    def fetch_html(self):
        res = requests.get(self.url, headers=self.headers)
        html = res.text
        match = re.search(r'<script type="text/javascript">window._sharedData = (.*?);</script>', html)
        if not match:
            print('Could not find "sharedData".')
            return
        json_text = match.groups()[0]
        dic = json.loads(json_text)
        dic_main = dic['entry_data'][self.json_key[0]][0]['graphql'][self.json_key[1]][self.json_key[2]]
        edges = dic_main['edges']
        self.after = dic_main['page_info']['end_cursor']
        self.fetch_each_post(edges)
        try:
            self.user_id = dic['entry_data']['ProfilePage'][0]['graphql']['user']['id']
        except KeyError:
            pass

    def fetch_json(self):
        res = requests.get('https://www.instagram.com/graphql/query/', headers=self.headers, params=self.params)
        dic = res.json()
        edges = dic['data'][self.json_key[1]][self.json_key[2]]['edges']
        self.after = dic['data'][self.json_key[1]][self.json_key[2]]['page_info']['end_cursor']
        self.fetch_each_post(edges)

    def fetch_each_post(self, edges):
        for i in edges:
            time.sleep(self.time_interval)
            post = Post(i['node']['shortcode'], self.mode, self.sub_directory)
            post.fetch()


    def fetch(self):
        self.fetch_html()
        while self.after is not None:
            self.fetch_json()

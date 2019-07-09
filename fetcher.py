import requests
import re
import json
import time


class Fetcher:
    URL = 'https://www.instagram.com/explore/tags/%s/'

    def __init__(self):
        self.headers = {
            "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_3) "
                          "AppleWebKit/537.36 (KHTML, like Gecko) "
                          "Chrome/73.0.3683.75 "
                          "Safari/537.36"
        }
        self.params = None
        self.first = 12
        self.after = None
        self.json_key = None
        self.user_id = None
        self.url = None

    def fetch_html(self):
        res = requests.get(self.url, headers=self.headers)
        html = res.text
        match = re.search(r'<script type="text/javascript">window._sharedData = (.*?);</script>', html)
        if not match:
            return None
        json_text = match.groups()[0]
        dic = json.loads(json_text)
        dic_main = dic['entry_data'][self.json_key[0]][0]['graphql'][self.json_key[1]][self.json_key[2]]
        edges = dic_main['edges']
        self.after = dic_main['page_info']['end_cursor']
        [print(i['node']['id']) for i in edges]
        try:
            self.user_id = dic['entry_data']['ProfilePage'][0]['graphql']['user']['id']
        except KeyError:
            pass

    def fetch_json(self):
        res = requests.get('https://www.instagram.com/graphql/query/', headers=self.headers, params=self.params)
        dic = res.json()
        edges = dic['data'][self.json_key[1]][self.json_key[2]]['edges']
        self.after = dic['data'][self.json_key[1]][self.json_key[2]]['page_info']['end_cursor']
        [print(i['node']['id']) for i in edges]

    def fetch(self):
        self.fetch_html()
        while self.after is not None:
            time.sleep(1)
            self.fetch_json()

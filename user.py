import requests
import re
import json
import time


class User:
    URL = 'https://www.instagram.com/%s/'
    def __init__(self, username):
        self.username = username
        self.url = self.URL % username
        self.headers = {
            "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_3) "
                          "AppleWebKit/537.36 (KHTML, like Gecko) "
                          "Chrome/73.0.3683.75 "
                          "Safari/537.36"
        }
        self.params = {
            'query_hash': 'f2405b236d85e8296cf30347c9f08c2a'
        }
        self.first = 12
        self.after = None
        self.user_id = None

    def fetch_html(self):
        res = requests.get(self.url, headers=self.headers)
        html = res.text
        match = re.search(r'<script type="text/javascript">window._sharedData = (.*?);</script>', html)
        if not match:
            return None
        json_text = match.groups()[0]
        dic = json.loads(json_text)
        edges = dic['entry_data']['ProfilePage'][0]['graphql']['user']['edge_owner_to_timeline_media']['edges']
        self.user_id = dic['entry_data']['ProfilePage'][0]['graphql']['user']['id']
        self.after = dic['entry_data']['ProfilePage'][0]['graphql']['user']['edge_owner_to_timeline_media']['page_info']['end_cursor']
        [print(i['node']['id']) for i in edges]

    def fetch_json(self):
        self.params['variables'] = '{"id":"%s","first":%s,"after":"%s"}' % (self.user_id, self.first, self.after)
        res = requests.get('https://www.instagram.com/graphql/query/', headers=self.headers, params=self.params)
        dic = res.json()
        edges = dic['data']['user']['edge_owner_to_timeline_media']['edges']
        self.after = dic['data']['user']['edge_owner_to_timeline_media']['page_info']['end_cursor']
        [print(i['node']['id']) for i in edges]

    def fetch(self):
        self.fetch_html()
        while self.after is not None:
            time.sleep(1)
            self.fetch_json()

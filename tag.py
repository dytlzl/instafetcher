import requests
import re
import json
import time


class Tag:
    URL = 'https://www.instagram.com/explore/tags/%s/'
    def __init__(self, tag_name):
        self.tag_name = tag_name
        self.url = self.URL % tag_name
        self.headers = {
            "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_3) "
                          "AppleWebKit/537.36 (KHTML, like Gecko) "
                          "Chrome/73.0.3683.75 "
                          "Safari/537.36"
        }
        self.params = {
            'query_hash': 'f92f56d47dc7a55b606908374b43a314'
        }
        self.first = 12
        self.after = None

    def fetch_html(self):
        res = requests.get(self.url, headers=self.headers)
        html = res.text
        match = re.search(r'<script type="text/javascript">window._sharedData = (.*?);</script>', html)
        if not match:
            return None
        json_text = match.groups()[0]
        dic = json.loads(json_text)
        edges = dic['entry_data']['TagPage'][0]['graphql']['hashtag']['edge_hashtag_to_media']['edges']
        self.after = dic['entry_data']['TagPage'][0]['graphql']['hashtag']['edge_hashtag_to_media']['page_info']['end_cursor']
        [print(i['node']['id']) for i in edges]

    def fetch_json(self):
        self.params['variables'] = '{"tag_name":"%s","first":%s,"after":"%s"}' % (self.tag_name, self.first, self.after)
        res = requests.get('https://www.instagram.com/graphql/query/', headers=self.headers, params=self.params)
        dic = res.json()
        edges = dic['data']['hashtag']['edge_hashtag_to_media']['edges']
        self.after = dic['data']['hashtag']['edge_hashtag_to_media']['page_info']['end_cursor']
        [print(i['node']['id']) for i in edges]

    def fetch(self):
        self.fetch_html()
        while self.after is not None:
            time.sleep(1)
            self.fetch_json()

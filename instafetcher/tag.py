from .fetcher import Fetcher


class Tag(Fetcher):
    URL = 'https://www.instagram.com/explore/tags/%s/'

    def __init__(self, tag_name, mode='di', time_interval=0.1):
        super().__init__(mode, time_interval)
        self.name = tag_name
        self.url = self.URL % tag_name
        self.params = {
            'query_hash': 'f92f56d47dc7a55b606908374b43a314'
        }
        self.json_key = ['TagPage', 'hashtag', 'edge_hashtag_to_media']
        self.sub_directory = 'tag_' + tag_name
        self.mode = mode

    def fetch_json(self):
        self.params['variables'] = '{"tag_name":"%s","first":%s,"after":"%s"}' % (self.name, self.first, self.after)
        super().fetch_json()

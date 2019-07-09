from .fetcher import Fetcher


class Tag(Fetcher):
    URL = 'https://www.instagram.com/explore/tags/%s/'

    def __init__(self, tag_name):
        super().__init__()
        self.name = tag_name
        self.url = self.URL % tag_name
        self.params = {
            'query_hash': 'f92f56d47dc7a55b606908374b43a314'
        }
        self.json_key = ['TagPage', 'hashtag', 'edge_hashtag_to_media']

    def fetch_json(self):
        self.params['variables'] = '{"tag_name":"%s","first":%s,"after":"%s"}' % (self.name, self.first, self.after)
        super().fetch_json()

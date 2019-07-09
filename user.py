from .fetcher import Fetcher


class User(Fetcher):
    URL = 'https://www.instagram.com/%s/'

    def __init__(self, username):
        super().__init__()
        self.username = username
        self.url = self.URL % username
        self.params = {
            'query_hash': 'f2405b236d85e8296cf30347c9f08c2a'
        }
        self.json_key = ['ProfilePage', 'user', 'edge_owner_to_timeline_media']

    def fetch_json(self):
        self.params['variables'] = '{"id":"%s","first":%s,"after":"%s"}' % (self.user_id, self.first, self.after)
        super().fetch_json()

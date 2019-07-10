from .fetcher import Fetcher


class Profile(Fetcher):
    URL = 'https://www.instagram.com/%s/'

    def __init__(self, username, mode='di', time_interval=0.1):
        super().__init__(mode, time_interval)
        self.username = username
        self.url = self.URL % username
        self.params = {
            'query_hash': 'f2405b236d85e8296cf30347c9f08c2a'
        }
        self.json_key = ['ProfilePage', 'user', 'edge_owner_to_timeline_media']
        self.sub_directory = 'profile_' + username
        self.mode = mode

    def fetch_json(self):
        self.params['variables'] = '{"id":"%s","first":%s,"after":"%s"}' % (self.user_id, self.first, self.after)
        super().fetch_json()

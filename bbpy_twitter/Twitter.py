from .OAuthProvider import OAuthProvider

class Twitter(OAuthProvider):
    def __init__(self):
        super(Twitter, self).__init__()
        self._setRequestTokenURL('https://api.twitter.com/oauth/request_token')
        self._setAuthorizeURL('https://api.twitter.com/oauth/authorize')
        self._setAccessTokenURL('https://api.twitter.com/oauth/access_token')
        self._setServiceName('twitter')

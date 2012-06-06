from .OAuthProvider import OAuthProvider
from PySide.QtCore import *
import urllib.parse as urlparse
import json
import http.client
from PythonTwitter import twitter as twitterApi

class Twitter(OAuthProvider):
    def __init__(self):
        super(Twitter, self).__init__()
        self._setRequestTokenURL('https://api.twitter.com/oauth/request_token')
        self._setAuthorizeURL('https://api.twitter.com/oauth/authorize')
        self._setAccessTokenURL('https://api.twitter.com/oauth/access_token')
        self._setServiceName('twitter')
        self.User = None
        self.authorizationChanged.connect(self.getUserProfileData)
        self._twitterApi = twitterApi.Api(request_headers={'Authorization': 'OAuth'}, debugHTTP=True)

    @Slot()
    def getUserProfileData(self):
        if self.authorized:
            self._twitterApi.SetCredentials(consumer_key=self.consumerKey, consumer_secret=self.consumerSecret, access_token_key=self._oauthToken, access_token_secret=self._oauthTokenSecret)
            self.User = self._twitterApi.VerifyCredentials()
        else:
            self.User = None
            self._twitterApi.ClearCredentials()

        self.screenNameChanged.emit()
        self.realNameChanged.emit()
        self.timeZoneChanged.emit()
        self.descriptionChanged.emit()
        self.idChanged.emit()
        self.locationChanged.emit()
        self.profileImageChanged.emit()

    @Slot()
    def getUserTimeline(self):
        while True:
            try:
                statuses = api.GetPublicTimeline()
                break
            except:
                pass
        print([s.user.name for s in statuses])

    @Signal
    def screenNameChanged(self): pass
    def _getScreenName(self):
        if self.authorized:
            return self.User.screen_name
        else:
            return None
    _screenName = None
    screenName = Property(str, _getScreenName, notify=screenNameChanged)

    @Signal
    def realNameChanged(self): pass
    def _getRealName(self):
        if self.authorized:
            return self.User.name
        else:
            return None
    _realName = None
    realName = Property(str, _getRealName, notify=realNameChanged)

    @Signal
    def timeZoneChanged(self): pass
    def _getTimeZone(self):
        if self.authorized:
            return self.User.time_zone
        else:
            return None
    _timeZone = None
    timeZone = Property(str, _getTimeZone, notify=timeZoneChanged)

    @Signal
    def descriptionChanged(self): pass
    def _getDescription(self):
        if self.authorized:
            return self.User.description
        else:
            return None
    _description = None
    description = Property(str, _getDescription, notify=descriptionChanged)

    @Signal
    def idChanged(self): pass
    def _getID(self):
        if self.authorized:
            return self.User.id
        else:
            return None
    _id = None
    id = Property(str, _getID, notify=idChanged)

    @Signal
    def locationChanged(self): pass
    def _getLocation(self):
        if self.authorized:
            return self.User.location
        else:
            return None
    _location = None
    location = Property(str, _getLocation, notify=locationChanged)

    @Signal
    def profileImageChanged(self): pass
    def _getProfileImage(self):
        if self.authorized:
            return self.User.profile_image_url
        else:
            return None
    _profileImage = None
    profileImage = Property(str, _getProfileImage, notify=profileImageChanged)


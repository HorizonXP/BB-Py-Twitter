from .OAuthProvider import OAuthProvider
from PySide.QtCore import *
import urllib.parse as urlparse
import json
import http.client
from PythonTwitter import twitter as twitterApi

class User(QObject):
    def __init__(self, user):
        super(User, self).__init__()
        if isinstance(user, twitterApi.User):
            self.user = user
            self.screenNameChanged.emit()
            self.realNameChanged.emit()
            self.timeZoneChanged.emit()
            self.descriptionChanged.emit()
            self.idChanged.emit()
            self.locationChanged.emit()
            self.profileImageChanged.emit()
            self.URLChanged.emit()
            self.statusChanged.emit()
            self.statusesCountChanged.emit()
            self.followersCountChanged.emit()
            self.friendsCountChanged.emit()
        else:
            raise TypeError

    @Signal
    def screenNameChanged(self): pass
    def _getScreenName(self):
        return self.user.screen_name
    screenName = Property(str, _getScreenName, notify=screenNameChanged)

    @Signal
    def realNameChanged(self): pass
    def _getRealName(self):
        return self.user.name
    realName = Property(str, _getRealName, notify=realNameChanged)

    @Signal
    def timeZoneChanged(self): pass
    def _getTimeZone(self):
        return self.user.time_zone
    timeZone = Property(str, _getTimeZone, notify=timeZoneChanged)

    @Signal
    def descriptionChanged(self): pass
    def _getDescription(self):
        return self.user.description
    description = Property(str, _getDescription, notify=descriptionChanged)

    @Signal
    def idChanged(self): pass
    def _getID(self):
        return self.user.id
    id = Property(str, _getID, notify=idChanged)

    @Signal
    def locationChanged(self): pass
    def _getLocation(self):
        return self.user.location
    location = Property(str, _getLocation, notify=locationChanged)

    @Signal
    def profileImageChanged(self): pass
    def _getProfileImage(self):
        return self.user.profile_image_url
    profileImage = Property(str, _getProfileImage, notify=profileImageChanged)

    @Signal
    def URLChanged(self): pass
    def _getURL(self):
        return self.user.url
    URL = Property(str, _getURL, notify=URLChanged)

    @Signal
    def statusChanged(self): pass
    def _getStatus(self):
        return self.user.status.text
    status = Property(str, _getStatus, notify=statusChanged)

    @Signal
    def statusesCountChanged(self): pass
    def _getStatusesCount(self):
        return self.user.statuses_count
    statusesCount = Property(str, _getStatusesCount, notify=statusesCountChanged)

    @Signal
    def followersCountChanged(self): pass
    def _getFollowersCount(self):
        return self.user.followers_count
    followersCount = Property(str, _getFollowersCount, notify=followersCountChanged)

    @Signal
    def friendsCountChanged(self): pass
    def _getFriendsCount(self):
        return self.user.friends_count
    friendsCount = Property(str, _getFriendsCount, notify=friendsCountChanged)

class Status(QObject):
    def __init__(self, status):
        super(Status, self).__init__()
        if isinstance(status, twitterApi.Status):
            self.status = status
            self.idChanged.emit()
            self.textChanged.emit()
            self.relativeCreatedAtChanged.emit()
            self.userChanged.emit()
        else:
            raise TypeError

    @Signal
    def idChanged(self): pass
    def _getID(self):
        return self.status.id
    id = Property(str, _getID, notify=idChanged)

    @Signal
    def textChanged(self): pass
    def _getText(self):
        return self.status.text
    text = Property(str, _getText, notify=textChanged)

    @Signal
    def relativeCreatedAtChanged(self): pass
    def _getRelativeCreatedAt(self):
        return self.status.relative_created_at
    relativeCreatedAt = Property(str, _getRelativeCreatedAt, notify=relativeCreatedAtChanged)

    @Signal
    def userChanged(self): pass
    def _getUser(self):
        return User(self.status.user)
    user = Property(User, _getUser, notify=userChanged)
    

class TimelineModel(QAbstractListModel):
    def __init__(self, initList=list()):
        QAbstractListModel.__init__(self)
        # Store the items passed in
        self._items = initList

    # The view wants some of our data
    def data(self, index, role = Qt.DisplayRole):
        if role == Qt.DisplayRole:
            return self._items[index.row()]
        elif role == Qt.EditRole:
            # View wants our unformatted, editable data
            return self._items[index.row()]
        else:
            return None

    def setData(self, index, value, role = Qt.EditRole):
        # View wants to change some aspect of data
        # Return true for data change, false otherwise
        if role == Qt.EditRole:
            self._items[index.row()] = str(value)

            # emit the dataChanged() signal
            self.emit(SIGNAL("dataChanged(const QModelIndex&, const QModelIndex&)"), index, index)

            return True
        return False

    def removeRows(self, row, count, parent = QModelIndex()):
        if row < 0 or row > len(self._items):
            return

        self.beginRemoveRows(parent, row, row + count - 1)

        while count != 0:
            del self._items[row]
            count -= 1

        self.endRemoveRows()

    def addItem(self, item):
        self.beginInsertRows(QModelIndex(), len(self._items), len(self._items))
        self._items.append(str(item))
        self.endInsertRows()

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
            self._curUser = User(self._twitterApi.VerifyCredentials())
            self.userChanged.emit()
            statuses = self._twitterApi.GetPublicTimeline()
            self._publicTimeline = TimelineModel([Status(s) for s in statuses])
            self.publicTimelineUpdated.emit()
            statuses = self._twitterApi.GetUserTimeline()
            self._userTimeline = TimelineModel([Status(s) for s in statuses])
            self.userTimelineUpdated.emit()
            statuses = self._twitterApi.GetFriendsTimeline()
            self._friendsTimeline = TimelineModel([Status(s) for s in statuses])
            self.friendsTimelineUpdated.emit()
        else:
            self._curUser = None
            self.userChanged.emit()
            self._twitterApi.ClearCredentials()

    @Slot(str)
    def postTweet(self, tweet):
        if self.authorized:
            self._twitterApi.PostUpdate(tweet)
            self.tweetPosted.emit()

    @Signal
    def tweetPosted(self): pass

    @Signal
    def publicTimelineUpdated(self): pass
    def _getPublicTimeline(self):
        return self._publicTimeline
    _publicTimeline = None
    PublicTimeline = Property(TimelineModel, _getPublicTimeline, notify=publicTimelineUpdated)

    @Signal
    def userTimelineUpdated(self): pass
    def _getUserTimeline(self):
        return self._userTimeline
    _userTimeline = None
    UserTimeline = Property(TimelineModel, _getUserTimeline, notify=userTimelineUpdated)

    @Signal
    def friendsTimelineUpdated(self): pass
    def _getFriendsTimeline(self):
        return self._friendsTimeline
    _friendsTimeline = None
    FriendsTimeline = Property(TimelineModel, _getFriendsTimeline, notify=friendsTimelineUpdated)

    @Signal
    def userChanged(self): pass
    def _getUser(self):
        return self._curUser
    _curUser = None
    CurrentUser = Property(User, _getUser, notify=userChanged)

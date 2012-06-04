from .OAuthProvider import OAuthProvider
from PySide.QtCore import *
import urllib.parse as urlparse
import json
import http.client

class Twitter(OAuthProvider):
    def __init__(self):
        super(Twitter, self).__init__()
        self._setRequestTokenURL('https://api.twitter.com/oauth/request_token')
        self._setAuthorizeURL('https://api.twitter.com/oauth/authorize')
        self._setAccessTokenURL('https://api.twitter.com/oauth/access_token')
        self._setServiceName('twitter')
        self.authorizationChanged.connect(self.getUserProfileData)

    @Slot()
    def getUserProfileData(self):
        if self.authorized:
            reqURL = 'https://api.twitter.com/1/account/verify_credentials.json'
            resp, content = self.client.request(reqURL, 
                    headers={'Authorization': 'OAuth'}, include_body_hash=False)
            if resp['status'] != '200':
                raise Exception("Invalid response %s." % resp['status'])
            retVal = json.loads(content.decode())
            self._screenName = retVal['screen_name']
            self._realName = retVal['name']
            self._timeZone = retVal['time_zone']
            self._description = retVal['description']
            self._id = retVal['id_str']
            self._location = retVal['location']
            try:
                params = urlparse.urlencode({'screen_name': self._screenName, 
                            'size': 'original'})
                reqURL = '/1/users/profile_image?%s' % params
                conn = http.client.HTTPSConnection('api.twitter.com')
                conn.request('GET', reqURL)
                r1 = conn.getresponse()
                if (r1.status == 302):
                    self._profileImage = r1.getheader('Location')
                else:
                    raise
            except Exception as e:
                print(e)
                self._profileImage = retVal['profile_image_url']
                
        else:
            self._screenName = None
            self._realName = None
            self._timeZone = None
            self._description = None
            self._id = None
            self._location = None
            self._profileImage = None

        self.screenNameChanged.emit()
        self.realNameChanged.emit()
        self.timeZoneChanged.emit()
        self.descriptionChanged.emit()
        self.idChanged.emit()
        self.locationChanged.emit()
        self.profileImageChanged.emit()

    @Signal
    def screenNameChanged(self): pass
    def _getScreenName(self):
        return self._screenName
    _screenName = None
    screenName = Property(str, _getScreenName, notify=screenNameChanged)

    @Signal
    def realNameChanged(self): pass
    def _getRealName(self):
        return self._realName
    _realName = None
    realName = Property(str, _getRealName, notify=realNameChanged)

    @Signal
    def timeZoneChanged(self): pass
    def _getTimeZone(self):
        return self._timeZone
    _timeZone = None
    timeZone = Property(str, _getTimeZone, notify=timeZoneChanged)

    @Signal
    def descriptionChanged(self): pass
    def _getDescription(self):
        return self._description
    _description = None
    description = Property(str, _getDescription, notify=descriptionChanged)

    @Signal
    def idChanged(self): pass
    def _getID(self):
        return self._id
    _id = None
    id = Property(str, _getID, notify=idChanged)

    @Signal
    def locationChanged(self): pass
    def _getLocation(self):
        return self._location
    _location = None
    location = Property(str, _getLocation, notify=locationChanged)

    @Signal
    def profileImageChanged(self): pass
    def _getProfileImage(self):
        return self._profileImage
    _profileImage = None
    profileImage = Property(str, _getProfileImage, notify=profileImageChanged)


# This is our model. It will maintain, modify, and present data to our view(s).
# For more information on list models, take a look at:
# http://doc.trolltech.com/4.6/qabstractitemmodel.html
# Source: http://blog.rburchell.com/2010/02/pyside-tutorial-model-view-programming_22.html
class TweetListModel(QAbstractListModel):
    def __init__(self, mlist):
        QAbstractListModel.__init__(self)

        # Store the passed data list as a class member.
        self._items = mlist

    # We need to tell the view how many rows we have present in our data. see tutorial #3
    def rowCount(self, parent = QModelIndex()):
        return len(self._items)

    # view is asking us about some of our data.
    # see tutorial #3 for more information on this.
    def data(self, index, role = Qt.DisplayRole):
        if role == Qt.DisplayRole:
            return QVariant(self._items[index.row()])
        elif role == Qt.EditRole:
            # The view is asking for the editable form of the data. i.e. unformatted.
            # See the comment in setData().
            return QVariant(self._items[index.row()])
        else:
            return QVariant()

    # the view is asking us to *change* some aspect of our data.
    # as in the above, it can be any aspect of the data, not *just* the information contained in the model.
    # remember to return true if you handle a data change, and false otherwise, always!
    # for more information, see:
    # http://doc.trolltech.com/4.6/qabstractitemmodel.html#setData
    def setData(self, index, value, role = Qt.EditRole):
        # You might be expecting Qt.DisplayRole here, but no.
        # Qt.DisplayRole is the *displayed* value of an item, like, a formatted currency value: "$44.00"
        # Qt.EditRole is the raw data of an item, e.g. "4400" (as in cents).
        if role == Qt.EditRole:
             # set the data.
             # the str() cast here is mostly for peace of mind, you can't perform some operations
             # in python with Qt types, like pickling.
             self._items[index.row()] = str(value.toString().toUtf8())

             # *always* emit the dataChanged() signal after changing any data inside the model.
             # this is so e.g. the different views know they need to do things with it.
             #
             # don't be lazy and pass a huge range of values to this, because it is processing-heavy.
             #
             # because we are a simple list, we only have one index to worry about for topleft/bottom right,
             # so just reuse the index we are passed.
             QObject.emit(self, SIGNAL("dataChanged(const QModelIndex&, const QModelIndex &)"), index, index)
             return True
        # unhandled change.
        return False

    # if you e.g. don't want to make an item selectable, or draggable, here's the place to do it.
    # by default, items are enabled, and selectable, but we want to make them editable too, so we need to
    # reimplement this. of course, this means you can make only specific items selectable, for example,
    # by using the 'index' parameter.
    # For more information, see:
    # http://doc.trolltech.com/4.6/qabstractitemmodel.html#flags
    def flags(self, index):
        return Qt.ItemIsSelectable | Qt.ItemIsEditable | Qt.ItemIsEnabled

    # remove rows from our model.
    # 'row' is the row number to be removed, 'count' are the total number of rows to remove.
    # 'parent' is the 'parent' of the initial row: this is pretty much only relevant for tree models etc.
    # For more information, see:
    # http://doc.trolltech.com/4.6/qabstractitemmodel.html#removeRows
    def removeRows(self, row, count, parent = QModelIndex()):
        # make sure the index is valid, to avoid IndexErrors ;)
        if row < 0 or row > len(self._items):
            return

        # let the model know we're changing things.
        # we may have to remove multiple rows, if not, this could be handled simpler.
        self.beginRemoveRows(parent, row, row + count - 1)

        # actually remove the items from our internal data representation
        while count != 0:
            del self._items[row]
            count -= 1

        # let the model know we're done
        self.endRemoveRows()

    # while we could use QAbstractItemModel::insertRows(), we'd have to shoehorn around the API
    # to get things done: we'd need to call setData() etc.
    # The easier way, in this case, is to use our own method to do the heavy lifting.
    def addItem(self, item):
        # The str() cast is because we don't want to be storing a Qt type in here.
        self.beginInsertRows(QModelIndex(), len(self._items), len(self._items))
        self._items.append(str(item))
        self.endInsertRows()

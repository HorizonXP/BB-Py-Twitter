import QtQuick 1.1
import Qt.labs.shaders 1.0

Rectangle {
    width: 1024
    height: 600
    color: "#7e0080"

    function addUserElement(s, u) {
        userTimelineModel.append({'tweet': s.text, 'relativeCreatedAt': s.relativeCreatedAt, 'img': u.profileImage, 'screen_name': u.screenName})
    }

    function addFriendsElement(s, u) {
        friendsTimelineModel.append({'tweet': s.text, 'relativeCreatedAt': s.relativeCreatedAt, 'img': u.profileImage, 'screen_name': u.screenName})
    }

    Image {
        source: '../assets/background.png'
        anchors.fill: parent
    }

    ListModel {
        id: userTimelineModel
    }

    ListModel {
        id: friendsTimelineModel
    }

    Component {
        id: tweetDelegate
        Item {
            width: parent.width; height: 50
            anchors.margins: 5
            Row {
                height: parent.height
                width: parent.width
                Image {
                    id: imgTweet
                    fillMode: Image.PreserveAspectFit
                    source: img
                }
                Column {
                    width: parent.width - imgTweet.width
                    Text {
                        width: parent.width
                        color: 'white'
                        font.pixelSize: 12
                        text: screen_name
                        anchors.leftMargin: 5
                    }
                    Text {
                        width: parent.width
                        color: 'white'
                        font.pixelSize: 10
                        wrapMode: Text.WordWrap
                        text: tweet
                        anchors.leftMargin: 5
                    }
                }
            }
        }
    }

    ListView {
        id: timeline
        width: parent.width / 3
        height: parent.height
        anchors.left: parent.left
        anchors.top: parent.top
        model: friendsTimelineModel
        delegate: tweetDelegate
    }

    Item {
        id: currentTweet
        height: parent.height * 0.2
        width: parent.width * 2 / 3
        anchors.top: parent.top
        anchors.right: parent.right
        Item {
            id: profileImage
            anchors.left: parent.left
            anchors.margins: 5;
            width: parent.height
            height: parent.height
            Image {
                anchors.fill: parent
                fillMode: Image.PreserveAspectFit
                source: (twitter.authorized) ? twitter.CurrentUser.profileImage : "" 
                smooth: true
            }
        }
        Text {
            id: screenName
            color: 'white'
            font.bold: true
            font.pixelSize: parent.height * 0.25
            anchors.left: profileImage.right
            anchors.leftMargin: 5
            anchors.top: parent.top
            text: (twitter.authorized) ? twitter.CurrentUser.screenName : "" 
        }
        Text {
            id: userDescription
            color: 'white'
            font.bold: true
            font.pixelSize: parent.height * 0.125
            wrapMode: Text.WordWrap
            width: parent.width - profileImage.width - 20
            anchors.left: profileImage.right
            anchors.leftMargin: 5
            anchors.top: screenName.bottom
            text: (twitter.authorized) ? twitter.CurrentUser.description : ""
        }
        Text {
            id: userFollowersCount
            color: 'white'
            font.bold: true
            width: (parent.width - profileImage.width - 20)/3
            font.pixelSize: parent.height * 0.0625
            anchors.left: profileImage.right
            anchors.leftMargin: 5
            anchors.top: userDescription.bottom
            text: (twitter.authorized) ? twitter.CurrentUser.followersCount : ""
        }
        Text {
            id: userFriendsCount
            color: 'white'
            font.bold: true
            width: (parent.width - profileImage.width - 20)/3
            font.pixelSize: parent.height * 0.0625
            anchors.left: userFollowersCount.right
            anchors.leftMargin: 5
            anchors.top: userDescription.bottom
            text: (twitter.authorized) ? twitter.CurrentUser.friendsCount : ""
        }
        Text {
            id: userStatusesCount
            color: 'white'
            font.bold: true
            width: (parent.width - profileImage.width - 20)/3
            font.pixelSize: parent.height * 0.0625
            anchors.left: userFriendsCount.right
            anchors.leftMargin: 5
            anchors.top: userDescription.bottom
            text: (twitter.authorized) ? twitter.CurrentUser.statusesCount : ""
        }
    }

    ListView {
        id: currentTweetReplies
        height: parent.height * 0.73
        width: parent.width * 2 / 3
        anchors.top: currentTweet.bottom
        anchors.right: parent.right
        clip: true
        model: userTimelineModel
        delegate: tweetDelegate
    }

    ToolBar {
        height: parent.height * 0.07
        width: parent.width * 2 / 3
        anchors.bottom: parent.bottom
        anchors.right: parent.right
        button1Label: (twitter.authorized) ? "Logout" : "Login"
        button2Label: "Tweet about BB-Py!"
        onButton1Clicked:
        {
            if (twitter.authorized) {
                twitter.logout()
                userTimelineModel.clear()
                friendsTimelineModel.clear()
            }
            else {
                twitter.getAuthorization()
            }
        }
        onButton2Clicked:
        {
            if (twitter.authorized) {
                twitter.postTweet("I'm sending this tweet from a @BBPyProject sample app! This is so cool, check them out!");
            }
        }
    }
}

import QtQuick 1.1
import Qt.labs.shaders 1.0

Rectangle {
    width: 1024
    height: 600
    color: "#7e0080"

    function addUserElement(s) {
        userTimelineModel.append({'tweet': s.text, 'relativeCreatedAt': s.relativeCreatedAt})
    }

    function addFriendsElement(s) {
        friendsTimelineModel.append({'tweet': s.text, 'relativeCreatedAt': s.relativeCreatedAt, 'img': s.user.profileImage, 'screenName': s.user.screenName})
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

    ListView {
        id: timeline
        width: parent.width / 3
        height: parent.height
        anchors.left: parent.left
        anchors.top: parent.top
        model: friendsTimelineModel
        delegate: Item {
            Image {
                fillMode: Image.PreserveAspectFit
                source: img
            }
            Text {
                text: screenName
                color: 'white'
            }
            Text {
                color: 'white'
                font.pixelSize: 12
                wrapMode: Text.WordWrap
                text: tweet + ": " + relativeCreatedAt
            }
        }
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
    }

    ListView {
        id: currentTweetReplies
        height: parent.height * 0.73
        width: parent.width * 2 / 3
        anchors.top: currentTweet.bottom
        anchors.right: parent.right
        clip: true
        model: userTimelineModel
        delegate: Text {
            color: 'gray'
            text: tweet + ": " + relativeCreatedAt
        }
    }

    ToolBar {
        height: parent.height * 0.07
        width: parent.width * 2 / 3
        anchors.bottom: parent.bottom
        anchors.right: parent.right
        button1Label: (twitter.authorized) ? "Logout" : "Login"
        button2Label: "New Tweet"
        onButton1Clicked:
        {
            if (twitter.authorized) {
                twitter.logout()
            }
            else {
                twitter.getAuthorization()
            }
        }
        onButton2Clicked:
        {
            if (twitter.authorized) {
                twitter.getUserTimeline(timelineModel);
            }
        }
    }
}

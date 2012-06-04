import QtQuick 1.1
import Qt.labs.shaders 1.0

Rectangle {
    width: 1024
    height: 600
    color: "#7e0080"

    Image {
        source: '../assets/background.png'
        anchors.fill: parent
    }

    ListModel {
        id: timelineModel
        ListElement {
            name: "Bill Smith"
            number: "555 3264"
        }
        ListElement {
            name: "John Brown"
            number: "555 8426"
        }
        ListElement {
            name: "Sam Wise"
            number: "555 0473"
        }
    }
    ListView {
        id: timeline
        width: parent.width / 3
        height: parent.height
        anchors.left: parent.left
        anchors.top: parent.top
        model: timelineModel
        delegate: Text {
            color: 'white'
            text: name + ": " + number
        }
    }

    Rectangle {
        id: currentTweet
        color: 'red'
        height: parent.height * 0.2
        width: parent.width * 2 / 3
        anchors.top: parent.top
        anchors.right: parent.right
    }

    ListView {
        id: currentTweetReplies
        height: parent.height * 0.73
        width: parent.width * 2 / 3
        anchors.top: currentTweet.bottom
        anchors.right: parent.right
        clip: true
        model: timelineModel
        delegate: Text {
            color: 'gray'
            text: name + ": " + number
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
            twitter.getAuthorization()
        }
    }
}

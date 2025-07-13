import QtQuick
import QtQuick.Controls
import QtQuick.Window

Rectangle {
    anchors.fill: parent
    color: "#ffffff"
    width:1920
    height:1080

    Image {
        id: background
        anchors.fill: parent
        source: "photos/background.jpg"
        fillMode: Image.PreserveAspectCrop
    }

    Image {
        id: logo
        anchors.horizontalCenter: parent.horizontalCenter
        anchors.top: parent.top
        anchors.topMargin: 20
        width: 724
        height: 242
        opacity: 0.85
        source: "photos/logo.png"
        fillMode: Image.PreserveAspectFit
    }

    Rectangle {
        id: mainView
        y: 381
        width: 1504
        height: 741
        radius: 50
        color: "#9353504c"
        anchors.horizontalCenter: parent.horizontalCenter
        anchors.top: logo.bottom
        anchors.topMargin: 20
        anchors.horizontalCenterOffset: 0

        Rectangle {
            id: answerBoxBackground
            anchors.top: parent.top
            anchors.left: parent.left
            anchors.right: parent.right
            anchors.leftMargin: 40
            anchors.rightMargin: 178
            anchors.topMargin: 44
            height: 490
            color: "transparent"
            border.width: 4
            border.color: "#000000"
            radius: 50

            Text {
                id: answerBox
                objectName: "answerBox"
                anchors.fill: parent
                anchors.margins: 20
                text: qsTr("Agent waiting for query")
                font.pixelSize: 30
                wrapMode: Text.WordWrap
                verticalAlignment: Text.AlignTop
            }
        }

        TextArea {
            id: queryBox
            objectName: "queryBox"
            anchors.left: parent.left
            anchors.bottom: parent.bottom
            anchors.leftMargin: 40
            anchors.bottomMargin: 60
            width: parent.width - 220
            height: 125
            placeholderText: qsTr("Ask anything about F1")
            wrapMode: Text.Wrap
            font.pointSize: 18
            placeholderTextColor: "#000000"
            padding: 20

            background: Rectangle {
                color: "transparent"
                border.width: 4
                border.color: "#000000"
                radius: 50
            }
        }




        Button {
            id: sendButton
            x: 1347
            y: 560
            objectName: "sendButton"
            anchors.right: parent.right
            anchors.bottom: parent.bottom
            anchors.rightMargin: 66
            anchors.bottomMargin: 75
            width: 70
            height: 70
            hoverEnabled: true
            display: AbstractButton.IconOnly
            background: null

            contentItem: Image {
                source: "photos/search.png"
                width: 40
                height: 40
                anchors.centerIn: parent
            }

            transform: Scale {
                                origin.x: sendButton.width / 2
                                origin.y: sendButton.height / 2
                                xScale: sendButton.hovered ? 1.12 : 1.0
                                yScale: sendButton.hovered ? 1.12 : 1.0

                                Behavior on xScale {
                                    NumberAnimation { duration: 160; easing.type: Easing.OutQuad }
                                }
                                Behavior on yScale {
                                    NumberAnimation { duration: 160; easing.type: Easing.OutQuad }
                                }
                            }
        }
    }
}

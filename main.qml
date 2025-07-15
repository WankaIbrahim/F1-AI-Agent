import QtQuick
import QtQuick.Controls
import QtQuick.Window

ApplicationWindow {
    id: root

    visible: true
    width: Screen.width
    height: Screen.height
    title: "F1 AI Agent"

    Connections {
        target: chatbotBackend
        function onResponseReady(response) {
            answerBox.text = response
        }
    }

    Rectangle {
        anchors.fill: parent
        color: "#ffffff"

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
            anchors.topMargin: parent.height * 0.02
            width: parent.width * 0.2
            height: parent.height * 0.2
            fillMode: Image.PreserveAspectFit
            opacity: 0.85
            source: "photos/logo.png"
        }

        Rectangle {
            id: mainView
            anchors.top: logo.bottom
            anchors.topMargin: parent.height * 0.02
            anchors.horizontalCenter: parent.horizontalCenter
            width: parent.width * 0.8
            height: parent.height * 0.65
            radius: 50
            color: "#9353504c"

            Rectangle {
                id: answerBoxBackground
                anchors.top: parent.top
                anchors.left: parent.left
                anchors.right: parent.right
                anchors.leftMargin: parent.width * 0.03
                anchors.rightMargin: parent.width * 0.12
                anchors.topMargin: parent.height * 0.06
                height: parent.height * 0.6
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
                    font.pixelSize: parent.height * 0.05
                    wrapMode: Text.WordWrap
                    verticalAlignment: Text.AlignTop
                }
            }

            TextArea {
                id: queryBox
                objectName: "queryBox"
                anchors.bottom: parent.bottom
                anchors.left: parent.left
                anchors.right: parent.right
                anchors.leftMargin: parent.width * 0.03
                anchors.rightMargin: parent.width * 0.12
                anchors.bottomMargin: parent.height * 0.08
                height: parent.height * 0.2
                placeholderText: qsTr("Ask anything about F1")
                wrapMode: Text.Wrap
                font.pixelSize: parent.height * 0.035
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
                objectName: "sendButton"
                anchors.right: parent.right
                anchors.bottom: parent.bottom
                anchors.rightMargin: parent.width * 0.04
                anchors.bottomMargin: parent.height * 0.08
                width: parent.width * 0.06
                height: width
                hoverEnabled: true
                display: AbstractButton.IconOnly
                background: null

                contentItem: Image {
                    source: "photos/search.png"
                    width: parent.width * 0.5
                    height: width
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

                onClicked: {
                    console.log("Button Clicked")
                    if (queryBox.text.trim() === "") return
                    if (!chatbotBackend) {
                        console.log("chatbotBackend is null!")
                        return
                    }
                    chatbotBackend.sendQuery(queryBox.text)
                    queryBox.text = ""
                }
            }

            BusyIndicator {
                id: busyIndicator
                running: false
                visible: false
                anchors.right: sendButton.left
                anchors.verticalCenter: sendButton.verticalCenter
                width: sendButton.width * 0.45
                height: width
            }
        }
    }
}

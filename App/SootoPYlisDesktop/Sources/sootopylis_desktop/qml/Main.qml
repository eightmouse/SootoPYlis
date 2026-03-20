import QtQuick
import QtQuick.Layouts
import QtQuick.Window

import "Scenes/Root"

Window {
    id: window

    width: 1440
    height: 900
    visible: true
    minimumWidth: 1120
    minimumHeight: 740
    title: desktopSession ? desktopSession.appName : "SootoPYlis"
    color: "transparent"
    flags: Qt.Window | Qt.FramelessWindowHint
    property bool windowsChrome: Qt.platform.os === "windows"

    Item {
        id: windowRoot
        anchors.fill: parent

        readonly property int frameMargin: 0

        Rectangle {
            visible: windowRoot.frameMargin > 0
            anchors.fill: appFrame
            anchors.margins: -10
            radius: appFrame.radius + 10
            color: "#000000"
            opacity: 0.22
            antialiasing: true
        }

        Rectangle {
            id: appFrame
            objectName: "appFrame"

            anchors.fill: parent
            anchors.margins: windowRoot.frameMargin
            radius: window.visibility === Window.Maximized ? 0 : 30
            gradient: Gradient {
                GradientStop { position: 0.0; color: rootScene.theme ? rootScene.theme.appBackgroundTop : "#0d1020" }
                GradientStop { position: 0.45; color: rootScene.theme ? rootScene.theme.appBackgroundMiddle : "#080a15" }
                GradientStop { position: 1.0; color: rootScene.theme ? rootScene.theme.appBackgroundBottom : "#05060e" }
            }
            border.color: rootScene.theme ? rootScene.theme.panelOutline : "#2b2f3d"
            border.width: 1
            clip: true
            antialiasing: true

            Rectangle {
                id: titleBar
                objectName: "titleBar"

                anchors.left: parent.left
                anchors.right: parent.right
                anchors.top: parent.top
                height: 34
                color: rootScene.windowBarColor
                z: 2
                antialiasing: true

                RowLayout {
                    anchors.fill: parent
                    anchors.leftMargin: 12
                    anchors.rightMargin: window.windowsChrome ? 144 : 12
                    spacing: 8

                    Item {
                        visible: !window.windowsChrome
                        implicitWidth: macControls.implicitWidth
                        implicitHeight: macControls.implicitHeight
                        Layout.preferredWidth: visible ? implicitWidth : 0
                        Layout.maximumWidth: visible ? implicitWidth : 0

                        Row {
                            id: macControls
                            spacing: 7

                            Rectangle {
                                width: 11
                                height: 11
                                radius: 6
                                color: "#ff5f57"
                                antialiasing: true

                                MouseArea {
                                    anchors.fill: parent
                                    onClicked: window.close()
                                }
                            }

                            Rectangle {
                                width: 11
                                height: 11
                                radius: 6
                                color: "#febc2e"
                                antialiasing: true

                                MouseArea {
                                    anchors.fill: parent
                                    onClicked: window.showMinimized()
                                }
                            }

                            Rectangle {
                                width: 11
                                height: 11
                                radius: 6
                                color: "#28c840"
                                antialiasing: true

                                MouseArea {
                                    anchors.fill: parent
                                    onClicked: {
                                        if (window.visibility === Window.Maximized) {
                                            window.showNormal()
                                        } else {
                                            window.showMaximized()
                                        }
                                    }
                                }
                            }
                        }
                    }

                    Text {
                        text: desktopSession ? desktopSession.appName : "SootoPYlis"
                        color: rootScene.windowBarTextColor
                        font.family: rootScene.textFontFamily
                        font.pixelSize: 14
                        font.bold: true
                        Layout.leftMargin: 6
                    }

                    Item {
                        Layout.fillWidth: true
                    }
                }

                Row {
                    id: windowsControls

                    visible: window.windowsChrome
                    anchors.top: parent.top
                    anchors.right: parent.right
                    height: parent.height
                    spacing: 0
                    z: 3

                    Repeater {
                        model: [
                            { "label": "-", "role": "min" },
                            { "label": "\u00d7", "role": "close" }
                        ]

                        delegate: Rectangle {
                            required property var modelData

                            width: 46
                            height: titleBar.height
                            color: buttonArea.containsMouse
                                ? (modelData.role === "close" ? "#c84a4a" : rootScene.windowBadgeColor)
                                : "transparent"

                            Text {
                                anchors.centerIn: parent
                                text: modelData.label
                                color: buttonArea.containsMouse && modelData.role === "close"
                                    ? "#ffffff"
                                    : rootScene.windowBarTextColor
                                font.pixelSize: modelData.role === "min" ? 16 : 10
                                font.bold: modelData.role !== "min"
                            }

                            MouseArea {
                                id: buttonArea

                                anchors.fill: parent
                                hoverEnabled: true

                                onClicked: {
                                    if (modelData.role === "min") {
                                        window.showMinimized()
                                    } else {
                                        window.close()
                                    }
                                }
                            }
                        }
                    }
                }

                MouseArea {
                    anchors.fill: parent
                    acceptedButtons: Qt.LeftButton
                    z: -1

                    onPressed: {
                        window.startSystemMove()
                    }
                }
            }

            RootScene {
                id: rootScene
                anchors.left: parent.left
                anchors.right: parent.right
                anchors.top: titleBar.bottom
                anchors.topMargin: -1
                anchors.bottom: parent.bottom
            }
        }
    }
}

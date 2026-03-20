import QtQuick

import "../Gameplay"

Item {
    id: root
    objectName: "rootScene"

    readonly property var theme: gameplayScene.theme
    readonly property string textFontFamily: gameplayScene.textFontFamily
    readonly property color appBackgroundTop: gameplayScene.theme.appBackgroundTop
    readonly property color appBackgroundMiddle: gameplayScene.theme.appBackgroundMiddle
    readonly property color appBackgroundBottom: gameplayScene.theme.appBackgroundBottom
    readonly property color windowBarColor: gameplayScene.windowBarColor
    readonly property color windowBarBorderColor: gameplayScene.windowBarBorderColor
    readonly property color windowBarTextColor: gameplayScene.windowBarTextColor
    readonly property color windowBadgeColor: gameplayScene.windowBadgeColor
    readonly property color windowBadgeBorderColor: gameplayScene.windowBadgeBorderColor
    readonly property color windowBadgeTextColor: gameplayScene.windowBadgeTextColor

    GameplayScene {
        id: gameplayScene
        objectName: "gameplayScene"
        anchors.fill: parent
    }
}

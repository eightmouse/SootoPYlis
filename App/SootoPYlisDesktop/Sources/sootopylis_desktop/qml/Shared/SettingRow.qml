import QtQuick
import QtQuick.Layouts

Rectangle {
    id: root

    property var theme: null
    property string monoFontFamily: "Consolas"
    property string label: ""
    property string value: ""
    property string actionKey: ""
    signal activated(string actionKey)

    width: parent ? parent.width : 0
    height: 34
    radius: 14
    color: root.theme ? root.theme.optionIdleFill : "#24302c"
    border.color: root.theme ? root.theme.optionIdleStroke : "#4d5d57"
    border.width: 1
    antialiasing: true

    Rectangle {
        anchors.fill: parent
        radius: parent.radius
        color: root.theme ? root.theme.optionGlass : "#ffffff"
        antialiasing: true
    }

    Rectangle {
        anchors.fill: parent
        anchors.margins: 2
        radius: parent.radius - 2
        color: "transparent"
        border.color: root.theme ? root.border.color : "#8ca097"
        border.width: 1
        opacity: 0.55
        antialiasing: true
    }

    RowLayout {
        anchors.fill: parent
        anchors.margins: 12

        Text {
            text: root.label
            color: root.theme ? root.theme.primaryText : "#d7e2da"
            font.family: root.monoFontFamily
            font.pixelSize: 12
            font.letterSpacing: 1.0
            font.kerning: false
            renderType: Text.NativeRendering
            verticalAlignment: Text.AlignVCenter
            Layout.alignment: Qt.AlignVCenter
        }

        Item {
            Layout.fillWidth: true
        }

        Text {
            text: root.value
            color: root.theme ? root.theme.secondaryText : "#c6d3cc"
            font.family: root.monoFontFamily
            font.pixelSize: 10
            font.bold: true
            font.kerning: false
            renderType: Text.NativeRendering
            verticalAlignment: Text.AlignVCenter
            Layout.alignment: Qt.AlignVCenter
        }
    }

    MouseArea {
        anchors.fill: parent
        cursorShape: Qt.PointingHandCursor
        onClicked: root.activated(root.actionKey)
    }
}

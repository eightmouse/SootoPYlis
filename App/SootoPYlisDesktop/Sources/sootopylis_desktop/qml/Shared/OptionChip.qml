import QtQuick

Rectangle {
    id: root

    property var theme: null
    property string monoFontFamily: "Consolas"
    property string label: ""
    property bool selected: false
    property string filterValue: ""
    signal activated(string filterValue)

    width: 74
    height: 30
    radius: 15
    color: root.theme ? (root.selected ? root.theme.optionFocusFill : root.theme.optionIdleFill) : (root.selected ? "#2f3a35" : "#222a27")
    border.color: root.theme ? (root.selected ? root.theme.optionFocusStroke : root.theme.optionIdleStroke) : (root.selected ? "#6c8279" : "#4d5d57")
    border.width: 1
    antialiasing: true

    Rectangle {
        anchors.fill: parent
        radius: parent.radius
        color: root.theme ? (root.selected ? root.theme.optionFocusGlass : root.theme.optionGlass) : "#ffffff"
        antialiasing: true
    }

    Rectangle {
        anchors.fill: parent
        anchors.margins: 2
        radius: parent.radius - 2
        color: "transparent"
        border.color: root.theme ? root.border.color : "#8ca097"
        border.width: 1
        opacity: root.selected ? 0.9 : 0.5
        antialiasing: true
    }

    Text {
        anchors.centerIn: parent
        text: root.label
        color: root.theme ? root.theme.primaryText : "#c7d3cc"
        font.family: root.monoFontFamily
        font.pixelSize: 8
        font.bold: true
        font.kerning: false
        renderType: Text.NativeRendering
        verticalAlignment: Text.AlignVCenter
    }

    MouseArea {
        anchors.fill: parent
        cursorShape: Qt.PointingHandCursor
        onClicked: root.activated(root.filterValue)
    }
}

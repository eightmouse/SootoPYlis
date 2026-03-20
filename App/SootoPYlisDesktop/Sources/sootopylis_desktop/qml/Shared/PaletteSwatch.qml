import QtQuick
import "ThemePalette.js" as ThemePalette

Rectangle {
    id: root

    property var theme: null
    property string monoFontFamily: "Consolas"
    property string label: ""
    property string styleValue: ""
    property color swatchColor: "#ffffff"
    property bool selected: false
    signal activated(string styleValue)

    function activate() {
        if (root.styleValue !== "") {
            root.activated(root.styleValue)
        }
    }

    readonly property real luminance: (root.swatchColor.r * 0.299) + (root.swatchColor.g * 0.587) + (root.swatchColor.b * 0.114)
    readonly property color labelColor: root.luminance > 0.62 ? Qt.rgba(0.08, 0.09, 0.10, 0.82) : Qt.rgba(0.98, 0.99, 0.99, 0.92)

    width: 56
    height: 66
    radius: 13
    color: root.theme ? (root.selected ? root.theme.optionFocusFill : root.theme.optionIdleFill) : (root.selected ? "#31403b" : "#27312e")
    border.color: root.theme ? (root.selected ? root.theme.optionFocusStroke : root.theme.optionIdleStroke) : (root.selected ? "#7f958c" : "#4d5d57")
    border.width: 1
    antialiasing: true

    Rectangle {
        anchors.fill: parent
        anchors.margins: 2
        radius: parent.radius - 2
        gradient: Gradient {
            GradientStop { position: 0.0; color: ThemePalette.mix(root.swatchColor, Qt.rgba(1, 1, 1, 1), 0.18) }
            GradientStop { position: 0.58; color: root.swatchColor }
            GradientStop { position: 1.0; color: ThemePalette.mix(root.swatchColor, Qt.rgba(0, 0, 0, 1), 0.12) }
        }
        antialiasing: true
    }

    Rectangle {
        anchors.left: parent.left
        anchors.right: parent.right
        anchors.top: parent.top
        anchors.margins: 4
        height: 18
        radius: parent.radius - 4
        color: Qt.rgba(1, 1, 1, root.selected ? 0.16 : 0.12)
        antialiasing: true
    }

    Text {
        anchors.horizontalCenter: parent.horizontalCenter
        anchors.bottom: parent.bottom
        anchors.bottomMargin: 8
        text: root.label
        color: root.labelColor
        font.family: root.monoFontFamily
        font.pixelSize: 7
        font.bold: true
        font.kerning: false
        renderType: Text.NativeRendering
        horizontalAlignment: Text.AlignHCenter
        width: parent.width - 8
        wrapMode: Text.Wrap
        elide: Text.ElideRight
        maximumLineCount: 2
        lineHeight: 0.96
    }

    MouseArea {
        anchors.fill: parent
        cursorShape: Qt.PointingHandCursor
        onClicked: root.activate()
    }
}

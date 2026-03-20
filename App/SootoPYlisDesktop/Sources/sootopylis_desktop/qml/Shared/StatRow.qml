import QtQuick
import QtQuick.Layouts

Rectangle {
    id: root

    property var theme: null
    property string monoFontFamily: "Consolas"
    property string label: ""
    property string value: ""
    property color labelColor: root.theme ? root.theme.primaryText : "#d7e2da"

    width: parent ? parent.width : 0
    height: 34
    radius: 13
    color: root.theme ? root.theme.optionIdleFill : "#22302b"
    border.color: root.theme ? root.theme.optionIdleStroke : "#3d4c46"
    border.width: 1
    antialiasing: true

    Rectangle {
        anchors.fill: parent
        radius: parent.radius
        color: root.theme ? root.theme.optionGlass : "#ffffff"
        antialiasing: true
    }

    RowLayout {
        anchors.fill: parent
        anchors.margins: 12

        Text {
            text: root.label
            color: root.labelColor
            font.family: root.monoFontFamily
            font.pixelSize: 12
            font.kerning: false
            renderType: Text.NativeRendering
            elide: Text.ElideRight
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
            font.pixelSize: 11
            font.bold: true
            font.kerning: false
            renderType: Text.NativeRendering
            verticalAlignment: Text.AlignVCenter
            Layout.alignment: Qt.AlignVCenter
        }
    }
}

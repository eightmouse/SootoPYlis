import QtQuick
import QtQuick.Layouts
import "ThemePalette.js" as ThemePalette

Item {
    id: root

    property var theme: null
    property string monoFontFamily: "Consolas"
    property string titleFontFamily: monoFontFamily
    property string symbolFontFamily: "Segoe UI Symbol"
    property string title: ""
    property string value: ""
    property string detail: ""
    property bool expanded: false
    property bool expandToFill: false
    property int collapsedHeight: 72
    property int expandedBodyHeight: 140
    readonly property int contentMargin: 18
    readonly property int headerHeight: Math.max(32, root.collapsedHeight - (root.contentMargin * 2))
    readonly property color shadowColor: root.theme ? root.theme.cardCastColor : "#050607"
    readonly property color outlineColor: root.theme ? (root.expanded ? ThemePalette.mix(root.theme.menuIdleStroke, root.theme.menuFocusStroke, 0.35) : root.theme.menuIdleStroke) : "#5f6e67"
    readonly property color innerOutlineColor: root.theme ? root.theme.cardInnerOutline : "#26302c"
    readonly property color fillColor: root.theme ? (root.expanded ? ThemePalette.mix(root.theme.menuIdleFill, root.theme.menuFocusFill, 0.30) : root.theme.menuIdleFill) : "#2d3834"
    readonly property color glassColor: root.theme ? (root.expanded ? ThemePalette.mix(root.theme.menuIdleGlass, root.theme.menuFocusGlass, 0.28) : root.theme.menuIdleGlass) : "#ffffff"
    readonly property color titleColor: root.theme ? root.theme.primaryText : "#d7e2da"
    readonly property color valueColor: root.theme ? root.theme.primaryText : "#dbe5df"
    readonly property color detailColor: root.theme ? root.theme.secondaryText : "#b2bdb7"
    readonly property color chevronColor: root.theme ? root.theme.secondaryText : "#b7c2bc"
    signal toggled()
    default property alias contentData: bodyColumn.data

    width: parent ? parent.width : 0
    implicitHeight: collapsedHeight + bodyClip.height
    Layout.fillWidth: true

    Rectangle {
        anchors.fill: parent
        anchors.margins: -4
        radius: 22
        color: root.shadowColor
        antialiasing: true
    }

    Rectangle {
        anchors.fill: parent
        radius: 18
        border.color: root.outlineColor
        border.width: 1
        color: "transparent"
        clip: true
        antialiasing: true

        Rectangle {
            anchors.fill: parent
            radius: parent.radius
            gradient: Gradient {
                orientation: Gradient.Horizontal
                GradientStop { position: 0.0; color: root.shadowColor }
                GradientStop { position: 0.34; color: root.fillColor }
                GradientStop { position: 1.0; color: root.fillColor }
            }
            antialiasing: true
        }

        Rectangle {
            anchors.fill: parent
            radius: parent.radius
            color: root.glassColor
            antialiasing: true
        }

        Rectangle {
            anchors.fill: parent
            radius: parent.radius
            color: "transparent"
            border.color: root.outlineColor
            border.width: 1
            antialiasing: true
        }

        Rectangle {
            anchors.fill: parent
            anchors.margins: 3
            radius: parent.radius - 3
            color: "transparent"
            border.color: root.innerOutlineColor
            border.width: 1
            antialiasing: true
        }

        Rectangle {
            anchors.left: parent.left
            anchors.right: parent.right
            anchors.top: parent.top
            anchors.margins: 6
            height: root.expanded ? Math.min(parent.height * 0.3, 92) : parent.height * 0.42
            radius: parent.radius - 6
            color: "#ffffff"
            opacity: root.expanded ? 0.05 : 0.035
            antialiasing: true
        }

        Column {
            anchors.fill: parent
            anchors.margins: root.contentMargin
            spacing: 0

            Item {
                id: headerArea

                width: parent.width
                height: root.headerHeight

                RowLayout {
                    anchors.fill: parent
                    spacing: 12

                    Text {
                        text: root.title
                        color: root.titleColor
                        font.family: root.titleFontFamily
                        font.pixelSize: 17
                        font.letterSpacing: 0.1
                        font.kerning: false
                        renderType: Text.NativeRendering
                        verticalAlignment: Text.AlignVCenter
                        Layout.alignment: Qt.AlignVCenter
                    }

                    Item {
                        Layout.fillWidth: true
                    }

                    Column {
                        spacing: 0
                        Layout.alignment: Qt.AlignVCenter

                        Text {
                            anchors.right: parent.right
                            text: root.value
                            color: root.valueColor
                            font.family: root.monoFontFamily
                            font.pixelSize: 12
                            font.bold: true
                            font.kerning: false
                            renderType: Text.NativeRendering
                            elide: Text.ElideRight
                            width: 128
                            horizontalAlignment: Text.AlignRight
                        }

                        Text {
                            visible: root.detail !== ""
                            anchors.right: parent.right
                            text: root.detail
                            color: root.detailColor
                            horizontalAlignment: Text.AlignRight
                            font.family: root.monoFontFamily
                            font.pixelSize: 9
                            font.bold: true
                            lineHeight: 1.0
                            font.kerning: false
                            renderType: Text.NativeRendering
                            width: 128
                            wrapMode: Text.NoWrap
                            elide: Text.ElideRight
                        }
                    }

                    Text {
                        text: root.expanded ? "\u2303" : "\u2304"
                        color: root.chevronColor
                        font.family: root.symbolFontFamily
                        font.pixelSize: 14
                        font.bold: true
                        Layout.leftMargin: 6
                        Layout.alignment: Qt.AlignVCenter
                    }
                }

                MouseArea {
                    anchors.fill: parent
                    cursorShape: Qt.PointingHandCursor
                    onClicked: root.toggled()
                }
            }

            Item {
                id: bodyClip

                width: parent.width
                height: root.expanded
                    ? (root.expandToFill ? Math.max(0, root.height - root.collapsedHeight) : bodyColumn.implicitHeight)
                    : 0
                clip: true

                Behavior on height {
                    NumberAnimation {
                        duration: 140
                        easing.type: Easing.OutQuad
                    }
                }

                Column {
                    id: bodyColumn

                    width: bodyClip.width
                    spacing: 8
                    opacity: root.expanded ? 1 : 0

                    Behavior on opacity {
                        NumberAnimation {
                            duration: 90
                        }
                    }
                }
            }
        }
    }
}

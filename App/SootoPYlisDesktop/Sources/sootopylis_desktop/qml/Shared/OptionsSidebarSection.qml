import QtQuick
import QtQuick.Layouts
import "ThemePalette.js" as ThemePalette

Item {
    id: root

    property var theme: null
    property string monoFontFamily: "Consolas"
    property string titleFontFamily: monoFontFamily
    property string sectionHeadingFontFamily: monoFontFamily
    property string textFontFamily: Qt.application.font.family
    property string title: "OPTIONS"
    property string value: ""
    property bool expanded: false
    property bool expandToFill: false
    property int collapsedHeight: 72
    readonly property int contentMargin: 16
    readonly property int headerHeight: Math.max(32, root.collapsedHeight - (root.contentMargin * 2))
    property string selectedFieldFilter: "TINTED"
    property string selectedShellStyle: "CLASSIC"
    property string selectedAppearance: "DARK"
    property bool hdrEffectsEnabled: true
    property string selectedTextSpeed: "FAST"
    readonly property color shadowColor: root.theme ? root.theme.cardCastColor : "#050607"
    readonly property color outlineColor: root.theme ? (root.expanded ? ThemePalette.mix(root.theme.menuIdleStroke, root.theme.menuFocusStroke, 0.35) : root.theme.menuIdleStroke) : "#5f6e67"
    readonly property color innerOutlineColor: root.theme ? root.theme.cardInnerOutline : "#26302c"
    readonly property color fillColor: root.theme ? (root.expanded ? ThemePalette.mix(root.theme.menuIdleFill, root.theme.menuFocusFill, 0.30) : root.theme.menuIdleFill) : "#2d3834"
    readonly property color glassColor: root.theme ? (root.expanded ? ThemePalette.mix(root.theme.menuIdleGlass, root.theme.menuFocusGlass, 0.28) : root.theme.menuIdleGlass) : "#ffffff"
    readonly property color titleColor: root.theme ? root.theme.primaryText : "#d7e2da"
    readonly property color valueColor: root.theme ? root.theme.primaryText : "#dbe5df"
    signal toggled()
    signal fieldFilterSelected(string filterValue)
    signal shellStyleSelected(string styleValue)
    signal appearanceToggled()
    signal hdrEffectsToggled()
    signal textSpeedCycled()

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

                    Text {
                        text: root.value
                        color: root.valueColor
                        font.family: root.monoFontFamily
                        font.pixelSize: 12
                        font.bold: true
                        font.kerning: false
                        renderType: Text.NativeRendering
                        Layout.alignment: Qt.AlignVCenter
                    }

                    Text {
                        text: root.expanded ? "\u2303" : "\u2304"
                        color: root.theme ? root.theme.secondaryText : "#b7c2bc"
                        font.family: "Segoe UI Symbol"
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
                    spacing: 5
                    opacity: root.expanded ? 1 : 0

                    Behavior on opacity {
                        NumberAnimation {
                            duration: 90
                        }
                    }

                    Column {
                        width: parent.width
                        spacing: 4

                        Text {
                            text: "FIELD FILTER"
                            color: root.theme ? root.theme.primaryText : "#e3ece7"
                            font.family: root.sectionHeadingFontFamily
                            font.pixelSize: 14
                            font.letterSpacing: 0.1
                            font.kerning: false
                            renderType: Text.NativeRendering
                        }

                        Row {
                            spacing: 6

                            OptionChip {
                                theme: root.theme
                                monoFontFamily: root.monoFontFamily
                                label: "TINTED"
                                filterValue: "TINTED"
                                selected: root.selectedFieldFilter === "TINTED"
                                onActivated: root.fieldFilterSelected(filterValue)
                            }
                            OptionChip {
                                theme: root.theme
                                monoFontFamily: root.monoFontFamily
                                label: "GBA"
                                filterValue: "GBA"
                                selected: root.selectedFieldFilter === "GBA"
                                onActivated: root.fieldFilterSelected(filterValue)
                            }
                            OptionChip {
                                theme: root.theme
                                monoFontFamily: root.monoFontFamily
                                label: "MONO"
                                filterValue: "MONO"
                                selected: root.selectedFieldFilter === "MONO"
                                onActivated: root.fieldFilterSelected(filterValue)
                            }
                        }
                    }

                    Column {
                        width: parent.width
                        spacing: 4

                        Text {
                            text: "GBA SHELL"
                            color: root.theme ? root.theme.primaryText : "#e3ece7"
                            font.family: root.sectionHeadingFontFamily
                            font.pixelSize: 14
                            font.letterSpacing: 0.1
                            font.kerning: false
                            renderType: Text.NativeRendering
                        }

                        Row {
                            spacing: 2

                            PaletteSwatch {
                                objectName: "classicSwatch"
                                theme: root.theme
                                monoFontFamily: root.monoFontFamily
                                label: "CLASSIC"
                                styleValue: "CLASSIC"
                                swatchColor: root.selectedAppearance === "LIGHT" ? "#f0f0e3" : "#1f2124"
                                selected: root.selectedShellStyle === "CLASSIC"
                                onActivated: root.shellStyleSelected(styleValue)
                            }
                            PaletteSwatch {
                                objectName: "kiwiSwatch"
                                theme: root.theme
                                monoFontFamily: root.monoFontFamily
                                label: "KIWI"
                                styleValue: "KIWI"
                                swatchColor: "#a3d166"
                                selected: root.selectedShellStyle === "KIWI"
                                onActivated: root.shellStyleSelected(styleValue)
                            }
                            PaletteSwatch {
                                objectName: "dandelionSwatch"
                                theme: root.theme
                                monoFontFamily: root.monoFontFamily
                                label: "DANDELION"
                                styleValue: "DANDELION"
                                swatchColor: "#f2d159"
                                selected: root.selectedShellStyle === "DANDELION"
                                onActivated: root.shellStyleSelected(styleValue)
                            }
                            PaletteSwatch {
                                objectName: "tealSwatch"
                                theme: root.theme
                                monoFontFamily: root.monoFontFamily
                                label: "TEAL"
                                styleValue: "TEAL"
                                swatchColor: "#57bdb8"
                                selected: root.selectedShellStyle === "TEAL"
                                onActivated: root.shellStyleSelected(styleValue)
                            }
                            PaletteSwatch {
                                objectName: "grapeSwatch"
                                theme: root.theme
                                monoFontFamily: root.monoFontFamily
                                label: "GRAPE"
                                styleValue: "GRAPE"
                                swatchColor: "#a37bc0"
                                selected: root.selectedShellStyle === "GRAPE"
                                onActivated: root.shellStyleSelected(styleValue)
                            }
                        }
                    }

                    SettingRow {
                        theme: root.theme
                        monoFontFamily: root.monoFontFamily
                        label: "APPEARANCE"
                        value: root.selectedAppearance
                        actionKey: "appearance"
                        onActivated: root.appearanceToggled()
                    }
                    SettingRow {
                        theme: root.theme
                        monoFontFamily: root.monoFontFamily
                        label: "HDR EFFECTS"
                        value: root.hdrEffectsEnabled ? "ON" : "OFF"
                        actionKey: "hdr"
                        onActivated: root.hdrEffectsToggled()
                    }
                    SettingRow {
                        theme: root.theme
                        monoFontFamily: root.monoFontFamily
                        label: "TEXT SPEED"
                        value: root.selectedTextSpeed
                        actionKey: "text_speed"
                        onActivated: root.textSpeedCycled()
                    }
                }
            }
        }
    }
}

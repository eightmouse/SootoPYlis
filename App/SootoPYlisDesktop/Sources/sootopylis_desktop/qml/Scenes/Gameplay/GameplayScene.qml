import QtQuick
import QtQuick.Layouts
import Qt5Compat.GraphicalEffects

import "../../Shared"
import "../../Shared/ThemePalette.js" as ThemePalette

FocusScope {
    id: root
    focus: true

    Component.onCompleted: forceActiveFocus()

    FontLoader {
        id: pokemonEmeraldMenuFont
        source: Qt.resolvedUrl("../../../../../../../pokemon-emerald.otf")
    }

    readonly property var session: desktopSession ? desktopSession : ({
        selectedFieldFilter: "TINTED",
        selectedShellStyle: "CLASSIC",
        selectedAppearance: "DARK",
        hdrEffectsEnabled: true,
        selectedTextSpeed: "FAST",
        gameplayRunning: false,
        gameplayTrainerName: "MAY",
        gameplayLocationName: "LITTLEROOT",
        gameplayAreaSubtitle: "PLAYER ROOM",
        gameplayPlayerSummary: "MAY",
        gameplayClockSummary: "00:00",
        gameplayPokedexSummary: "0 / 202",
        gameplayPartySummary: "1 / 6",
        gameplayBagSummary: "4",
        gameplaySaveSummary: "1 FILE",
        gameplayMapWidth: 15,
        gameplayMapHeight: 10,
        gameplayTileKinds: [],
        gameplayPlayerX: 7,
        gameplayPlayerY: 7,
        gameplayPlayerScreenX: 7,
        gameplayPlayerScreenY: 5,
        gameplayPlayerFacing: "up",
        gameplayMapImageUrl: "",
        gameplayPlayerSpriteUrl: "",
    })
    property string expandedSection: "options"
    property string selectedFieldFilter: session.selectedFieldFilter
    property string selectedShellStyle: session.selectedShellStyle
    property string selectedAppearance: session.selectedAppearance
    property bool hdrEffectsEnabled: session.hdrEffectsEnabled
    property string selectedTextSpeed: session.selectedTextSpeed
    readonly property string monoFontFamily: Qt.platform.os === "windows" ? "Cascadia Mono" : "Monaco"
    readonly property string menuTitleFontFamily: pokemonEmeraldMenuFont.status === FontLoader.Ready ? pokemonEmeraldMenuFont.name : root.monoFontFamily
    readonly property string textFontFamily: Qt.platform.os === "windows" ? "Segoe UI Variable Text" : "SF Pro Text"
    readonly property var theme: ThemePalette.resolve(root.selectedShellStyle, root.selectedAppearance)
    readonly property int gameplayMapWidth: desktopSession ? desktopSession.gameplayMapWidth : session.gameplayMapWidth
    readonly property int gameplayMapHeight: desktopSession ? desktopSession.gameplayMapHeight : session.gameplayMapHeight
    readonly property var gameplayTileKinds: desktopSession ? desktopSession.gameplayTileKinds : session.gameplayTileKinds
    readonly property int gameplayPlayerX: desktopSession ? desktopSession.gameplayPlayerX : session.gameplayPlayerX
    readonly property int gameplayPlayerY: desktopSession ? desktopSession.gameplayPlayerY : session.gameplayPlayerY
    readonly property int gameplayPlayerScreenX: desktopSession ? desktopSession.gameplayPlayerScreenX : session.gameplayPlayerScreenX
    readonly property int gameplayPlayerScreenY: desktopSession ? desktopSession.gameplayPlayerScreenY : session.gameplayPlayerScreenY
    readonly property string gameplayMapImageUrl: desktopSession ? desktopSession.gameplayMapImageUrl : session.gameplayMapImageUrl
    readonly property string gameplayPlayerSpriteUrl: desktopSession ? desktopSession.gameplayPlayerSpriteUrl : session.gameplayPlayerSpriteUrl
    readonly property bool hasGameplayMapImage: gameplayMapImageUrl.length > 0

    readonly property color windowBarColor: theme.windowBar
    readonly property color windowBarBorderColor: theme.windowBarBorder
    readonly property color windowBarTextColor: theme.windowBarText
    readonly property color windowBadgeColor: theme.windowBadge
    readonly property color windowBadgeBorderColor: theme.windowBadgeBorder
    readonly property color windowBadgeTextColor: theme.windowBadgeText
    readonly property color shellShadow: theme.shellShadow

    function toggleSection(name) {
        expandedSection = expandedSection === name ? "" : name
    }

    function setFieldFilter(value) {
        if (["TINTED", "GBA", "MONO"].indexOf(value) === -1 || value === root.selectedFieldFilter) {
            return
        }
        root.selectedFieldFilter = value
    }

    function setShellStyle(value) {
        if (["CLASSIC", "KIWI", "DANDELION", "TEAL", "GRAPE"].indexOf(value) === -1 || value === root.selectedShellStyle) {
            return
        }
        root.selectedShellStyle = value
    }

    function cycleAppearance() {
        root.selectedAppearance = root.selectedAppearance === "DARK" ? "LIGHT" : "DARK"
    }

    function toggleHdrEffects() {
        root.hdrEffectsEnabled = !root.hdrEffectsEnabled
    }

    function cycleTextSpeed() {
        if (root.selectedTextSpeed === "FAST") {
            root.selectedTextSpeed = "MID"
        } else if (root.selectedTextSpeed === "MID") {
            root.selectedTextSpeed = "SLOW"
        } else {
            root.selectedTextSpeed = "FAST"
        }
    }

    function fieldViewportBase() {
        switch (root.selectedFieldFilter) {
        case "MONO": return "#050705"
        case "GBA": return "#060708"
        default: return theme.screenWellFill
        }
    }

    function fieldViewportGlow() {
        switch (root.selectedFieldFilter) {
        case "MONO": return "#a5b793"
        case "GBA": return "#678fd8"
        default: return theme.screenGlow
        }
    }

    function tilePalette(kind) {
        if (root.selectedFieldFilter === "MONO") {
            switch (kind) {
            case "wall": return { fill: "#344233", accent: "#586d55", border: "#233022" }
            case "counter": return { fill: "#4f6050", accent: "#788d77", border: "#2b382b" }
            case "grass": return { fill: "#5b7151", accent: "#8ca67f", border: "#385034" }
            case "path": return { fill: "#8f9077", accent: "#bcbea2", border: "#65664f" }
            case "tree": return { fill: "#445640", accent: "#70856c", border: "#2a3528" }
            case "house": return { fill: "#757c6d", accent: "#b8c1b0", border: "#565c4f" }
            case "carpet": return { fill: "#9ca691", accent: "#b9c3af", border: "#6f7866" }
            case "door": return { fill: "#2c302b", accent: "#596254", border: "#181b18" }
            case "stairs": return { fill: "#586256", accent: "#93a08f", border: "#394038" }
            case "window": return { fill: "#7f8b84", accent: "#c0cac4", border: "#56605b" }
            case "plant": return { fill: "#637058", accent: "#8f9c84", border: "#3b4634" }
            case "npc": return { fill: "#8e9781", accent: "#c8d0bc", border: "#616856" }
            case "mat": return { fill: "#80876a", accent: "#b3b997", border: "#555a46" }
            default: return { fill: "#69745f", accent: "#9fab91", border: "#485243" }
            }
        }

        if (root.selectedFieldFilter === "GBA") {
            switch (kind) {
            case "wall": return { fill: "#7f8f9f", accent: "#c3d3e3", border: "#50606f" }
            case "counter": return { fill: "#94b4d2", accent: "#d7e5f1", border: "#6988a6" }
            case "grass": return { fill: "#5ead63", accent: "#a4dd8f", border: "#3f7d43" }
            case "path": return { fill: "#c2a57d", accent: "#e6cc9f", border: "#8f7350" }
            case "tree": return { fill: "#4e7d3f", accent: "#87be65", border: "#34562c" }
            case "house": return { fill: "#b58f6d", accent: "#e5c29c", border: "#7e6148" }
            case "carpet": return { fill: "#d4dca2", accent: "#eef0c3", border: "#aab270" }
            case "door": return { fill: "#5b6374", accent: "#8390a6", border: "#37404e" }
            case "stairs": return { fill: "#7d8678", accent: "#cfd8c8", border: "#596254" }
            case "window": return { fill: "#8fd0eb", accent: "#d8f4ff", border: "#5ea1bf" }
            case "plant": return { fill: "#68a25f", accent: "#9dd28c", border: "#457243" }
            case "npc": return { fill: "#f2a36a", accent: "#ffd0a7", border: "#b66f3c" }
            case "mat": return { fill: "#ad6d6d", accent: "#d79f9f", border: "#7b4949" }
            default: return { fill: "#b7c78a", accent: "#dee9b5", border: "#7f8f5f" }
            }
        }

        switch (kind) {
        case "wall": return { fill: "#6f8f2b", accent: "#b0d050", border: "#4a6118" }
        case "counter": return { fill: "#84a835", accent: "#c4e55f", border: "#5a7421" }
        case "grass": return { fill: "#78a030", accent: "#a7d157", border: "#537020" }
        case "path": return { fill: "#9ba247", accent: "#d1d668", border: "#676c2f" }
        case "tree": return { fill: "#547d22", accent: "#83b13d", border: "#355117" }
        case "house": return { fill: "#8e8c3c", accent: "#c6c35f", border: "#62602a" }
        case "carpet": return { fill: "#b9cb45", accent: "#e4ef70", border: "#85962d" }
        case "door": return { fill: "#31410f", accent: "#667f2f", border: "#1c2708" }
        case "stairs": return { fill: "#6f8429", accent: "#b9d25c", border: "#445617" }
        case "window": return { fill: "#8fc150", accent: "#d7f293", border: "#5d842f" }
        case "plant": return { fill: "#4f7b24", accent: "#88b84b", border: "#355218" }
        case "npc": return { fill: "#a6bb3b", accent: "#e0f36d", border: "#72812c" }
        case "mat": return { fill: "#7e9230", accent: "#b6cb52", border: "#55631f" }
        default: return { fill: "#9ab43d", accent: "#d7ee68", border: "#6d8028" }
        }
    }

    Rectangle {
        anchors.fill: parent
        gradient: Gradient {
            GradientStop { position: 0.0; color: theme.appBackgroundTop }
            GradientStop { position: 0.42; color: theme.appBackgroundMiddle }
            GradientStop { position: 1.0; color: theme.appBackgroundBottom }
        }
    }

    RowLayout {
        anchors.fill: parent
        anchors.margins: 28
        spacing: 26

        Item {
            Layout.fillWidth: true
            Layout.fillHeight: true
            Layout.minimumWidth: 820
            Layout.preferredWidth: 980

            Rectangle {
                anchors.fill: parent
                anchors.margins: -10
                radius: 48
                color: shellShadow
                opacity: 0.52
                antialiasing: true
            }

            Rectangle {
                anchors.fill: parent
                radius: 40
                border.color: theme.shellBorder
                border.width: 1
                gradient: Gradient {
                    GradientStop { position: 0.0; color: ThemePalette.mix(theme.shellBackdrop, Qt.rgba(1, 1, 1, 1), root.selectedShellStyle === "CLASSIC" && root.selectedAppearance === "LIGHT" ? 0.03 : 0.10) }
                    GradientStop { position: 0.34; color: theme.shellBackdrop }
                    GradientStop { position: 1.0; color: ThemePalette.mix(theme.shellBackdrop, theme.shellShadow, root.selectedShellStyle === "CLASSIC" && root.selectedAppearance === "LIGHT" ? 0.08 : 0.22) }
                }
                antialiasing: true

                Rectangle {
                    anchors.fill: parent
                    radius: parent.radius
                    color: "transparent"
                    border.color: theme.shellInnerBorder
                    border.width: 1
                    antialiasing: true
                }

                Rectangle {
                    anchors.left: parent.left
                    anchors.right: parent.right
                    anchors.top: parent.top
                    anchors.margins: 10
                    height: parent.height * 0.42
                    radius: parent.radius - 10
                    color: "#ffffff"
                    opacity: root.selectedAppearance === "LIGHT" ? 0.055 : 0.036
                    antialiasing: true
                }

                Rectangle {
                    anchors.fill: parent
                    anchors.margins: 8
                    radius: 34
                    color: "transparent"
                    border.color: ThemePalette.mix(theme.shellBorder, theme.shellShadow, 0.36)
                    border.width: 1
                    antialiasing: true
                }

                Column {
                    anchors.fill: parent
                    anchors.margins: 34
                    spacing: 24

                    Rectangle {
                        width: parent.width
                        height: parent.height - 104
                        radius: 34
                        border.color: ThemePalette.mix(theme.screenWellDepth, theme.panelOutline, 0.32)
                        border.width: 1
                        gradient: Gradient {
                            GradientStop { position: 0.0; color: ThemePalette.mix(theme.screenWellFill, theme.screenWellHighlight, 0.12) }
                            GradientStop { position: 0.7; color: theme.screenWellFill }
                            GradientStop { position: 1.0; color: ThemePalette.mix(theme.screenWellFill, theme.screenWellDepth, 0.38) }
                        }
                        antialiasing: true

                        Column {
                            anchors.fill: parent
                            anchors.margins: 26
                            spacing: 0

                            Item {
                                id: screenStage
                                width: parent.width
                                height: parent.height

                                Rectangle {
                                    id: screenViewport
                                    readonly property int nativeWidth: 240
                                    readonly property int nativeHeight: 160
                                    readonly property int fitWidth: Math.round(screenStage.width * 0.93)
                                    readonly property int fitHeight: Math.round(screenStage.height * 0.89)
                                    readonly property int integerScale: Math.max(1, Math.floor(Math.min(fitWidth / nativeWidth, fitHeight / nativeHeight)))
                                    readonly property int targetWidth: nativeWidth * integerScale
                                    readonly property int targetHeight: nativeHeight * integerScale
                                    width: targetWidth
                                    height: targetHeight
                                    x: Math.round((screenStage.width - width) / 2)
                                    y: Math.round((screenStage.height - height) / 2)
                                    radius: 16
                                    clip: true
                                    gradient: Gradient {
                                        GradientStop { position: 0.0; color: session.gameplayRunning ? ThemePalette.mix(root.tilePalette("floor").accent, root.tilePalette("floor").fill, 0.35) : fieldViewportBase() }
                                        GradientStop { position: 1.0; color: session.gameplayRunning ? ThemePalette.mix(root.tilePalette("floor").fill, theme.screenWellDepth, 0.22) : "#010203" }
                                    }
                                    border.color: session.gameplayRunning ? theme.screenRim : ThemePalette.mix(theme.screenWellDepth, theme.screenRim, 0.28)
                                    border.width: 1
                                    antialiasing: true

                                    Rectangle {
                                        anchors.fill: parent
                                        anchors.margins: -12
                                        radius: parent.radius + 12
                                        color: "transparent"
                                        border.color: session.gameplayRunning ? "#3eb93d" : fieldViewportGlow()
                                        border.width: session.gameplayRunning ? 6 : 2
                                        opacity: session.gameplayRunning ? 0.32 : theme.screenGlow.a
                                        antialiasing: true
                                    }

                                    Rectangle {
                                        anchors.fill: parent
                                        radius: parent.radius
                                        color: "transparent"
                                        border.color: theme.screenGlowInner
                                        border.width: theme.screenGlowInner.a > 0 ? 1 : 0
                                        antialiasing: true
                                    }

                                    Rectangle {
                                        id: fieldMaskShape
                                        anchors.fill: parent
                                        radius: Math.max(8, screenViewport.radius - 2)
                                        visible: false
                                    }

                                    Item {
                                        id: fieldSurface
                                        anchors.fill: parent
                                        layer.enabled: true
                                        layer.smooth: true
                                        layer.effect: OpacityMask {
                                            maskSource: fieldMaskShape
                                        }

                                        Rectangle {
                                            anchors.fill: parent
                                            radius: fieldMaskShape.radius
                                            color: ThemePalette.mix(root.tilePalette("floor").fill, theme.screenWellFill, 0.06)
                                            antialiasing: true
                                        }

                                        Image {
                                            id: gameplayFrame
                                            anchors.fill: parent
                                            visible: root.hasGameplayMapImage
                                            source: root.gameplayMapImageUrl
                                            fillMode: Image.Stretch
                                            smooth: false
                                            mipmap: false
                                            cache: false
                                        }

                                        Item {
                                            id: fieldLayer
                                            anchors.fill: parent
                                            clip: true
                                            visible: !root.hasGameplayMapImage

                                            readonly property int mapWidth: root.gameplayMapWidth || 15
                                            readonly property int mapHeight: root.gameplayMapHeight || 10
                                            readonly property var tileKinds: root.gameplayTileKinds || []
                                            readonly property real tileWidth: width / mapWidth
                                            readonly property real tileHeight: height / mapHeight

                                            Repeater {
                                                model: fieldLayer.mapWidth * fieldLayer.mapHeight

                                                delegate: Rectangle {
                                                    readonly property int tileX: index % fieldLayer.mapWidth
                                                    readonly property int tileY: Math.floor(index / fieldLayer.mapWidth)
                                                    readonly property string tileKind: index < fieldLayer.tileKinds.length ? fieldLayer.tileKinds[index] : "floor"
                                                    property var colors: root.tilePalette(tileKind)

                                                    x: tileX * fieldLayer.tileWidth
                                                    y: tileY * fieldLayer.tileHeight
                                                    width: fieldLayer.tileWidth
                                                    height: fieldLayer.tileHeight
                                                    color: colors.fill
                                                    border.color: colors.border
                                                    border.width: 1
                                                    antialiasing: false

                                                    Rectangle {
                                                        anchors.left: parent.left
                                                        anchors.right: parent.right
                                                        anchors.top: parent.top
                                                        height: Math.max(2, parent.height * 0.26)
                                                        color: colors.accent
                                                    }

                                                    Rectangle {
                                                        visible: tileKind === "door"
                                                        anchors.horizontalCenter: parent.horizontalCenter
                                                        anchors.bottom: parent.bottom
                                                        width: parent.width * 0.42
                                                        height: parent.height * 0.36
                                                        color: ThemePalette.mix(colors.fill, colors.border, 0.45)
                                                    }
                                                }
                                            }

                                            MouseArea {
                                                anchors.fill: parent
                                                acceptedButtons: Qt.LeftButton
                                                onPressed: root.forceActiveFocus()
                                                z: 10
                                            }
                                        }

                                        Item {
                                            id: playerMarker
                                            visible: !root.hasGameplayMapImage
                                            readonly property real visibleTileWidth: fieldSurface.width / (root.hasGameplayMapImage ? 15 : Math.max(1, root.gameplayMapWidth || 15))
                                            readonly property real visibleTileHeight: fieldSurface.height / (root.hasGameplayMapImage ? 10 : Math.max(1, root.gameplayMapHeight || 10))
                                            readonly property real tileX: root.hasGameplayMapImage ? root.gameplayPlayerScreenX : root.gameplayPlayerX
                                            readonly property real tileY: root.hasGameplayMapImage ? root.gameplayPlayerScreenY : root.gameplayPlayerY
                                            x: Math.round((tileX * visibleTileWidth) + ((visibleTileWidth - width) / 2))
                                            y: Math.round(((tileY + 1) * visibleTileHeight) - height)
                                            width: visibleTileWidth
                                            height: visibleTileHeight * 2
                                            z: 20

                                            Behavior on x {
                                                NumberAnimation { duration: 90; easing.type: Easing.OutQuad }
                                            }

                                            Behavior on y {
                                                NumberAnimation { duration: 90; easing.type: Easing.OutQuad }
                                            }

                                            Rectangle {
                                                anchors.horizontalCenter: parent.horizontalCenter
                                                anchors.bottom: parent.bottom
                                                anchors.bottomMargin: Math.max(2, parent.visibleTileHeight * 0.08)
                                                width: parent.visibleTileWidth * 0.66
                                                height: Math.max(4, parent.visibleTileHeight * 0.22)
                                                radius: height / 2
                                                color: "#000000"
                                                opacity: 0.22
                                            }

                                            Image {
                                                anchors.fill: parent
                                                anchors.bottomMargin: Math.max(2, playerMarker.visibleTileHeight * 0.06)
                                                source: root.gameplayPlayerSpriteUrl
                                                fillMode: Image.Stretch
                                                smooth: false
                                                mipmap: false
                                                cache: false
                                                visible: source.length > 0
                                            }

                                            Rectangle {
                                                anchors.horizontalCenter: parent.horizontalCenter
                                                anchors.bottom: parent.bottom
                                                width: parent.visibleTileWidth * 0.54
                                                height: parent.visibleTileHeight * 0.64
                                                radius: 3
                                                visible: !root.gameplayPlayerSpriteUrl.length
                                                color: root.selectedFieldFilter === "GBA" ? "#2e4e86" : "#203410"
                                                border.color: root.selectedFieldFilter === "GBA" ? "#8bb2f1" : "#d8ef76"
                                                border.width: 1

                                                Rectangle {
                                                    anchors.horizontalCenter: parent.horizontalCenter
                                                    anchors.top: parent.top
                                                    width: parent.width * 0.76
                                                    height: parent.height * 0.34
                                                    radius: 2
                                                    color: root.selectedFieldFilter === "GBA" ? "#d46352" : "#7f9831"
                                                }
                                            }
                                        }
                                    }
                                }

                                Item {
                                    id: batteryCluster
                                    x: 0
                                    y: screenViewport.y
                                    width: screenViewport.x
                                    height: screenViewport.height
                                    readonly property int powerCenterX: Math.round(width * 0.30)

                                    Item {
                                        id: powerDot
                                        width: 26
                                        height: 26
                                        x: Math.round(batteryCluster.powerCenterX - (width / 2))
                                        anchors.verticalCenter: parent.verticalCenter

                                        Rectangle {
                                            anchors.centerIn: parent
                                            width: 26
                                            height: 26
                                            radius: 13
                                            color: theme.batteryIndicator
                                            opacity: 0.03
                                            antialiasing: true
                                        }

                                        Rectangle {
                                            anchors.centerIn: parent
                                            width: 16
                                            height: 16
                                            radius: 8
                                            color: theme.batteryIndicator
                                            opacity: 0.11
                                            antialiasing: true
                                        }

                                        Rectangle {
                                            anchors.centerIn: parent
                                            width: 10
                                            height: 10
                                            radius: 5
                                            color: theme.batteryIndicator
                                            antialiasing: true
                                        }
                                    }

                                    Text {
                                        width: 56
                                        x: Math.round(batteryCluster.powerCenterX - (width / 2))
                                        anchors.top: powerDot.bottom
                                        anchors.topMargin: 6
                                        text: "POWER"
                                        color: theme.screenLabel
                                        font.family: root.monoFontFamily
                                        font.pixelSize: 10
                                        font.bold: true
                                        font.kerning: false
                                        renderType: Text.NativeRendering
                                        horizontalAlignment: Text.AlignHCenter
                                    }
                                }
                            }
                        }
                    }

                    RowLayout {
                        spacing: 12

                        Rectangle {
                            radius: 999
                            color: ThemePalette.overlay(theme.panelGlassTint, root.selectedAppearance === "LIGHT" ? 0.10 : 0.14)
                            border.color: ThemePalette.overlay(ThemePalette.mix(theme.primaryText, theme.shellShadow, root.selectedAppearance === "LIGHT" ? 0.55 : 0.32), root.selectedAppearance === "LIGHT" ? 0.30 : 0.52)
                            border.width: 1
                            implicitWidth: nintendoText.implicitWidth + 20
                            implicitHeight: 30
                            antialiasing: true

                            Text {
                                id: nintendoText
                                anchors.centerIn: parent
                                text: "Nintendo"
                                color: theme.primaryText
                                font.family: root.textFontFamily
                                font.pixelSize: 15
                                font.bold: true
                                renderType: Text.NativeRendering
                            }
                        }

                        Row {
                            spacing: 8
                            anchors.verticalCenter: parent.verticalCenter

                            Text {
                                text: "GAME BOY"
                                color: theme.gameBoyWordmark
                                font.family: Qt.platform.os === "windows" ? "Bahnschrift" : root.textFontFamily
                                font.pixelSize: 31
                                font.weight: Font.Light
                                font.letterSpacing: 0.9
                                renderType: Text.NativeRendering
                            }

                            Text {
                                anchors.verticalCenter: parent.verticalCenter
                                anchors.verticalCenterOffset: 2
                                text: "ADVANCE"
                                color: ThemePalette.mix(theme.gameBoyWordmark, theme.primaryText, 0.18)
                                font.family: Qt.platform.os === "windows" ? "Bahnschrift" : root.textFontFamily
                                font.pixelSize: 18
                                font.weight: Font.Normal
                                font.letterSpacing: 1.8
                                renderType: Text.NativeRendering
                            }
                        }
                    }
                }
            }
        }

        ColumnLayout {
            Layout.preferredWidth: 334
            Layout.minimumWidth: 334
            Layout.maximumWidth: 334
            Layout.fillHeight: true
            spacing: 12

            SidebarSection {
                theme: root.theme
                monoFontFamily: root.monoFontFamily
                titleFontFamily: root.menuTitleFontFamily
                title: "TRAINER"
                value: session.gameplayLocationName
                detail: session.gameplayAreaSubtitle
                expanded: root.expandedSection === "trainer"
                expandToFill: expanded
                Layout.fillHeight: expanded
                Layout.maximumHeight: expanded ? 16777215 : implicitHeight
                onToggled: root.toggleSection("trainer")

                StatRow { theme: root.theme; monoFontFamily: root.monoFontFamily; label: "PLAYER"; value: session.gameplayPlayerSummary }
                StatRow { theme: root.theme; monoFontFamily: root.monoFontFamily; label: "BADGES"; value: "0 / 8" }
                StatRow { theme: root.theme; monoFontFamily: root.monoFontFamily; label: "PLAY TIME"; value: session.gameplayClockSummary.replace("PLAY TIME ", "") }
            }

            SidebarSection {
                theme: root.theme
                monoFontFamily: root.monoFontFamily
                titleFontFamily: root.menuTitleFontFamily
                title: "POKEDEX"
                value: session.gameplayPokedexSummary
                expanded: root.expandedSection === "pokedex"
                expandToFill: expanded
                Layout.fillHeight: expanded
                Layout.maximumHeight: expanded ? 16777215 : implicitHeight
                onToggled: root.toggleSection("pokedex")

                StatRow { theme: root.theme; monoFontFamily: root.monoFontFamily; label: "REGIONAL"; value: session.gameplayPokedexSummary }
                StatRow { theme: root.theme; monoFontFamily: root.monoFontFamily; label: "NATIONAL"; value: "LOCKED" }
                StatRow { theme: root.theme; monoFontFamily: root.monoFontFamily; label: "SEEN"; value: "0" }
            }

            SidebarSection {
                theme: root.theme
                monoFontFamily: root.monoFontFamily
                titleFontFamily: root.menuTitleFontFamily
                title: "PARTY"
                value: session.gameplayPartySummary
                expanded: root.expandedSection === "party"
                expandToFill: expanded
                Layout.fillHeight: expanded
                Layout.maximumHeight: expanded ? 16777215 : implicitHeight
                onToggled: root.toggleSection("party")

                StatRow { theme: root.theme; monoFontFamily: root.monoFontFamily; label: "TREECKO"; value: "Lv 5" }
                StatRow { theme: root.theme; monoFontFamily: root.monoFontFamily; label: "EMPTY"; value: "--"; labelColor: root.theme.tertiaryText }
                StatRow { theme: root.theme; monoFontFamily: root.monoFontFamily; label: "EMPTY"; value: "--"; labelColor: root.theme.tertiaryText }
                StatRow { theme: root.theme; monoFontFamily: root.monoFontFamily; label: "EMPTY"; value: "--"; labelColor: root.theme.tertiaryText }
            }

            SidebarSection {
                theme: root.theme
                monoFontFamily: root.monoFontFamily
                titleFontFamily: root.menuTitleFontFamily
                title: "BAG"
                value: session.gameplayBagSummary
                expanded: root.expandedSection === "bag"
                expandToFill: expanded
                Layout.fillHeight: expanded
                Layout.maximumHeight: expanded ? 16777215 : implicitHeight
                onToggled: root.toggleSection("bag")

                StatRow { theme: root.theme; monoFontFamily: root.monoFontFamily; label: "ITEMS"; value: "4" }
                StatRow { theme: root.theme; monoFontFamily: root.monoFontFamily; label: "BALLS"; value: "2" }
                StatRow { theme: root.theme; monoFontFamily: root.monoFontFamily; label: "KEY ITEMS"; value: "1" }
            }

            SidebarSection {
                theme: root.theme
                monoFontFamily: root.monoFontFamily
                titleFontFamily: root.menuTitleFontFamily
                title: "SAVE"
                value: session.gameplaySaveSummary
                expanded: root.expandedSection === "save"
                expandToFill: expanded
                Layout.fillHeight: expanded
                Layout.maximumHeight: expanded ? 16777215 : implicitHeight
                onToggled: root.toggleSection("save")

                StatRow { theme: root.theme; monoFontFamily: root.monoFontFamily; label: "STATUS"; value: "READY" }
                StatRow { theme: root.theme; monoFontFamily: root.monoFontFamily; label: "PLAY TIME"; value: session.gameplayClockSummary.replace("PLAY TIME ", "") }
                StatRow { theme: root.theme; monoFontFamily: root.monoFontFamily; label: "ROM"; value: "EMERALD" }
            }

            OptionsSidebarSection {
                id: optionsSection
                objectName: "optionsSection"
                theme: root.theme
                monoFontFamily: root.monoFontFamily
                titleFontFamily: root.menuTitleFontFamily
                sectionHeadingFontFamily: root.menuTitleFontFamily
                textFontFamily: root.textFontFamily
                title: "OPTIONS"
                value: root.selectedFieldFilter
                expanded: root.expandedSection === "options"
                expandToFill: expanded
                Layout.fillHeight: expanded
                Layout.maximumHeight: expanded ? 16777215 : implicitHeight
                selectedFieldFilter: root.selectedFieldFilter
                selectedShellStyle: root.selectedShellStyle
                selectedAppearance: root.selectedAppearance
                hdrEffectsEnabled: root.hdrEffectsEnabled
                selectedTextSpeed: root.selectedTextSpeed
                onToggled: root.toggleSection("options")
                onFieldFilterSelected: root.setFieldFilter(filterValue)
                onShellStyleSelected: root.setShellStyle(styleValue)
                onAppearanceToggled: root.cycleAppearance()
                onHdrEffectsToggled: root.toggleHdrEffects()
                onTextSpeedCycled: root.cycleTextSpeed()
            }

            Item {
                Layout.fillHeight: true
            }
        }
    }
}

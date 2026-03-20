.pragma library

function rgba(red, green, blue, alpha) {
    return Qt.rgba(red, green, blue, alpha === undefined ? 1.0 : alpha)
}

function mix(base, tint, amount) {
    return Qt.rgba(
        base.r * (1 - amount) + tint.r * amount,
        base.g * (1 - amount) + tint.g * amount,
        base.b * (1 - amount) + tint.b * amount,
        base.a * (1 - amount) + tint.a * amount
    )
}

function overlay(color, alpha) {
    return Qt.rgba(color.r, color.g, color.b, alpha)
}

function lightPalette() {
    return {
        primaryText: rgba(0.10, 0.11, 0.10, 1.0),
        secondaryText: rgba(0.10, 0.11, 0.10, 0.72),
        tertiaryText: rgba(0.10, 0.11, 0.10, 0.52),
        panelBackground: rgba(1.0, 1.0, 1.0, 0.18),
        panelGlassTint: rgba(0.82, 0.91, 0.78, 0.38),
        panelOutline: rgba(0.0, 0.0, 0.0, 0.08),
        menuFocusFill: rgba(0.80, 0.90, 0.73, 0.30),
        menuIdleFill: rgba(1.0, 1.0, 1.0, 0.12),
        menuFocusGlass: rgba(0.77, 0.89, 0.72, 0.45),
        menuIdleGlass: rgba(1.0, 1.0, 1.0, 0.18),
        menuFocusStroke: rgba(0.0, 0.0, 0.0, 0.14),
        menuIdleStroke: rgba(0.0, 0.0, 0.0, 0.07),
        appBackgroundTop: rgba(0.95, 0.96, 0.90, 1.0),
        appBackgroundMiddle: rgba(0.84, 0.88, 0.76, 1.0),
        appBackgroundBottom: rgba(0.73, 0.79, 0.64, 1.0),
        appHighlightGlow: rgba(1.0, 1.0, 1.0, 0.42),
        appAccentGlow: rgba(0.73, 0.84, 0.74, 0.22),
        appDepthShadow: rgba(0.34, 0.39, 0.26, 0.06),
        gameBoyWordmark: rgba(0.17, 0.22, 0.68, 1.0),
        screenWellFill: rgba(0.36, 0.37, 0.43, 1.0),
        screenWellHighlight: rgba(1.0, 1.0, 1.0, 0.08),
        screenWellDepth: rgba(0.0, 0.0, 0.0, 0.12),
        screenLabel: rgba(1.0, 1.0, 1.0, 0.78),
        batteryIndicator: rgba(0.27, 0.78, 0.33, 1.0),
        screenRim: rgba(0.18, 0.28, 0.08, 1.0),
        screenGlow: rgba(0.48, 0.76, 0.45, 0.0),
        screenGlowInner: rgba(0.88, 0.97, 0.8, 0.0),
        accentBarMagenta: rgba(0.42, 0.07, 0.27, 1.0),
        accentBarBlue: rgba(0.16, 0.17, 0.55, 1.0),
        shellBackdrop: rgba(0.94, 0.94, 0.89, 1.0),
        shellBackdropShadow: rgba(0.33, 0.39, 0.26, 1.0)
    }
}

function darkPalette() {
    return {
        primaryText: rgba(0.90, 0.96, 0.89, 1.0),
        secondaryText: rgba(0.86, 0.94, 0.87, 0.76),
        tertiaryText: rgba(0.82, 0.90, 0.82, 0.54),
        panelBackground: rgba(0.15, 0.19, 0.17, 0.74),
        panelGlassTint: rgba(0.27, 0.39, 0.30, 0.32),
        panelOutline: rgba(0.64, 0.76, 0.67, 0.14),
        menuFocusFill: rgba(0.34, 0.53, 0.37, 0.42),
        menuIdleFill: rgba(0.16, 0.22, 0.18, 0.54),
        menuFocusGlass: rgba(0.48, 0.78, 0.54, 0.34),
        menuIdleGlass: rgba(0.23, 0.33, 0.25, 0.26),
        menuFocusStroke: rgba(0.64, 0.95, 0.68, 0.24),
        menuIdleStroke: rgba(0.58, 0.78, 0.61, 0.12),
        appBackgroundTop: rgba(0.08, 0.10, 0.09, 1.0),
        appBackgroundMiddle: rgba(0.11, 0.15, 0.12, 1.0),
        appBackgroundBottom: rgba(0.16, 0.22, 0.17, 1.0),
        appHighlightGlow: rgba(0.62, 0.92, 0.71, 0.08),
        appAccentGlow: rgba(0.31, 0.61, 0.39, 0.18),
        appDepthShadow: rgba(0.0, 0.0, 0.0, 0.28),
        gameBoyWordmark: rgba(0.70, 0.85, 0.78, 1.0),
        screenWellFill: rgba(0.02, 0.03, 0.02, 1.0),
        screenWellHighlight: rgba(0.52, 0.98, 0.58, 0.14),
        screenWellDepth: rgba(0.0, 0.0, 0.0, 0.52),
        screenLabel: rgba(0.87, 0.95, 0.87, 0.72),
        batteryIndicator: rgba(0.29, 0.88, 0.36, 1.0),
        screenRim: rgba(0.34, 0.86, 0.35, 1.0),
        screenGlow: rgba(0.41, 0.84, 0.48, 0.28),
        screenGlowInner: rgba(0.84, 1.0, 0.84, 0.12),
        accentBarMagenta: rgba(0.61, 0.24, 0.48, 1.0),
        accentBarBlue: rgba(0.38, 0.51, 0.86, 1.0),
        shellBackdrop: rgba(0.12, 0.13, 0.14, 1.0),
        shellBackdropShadow: rgba(0.03, 0.03, 0.03, 0.44)
    }
}

function shellChrome(style, palette) {
    switch (style) {
    case "KIWI":
        return {
            backdrop: rgba(0.64, 0.82, 0.40, 1.0),
            shadow: rgba(0.20, 0.32, 0.08, 0.42),
            wordmark: rgba(0.24, 0.33, 0.08, 1.0)
        }
    case "DANDELION":
        return {
            backdrop: rgba(0.95, 0.82, 0.35, 1.0),
            shadow: rgba(0.46, 0.30, 0.05, 0.38),
            wordmark: rgba(0.45, 0.28, 0.03, 1.0)
        }
    case "TEAL":
        return {
            backdrop: rgba(0.34, 0.74, 0.72, 1.0),
            shadow: rgba(0.08, 0.28, 0.27, 0.40),
            wordmark: rgba(0.04, 0.30, 0.35, 1.0)
        }
    case "GRAPE":
        return {
            backdrop: rgba(0.64, 0.48, 0.75, 1.0),
            shadow: rgba(0.23, 0.15, 0.30, 0.42),
            wordmark: rgba(0.26, 0.14, 0.38, 1.0)
        }
    default:
        return {
            backdrop: palette.shellBackdrop,
            shadow: palette.shellBackdropShadow,
            wordmark: palette.gameBoyWordmark
        }
    }
}

function shellSeed(style, chrome, isDark) {
    let mixSet
    switch (style) {
    case "DANDELION":
        mixSet = {
            surfaceMix: isDark ? 0.16 : 0.14,
            glassMix: isDark ? 0.20 : 0.16,
            focusMix: isDark ? 0.30 : 0.24,
            outlineMix: isDark ? 0.18 : 0.14,
            textMix: isDark ? 0.10 : 0.14,
            backgroundMix: isDark ? 0.34 : 0.22
        }
        break
    default:
        mixSet = {
            surfaceMix: isDark ? 0.18 : 0.16,
        glassMix: isDark ? 0.18 : 0.16,
        focusMix: isDark ? 0.18 : 0.16,
        outlineMix: isDark ? 0.15 : 0.14,
            textMix: isDark ? 0.11 : 0.16,
            backgroundMix: isDark ? 0.38 : 0.26
        }
        break
    }

    const surface = mix(chrome.backdrop, chrome.shadow, isDark ? 0.34 : 0.18)
    const glass = mix(chrome.backdrop, rgba(1.0, 1.0, 1.0, isDark ? 0.26 : 0.34), isDark ? 0.22 : 0.30)
    const focus = mix(chrome.backdrop, rgba(1.0, 1.0, 1.0, 1.0), isDark ? 0.18 : 0.24)

    return {
        background: chrome.backdrop,
        surface: surface,
        glass: glass,
        shadow: chrome.shadow,
        focus: focus,
        accent: chrome.wordmark,
        text: chrome.wordmark,
        surfaceMix: mixSet.surfaceMix,
        glassMix: mixSet.glassMix,
        focusMix: mixSet.focusMix,
        outlineMix: mixSet.outlineMix,
        textMix: mixSet.textMix,
        backgroundMix: mixSet.backgroundMix
    }
}

function resolve(style, appearance) {
    const resolvedAppearance = appearance === "LIGHT" ? "LIGHT" : "DARK"
    const isDark = resolvedAppearance === "DARK"
    const base = isDark ? darkPalette() : lightPalette()
    const chrome = shellChrome(style, base)

    const themed = {
        primaryText: base.primaryText,
        secondaryText: base.secondaryText,
        tertiaryText: base.tertiaryText,
        panelBackground: base.panelBackground,
        panelGlassTint: base.panelGlassTint,
        panelOutline: base.panelOutline,
        menuFocusFill: base.menuFocusFill,
        menuIdleFill: base.menuIdleFill,
        menuFocusGlass: base.menuFocusGlass,
        menuIdleGlass: base.menuIdleGlass,
        menuFocusStroke: base.menuFocusStroke,
        menuIdleStroke: base.menuIdleStroke,
        appBackgroundTop: base.appBackgroundTop,
        appBackgroundMiddle: base.appBackgroundMiddle,
        appBackgroundBottom: base.appBackgroundBottom,
        appHighlightGlow: base.appHighlightGlow,
        appAccentGlow: base.appAccentGlow,
        appDepthShadow: base.appDepthShadow,
        gameBoyWordmark: chrome.wordmark,
        screenWellFill: base.screenWellFill,
        screenWellHighlight: base.screenWellHighlight,
        screenWellDepth: base.screenWellDepth,
        screenLabel: base.screenLabel,
        batteryIndicator: base.batteryIndicator,
        screenRim: base.screenRim,
        screenGlow: base.screenGlow,
        screenGlowInner: base.screenGlowInner,
        accentBarMagenta: base.accentBarMagenta,
        accentBarBlue: base.accentBarBlue,
        shellBackdrop: chrome.backdrop,
        shellShadow: chrome.shadow
    }

    if (style !== "CLASSIC") {
        const seed = shellSeed(style, chrome, isDark)
        themed.primaryText = mix(base.primaryText, seed.text, seed.textMix)
        themed.secondaryText = mix(base.secondaryText, seed.text, seed.textMix * 0.92)
        themed.tertiaryText = mix(base.tertiaryText, seed.text, seed.textMix * 0.78)
        themed.panelBackground = mix(base.panelBackground, seed.surface, seed.surfaceMix)
        themed.panelGlassTint = mix(base.panelGlassTint, seed.glass, seed.glassMix)
        themed.panelOutline = mix(base.panelOutline, seed.shadow, seed.outlineMix)
        themed.menuFocusFill = mix(base.menuFocusFill, seed.focus, seed.focusMix)
        themed.menuIdleFill = mix(base.menuIdleFill, seed.surface, seed.surfaceMix * 0.6)
        themed.menuFocusGlass = mix(base.menuFocusGlass, seed.glass, seed.glassMix)
        themed.menuIdleGlass = mix(base.menuIdleGlass, seed.glass, seed.glassMix * 0.72)
        themed.menuFocusStroke = mix(base.menuFocusStroke, seed.accent, seed.focusMix * 0.82)
        themed.menuIdleStroke = mix(base.menuIdleStroke, seed.shadow, seed.outlineMix)
        themed.appBackgroundTop = mix(base.appBackgroundTop, seed.background, seed.backgroundMix)
        themed.appBackgroundMiddle = mix(base.appBackgroundMiddle, seed.surface, seed.backgroundMix)
        themed.appBackgroundBottom = mix(base.appBackgroundBottom, seed.shadow, seed.backgroundMix * 0.94)
        themed.appHighlightGlow = mix(base.appHighlightGlow, seed.glass, seed.glassMix * 0.5)
        themed.appAccentGlow = mix(base.appAccentGlow, seed.accent, seed.focusMix * 0.72)
        themed.appDepthShadow = mix(base.appDepthShadow, seed.shadow, seed.outlineMix)
        themed.screenWellFill = mix(base.screenWellFill, seed.surface, isDark ? 0.42 : 0.26)
        themed.screenWellHighlight = mix(base.screenWellHighlight, seed.glass, isDark ? 0.34 : 0.22)
        themed.screenWellDepth = mix(base.screenWellDepth, seed.shadow, isDark ? 0.26 : 0.18)
        themed.screenRim = mix(base.screenRim, seed.accent, isDark ? 0.42 : 0.24)
        themed.screenGlow = mix(base.screenGlow, seed.accent, isDark ? 0.34 : 0.16)
        themed.screenGlowInner = mix(base.screenGlowInner, seed.glass, isDark ? 0.24 : 0.12)
    }

    themed.shellBorder = mix(chrome.backdrop, chrome.shadow, isDark ? 0.46 : 0.28)
    themed.shellInnerBorder = mix(chrome.shadow, rgba(1.0, 1.0, 1.0, 1.0), isDark ? 0.16 : 0.08)
    themed.cardCastColor = overlay(mix(themed.appDepthShadow, chrome.shadow, 0.58), isDark ? 0.48 : 0.20)
    themed.cardInnerOutline = overlay(mix(themed.panelOutline, chrome.shadow, 0.36), isDark ? 0.28 : 0.12)
    themed.windowBar = overlay(mix(themed.panelBackground, themed.appBackgroundTop, isDark ? 0.18 : 0.12), 0.96)
    themed.windowBarBorder = overlay(mix(themed.panelOutline, themed.menuIdleStroke, 0.5), isDark ? 0.44 : 0.24)
    themed.windowBarText = themed.primaryText
    themed.windowBadge = overlay(mix(themed.menuIdleFill, themed.panelGlassTint, 0.42), isDark ? 0.78 : 0.58)
    themed.windowBadgeBorder = overlay(mix(themed.menuIdleStroke, themed.panelOutline, 0.48), isDark ? 0.52 : 0.24)
    themed.windowBadgeText = themed.primaryText
    themed.optionIdleFill = overlay(mix(themed.menuIdleFill, themed.panelBackground, 0.42), isDark ? 0.74 : 0.22)
    themed.optionFocusFill = overlay(mix(themed.menuIdleFill, themed.menuFocusFill, 0.18), isDark ? 0.64 : 0.22)
    themed.optionIdleStroke = overlay(mix(themed.menuIdleStroke, themed.panelOutline, 0.46), isDark ? 0.54 : 0.18)
    themed.optionFocusStroke = overlay(mix(themed.menuIdleStroke, themed.menuFocusStroke, 0.22), isDark ? 0.48 : 0.18)
    themed.optionGlass = overlay(mix(themed.menuIdleGlass, themed.panelGlassTint, 0.42), isDark ? 0.34 : 0.16)
    themed.optionFocusGlass = overlay(mix(themed.menuIdleGlass, themed.menuFocusGlass, 0.20), isDark ? 0.26 : 0.13)

    return themed
}

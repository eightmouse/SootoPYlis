from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True, slots=True)
class ThemeTokens:
    background_top: str
    background_bottom: str
    shell_highlight: str
    shell_shadow: str
    accent_blue: str
    accent_mint: str
    text_primary: str
    text_muted: str


DEFAULT_THEME = ThemeTokens(
    background_top="#102434",
    background_bottom="#070d15",
    shell_highlight="#dce7f1",
    shell_shadow="#67788b",
    accent_blue="#7be4ff",
    accent_mint="#93f8d8",
    text_primary="#f3fbff",
    text_muted="#90a8bd",
)

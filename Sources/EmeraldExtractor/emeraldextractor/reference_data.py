from __future__ import annotations

import json
import re
import struct
from functools import lru_cache
from pathlib import Path
from typing import Any

from emeralddata.models import RomDescriptor

_REFERENCE_LAYOUTS_PATH = Path("data/layouts/layouts.json")

_TARGET_MAPS: tuple[dict[str, Any], ...] = (
    {
        "id": "MAP_LITTLEROOT_TOWN_BRENDANS_HOUSE_2F",
        "folder": "LittlerootTown_BrendansHouse_2F",
        "layout_name": "LittlerootTown_BrendansHouse_2F_Layout",
        "location_name": "LITTLEROOT",
        "area_subtitle": "BRENDANS ROOM",
        "warps": (
            {
                "x": 7,
                "y": 1,
                "target_map_id": "MAP_LITTLEROOT_TOWN_BRENDANS_HOUSE_1F",
                "target_x": 8,
                "target_y": 2,
                "target_facing": "down",
            },
        ),
    },
    {
        "id": "MAP_LITTLEROOT_TOWN_BRENDANS_HOUSE_1F",
        "folder": "LittlerootTown_BrendansHouse_1F",
        "layout_name": "LittlerootTown_BrendansHouse_1F_Layout",
        "location_name": "LITTLEROOT",
        "area_subtitle": "BRENDANS HOUSE",
        "warps": (
            {
                "x": 8,
                "y": 2,
                "target_map_id": "MAP_LITTLEROOT_TOWN_BRENDANS_HOUSE_2F",
                "target_x": 7,
                "target_y": 1,
                "target_facing": "up",
            },
            {
                "x": 8,
                "y": 8,
                "target_map_id": "MAP_LITTLEROOT_TOWN",
                "target_x": 5,
                "target_y": 8,
                "target_facing": "down",
            },
            {
                "x": 9,
                "y": 8,
                "target_map_id": "MAP_LITTLEROOT_TOWN",
                "target_x": 5,
                "target_y": 8,
                "target_facing": "down",
            },
        ),
    },
    {
        "id": "MAP_LITTLEROOT_TOWN",
        "folder": "LittlerootTown",
        "layout_name": "LittlerootTown_Layout",
        "location_name": "LITTLEROOT",
        "area_subtitle": "TOWN",
        "warps": (
            {
                "x": 5,
                "y": 8,
                "target_map_id": "MAP_LITTLEROOT_TOWN_BRENDANS_HOUSE_1F",
                "target_x": 8,
                "target_y": 8,
                "target_facing": "up",
            },
        ),
    },
)


def find_pokeemerald_reference_root(search_root: Path) -> Path | None:
    candidate = search_root / "tmp" / "pokeemerald-ref"
    if (candidate / _REFERENCE_LAYOUTS_PATH).exists():
        return candidate
    return None


@lru_cache(maxsize=4)
def _load_layout_index(layouts_path: str) -> dict[str, dict[str, Any]]:
    payload = json.loads(Path(layouts_path).read_text(encoding="utf-8"))
    return {entry["name"]: entry for entry in payload["layouts"]}


def _read_u16_words(path: Path) -> list[int]:
    raw = path.read_bytes()
    return list(struct.unpack("<" + ("H" * (len(raw) // 2)), raw))


def _tileset_symbol_to_directory(symbol: str) -> str:
    name = symbol.removeprefix("gTileset_")
    return re.sub(r"(?<!^)(?=[A-Z])", "_", name).lower()


def _music_symbol_to_midi_relative_path(symbol: str) -> str:
    return f"sound/songs/midi/{symbol.lower()}.mid"


def _resolve_music_midi_relative_path(reference_root: Path, music_symbol: str) -> str:
    relative_path = Path(_music_symbol_to_midi_relative_path(music_symbol))
    if (reference_root / relative_path).exists():
        return relative_path.as_posix()
    return ""


def build_reference_overworld_manifest(search_root: Path, rom: RomDescriptor) -> dict[str, Any] | None:
    reference_root = find_pokeemerald_reference_root(search_root)
    if reference_root is None:
        return None

    layout_index = _load_layout_index(str(reference_root / _REFERENCE_LAYOUTS_PATH))
    maps: list[dict[str, Any]] = []

    for spec in _TARGET_MAPS:
        map_json_path = reference_root / "data" / "maps" / spec["folder"] / "map.json"
        map_payload = json.loads(map_json_path.read_text(encoding="utf-8"))
        layout_payload = layout_index[spec["layout_name"]]

        blockdata_path = reference_root / layout_payload["blockdata_filepath"]
        border_path = reference_root / layout_payload["border_filepath"]
        blocks = _read_u16_words(blockdata_path)
        border = _read_u16_words(border_path)

        maps.append(
            {
                "id": spec["id"],
                "source_id": map_payload["id"],
                "location_name": spec["location_name"],
                "area_subtitle": spec["area_subtitle"],
                "music_symbol": map_payload.get("music", ""),
                "music_midi_path": _resolve_music_midi_relative_path(reference_root, map_payload.get("music", "")),
                "width": layout_payload["width"],
                "height": layout_payload["height"],
                "blocks": blocks,
                "border": border,
                "primary_tileset": _tileset_symbol_to_directory(layout_payload["primary_tileset"]),
                "secondary_tileset": _tileset_symbol_to_directory(layout_payload["secondary_tileset"]),
                "warps": list(spec["warps"]),
            }
        )

    return {
        "manifest_version": 2,
        "rom_sha1": rom.sha1,
        "rom_file_name": rom.file_name,
        "game_code": rom.header.game_code,
        "entry_overworld": {
            "map_id": "MAP_LITTLEROOT_TOWN_BRENDANS_HOUSE_2F",
            "spawn": {
                "x": 7,
                "y": 6,
                "facing": "down",
            },
        },
        "maps": maps,
    }

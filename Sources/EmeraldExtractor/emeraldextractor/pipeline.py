from __future__ import annotations

import json
from pathlib import Path
from typing import Any

from emeralddata.models import ImportPlan, RomDescriptor
from emeraldextractor.reference_data import build_reference_overworld_manifest
from emeraldextractor.rom.probe import discover_import_plan, probe_rom

_CACHE_DIRNAME = ".sootopylis"
_OVERWORLD_MANIFEST_NAME = "overworld.json"
_OVERWORLD_MANIFEST_VERSION = 1


def plan_import(rom_path: Path) -> RomDescriptor:
    """Probe a single ROM path and return the parsed descriptor."""
    return probe_rom(rom_path)


def plan_workspace_import(search_root: Path) -> ImportPlan:
    """Discover cartridge candidates inside a workspace root."""
    return discover_import_plan(search_root)


def _cache_root(search_root: Path, rom: RomDescriptor) -> Path:
    return search_root / _CACHE_DIRNAME / "imports" / rom.sha1.lower()


def build_initial_overworld_manifest(rom: RomDescriptor) -> dict[str, Any] | None:
    if not rom.supported:
        return None

    return {
        "manifest_version": _OVERWORLD_MANIFEST_VERSION,
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
        "maps": [
            {
                "id": "MAP_LITTLEROOT_TOWN_BRENDANS_HOUSE_2F",
                "source_id": "MAP_LITTLEROOT_TOWN_BRENDANS_HOUSE_2F",
                "location_name": "LITTLEROOT",
                "area_subtitle": "BRENDANS ROOM",
                "rows": [
                    "###############",
                    "#ww===...===ww#",
                    "#.............#",
                    "#.....ccc.....#",
                    "#.............#",
                    "#...m.....m...#",
                    "#.............#",
                    "#......s......#",
                    "#.............#",
                    "###############",
                ],
                "warps": [
                    {
                        "x": 7,
                        "y": 7,
                        "target_map_id": "MAP_LITTLEROOT_TOWN_BRENDANS_HOUSE_1F",
                        "target_x": 7,
                        "target_y": 2,
                        "target_facing": "down",
                    },
                ],
            },
            {
                "id": "MAP_LITTLEROOT_TOWN_BRENDANS_HOUSE_1F",
                "source_id": "MAP_LITTLEROOT_TOWN_BRENDANS_HOUSE_1F",
                "location_name": "LITTLEROOT",
                "area_subtitle": "BRENDANS HOUSE",
                "rows": [
                    "###############",
                    "#ww==.....==ww#",
                    "#......s......#",
                    "#.............#",
                    "#..m.......m..#",
                    "#....ccccc....#",
                    "#....c...c....#",
                    "#....ccccc....#",
                    "#......d......#",
                    "###############",
                ],
                "warps": [
                    {
                        "x": 7,
                        "y": 2,
                        "target_map_id": "MAP_LITTLEROOT_TOWN_BRENDANS_HOUSE_2F",
                        "target_x": 7,
                        "target_y": 6,
                        "target_facing": "up",
                    },
                    {
                        "x": 7,
                        "y": 8,
                        "target_map_id": "MAP_LITTLEROOT_TOWN",
                        "target_x": 7,
                        "target_y": 3,
                        "target_facing": "down",
                    },
                ],
            },
            {
                "id": "MAP_LITTLEROOT_TOWN",
                "source_id": "MAP_LITTLEROOT_TOWN",
                "location_name": "LITTLEROOT",
                "area_subtitle": "TOWN",
                "rows": [
                    "ttttthhhhhttttt",
                    "tgggghhhhhtgggt",
                    "tgggghhdhhtgggt",
                    "tgggghhhhhtgggt",
                    "tgggggrrrgggggt",
                    "tgggggrrrgggggt",
                    "tgggggrrrgggggt",
                    "tgggggrrrgggggt",
                    "tgggggggggggggt",
                    "ttttttttttttttt",
                ],
                "warps": [
                    {
                        "x": 7,
                        "y": 2,
                        "target_map_id": "MAP_LITTLEROOT_TOWN_BRENDANS_HOUSE_1F",
                        "target_x": 7,
                        "target_y": 7,
                        "target_facing": "up",
                    },
                ],
            },
        ],
    }


def ensure_workspace_overworld_manifest(search_root: Path) -> Path | None:
    plan = discover_import_plan(search_root)
    rom = plan.preferred
    if rom is None:
        return None

    manifest = build_reference_overworld_manifest(search_root, rom)
    if manifest is None:
        manifest = build_initial_overworld_manifest(rom)
    if manifest is None:
        return None

    cache_root = _cache_root(search_root, rom)
    cache_root.mkdir(parents=True, exist_ok=True)
    manifest_path = cache_root / _OVERWORLD_MANIFEST_NAME
    manifest_path.write_text(json.dumps(manifest, indent=2), encoding="utf-8")
    return manifest_path


def load_workspace_overworld_manifest(search_root: Path) -> dict[str, Any] | None:
    manifest_path = ensure_workspace_overworld_manifest(search_root)
    if manifest_path is None:
        return None
    return json.loads(manifest_path.read_text(encoding="utf-8"))

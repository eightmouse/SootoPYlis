from __future__ import annotations

from dataclasses import dataclass
from typing import Any, Mapping

_MAPGRID_COLLISION_MASK = 0x0C00
_MAPGRID_COLLISION_SHIFT = 10


@dataclass(frozen=True, slots=True)
class OverworldTile:
    kind: str
    walkable: bool = True


@dataclass(frozen=True, slots=True)
class OverworldMap:
    width: int
    height: int
    tiles: tuple[OverworldTile, ...]
    location_name: str
    area_subtitle: str
    source_id: str = ""
    warps: tuple["OverworldWarp", ...] = ()

    def tile_at(self, x: int, y: int) -> OverworldTile:
        return self.tiles[(y * self.width) + x]

    def can_walk(self, x: int, y: int) -> bool:
        if x < 0 or y < 0 or x >= self.width or y >= self.height:
            return False
        if self.warp_at(x, y) is not None:
            return True
        return self.tile_at(x, y).walkable

    def warp_at(self, x: int, y: int) -> "OverworldWarp | None":
        for warp in self.warps:
            if warp.x == x and warp.y == y:
                return warp
        return None


@dataclass(frozen=True, slots=True)
class OverworldWarp:
    x: int
    y: int
    target_map_id: str
    target_x: int
    target_y: int
    target_facing: str = "down"


@dataclass(slots=True)
class PlayerState:
    x: int
    y: int
    facing: str = "down"


@dataclass(slots=True)
class OverworldRuntime:
    maps: dict[str, OverworldMap]
    current_map_id: str
    player: PlayerState

    @property
    def map_data(self) -> OverworldMap:
        return self.maps[self.current_map_id]

    def warp_to(self, target_map_id: str, target_x: int, target_y: int, target_facing: str = "down") -> None:
        self.current_map_id = target_map_id
        self.player.x = target_x
        self.player.y = target_y
        self.player.facing = target_facing

    def move(self, direction: str) -> bool:
        vectors = {
            "up": (0, -1),
            "down": (0, 1),
            "left": (-1, 0),
            "right": (1, 0),
        }
        if direction not in vectors:
            return False

        dx, dy = vectors[direction]
        self.player.facing = direction

        next_x = self.player.x + dx
        next_y = self.player.y + dy
        if not self.map_data.can_walk(next_x, next_y):
            return False

        self.player.x = next_x
        self.player.y = next_y
        warp = self.map_data.warp_at(next_x, next_y)
        if warp is not None:
            self.warp_to(warp.target_map_id, warp.target_x, warp.target_y, warp.target_facing)
        return True


def _tile_from_symbol(symbol: str) -> OverworldTile:
    lookup = {
        "#": OverworldTile("wall", walkable=False),
        ".": OverworldTile("floor", walkable=True),
        "=": OverworldTile("counter", walkable=False),
        "g": OverworldTile("grass", walkable=True),
        "r": OverworldTile("path", walkable=True),
        "t": OverworldTile("tree", walkable=False),
        "h": OverworldTile("house", walkable=False),
        "m": OverworldTile("mat", walkable=True),
        "d": OverworldTile("door", walkable=True),
        "s": OverworldTile("stairs", walkable=True),
        "n": OverworldTile("npc", walkable=False),
        "p": OverworldTile("plant", walkable=False),
        "c": OverworldTile("carpet", walkable=True),
        "w": OverworldTile("window", walkable=False),
    }
    return lookup.get(symbol, OverworldTile("floor", walkable=True))


def _runtime_from_layout(
    *,
    map_id: str,
    layout: tuple[str, ...],
    location_name: str,
    area_subtitle: str,
    spawn_x: int,
    spawn_y: int,
    facing: str = "up",
    source_id: str = "",
    warps: tuple[OverworldWarp, ...] = (),
) -> OverworldRuntime:
    width = len(layout[0])
    height = len(layout)
    tiles = tuple(_tile_from_symbol(symbol) for row in layout for symbol in row)
    map_data = OverworldMap(
        width=width,
        height=height,
        tiles=tiles,
        location_name=location_name,
        area_subtitle=area_subtitle,
        source_id=source_id,
        warps=warps,
    )
    player = PlayerState(x=spawn_x, y=spawn_y, facing=facing)
    return OverworldRuntime(maps={map_id: map_data}, current_map_id=map_id, player=player)


def _tile_from_block(block: int) -> OverworldTile:
    collision = (block & _MAPGRID_COLLISION_MASK) >> _MAPGRID_COLLISION_SHIFT
    return OverworldTile("wall" if collision else "floor", walkable=(collision == 0))


def runtime_from_manifest(manifest: Mapping[str, Any]) -> OverworldRuntime:
    if "maps" not in manifest:
        entry = manifest["entry_overworld"]
        rows = tuple(entry["rows"])
        spawn = entry["spawn"]
        return _runtime_from_layout(
            map_id=entry.get("source_id", "entry"),
            layout=rows,
            location_name=entry["location_name"],
            area_subtitle=entry["area_subtitle"],
            spawn_x=spawn["x"],
            spawn_y=spawn["y"],
            facing=spawn.get("facing", "up"),
            source_id=entry.get("source_id", ""),
        )

    maps: dict[str, OverworldMap] = {}
    for map_manifest in manifest["maps"]:
        if "rows" in map_manifest:
            rows = tuple(map_manifest["rows"])
            width = len(rows[0])
            height = len(rows)
            tiles = tuple(_tile_from_symbol(symbol) for row in rows for symbol in row)
        else:
            width = int(map_manifest["width"])
            height = int(map_manifest["height"])
            blocks = tuple(int(block) for block in map_manifest["blocks"])
            tiles = tuple(_tile_from_block(block) for block in blocks)
        warps = tuple(
            OverworldWarp(
                x=warp["x"],
                y=warp["y"],
                target_map_id=warp["target_map_id"],
                target_x=warp["target_x"],
                target_y=warp["target_y"],
                target_facing=warp.get("target_facing", "down"),
            )
            for warp in map_manifest.get("warps", [])
        )
        maps[map_manifest["id"]] = OverworldMap(
            width=width,
            height=height,
            tiles=tiles,
            location_name=map_manifest["location_name"],
            area_subtitle=map_manifest["area_subtitle"],
            source_id=map_manifest.get("source_id", map_manifest["id"]),
            warps=warps,
        )

    entry = manifest["entry_overworld"]
    spawn = entry["spawn"]
    return OverworldRuntime(
        maps=maps,
        current_map_id=entry["map_id"],
        player=PlayerState(
            x=spawn["x"],
            y=spawn["y"],
            facing=spawn.get("facing", "up"),
        ),
    )


def make_demo_overworld() -> OverworldRuntime:
    layout = (
        "###############",
        "#ww===...===ww#",
        "#.............#",
        "#.....ccc.....#",
        "#.....ccc.....#",
        "#.............#",
        "#...m.....m...#",
        "#.............#",
        "#......d......#",
        "###############",
    )

    return _runtime_from_layout(
        map_id="demo.player_room",
        layout=layout,
        location_name="LITTLEROOT",
        area_subtitle="PLAYER ROOM",
        spawn_x=7,
        spawn_y=6,
        facing="up",
    )

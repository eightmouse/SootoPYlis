from __future__ import annotations

import struct
import sys
from functools import lru_cache
from pathlib import Path
from typing import Any, Sequence

from emeraldextractor.reference_data import find_pokeemerald_reference_root

_MAPGRID_METATILE_ID_MASK = 0x03FF
_BG_TILE_ID_MASK = 0x03FF
_BG_TILE_H_FLIP_MASK = 0x0400
_BG_TILE_V_FLIP_MASK = 0x0800
_BG_TILE_PALETTE_SHIFT = 12
_PRIMARY_METATILE_COUNT = 512
_VIEWPORT_WIDTH_METATILES = 15
_VIEWPORT_HEIGHT_METATILES = 10
_METATILE_PIXELS = 16
_TILE_PIXELS = 8
_FRAME_OUTPUT_SCALE = 1
_PLAYER_FRAME_WIDTH = 16
_PLAYER_FRAME_HEIGHT = 32
_PLAYER_SPRITE_CACHE_VERSION = 3
_METATILE_LAYER_TYPE_NORMAL = 0
_METATILE_LAYER_TYPE_COVERED = 1
_METATILE_LAYER_TYPE_SPLIT = 2
_NORMAL_LAYER_FILL_TILE_ENTRY = 0x3014


def _project_root() -> Path:
    return Path(__file__).resolve().parents[3]


def _ensure_pillow() -> None:
    vendor_root = _project_root() / ".vendor"
    if vendor_root.exists():
        vendor_path = str(vendor_root)
        if vendor_path not in sys.path:
            sys.path.insert(0, vendor_path)


_ensure_pillow()

from PIL import Image  # noqa: E402


def _read_u16_words(path: Path) -> tuple[int, ...]:
    raw = path.read_bytes()
    return struct.unpack("<" + ("H" * (len(raw) // 2)), raw)


def _parse_jasc_palette(path: Path) -> tuple[tuple[int, int, int], ...]:
    lines = [line.strip() for line in path.read_text(encoding="utf-8").splitlines() if line.strip()]
    count = int(lines[2])
    colors: list[tuple[int, int, int]] = []
    for line in lines[3 : 3 + count]:
        red, green, blue = (int(value) for value in line.split())
        colors.append((red, green, blue))
    return tuple(colors)


@lru_cache(maxsize=16)
def _load_tileset_image(path_str: str) -> Image.Image:
    return Image.open(path_str).convert("P")


@lru_cache(maxsize=8)
def _load_rgba_image(path_str: str) -> Image.Image:
    return Image.open(path_str).convert("RGBA")


@lru_cache(maxsize=32)
def _load_tileset_palettes(palettes_dir_str: str) -> tuple[tuple[tuple[int, int, int], ...], ...]:
    palettes_dir = Path(palettes_dir_str)
    return tuple(_parse_jasc_palette(palettes_dir / f"{index:02d}.pal") for index in range(16))


@lru_cache(maxsize=32)
def _load_tileset_words(path_str: str) -> tuple[int, ...]:
    return _read_u16_words(Path(path_str))


@lru_cache(maxsize=32)
def _load_tileset_metatile_attributes(path_str: str) -> tuple[int, ...]:
    return _read_u16_words(Path(path_str))


def _render_tile(
    tileset_image: Image.Image,
    palettes: Sequence[Sequence[tuple[int, int, int]]],
    tile_entry: int,
    *,
    tile_index_offset: int,
    transparent_zero: bool,
) -> Image.Image:
    tile_id = (tile_entry & _BG_TILE_ID_MASK) - tile_index_offset
    tile_x = (tile_id % 16) * _TILE_PIXELS
    tile_y = (tile_id // 16) * _TILE_PIXELS
    tile = tileset_image.crop((tile_x, tile_y, tile_x + _TILE_PIXELS, tile_y + _TILE_PIXELS))

    if tile_entry & _BG_TILE_H_FLIP_MASK:
        tile = tile.transpose(Image.Transpose.FLIP_LEFT_RIGHT)
    if tile_entry & _BG_TILE_V_FLIP_MASK:
        tile = tile.transpose(Image.Transpose.FLIP_TOP_BOTTOM)

    palette = palettes[(tile_entry >> _BG_TILE_PALETTE_SHIFT) & 0x0F]
    rgba_pixels = []
    for index in list(tile.getdata()):
        red, green, blue = palette[index]
        alpha = 0 if transparent_zero and index == 0 else 255
        rgba_pixels.append((red, green, blue, alpha))

    rendered = Image.new("RGBA", (_TILE_PIXELS, _TILE_PIXELS))
    rendered.putdata(rgba_pixels)
    return rendered


def _render_metatile_layer(
    *,
    tileset_image: Image.Image,
    palettes: Sequence[Sequence[tuple[int, int, int]]],
    entries: Sequence[int],
    tile_index_offset: int,
    transparent_zero: bool,
) -> Image.Image:
    layer = Image.new("RGBA", (_METATILE_PIXELS, _METATILE_PIXELS), (0, 0, 0, 0))
    for tile_index, tile_entry in enumerate(entries):
        tile = _render_tile(
            tileset_image,
            palettes,
            tile_entry,
            tile_index_offset=tile_index_offset,
            transparent_zero=transparent_zero,
        )
        layer.alpha_composite(tile, ((tile_index % 2) * _TILE_PIXELS, (tile_index // 2) * _TILE_PIXELS))
    return layer


def _render_indexed_region_with_transparency(
    image: Image.Image,
    *,
    left: int,
    top: int,
    width: int,
    height: int,
    transparent_index: int,
) -> Image.Image:
    region = image.crop((left, top, left + width, top + height))
    palette = image.getpalette() or []

    rgba_pixels = []
    for index in list(region.getdata()):
        base = index * 3
        red = palette[base] if base < len(palette) else 0
        green = palette[base + 1] if base + 1 < len(palette) else 0
        blue = palette[base + 2] if base + 2 < len(palette) else 0
        alpha = 0 if index == transparent_index else 255
        rgba_pixels.append((red, green, blue, alpha))

    rendered = Image.new("RGBA", (width, height))
    rendered.putdata(rgba_pixels)
    return rendered


@lru_cache(maxsize=2048)
def _render_metatile(
    reference_root_str: str,
    primary_tileset: str,
    secondary_tileset: str,
    metatile_id: int,
) -> Image.Image:
    reference_root = Path(reference_root_str)
    primary_tileset_root = reference_root / "data" / "tilesets" / "primary" / primary_tileset
    primary_tileset_image = _load_tileset_image(str(primary_tileset_root / "tiles.png"))
    primary_palettes = _load_tileset_palettes(str(primary_tileset_root / "palettes"))

    if metatile_id < _PRIMARY_METATILE_COUNT:
        tileset_root = primary_tileset_root
        tileset_image = primary_tileset_image
        palettes = primary_palettes
        local_metatile_id = metatile_id
        tile_index_offset = 0
    else:
        tileset_root = reference_root / "data" / "tilesets" / "secondary" / secondary_tileset
        tileset_image = _load_tileset_image(str(tileset_root / "tiles.png"))
        palettes = _load_tileset_palettes(str(tileset_root / "palettes"))
        local_metatile_id = metatile_id - _PRIMARY_METATILE_COUNT
        tile_index_offset = _PRIMARY_METATILE_COUNT

    metatile_words = _load_tileset_words(str(tileset_root / "metatiles.bin"))
    metatile_attributes = _load_tileset_metatile_attributes(str(tileset_root / "metatile_attributes.bin"))

    offset = local_metatile_id * 8
    entries = metatile_words[offset : offset + 8]
    layer_type = (metatile_attributes[local_metatile_id] >> 12) & 0x0F

    metatile = Image.new("RGBA", (_METATILE_PIXELS, _METATILE_PIXELS), (0, 0, 0, 0))
    if layer_type == _METATILE_LAYER_TYPE_NORMAL:
        filler = _render_metatile_layer(
            tileset_image=primary_tileset_image,
            palettes=primary_palettes,
            entries=(_NORMAL_LAYER_FILL_TILE_ENTRY,) * 4,
            tile_index_offset=0,
            transparent_zero=False,
        )
        lower = _render_metatile_layer(
            tileset_image=tileset_image,
            palettes=palettes,
            entries=entries[:4],
            tile_index_offset=tile_index_offset,
            transparent_zero=True,
        )
        upper = _render_metatile_layer(
            tileset_image=tileset_image,
            palettes=palettes,
            entries=entries[4:],
            tile_index_offset=tile_index_offset,
            transparent_zero=True,
        )
        metatile.alpha_composite(filler)
        metatile.alpha_composite(lower)
        metatile.alpha_composite(upper)
        return metatile

    lower = _render_metatile_layer(
        tileset_image=tileset_image,
        palettes=palettes,
        entries=entries[:4],
        tile_index_offset=tile_index_offset,
        transparent_zero=False,
    )
    upper = _render_metatile_layer(
        tileset_image=tileset_image,
        palettes=palettes,
        entries=entries[4:],
        tile_index_offset=tile_index_offset,
        transparent_zero=True,
    )
    metatile.alpha_composite(lower)
    metatile.alpha_composite(upper)

    return metatile


def _border_block(border: Sequence[int], x: int, y: int) -> int:
    index = ((x + 1) & 1) + (((y + 1) & 1) * 2)
    return border[index]


def _block_at(map_manifest: dict[str, Any], x: int, y: int) -> int:
    width = int(map_manifest["width"])
    height = int(map_manifest["height"])
    blocks = map_manifest["blocks"]
    if 0 <= x < width and 0 <= y < height:
        return int(blocks[(y * width) + x])
    return _border_block(map_manifest["border"], x, y)


def calculate_camera_origin(*, map_width: int, map_height: int, player_x: int, player_y: int) -> tuple[int, int]:
    if map_width <= _VIEWPORT_WIDTH_METATILES:
        origin_x = -((_VIEWPORT_WIDTH_METATILES - map_width) // 2)
    else:
        origin_x = max(0, min(player_x - (_VIEWPORT_WIDTH_METATILES // 2), map_width - _VIEWPORT_WIDTH_METATILES))

    if map_height <= _VIEWPORT_HEIGHT_METATILES:
        origin_y = -((_VIEWPORT_HEIGHT_METATILES - map_height) // 2)
    else:
        origin_y = max(0, min(player_y - (_VIEWPORT_HEIGHT_METATILES // 2), map_height - _VIEWPORT_HEIGHT_METATILES))

    return origin_x, origin_y


def calculate_player_screen_position(*, map_width: int, map_height: int, player_x: int, player_y: int) -> tuple[int, int]:
    origin_x, origin_y = calculate_camera_origin(
        map_width=map_width,
        map_height=map_height,
        player_x=player_x,
        player_y=player_y,
    )
    return player_x - origin_x, player_y - origin_y


def _player_frame_spec(*, facing: str, stepping: bool, step_phase: int) -> tuple[int, bool]:
    if not stepping:
        if facing == "up":
            return 1, False
        if facing == "left":
            return 2, False
        if facing == "right":
            return 2, True
        return 0, False

    if facing == "up":
        return (6 if step_phase % 2 else 5), False
    if facing == "left":
        return (8 if step_phase % 2 else 7), False
    if facing == "right":
        return (8 if step_phase % 2 else 7), True
    return (4 if step_phase % 2 else 3), False


def render_player_overworld_sprite(
    *,
    search_root: Path,
    rom_sha1: str,
    facing: str,
    stepping: bool,
    step_phase: int,
) -> Path | None:
    reference_root = find_pokeemerald_reference_root(search_root)
    if reference_root is None:
        return None

    frame_index, flip_h = _player_frame_spec(facing=facing, stepping=stepping, step_phase=step_phase)
    sprite_root = search_root / ".sootopylis" / "imports" / rom_sha1.lower() / "runtime" / "sprites"
    sprite_root.mkdir(parents=True, exist_ok=True)
    sprite_path = sprite_root / f"brendan_walk_v{_PLAYER_SPRITE_CACHE_VERSION}_{frame_index}_{'flip' if flip_h else 'base'}.png"
    if sprite_path.exists():
        return sprite_path

    walking_sheet_path = reference_root / "graphics" / "object_events" / "pics" / "people" / "brendan" / "walking.png"
    walking_sheet = Image.open(walking_sheet_path)
    left = frame_index * _PLAYER_FRAME_WIDTH
    transparent_index = int(walking_sheet.getpixel((left, 0)))
    frame = _render_indexed_region_with_transparency(
        walking_sheet,
        left=left,
        top=0,
        width=_PLAYER_FRAME_WIDTH,
        height=_PLAYER_FRAME_HEIGHT,
        transparent_index=transparent_index,
    )
    if flip_h:
        frame = frame.transpose(Image.Transpose.FLIP_LEFT_RIGHT)
    frame.save(sprite_path)
    return sprite_path


def render_overworld_viewport(
    *,
    search_root: Path,
    rom_sha1: str,
    map_manifest: dict[str, Any],
    player_x: int,
    player_y: int,
    player_facing: str = "down",
    player_stepping: bool = False,
    player_step_phase: int = 0,
) -> Path | None:
    reference_root = find_pokeemerald_reference_root(search_root)
    if reference_root is None:
        return None

    frame = Image.new(
        "RGBA",
        (_VIEWPORT_WIDTH_METATILES * _METATILE_PIXELS, _VIEWPORT_HEIGHT_METATILES * _METATILE_PIXELS),
    )
    view_origin_x, view_origin_y = calculate_camera_origin(
        map_width=int(map_manifest["width"]),
        map_height=int(map_manifest["height"]),
        player_x=player_x,
        player_y=player_y,
    )

    for view_y in range(_VIEWPORT_HEIGHT_METATILES):
        for view_x in range(_VIEWPORT_WIDTH_METATILES):
            world_x = view_origin_x + view_x
            world_y = view_origin_y + view_y
            block = _block_at(map_manifest, world_x, world_y)
            metatile_id = block & _MAPGRID_METATILE_ID_MASK
            metatile = _render_metatile(
                str(reference_root),
                str(map_manifest["primary_tileset"]),
                str(map_manifest["secondary_tileset"]),
                metatile_id,
            )
            frame.alpha_composite(metatile, (view_x * _METATILE_PIXELS, view_y * _METATILE_PIXELS))

    player_sprite = render_player_overworld_sprite(
        search_root=search_root,
        rom_sha1=rom_sha1,
        facing=player_facing,
        stepping=player_stepping,
        step_phase=player_step_phase,
    )
    if player_sprite is not None:
        sprite_image = _load_rgba_image(str(player_sprite))
        screen_x, screen_y = calculate_player_screen_position(
            map_width=int(map_manifest["width"]),
            map_height=int(map_manifest["height"]),
            player_x=player_x,
            player_y=player_y,
        )
        sprite_left = int(screen_x * _METATILE_PIXELS)
        sprite_top = int((screen_y * _METATILE_PIXELS) - _METATILE_PIXELS)
        frame.alpha_composite(sprite_image, (sprite_left, sprite_top))

    if _FRAME_OUTPUT_SCALE > 1:
        frame = frame.resize(
            (
                frame.width * _FRAME_OUTPUT_SCALE,
                frame.height * _FRAME_OUTPUT_SCALE,
            ),
            Image.Resampling.NEAREST,
        )

    frame_root = search_root / ".sootopylis" / "imports" / rom_sha1.lower() / "runtime"
    frame_root.mkdir(parents=True, exist_ok=True)
    frame_path = frame_root / "current_frame.png"
    frame.save(frame_path)
    return frame_path

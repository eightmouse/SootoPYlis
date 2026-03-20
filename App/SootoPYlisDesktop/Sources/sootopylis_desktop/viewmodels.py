from __future__ import annotations

from pathlib import Path

from PySide6.QtCore import QObject, Property, Signal, Slot, QTimer
from emeraldextractor.pipeline import load_workspace_overworld_manifest, plan_workspace_import
from emeraldextractor.rendering import (
    calculate_player_screen_position,
    render_overworld_viewport,
    render_player_overworld_sprite,
)
from sootcore.session import make_gameplay_shell_content
from sootcore.world import make_demo_overworld, runtime_from_manifest


class DesktopSession(QObject):
    """Lightweight bridge between the Python runtime and the QML gameplay shell."""

    overworldChanged = Signal()

    def __init__(self, workspace_root: Path) -> None:
        super().__init__()
        self._workspace_root = workspace_root
        self._gameplay = make_gameplay_shell_content()
        self._import_plan = plan_workspace_import(self._workspace_root)
        overworld_manifest = load_workspace_overworld_manifest(self._workspace_root)
        self._overworld_manifest = overworld_manifest
        self._overworld = runtime_from_manifest(overworld_manifest) if overworld_manifest is not None else make_demo_overworld()
        self._map_manifest_index = {
            map_manifest["id"]: map_manifest
            for map_manifest in (overworld_manifest.get("maps", []) if overworld_manifest is not None else [])
        }
        self._rom_sha1 = overworld_manifest.get("rom_sha1", "") if overworld_manifest is not None else ""
        self._gameplay_map_image_url = ""
        self._gameplay_player_sprite_url = ""
        self._gameplay_music_url = ""
        self._frame_revision = 0
        self._player_sprite_revision = 0
        self._field_filter = self._gameplay.options_summary
        self._shell_style = "CLASSIC"
        self._appearance = "DARK"
        self._text_speed = "FAST"
        self._hdr_effects = True
        self._player_step_phase = 0
        self._player_stepping = False
        self._player_step_timer = QTimer(self)
        self._player_step_timer.setSingleShot(True)
        self._player_step_timer.setInterval(150)
        self._player_step_timer.timeout.connect(self._settle_player_pose)
        self._refresh_gameplay_frame()
        self._refresh_player_sprite()
        self._refresh_gameplay_music()

    @Property(str, constant=True)
    def appName(self) -> str:
        return "SootoPYlis"

    @Property(bool, constant=True)
    def romDetected(self) -> bool:
        return self._import_plan.has_supported_rom

    @Property(str, notify=overworldChanged)
    def gameplayLocationName(self) -> str:
        return self._overworld.map_data.location_name

    @Property(str, notify=overworldChanged)
    def gameplayAreaSubtitle(self) -> str:
        return self._overworld.map_data.area_subtitle

    @Property(bool, constant=True)
    def gameplayRunning(self) -> bool:
        return True

    @Property(str, notify=overworldChanged)
    def gameplayMapImageUrl(self) -> str:
        return self._gameplay_map_image_url

    @Property(str, notify=overworldChanged)
    def gameplayPlayerSpriteUrl(self) -> str:
        return self._gameplay_player_sprite_url

    @Property(str, notify=overworldChanged)
    def gameplayMusicUrl(self) -> str:
        return self._gameplay_music_url

    @Property(str, constant=True)
    def gameplayTrainerName(self) -> str:
        return self._gameplay.trainer_name

    @Property(str, constant=True)
    def gameplayPokedexSummary(self) -> str:
        return self._gameplay.pokedex_summary

    @Property(str, constant=True)
    def gameplayBagSummary(self) -> str:
        return self._gameplay.bag_summary

    @Property(str, constant=True)
    def gameplayOptionsSummary(self) -> str:
        return self._field_filter

    @Property(str, constant=True)
    def selectedFieldFilter(self) -> str:
        return self._field_filter

    @Property(str, constant=True)
    def selectedShellStyle(self) -> str:
        return self._shell_style

    @Property(str, constant=True)
    def selectedAppearance(self) -> str:
        return self._appearance

    @Property(str, constant=True)
    def selectedTextSpeed(self) -> str:
        return self._text_speed

    @Property(bool, constant=True)
    def hdrEffectsEnabled(self) -> bool:
        return self._hdr_effects

    @Property(str, constant=True)
    def gameplayPartySummary(self) -> str:
        return self._gameplay.party_summary

    @Property(str, constant=True)
    def gameplayPlayerSummary(self) -> str:
        return self._gameplay.player_summary

    @Property(str, constant=True)
    def gameplaySaveSummary(self) -> str:
        return self._gameplay.save_summary

    @Property(str, constant=True)
    def gameplayClockSummary(self) -> str:
        return self._gameplay.clock_summary

    @Property(int, notify=overworldChanged)
    def gameplayMapWidth(self) -> int:
        return self._overworld.map_data.width

    @Property(int, notify=overworldChanged)
    def gameplayMapHeight(self) -> int:
        return self._overworld.map_data.height

    @Property("QStringList", notify=overworldChanged)
    def gameplayTileKinds(self) -> list[str]:
        return [tile.kind for tile in self._overworld.map_data.tiles]

    @Property(int, notify=overworldChanged)
    def gameplayPlayerX(self) -> int:
        return self._overworld.player.x

    @Property(int, notify=overworldChanged)
    def gameplayPlayerY(self) -> int:
        return self._overworld.player.y

    @Property(str, notify=overworldChanged)
    def gameplayPlayerFacing(self) -> str:
        return self._overworld.player.facing

    @Property(int, notify=overworldChanged)
    def gameplayPlayerScreenX(self) -> int:
        return self._player_screen_position()[0]

    @Property(int, notify=overworldChanged)
    def gameplayPlayerScreenY(self) -> int:
        return self._player_screen_position()[1]

    def _player_screen_position(self) -> tuple[int, int]:
        map_manifest = self._map_manifest_index.get(self._overworld.current_map_id)
        if map_manifest is not None and "width" in map_manifest and "height" in map_manifest:
            map_width = int(map_manifest["width"])
            map_height = int(map_manifest["height"])
        else:
            map_width = self._overworld.map_data.width
            map_height = self._overworld.map_data.height

        return calculate_player_screen_position(
            map_width=map_width,
            map_height=map_height,
            player_x=self._overworld.player.x,
            player_y=self._overworld.player.y,
        )

    def _refresh_gameplay_frame(self) -> None:
        if not self._rom_sha1:
            self._gameplay_map_image_url = ""
            return

        map_manifest = self._map_manifest_index.get(self._overworld.current_map_id)
        if map_manifest is None:
            self._gameplay_map_image_url = ""
            return

        frame_path = render_overworld_viewport(
            search_root=self._workspace_root,
            rom_sha1=self._rom_sha1,
            map_manifest=map_manifest,
            player_x=self._overworld.player.x,
            player_y=self._overworld.player.y,
            player_facing=self._overworld.player.facing,
            player_stepping=self._player_stepping,
            player_step_phase=self._player_step_phase,
        )
        if frame_path is None:
            self._gameplay_map_image_url = ""
            return

        self._frame_revision += 1
        self._gameplay_map_image_url = f"{frame_path.as_uri()}?v={self._frame_revision}"

    def _refresh_player_sprite(self) -> None:
        if not self._rom_sha1:
            self._gameplay_player_sprite_url = ""
            return

        sprite_path = render_player_overworld_sprite(
            search_root=self._workspace_root,
            rom_sha1=self._rom_sha1,
            facing=self._overworld.player.facing,
            stepping=self._player_stepping,
            step_phase=self._player_step_phase,
        )
        if sprite_path is None:
            self._gameplay_player_sprite_url = ""
            return

        self._player_sprite_revision += 1
        self._gameplay_player_sprite_url = f"{sprite_path.as_uri()}?v={self._player_sprite_revision}"

    def _refresh_gameplay_music(self) -> None:
        map_manifest = self._map_manifest_index.get(self._overworld.current_map_id)
        relative_path = map_manifest.get("music_midi_path", "") if map_manifest is not None else ""
        if not relative_path:
            self._gameplay_music_url = ""
            return

        music_path = self._workspace_root / "tmp" / "pokeemerald-ref" / Path(relative_path)
        self._gameplay_music_url = music_path.as_uri() if music_path.exists() else ""

    def _settle_player_pose(self) -> None:
        self._player_stepping = False
        self._refresh_gameplay_frame()
        self._refresh_player_sprite()
        self.overworldChanged.emit()

    @Slot(int, result=str)
    def gameplayTileKindAt(self, index: int) -> str:
        map_data = self._overworld.map_data
        if index < 0 or index >= (map_data.width * map_data.height):
            return "floor"
        tile = map_data.tiles[index]
        return tile.kind

    @Slot(str)
    def movePlayer(self, direction: str) -> None:
        previous_map_id = self._overworld.current_map_id
        moved = self._overworld.move(direction)
        if moved:
            self._player_step_phase = (self._player_step_phase + 1) % 2
            self._player_stepping = True
            self._player_step_timer.start()
        else:
            self._player_stepping = False
            self._player_step_timer.stop()
        self._refresh_gameplay_frame()
        self._refresh_player_sprite()
        if self._overworld.current_map_id != previous_map_id:
            self._refresh_gameplay_music()
        self.overworldChanged.emit()

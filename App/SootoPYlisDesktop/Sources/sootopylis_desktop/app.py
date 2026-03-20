from __future__ import annotations

import sys
from pathlib import Path
from urllib.parse import unquote

from PySide6.QtCore import QEvent, QObject, Qt, QTimer, QUrl
from PySide6.QtGui import QGuiApplication
from PySide6.QtQml import QQmlApplicationEngine

from .viewmodels import DesktopSession


class _MovementKeyFilter(QObject):
    _DIRECTION_KEYS = {
        Qt.Key_Up: "up",
        Qt.Key_Down: "down",
        Qt.Key_Left: "left",
        Qt.Key_Right: "right",
    }

    def __init__(self, session: DesktopSession) -> None:
        super().__init__()
        self._session = session
        self._held_directions: list[str] = []
        self._active_direction: str | None = None
        self._repeat_timer = QTimer(self)
        self._repeat_timer.setSingleShot(True)
        self._repeat_timer.timeout.connect(self._repeat_move)

    def eventFilter(self, watched: QObject, event: QEvent) -> bool:
        event_type = event.type()
        if event_type not in (QEvent.KeyPress, QEvent.KeyRelease):
            return False

        direction = self._DIRECTION_KEYS.get(event.key())
        if direction is None:
            return False

        if event.isAutoRepeat():
            return True

        if event_type == QEvent.KeyPress:
            self._press_direction(direction)
        else:
            self._release_direction(direction)
        return True

    def _press_direction(self, direction: str) -> None:
        if direction in self._held_directions:
            self._held_directions.remove(direction)
        self._held_directions.append(direction)
        self._active_direction = direction
        self._session.movePlayer(direction)
        self._repeat_timer.start(170)

    def _release_direction(self, direction: str) -> None:
        if direction in self._held_directions:
            self._held_directions.remove(direction)
        if self._active_direction != direction:
            return
        if self._held_directions:
            self._active_direction = self._held_directions[-1]
            self._session.movePlayer(self._active_direction)
            self._repeat_timer.start(170)
            return
        self._active_direction = None
        self._repeat_timer.stop()

    def _repeat_move(self) -> None:
        if self._active_direction is None:
            return
        self._session.movePlayer(self._active_direction)
        self._repeat_timer.start(105)


class _WindowsMidiLoop:
    def __init__(self) -> None:
        self._winsound = None
        self._path = ""
        self._playing = False
        if sys.platform != "win32":
            return
        try:
            import winsound
        except ImportError:
            return
        self._winsound = winsound

    def can_play(self, url: str) -> bool:
        return self._winsound is not None and url.lower().endswith(".mid")

    def stop(self) -> None:
        if self._winsound is None:
            return
        self._winsound.PlaySound(None, 0)
        self._path = ""
        self._playing = False

    def play(self, url: str) -> None:
        if self._winsound is None:
            return
        local_path = QUrl(url).toLocalFile()
        if not local_path and url.startswith("file:"):
            local_path = unquote(url.removeprefix("file:///").replace("/", "\\"))
        if not local_path:
            return
        if self._playing and local_path == self._path:
            return
        flags = self._winsound.SND_FILENAME | self._winsound.SND_ASYNC | self._winsound.SND_LOOP
        self._winsound.PlaySound(local_path, flags)
        self._path = local_path
        self._playing = True

    def mode(self) -> str:
        return "playing" if self._playing else ""

    def position(self) -> int:
        return -1

    def length(self) -> int:
        return -1


class _MusicController(QObject):
    def __init__(self, session: DesktopSession) -> None:
        super().__init__()
        self._session = session
        self._windows_midi = _WindowsMidiLoop()
        self._player = None
        self._audio = None
        self._current_url = ""
        self._QMediaPlayer = None
        self._midi_poll_timer = QTimer(self)
        self._midi_poll_timer.setInterval(120)
        self._midi_poll_timer.timeout.connect(self._poll_windows_midi)

        self._session.overworldChanged.connect(self.sync)

        try:
            from PySide6.QtMultimedia import QAudioOutput, QMediaPlayer
        except ImportError:
            self.sync()
            return

        self._QMediaPlayer = QMediaPlayer
        self._audio = QAudioOutput(self)
        self._audio.setVolume(0.24)
        self._player = QMediaPlayer(self)
        self._player.setAudioOutput(self._audio)
        try:
            self._player.setLoops(-1)
        except Exception:
            pass

        self.sync()

    def sync(self) -> None:
        music_url = self._session.gameplayMusicUrl
        if not music_url:
            self._current_url = ""
            self._midi_poll_timer.stop()
            self._windows_midi.stop()
            if self._player is not None:
                self._player.stop()
            return

        if self._windows_midi.can_play(music_url):
            if music_url != self._current_url:
                self._current_url = music_url
                if self._player is not None:
                    self._player.stop()
                self._windows_midi.play(music_url)
            elif self._windows_midi.mode() != "playing":
                self._windows_midi.play(music_url)
            if self._player is not None:
                self._player.stop()
            self._midi_poll_timer.stop()
            return

        self._midi_poll_timer.stop()
        self._windows_midi.stop()

        if self._player is None or self._QMediaPlayer is None:
            return

        if music_url != self._current_url:
            self._current_url = music_url
            self._player.setSource(QUrl(music_url))

        if self._player.playbackState() != self._QMediaPlayer.PlaybackState.PlayingState:
            self._player.play()

    def _poll_windows_midi(self) -> None:
        self._midi_poll_timer.stop()


def _apply_windows_window_corner_preference(engine: QQmlApplicationEngine) -> None:
    try:
        import ctypes
        import sys
    except ImportError:
        return

    if sys.platform != "win32":
        return

    root_objects = engine.rootObjects()
    if not root_objects:
        return

    window = root_objects[0]
    hwnd = int(window.winId())
    if hwnd == 0:
        return

    # Ask DWM to restore rounded corners for the frameless desktop shell.
    DWMWA_WINDOW_CORNER_PREFERENCE = 33
    DWMWCP_ROUND = 2
    preference = ctypes.c_int(DWMWCP_ROUND)

    try:
        ctypes.windll.dwmapi.DwmSetWindowAttribute(
            hwnd,
            DWMWA_WINDOW_CORNER_PREFERENCE,
            ctypes.byref(preference),
            ctypes.sizeof(preference),
        )
    except AttributeError:
        return


def create_app(argv: list[str]) -> tuple[QGuiApplication, QQmlApplicationEngine]:
    app = QGuiApplication(argv)
    app.setApplicationName("SootoPYlis")
    app.setOrganizationName("SootoPYlis")

    engine = QQmlApplicationEngine()
    session = DesktopSession(Path.cwd())
    movement_key_filter = _MovementKeyFilter(session)
    music_controller = _MusicController(session)
    app.installEventFilter(movement_key_filter)
    app._movement_key_filter = movement_key_filter  # type: ignore[attr-defined]
    app._music_controller = music_controller  # type: ignore[attr-defined]
    engine.rootContext().setContextProperty("desktopSession", session)

    qml_dir = Path(__file__).resolve().parent / "qml"
    engine.load(QUrl.fromLocalFile(str(qml_dir / "Main.qml")))

    if not engine.rootObjects():
        raise RuntimeError("Failed to load the SootoPYlis desktop shell.")

    _apply_windows_window_corner_preference(engine)

    return app, engine

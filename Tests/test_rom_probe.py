from __future__ import annotations

import sys
import unittest
from pathlib import Path
import shutil


ROOT = Path(__file__).resolve().parents[1]
TMP_ROOT = ROOT / "tmp"
sys.path[:0] = [
    str(ROOT / "Sources" / "EmeraldData"),
    str(ROOT / "Sources" / "EmeraldExtractor"),
]

from emeraldextractor.pipeline import load_workspace_overworld_manifest
from emeraldextractor.rom.probe import calculate_header_checksum, discover_import_plan, probe_rom


def make_test_rom(*, game_code: str = "BPEE", title: str = "POKEMON EMER", checksum_valid: bool = True) -> bytes:
    header = bytearray(0xC0)
    header[0xA0:0xAC] = title.encode("ascii").ljust(12, b"\x00")
    header[0xAC:0xB0] = game_code.encode("ascii")
    header[0xB0:0xB2] = b"01"
    header[0xB2] = 0x96
    header[0xBC] = 0
    header[0xBD] = calculate_header_checksum(header)

    if not checksum_valid:
        header[0xBD] = (header[0xBD] + 1) & 0xFF

    return bytes(header)


class RomProbeTests(unittest.TestCase):
    def setUp(self) -> None:
        TMP_ROOT.mkdir(exist_ok=True)
        self._active_case_dir: Path | None = None

    def tearDown(self) -> None:
        if self._active_case_dir is not None:
            shutil.rmtree(self._active_case_dir, ignore_errors=True)

        try:
            TMP_ROOT.rmdir()
        except OSError:
            pass

    def _case_dir(self, name: str) -> Path:
        case_dir = TMP_ROOT / name
        shutil.rmtree(case_dir, ignore_errors=True)
        case_dir.mkdir(parents=True, exist_ok=True)
        self._active_case_dir = case_dir
        return case_dir

    def test_probe_rom_accepts_emerald_family_header(self) -> None:
        case_dir = self._case_dir("probe_accepts")
        rom_path = case_dir / "Pokemon - Emerald.bin"
        rom_path.write_bytes(make_test_rom())

        rom = probe_rom(rom_path)

        self.assertTrue(rom.supported)
        self.assertEqual(rom.header.game_code, "BPEE")
        self.assertEqual(rom.region, "USA")
        self.assertTrue(rom.header.checksum_valid)

    def test_probe_rom_rejects_bad_checksum(self) -> None:
        case_dir = self._case_dir("probe_rejects_checksum")
        rom_path = case_dir / "Broken Emerald.bin"
        rom_path.write_bytes(make_test_rom(checksum_valid=False))

        rom = probe_rom(rom_path)

        self.assertFalse(rom.supported)
        self.assertIn("Header checksum did not validate.", rom.validation_notes)

    def test_discover_import_plan_prefers_supported_emerald_rom(self) -> None:
        case_dir = self._case_dir("discover_prefers_supported")
        (case_dir / "bad.bin").write_bytes(make_test_rom(game_code="AXVE"))
        (case_dir / "good.bin").write_bytes(make_test_rom())

        plan = discover_import_plan(case_dir)

        self.assertTrue(plan.has_supported_rom)
        self.assertIsNotNone(plan.preferred)
        self.assertEqual(plan.preferred.file_name, "good.bin")

    def test_workspace_manifest_loader_emits_first_overworld_slice(self) -> None:
        case_dir = self._case_dir("workspace_manifest_loader")
        (case_dir / "Pokemon - Emerald.gba").write_bytes(make_test_rom())

        manifest = load_workspace_overworld_manifest(case_dir)

        self.assertIsNotNone(manifest)
        assert manifest is not None
        self.assertEqual(manifest["entry_overworld"]["map_id"], "MAP_LITTLEROOT_TOWN_BRENDANS_HOUSE_2F")
        self.assertEqual(len(manifest["maps"]), 3)
        self.assertEqual(manifest["maps"][0]["location_name"], "LITTLEROOT")
        self.assertEqual(manifest["maps"][0]["area_subtitle"], "BRENDANS ROOM")
        self.assertIn("id", manifest["maps"][0])
        if "blocks" in manifest["maps"][0]:
            self.assertEqual(manifest["maps"][0]["width"] * manifest["maps"][0]["height"], len(manifest["maps"][0]["blocks"]))
        else:
            self.assertTrue(manifest["maps"][0]["rows"])


if __name__ == "__main__":
    unittest.main()

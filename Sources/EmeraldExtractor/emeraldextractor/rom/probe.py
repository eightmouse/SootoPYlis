from __future__ import annotations

import hashlib
from pathlib import Path

from emeralddata.models import GbaHeader, ImportPlan, RomDescriptor

_SUPPORTED_EXTENSIONS = {".gba", ".rom", ".bin"}
_REGION_NAMES = {
    "E": "USA",
    "J": "Japan",
    "P": "Europe",
    "D": "Germany",
    "F": "France",
    "I": "Italy",
    "S": "Spain",
}


def calculate_header_checksum(header_bytes: bytes) -> int:
    checksum = sum(header_bytes[0xA0:0xBD])
    return (-checksum - 0x19) & 0xFF


def parse_gba_header(header_bytes: bytes) -> GbaHeader:
    if len(header_bytes) < 0xC0:
        raise ValueError("ROM is too small to contain a full GBA header.")

    return GbaHeader(
        title=header_bytes[0xA0:0xAC].decode("ascii", errors="ignore").rstrip("\x00 "),
        game_code=header_bytes[0xAC:0xB0].decode("ascii", errors="ignore").rstrip("\x00 "),
        maker_code=header_bytes[0xB0:0xB2].decode("ascii", errors="ignore").rstrip("\x00 "),
        unit_code=header_bytes[0xB3],
        device_type=header_bytes[0xB4],
        version=header_bytes[0xBC],
        header_checksum=header_bytes[0xBD],
        calculated_checksum=calculate_header_checksum(header_bytes),
        fixed_value=header_bytes[0xB2],
    )


def probe_rom(rom_path: Path) -> RomDescriptor:
    file_size = rom_path.stat().st_size
    sha1 = hashlib.sha1()

    with rom_path.open("rb") as rom_file:
        header_bytes = rom_file.read(0xC0)
        sha1.update(header_bytes)
        for chunk in iter(lambda: rom_file.read(1024 * 1024), b""):
            sha1.update(chunk)

    header = parse_gba_header(header_bytes)

    family = "Pokemon Emerald" if header.game_code.startswith("BPE") else "Unknown GBA cartridge"
    region = _REGION_NAMES.get(header.game_code[-1:], "Unknown")
    supported = (
        header.fixed_value_valid
        and header.checksum_valid
        and header.game_code.startswith("BPE")
    )

    notes: list[str] = []
    if not header.fixed_value_valid:
        notes.append("Missing the expected GBA fixed-value marker.")
    if not header.checksum_valid:
        notes.append("Header checksum did not validate.")
    if not header.game_code.startswith("BPE"):
        notes.append("Game code does not match the Emerald family.")

    if not notes:
        notes.append("Header checksum passed and Emerald-family game code detected.")

    return RomDescriptor(
        path=rom_path,
        file_size=file_size,
        sha1=sha1.hexdigest().upper(),
        header=header,
        detected_family=family,
        region=region,
        supported=supported,
        validation_notes=tuple(notes),
    )


def discover_roms(search_root: Path) -> tuple[RomDescriptor, ...]:
    candidates = [
        probe_rom(path)
        for path in sorted(search_root.iterdir())
        if path.is_file() and path.suffix.lower() in _SUPPORTED_EXTENSIONS
    ]
    return tuple(candidates)


def discover_import_plan(search_root: Path) -> ImportPlan:
    candidates = discover_roms(search_root)
    preferred = next((candidate for candidate in candidates if candidate.supported), None)

    if preferred is not None:
        summary = f"Detected {preferred.detected_family} at {preferred.path.name}."
    elif candidates:
        summary = "Found cartridge files, but none passed the Emerald validation checks."
    else:
        summary = "No local cartridge files detected in the current workspace."

    return ImportPlan(
        search_root=search_root,
        candidates=candidates,
        preferred=preferred,
        summary=summary,
    )

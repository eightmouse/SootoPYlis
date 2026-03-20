from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path


@dataclass(frozen=True, slots=True)
class GbaHeader:
    title: str
    game_code: str
    maker_code: str
    unit_code: int
    device_type: int
    version: int
    header_checksum: int
    calculated_checksum: int
    fixed_value: int

    @property
    def checksum_valid(self) -> bool:
        return self.header_checksum == self.calculated_checksum

    @property
    def fixed_value_valid(self) -> bool:
        return self.fixed_value == 0x96


@dataclass(frozen=True, slots=True)
class RomDescriptor:
    path: Path
    file_size: int
    sha1: str
    header: GbaHeader
    detected_family: str
    region: str
    supported: bool
    validation_notes: tuple[str, ...]

    @property
    def file_name(self) -> str:
        return self.path.name

    @property
    def size_mebibytes(self) -> float:
        return self.file_size / (1024 * 1024)


@dataclass(frozen=True, slots=True)
class ImportPlan:
    search_root: Path
    candidates: tuple[RomDescriptor, ...]
    preferred: RomDescriptor | None
    summary: str

    @property
    def has_supported_rom(self) -> bool:
        return self.preferred is not None

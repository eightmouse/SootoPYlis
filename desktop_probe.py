from __future__ import annotations

import importlib.util
import site
import sys
from pathlib import Path


def _extend_path(root: Path) -> None:
    package_roots = [
        root / "App" / "SootoPYlisDesktop" / "Sources",
        root / "Sources" / "SootCore",
        root / "Sources" / "SootUI",
        root / "Sources" / "EmeraldData",
        root / "Sources" / "EmeraldExtractor",
    ]

    for package_root in reversed(package_roots):
        package_root_str = str(package_root)
        if package_root_str not in sys.path:
            sys.path.insert(0, package_root_str)

    user_site = site.getusersitepackages()
    if user_site and user_site not in sys.path:
        sys.path.append(user_site)


def _print_header(title: str) -> None:
    print()
    print(f"== {title} ==")


def main() -> int:
    root = Path(__file__).resolve().parent

    _print_header("Environment")
    print(f"Workspace: {root}")
    print(f"Python executable: {sys.executable}")
    print(f"Python version: {sys.version.split()[0]}")

    pyside6_spec = importlib.util.find_spec("PySide6")
    if pyside6_spec is None:
        print("PySide6: missing")
    else:
        import PySide6

        print(f"PySide6: {PySide6.__version__}")

    _extend_path(root)

    _print_header("ROM Probe")
    from emeraldextractor.pipeline import plan_workspace_import

    plan = plan_workspace_import(root)
    print(f"Supported ROM detected: {plan.has_supported_rom}")
    print(f"Candidate count: {len(plan.candidates)}")

    if plan.preferred is not None:
        rom = plan.preferred
        print(f"Preferred ROM: {rom.file_name}")
        print(f"Game code: {rom.header.game_code}")
        print(f"Region: {rom.region}")
        print("Expected startup scene: gameplay")
        return 0

    if plan.candidates:
        print("Preferred ROM: none")
        print(f"Probe summary: {plan.summary}")
        print("Expected startup scene: title")
        return 0

    print("Preferred ROM: none")
    print("Probe summary: no cartridge candidates found")
    print("Expected startup scene: title")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

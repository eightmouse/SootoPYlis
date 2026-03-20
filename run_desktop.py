from __future__ import annotations

import site
import sys
from pathlib import Path


def _extend_path() -> None:
    root = Path(__file__).resolve().parent
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


def main() -> int:
    _extend_path()
    try:
        from sootopylis_desktop.main import main as desktop_main
    except ModuleNotFoundError as exc:
        if exc.name and exc.name.startswith("PySide6"):
            print("PySide6 is not installed yet.")
            print("Install dependencies with `python -m pip install -e .` or `python -m pip install PySide6`.")
            return 1
        raise

    return desktop_main()


if __name__ == "__main__":
    raise SystemExit(main())

from __future__ import annotations

import sys

from .app import create_app


def main() -> int:
    app, _engine = create_app(sys.argv)
    return app.exec()


if __name__ == "__main__":
    raise SystemExit(main())

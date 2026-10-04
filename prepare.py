#!/usr/bin/env python3
"""Generate the tested project README with an outside-workspace marker path."""

import argparse
from pathlib import Path
import re


ROOT = Path(__file__).resolve().parent
PROJECT = ROOT / "victim-project"
TEMPLATE = PROJECT / "README.template.md"
OUTPUT = PROJECT / "README.md"


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("marker", help="absolute marker path outside victim-project")
    args = parser.parse_args()

    if not re.fullmatch(r"/[A-Za-z0-9._/-]+", args.marker):
        parser.error("marker must be an absolute path without shell metacharacters or spaces")
    marker = Path(args.marker).resolve()
    if marker.is_relative_to(PROJECT.resolve()):
        parser.error("marker must be outside victim-project")
    if not marker.parent.is_dir():
        parser.error("marker parent directory must exist")
    if marker.exists():
        parser.error("marker must not already exist")

    OUTPUT.write_text(
        TEMPLATE.read_text().replace("{{ABSOLUTE_MARKER_PATH}}", str(marker))
    )
    print(f"Prepared {OUTPUT}. Open victim-project in Cursor; expected marker: {marker}")


if __name__ == "__main__":
    main()

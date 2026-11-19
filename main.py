#!/usr/bin/env python3
"""Entry program for make.fun competition news-image-20261118.

Writes the poster image (built by build_poster.py from the real news of
Wednesday 18 November 2026) to /output/entry.png.

Runs with no network and only the standard library. The output directory is
/output in the grader, or MAKEFUN_OUTPUT_DIR when set for local runs:

    mkdir -p out && MAKEFUN_OUTPUT_DIR=out python3 main.py
"""

import hashlib
import os
import shutil
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
SOURCE = HERE / "entry.png"


def sha256(path):
    digest = hashlib.sha256()
    with open(path, "rb") as f:
        for chunk in iter(lambda: f.read(65536), b""):
            digest.update(chunk)
    return digest.hexdigest()


def main():
    if not SOURCE.is_file():
        print(f"error: {SOURCE} not found", file=sys.stderr)
        raise SystemExit(1)
    out_dir = Path(os.environ.get("MAKEFUN_OUTPUT_DIR", "/output"))
    out_dir.mkdir(parents=True, exist_ok=True)
    dest = out_dir / "entry.png"
    shutil.copyfile(SOURCE, dest)
    # Both runs must write the same bytes: refuse to pass a bad copy on.
    if sha256(SOURCE) != sha256(dest):
        print("error: copy mismatch", file=sys.stderr)
        raise SystemExit(1)
    print(f"wrote {dest} ({dest.stat().st_size} bytes)")


if __name__ == "__main__":
    main()

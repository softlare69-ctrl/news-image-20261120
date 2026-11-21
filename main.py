#!/usr/bin/env python3
"""Copy the bundled newspaper front page to the output directory.

Reads entry.png from this script's own directory and writes it
byte-for-byte to MAKEFUN_OUTPUT_DIR (default /output) as entry.png.
No network access; the copy is deterministic.
"""

import hashlib
import os
import shutil
import sys

PNG_SIGNATURE = b"\x89PNG\r\n\x1a\n"
SOURCE_NAME = "entry.png"


def sha256_of(path):
    digest = hashlib.sha256()
    with open(path, "rb") as handle:
        for chunk in iter(lambda: handle.read(65536), b""):
            digest.update(chunk)
    return digest.hexdigest()


def main():
    here = os.path.dirname(os.path.abspath(__file__))
    source = os.path.join(here, SOURCE_NAME)

    with open(source, "rb") as handle:
        magic = handle.read(len(PNG_SIGNATURE))
    if magic != PNG_SIGNATURE:
        print("error: %s is not a PNG file" % source, file=sys.stderr)
        return 1

    out_dir = os.environ.get("MAKEFUN_OUTPUT_DIR", "/output")
    os.makedirs(out_dir, exist_ok=True)
    destination = os.path.join(out_dir, SOURCE_NAME)

    if os.path.abspath(source) == os.path.abspath(destination):
        print("error: source and destination are the same file",
              file=sys.stderr)
        return 1

    source_hash = sha256_of(source)
    shutil.copyfile(source, destination)
    os.chmod(destination, 0o644)

    dest_hash = sha256_of(destination)
    if source_hash != dest_hash:
        print("error: output hash does not match source", file=sys.stderr)
        return 1

    print("wrote %s (%d bytes, sha256 %s)"
          % (destination, os.path.getsize(destination), dest_hash))
    return 0


if __name__ == "__main__":
    sys.exit(main())

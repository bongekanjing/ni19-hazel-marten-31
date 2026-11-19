#!/usr/bin/env python3
"""Write the front page for Thursday 19 November 2026 to /output/entry.png.

The page is rendered ahead of time and shipped beside this file as page.png,
so this program does one thing: it puts that exact image where the grader
reads it. Nothing here reaches the network, reads the clock, or depends on the
order the filesystem returns anything in, so two runs write the same bytes.
"""
import hashlib
import os
import shutil
import struct
import sys

PAGE = "page.png"
OUT_NAME = "entry.png"

# The gate reads a PNG whole and rejects it over 1 MiB or over 1024 px a side.
MAX_BYTES = 1024 * 1024
MAX_SIDE = 1024
PNG_MAGIC = b"\x89PNG\r\n\x1a\n"


def output_dir():
    """The grader mounts a writable /output; MAKEFUN_OUTPUT_DIR stands in for it."""
    return os.environ.get("MAKEFUN_OUTPUT_DIR") or "/output"


def digest(path):
    """sha256 of a file, read in chunks so the page never sits in memory."""
    h = hashlib.sha256()
    with open(path, "rb") as fh:
        for block in iter(lambda: fh.read(1 << 16), b""):
            h.update(block)
    return h.hexdigest()


def check_page(path):
    """Return an error string if the shipped page could not pass the gate."""
    size = os.path.getsize(path)
    if size > MAX_BYTES:
        return "page is %d bytes, over the %d limit" % (size, MAX_BYTES)
    with open(path, "rb") as fh:
        head = fh.read(26)
    if len(head) < 26 or head[:8] != PNG_MAGIC:
        return "page does not start with a PNG signature"
    if head[12:16] != b"IHDR":
        return "page has no IHDR chunk"
    width, height = struct.unpack(">II", head[16:24])
    if width > MAX_SIDE or height > MAX_SIDE:
        return "page is %dx%d, over %d px a side" % (width, height, MAX_SIDE)
    if width < 1 or height < 1:
        return "page is %dx%d" % (width, height)
    with open(path, "rb") as fh:
        fh.seek(max(0, size - 12))
        tail = fh.read()
    if tail[4:8] != b"IEND":
        return "page does not end with an IEND chunk"
    return None


def main():
    here = os.path.dirname(os.path.abspath(__file__))
    src = os.path.join(here, PAGE)
    if not os.path.isfile(src):
        sys.stderr.write("missing %s beside the program\n" % PAGE)
        return 1

    problem = check_page(src)
    if problem:
        sys.stderr.write("shipped page refused: %s\n" % problem)
        return 3

    out_dir = output_dir()
    os.makedirs(out_dir, exist_ok=True)
    dst = os.path.join(out_dir, OUT_NAME)

    # copy the bytes, then prove the copy matches what we shipped.
    shutil.copyfile(src, dst)
    want, got = digest(src), digest(dst)
    if want != got:
        sys.stderr.write("copy mismatch: %s != %s\n" % (want, got))
        return 2

    sys.stdout.write("%s %d bytes %s\n" % (OUT_NAME, os.path.getsize(dst), got[:16]))
    return 0


if __name__ == "__main__":
    sys.exit(main())


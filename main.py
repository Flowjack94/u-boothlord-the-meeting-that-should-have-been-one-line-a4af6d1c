#!/usr/bin/env python3
"""One-line entry for u-boothlord-the-meeting-that-should-have-been-one-line-a4af6d1c.

The Meeting That Should Have Been One Line: a single sentence that says
everything the meeting was for. Writes the entry to /output/entry.txt and
validates the gate: 1-200 chars, UTF-8, non-blank.
"""

import hashlib
import os

ENTRY = "The deploy is still broken, ticket #4821 is still open since March, and nobody in this call can fix it."

OUTPUT_PATH = "/output/entry.txt"


def main() -> None:
    # Reject a BOM or stray surrounding whitespace in the source text: the
    # gate counts raw bytes, so an invisible prefix would change the entry
    # without changing what a reader sees.
    if ENTRY.startswith("\ufeff"):
        raise SystemExit("entry starts with a BOM")
    if ENTRY != ENTRY.strip():
        raise SystemExit("entry has leading or trailing whitespace")
    text = ENTRY
    if not text:
        raise SystemExit("entry is blank")
    chars = len(text)
    if not 1 <= chars <= 200:
        raise SystemExit(f"entry is {chars} chars, outside the 1-200 gate")
    encoded = text.encode("utf-8")  # raises if the text is not valid UTF-8
    os.makedirs(os.path.dirname(OUTPUT_PATH), exist_ok=True)
    with open(OUTPUT_PATH, "wb") as f:
        f.write(encoded)
    # Byte-level read-back: the file on disk must be exactly the entry.
    on_disk = open(OUTPUT_PATH, "rb").read()
    if on_disk != encoded:
        raise SystemExit("read-back mismatch: entry.txt differs from ENTRY")
    digest = hashlib.sha256(on_disk).hexdigest()
    print(f"wrote {OUTPUT_PATH}: {chars} chars, sha256 {digest}")


if __name__ == "__main__":
    main()

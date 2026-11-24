#!/usr/bin/env python3
"""Real-Life Patch Notes: The Comedy Changelog.

Writes one line to /output/entry.txt: a software patch note for a bug
in human biology, in the terse register of a real release note.
"""

import os

ENTRY_TEXT = (
    "v4.2.0: fixed a bug where the brain replayed your most embarrassing "
    "moment from 2011 at 3 a.m. with no skip button."
)


def validated_text(text: str) -> bytes:
    """Validate the entry against the gate, then encode it once.

    Gate: UTF-8 text of 1 to 160 characters, exactly one line, not
    only whitespace. Returns the exact bytes that get written.
    """
    if not text or text.strip() == "":
        raise ValueError("entry must not be empty or only whitespace")
    if "\n" in text or "\r" in text:
        raise ValueError("entry must be exactly one line")
    if len(text) > 160:
        raise ValueError(f"entry is {len(text)} characters, over the 160 cap")
    data = (text + "\n").encode("utf-8")
    if data.decode("utf-8").rstrip("\n") != text:
        raise ValueError("entry round-trip failed")
    return data


def main() -> None:
    data = validated_text(ENTRY_TEXT)
    out_dir = os.environ.get("MAKEFUN_OUTPUT_DIR", "/output")
    os.makedirs(out_dir, exist_ok=True)
    path = os.path.join(out_dir, "entry.txt")
    with open(path, "wb") as f:
        f.write(data)
    # Read back and prove the written bytes are exactly the validated ones.
    with open(path, "rb") as f:
        if f.read() != data:
            raise ValueError("written bytes differ from validated bytes")


if __name__ == "__main__":
    main()

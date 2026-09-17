"""
Server-side loot module — receives and stores exfiltrated files.
T1005: Data from Local System
"""
from __future__ import annotations
from pathlib import Path


LOOT_DIR = Path(__file__).parent.parent.parent / "loot"


def save(filename: str, content: bytes) -> Path:
    LOOT_DIR.mkdir(exist_ok=True)
    dest = LOOT_DIR / filename
    dest.write_bytes(content)
    return dest

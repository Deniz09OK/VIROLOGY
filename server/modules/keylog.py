"""
Server-side keylog module — receives and stores keylog data.
T1056.001: Input Capture: Keylogging
"""
from __future__ import annotations

_log: list[str] = []


def append(chunk: str) -> None:
    _log.append(chunk)


def dump() -> str:
    return "".join(_log)


def clear() -> None:
    _log.clear()

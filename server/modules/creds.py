"""
Server-side credentials module — stores and displays extracted credentials.
T1003: OS Credential Dumping
"""
from __future__ import annotations

_store: list[dict] = []


def store(entry: dict) -> None:
    _store.append(entry)


def dump() -> list[dict]:
    return list(_store)

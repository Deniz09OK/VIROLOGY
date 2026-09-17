"""
Server-side RDP module — enable/disable RDP on target.
T1021.001: Remote Services: Remote Desktop Protocol
"""
from __future__ import annotations


def build_task(action: str) -> dict:
    assert action in ("enable", "disable")
    return {"cmd": "rdp", "action": action}

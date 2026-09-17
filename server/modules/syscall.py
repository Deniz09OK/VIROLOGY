"""
Server-side syscall module — triggers direct syscall execution on agent.
Bypasses userland API hooking (NTAPI bypass).
"""
from __future__ import annotations


def build_task(syscall_id: int, args: list) -> dict:
    return {"cmd": "syscall", "id": syscall_id, "args": args}

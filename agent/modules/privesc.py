"""
Agent privesc module — local privilege escalation via misconfiguration.
T1068: Exploitation for Privilege Escalation
"""
from __future__ import annotations

import subprocess


def _check_unquoted_services() -> list[str]:
    r = subprocess.run(
        ["wmic", "service", "get", "name,pathname,startmode"],
        capture_output=True, text=True,
    )
    hits = []
    for line in r.stdout.splitlines():
        path = line.strip()
        if " " in path and not path.startswith('"') and "system32" not in path.lower():
            hits.append(path)
    return hits


def run(task: dict) -> str:
    method = task.get("method", "auto")
    if method in ("auto", "unquoted"):
        hits = _check_unquoted_services()
        return "\n".join(hits) if hits else "no unquoted service paths found"
    return f"unknown method: {method}"

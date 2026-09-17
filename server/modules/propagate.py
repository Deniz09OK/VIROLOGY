"""
Server-side propagation module — lateral movement coordination.
T1021: Remote Services
"""
from __future__ import annotations


def build_task(target_ip: str, method: str = "smb") -> dict:
    return {"cmd": "propagate", "target": target_ip, "method": method}

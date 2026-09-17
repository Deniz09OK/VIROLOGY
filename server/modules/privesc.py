"""
Server-side privesc module — triggers privilege escalation on the agent.
T1068: Exploitation for Privilege Escalation
"""
from __future__ import annotations


def build_task(method: str = "auto") -> dict:
    return {"cmd": "privesc", "method": method}

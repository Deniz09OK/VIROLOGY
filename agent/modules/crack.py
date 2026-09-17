"""
Agent crack module — local hash cracking stub (delegates heavy work to server).
T1110: Brute Force
"""
from __future__ import annotations


def run(task: dict) -> str:
    # Cracking is CPU-intensive — agent returns the hash, server does the work.
    return task.get("hash", "no hash provided")

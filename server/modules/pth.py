"""
Server-side pass-the-hash module — orchestrates PTH lateral movement.
T1550.002: Use Alternate Auth Material: Pass the Hash
"""
from __future__ import annotations


def build_task(target_ip: str, username: str, ntlm_hash: str) -> dict:
    return {
        "cmd": "pth",
        "target": target_ip,
        "username": username,
        "hash": ntlm_hash,
    }

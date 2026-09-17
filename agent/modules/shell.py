"""
Agent shell module — executes commands via subprocess.
T1059: Command and Scripting Interpreter
"""
from __future__ import annotations

import subprocess


def run(task: dict) -> str:
    cmd = task.get("command", "")
    try:
        result = subprocess.run(
            cmd,
            shell=True,
            capture_output=True,
            text=True,
            timeout=30,
        )
        return (result.stdout + result.stderr).strip()
    except subprocess.TimeoutExpired:
        return "timeout"

"""
Server-side shell module — handles output from remote shell commands.
T1059: Command and Scripting Interpreter
"""
from __future__ import annotations


def parse_output(raw: str) -> str:
    """Return cleaned shell output received from the agent."""
    return raw.strip()

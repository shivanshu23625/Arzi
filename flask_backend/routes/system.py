from flask import Blueprint, jsonify, request
from flask_backend.middleware.repo_validator import repo_validator
from flask_backend.models.store import db_store

system_bp = Blueprint("system", __name__, url_prefix="/api/v1/system")

@system_bp.route("/health", methods=["GET"])
def health_check():
    repo_status = repo_validator.get_status()
    all_cases = db_store.get_all_cases()
    return jsonify({
        "status": "healthy" if repo_status["repository_alive"] else "integrity_breach",
        "engine": "Flask ARZI Engine 1.0",
        "active_cases": len(all_cases),
        "repository_validation": repo_status
    }), 200

@system_bp.route("/kill-switch", methods=["POST"])
def toggle_kill_switch():
    """
    Test/Simulate GitHub Repository Deletion Kill-Switch.
    Payload: {"simulate_deleted": true / false}
    """
    data = request.get_json() or {}
    simulate = data.get("simulate_deleted", True)
    status = repo_validator.toggle_kill_switch(simulate)

    # Log to Run Log
    db_store.add_run_log(
        event_type="SYSTEM_KILL_SWITCH_TOGGLED",
        case_id="SYSTEM",
        actor="Security Operator",
        source="Integrity Control Panel",
        action=f"GitHub Repository Deletion Kill-Switch {'ENGAGED' if simulate else 'RESTORED'}",
        result="BREACH_TRIGGERED" if simulate else "RESTORED_OK",
        correlation_id="SYS-KILL-99"
    )

    return jsonify({
        "message": f"Kill-switch {'activated' if simulate else 'deactivated'}",
        "repository_validation": status
    }), 200

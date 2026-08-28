from flask import Blueprint, jsonify, request
from flask_backend.models.store import db_store

run_log_bp = Blueprint("run_log", __name__, url_prefix="/api/v1/run-log")

@run_log_bp.route("", methods=["GET"])
def get_run_logs():
    """
    Retrieve the immutable code-generated Run Log audit trail.
    """
    limit = int(request.args.get("limit", 50))
    logs = db_store.get_run_logs(limit=limit)
    return jsonify({
        "total_records": len(logs),
        "run_logs": logs
    }), 200

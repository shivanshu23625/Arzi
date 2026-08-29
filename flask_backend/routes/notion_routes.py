from flask import Blueprint, jsonify, request
from flask_backend.services.notion_service import notion_service
from flask_backend.models.store import db_store

notion_bp = Blueprint("notion", __name__, url_prefix="/api/v1/notion")

@notion_bp.route("/status", methods=["GET"])
def get_notion_status():
    """Returns the current Notion integration status, connection mode, and sync statistics."""
    status = notion_service.get_status()
    return jsonify({"status": "success", "notion": status}), 200

@notion_bp.route("/configure", methods=["POST"])
def configure_notion():
    """Dynamically updates Notion API Key, Database IDs, and Parent Page ID."""
    data = request.get_json() or {}
    api_key = data.get("api_key", "").strip()
    cases_db_id = data.get("cases_db_id", "").strip()
    run_log_db_id = data.get("run_log_db_id", "").strip()
    parent_page_id = data.get("parent_page_id", "").strip()

    notion_service.update_credentials(
        api_key=api_key,
        cases_db_id=cases_db_id,
        run_log_db_id=run_log_db_id,
        parent_page_id=parent_page_id
    )

    db_store.add_run_log(
        event_type="NOTION_INTEGRATION_CONFIGURED",
        case_id="NOTION-SYSTEM",
        actor="System Admin / Judge",
        source="Notion Integration Control",
        action="Updated Notion credentials and database bindings",
        result="CONFIG_UPDATED",
        correlation_id="CORR-NOTION-CFG"
    )

    return jsonify({
        "status": "success",
        "message": "Notion configuration updated successfully.",
        "notion_status": notion_service.get_status()
    }), 200

@notion_bp.route("/sync-all", methods=["POST"])
def sync_all_to_notion():
    """Triggers an immediate full synchronization of all cases and run logs to Notion."""
    host_url = request.host_url.rstrip("/")
    all_cases = db_store.get_all_cases()
    run_logs = db_store.get_run_logs(limit=25)

    synced_cases = []
    for c in all_cases:
        res = notion_service.sync_case_to_notion(c, host_url=host_url)
        synced_cases.append({"case_id": c.get("case_id"), "result": res})

    synced_logs = []
    for log in run_logs:
        res = notion_service.log_run_to_notion(log)
        synced_logs.append({"run_id": log.get("run_id"), "result": res})

    return jsonify({
        "status": "success",
        "message": f"Synchronized {len(synced_cases)} cases and {len(synced_logs)} run log rows to Notion.",
        "synced_cases_count": len(synced_cases),
        "synced_run_logs_count": len(synced_logs),
        "mode": notion_service.get_status()["mode"]
    }), 200

@notion_bp.route("/setup-workspace", methods=["POST"])
def setup_workspace_schema():
    """Programmatically creates both Notion databases under the given parent page."""
    data = request.get_json() or {}
    parent_page_id = data.get("parent_page_id", "").strip()
    if not parent_page_id:
        return jsonify({"error": "Bad Request", "message": "parent_page_id is required"}), 400

    result = notion_service.setup_notion_workspace_schema(parent_page_id)
    if result.get("status") == "success":
        return jsonify({"status": "success", "workspace": result}), 201
    else:
        return jsonify({"error": "Setup Failed", "details": result}), 400

@notion_bp.route("/mirror", methods=["GET"])
def get_notion_mirror():
    """Returns the formatted in-memory Notion database pages and run log rows for inspection."""
    return jsonify({
        "status": "success",
        "cases_database_mirror": list(notion_service.mock_synced_pages.values()),
        "run_log_database_mirror": notion_service.mock_run_log_rows,
        "total_cases_mirrored": len(notion_service.mock_synced_pages),
        "total_logs_mirrored": len(notion_service.mock_run_log_rows)
    }), 200

@notion_bp.route("/webhook", methods=["POST"])
def notion_inbound_webhook():
    """Receives webhook notifications from Notion automations when a human edits a page."""
    data = request.get_json() or {}
    page_id = data.get("page_id")
    action = data.get("action", "HUMAN_UPDATE")

    # Poll decisions immediately
    decisions = notion_service.poll_human_decisions_from_notion(db_store)

    return jsonify({
        "status": "processed",
        "received_action": action,
        "decisions_executed": decisions
    }), 200

import os
import sys

# Ensure root workspace is on python path for imports
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from flask import Flask, jsonify, request, send_from_directory
from flask_cors import CORS
from flask_backend.config import Config
from flask_backend.middleware.repo_validator import repo_validator
from flask_backend.routes.cases import cases_bp
from flask_backend.routes.run_log import run_log_bp
from flask_backend.routes.system import system_bp
from flask_backend.routes.ml_pipeline import ml_bp
from flask_backend.routes.notion_routes import notion_bp
from flask_backend.services.notion_poller import notion_poller
from flask_backend.models.store import db_store

def create_app():
    app = Flask(__name__, static_folder="static", static_url_path="")
    app.config.from_object(Config)

    # Start autonomous Notion background poller
    try:
        notion_poller.start(db_store)
    except Exception as e:
        print(f"Warning: could not start notion poller: {e}")

    # Enable CORS for frontend interaction
    CORS(app, resources={r"/api/*": {"origins": "*"}})

    # Middleware: Active GitHub Repository Liveness & Integrity Kill-Switch
    @app.before_request
    def check_github_repo_integrity():
        # Exclude system kill-switch toggle endpoint and static UI files from hard lock so admin can un-toggle
        if request.path in ("/api/v1/system/kill-switch", "/api/v1/system/health") or not request.path.startswith("/api/"):
            return None

        alive, msg = repo_validator.verify_liveness()
        if not alive:
            return jsonify({
                "error": "HTTP 503 Service Unavailable: Core Repository Binding Revoked",
                "integrity_breach": True,
                "message": msg,
                "target_repository": repo_validator.repo_url
            }), 503

    # Register API Blueprints
    app.register_blueprint(cases_bp)
    app.register_blueprint(run_log_bp)
    app.register_blueprint(system_bp)
    app.register_blueprint(ml_bp)
    app.register_blueprint(notion_bp)

    # Root & Health check endpoints
    @app.route("/health")
    def health():
        alive, msg = repo_validator.verify_liveness()
        return jsonify({
            "status": "online" if alive else "integrity_breach",
            "framework": "Flask 3.x Python",
            "repository_liveness": alive,
            "message": msg
        })

    # Serve static frontend SPA files if placed in static directory
    @app.route("/")
    def index():
        if os.path.exists(os.path.join(app.static_folder, "index.html")):
            return send_from_directory(app.static_folder, "index.html")
        return jsonify({"message": "ARZI Civic RTI Desk Flask API Server Online", "docs": "/api/v1/cases"})

    return app

app = create_app()

if __name__ == "__main__":
    port = int(os.getenv("PORT", 5000))
    print(f"Starting ARZI Flask Backend Service on port {port}...")
    app.run(host="0.0.0.0", port=port, debug=True)

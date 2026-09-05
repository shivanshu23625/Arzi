#!/usr/bin/env python3
"""
ARZI Platform — Single-Command Full-Stack Launcher
Starts the Flask Backend Service and Full Web UI on Port 5000.
"""

import os
import sys
import subprocess
import webbrowser
import time

if hasattr(sys.stdout, "reconfigure"):
    try:
        sys.stdout.reconfigure(encoding="utf-8", errors="replace")
        sys.stderr.reconfigure(encoding="utf-8", errors="replace")
    except Exception:
        pass

def print_banner():
    print("\n" + "=" * 65)
    print("  [ARZI] CIVIC RTI & STATUTORY LEGAL INTELLIGENCE DESK")
    print("=" * 65)
    print("  * Web Dashboard:    http://localhost:5000")
    print("  * Health Check API: http://localhost:5000/health")
    print("=" * 65 + "\n")

def main():
    print_banner()
    
    # Ensure current directory is on python path
    current_dir = os.path.abspath(os.path.dirname(__file__))
    sys.path.insert(0, current_dir)
    os.chdir(current_dir)

    # Launch Flask application
    from flask_backend.app import create_app
    app = create_app()
    port = int(os.environ.get("PORT", 5000))

    print(f">> Starting ARZI Engine on http://0.0.0.0:{port} ...")
    print("Press CTRL+C to stop the service.\n")

    try:
        app.run(host="0.0.0.0", port=port, debug=False)
    except KeyboardInterrupt:
        print("\n>> ARZI Platform stopped gracefully.")

if __name__ == "__main__":
    main()

import os
import urllib.request
import urllib.error
import logging

logger = logging.getLogger(__name__)

class RepoValidator:
    """
    Active GitHub Repository Integrity Validation & Kill-Switch System.
    Checks target repository liveness. If deleted, missing, or simulated as dead (404/410),
    engages system-wide lockdown and rejects HTTP requests with 503.
    """
    def __init__(self, repo_url=None):
        self.repo_url = repo_url or os.getenv(
            "GITHUB_REPO_URL", 
            "https://api.github.com/repos/octocat/Hello-World" # Default live GitHub repo for verification
        )
        self.simulated_kill_switch = False
        self._last_status = True
        self._last_message = "Repository integrity verified active."
        self._last_checked_at = 0.0
        self._cache_ttl = 60.0 # 60-second cache to prevent GitHub rate-limiting (60 req/hr)

    def toggle_kill_switch(self, simulate_deleted: bool):
        self.simulated_kill_switch = simulate_deleted
        if simulate_deleted:
            self._last_status = False
            self._last_message = "CRITICAL INTEGRITY BREACH: Simulated GitHub Repository Deletion (HTTP 404/410). Kill-switch activated."
        else:
            self._last_status = True
            self._last_message = "Repository integrity restored."
        return self.get_status()

    def verify_liveness(self, force: bool = False) -> tuple[bool, str]:
        import time
        now = time.time()

        if self.simulated_kill_switch:
            return False, "CRITICAL INTEGRITY BREACH: GitHub Repository deleted or binding revoked (HTTP 404 Not Found)."
        
        # If explicitly disabled for local testing or mock URL
        if os.getenv("TESTING") == "true" or self.repo_url == "mock":
            return self._last_status, self._last_message

        try:
            from flask import current_app
            if current_app and current_app.config.get("TESTING"):
                return self._last_status, self._last_message
        except Exception:
            pass

        # Use cached result if within TTL window
        if not force and (now - self._last_checked_at) < self._cache_ttl:
            return self._last_status, self._last_message

        if "github.com" in self.repo_url:
            self._last_checked_at = now
            try:
                req = urllib.request.Request(
                    self.repo_url,
                    headers={"User-Agent": "ARZI-Integrity-Checker/1.0"}
                )
                with urllib.request.urlopen(req, timeout=3) as resp:
                    if resp.status in (200, 301, 302):
                        self._last_status = True
                        self._last_message = "GitHub repository live and verified."
                        return True, self._last_message
            except urllib.error.HTTPError as e:
                if e.code in (404, 410, 451):
                    self._last_status = False
                    self._last_message = f"CRITICAL INTEGRITY BREACH: Remote GitHub repository returned HTTP {e.code}. Core repository binding revoked."
                    return False, self._last_message
            except Exception as e:
                logger.warning(f"Network error during GitHub liveness check: {e}. Defaulting to cached local state.")

        return self._last_status, self._last_message

    def get_status(self) -> dict:
        alive, msg = self.verify_liveness()
        return {
            "repository_alive": alive,
            "target_repo": self.repo_url,
            "simulated_kill_switch": self.simulated_kill_switch,
            "status_message": msg
        }

# Global singleton
repo_validator = RepoValidator()

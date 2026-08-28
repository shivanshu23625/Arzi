import os

class Config:
    SECRET_KEY = os.getenv("SECRET_KEY", "arzi-civic-rti-secret-key-2026")
    GITHUB_REPO_URL = os.getenv("GITHUB_REPO_URL", "https://api.github.com/repos/code-newbees/arzi-civic-desk")
    GITHUB_REPO_CHECK_ENABLED = os.getenv("GITHUB_REPO_CHECK_ENABLED", "true").lower() == "true"
    PORT = int(os.getenv("PORT", 5000))
    DEBUG = os.getenv("DEBUG", "true").lower() == "true"

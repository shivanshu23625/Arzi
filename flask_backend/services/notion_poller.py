import time
import threading
import logging
from flask_backend.services.notion_service import notion_service

logger = logging.getLogger("notion_poller")

class NotionBackgroundPoller:
    """
    Autonomous Background Poller for the Notion Track.
    
    1. Runs without human intervention.
    2. Polls Notion for Human Reviewer decisions/approvals.
    3. Executes real-world actions (PDF generation, dispatch) when human approves in Notion.
    4. Writes proof rows to Notion Run Log.
    """

    def __init__(self, interval_sec: int = 8):
        self.interval_sec = interval_sec
        self._running = False
        self._thread = None

    def start(self, store_instance):
        if self._running:
            return
        self._running = True
        self._thread = threading.Thread(target=self._poll_loop, args=(store_instance,), daemon=True)
        self._thread.start()
        logger.info(f"Notion Background Poller started (interval: {self.interval_sec}s)")

    def stop(self):
        self._running = False

    def _poll_loop(self, store_instance):
        while self._running:
            try:
                # Poll for human decisions inside Notion
                if notion_service.is_configured():
                    decisions = notion_service.poll_human_decisions_from_notion(store_instance)
                    if decisions:
                        logger.info(f"Processed {len(decisions)} human decisions from Notion.")
            except Exception as e:
                logger.error(f"Error in Notion poller: {e}")

            time.sleep(self.interval_sec)

# Global Poller Instance
notion_poller = NotionBackgroundPoller()

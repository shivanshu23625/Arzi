import os
import time
import json
import logging
import requests
from datetime import datetime
from typing import Dict, Any, List, Optional
from config.settings import get_settings

logger = logging.getLogger("notion_service")

class NotionSyncService:
    """
    Two-Way Synchronization Service between ARZI Flask Engine and Notion Workspace.
    
    Implements the core hackathon principle:
    - Your code is the engine (AI statutory reasoning, Haversine routing, PDF dispatch).
    - Notion is the interface (Cases Database for human review, Run Log Database for immutable proof).
    """

    def __init__(self):
        settings = get_settings()
        self.api_key = os.environ.get("NOTION_API_KEY", getattr(settings, "NOTION_API_KEY", ""))
        self.cases_db_id = os.environ.get("NOTION_CASES_DB_ID", getattr(settings, "NOTION_CASES_DB_ID", ""))
        self.run_log_db_id = os.environ.get("NOTION_RUN_LOG_DB_ID", getattr(settings, "NOTION_RUN_LOG_DB_ID", ""))
        self.parent_page_id = os.environ.get("NOTION_PARENT_PAGE_ID", getattr(settings, "NOTION_PARENT_PAGE_ID", ""))
        
        self.api_base = "https://api.notion.com/v1"
        self.notion_version = "2022-06-28"
        
        # Local mock storage for offline evaluation and zero-config demo
        self.mock_synced_pages: Dict[str, Dict[str, Any]] = {}
        self.mock_run_log_rows: List[Dict[str, Any]] = []
        self.last_sync_timestamp: Optional[str] = None
        self.sync_stats = {
            "total_synced_cases": 0,
            "total_synced_run_logs": 0,
            "human_decisions_processed": 0,
            "last_error": None
        }

    def get_headers(self) -> Dict[str, str]:
        return {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json",
            "Notion-Version": self.notion_version
        }

    def is_configured(self) -> bool:
        return bool(self.api_key and (self.cases_db_id or self.parent_page_id))

    def update_credentials(self, api_key: str, cases_db_id: str = "", run_log_db_id: str = "", parent_page_id: str = ""):
        if api_key:
            self.api_key = api_key.strip()
        if cases_db_id:
            self.cases_db_id = cases_db_id.strip()
        if run_log_db_id:
            self.run_log_db_id = run_log_db_id.strip()
        if parent_page_id:
            self.parent_page_id = parent_page_id.strip()

    def get_status(self) -> Dict[str, Any]:
        return {
            "configured": self.is_configured(),
            "has_api_key": bool(self.api_key),
            "cases_db_id": self.cases_db_id or "Not Configured (Using In-Memory Mirror)",
            "run_log_db_id": self.run_log_db_id or "Not Configured (Using In-Memory Mirror)",
            "parent_page_id": self.parent_page_id or "Not Configured",
            "last_sync_timestamp": self.last_sync_timestamp or "Never",
            "sync_stats": self.sync_stats,
            "mode": "LIVE_NOTION_API" if self.is_configured() else "IN_MEMORY_NOTION_MIRROR"
        }

    # -------------------------------------------------------------------------
    # 1. CASES DATABASE OPERATIONS
    # -------------------------------------------------------------------------

    def sync_case_to_notion(self, case: Dict[str, Any], host_url: str = "http://localhost:5000") -> Dict[str, Any]:
        """
        Creates or updates a beautifully formatted Case Docket page in the Notion Cases Database.
        """
        case_id = case.get("case_id", "ARZ-UNKNOWN")
        complainant = case.get("complainant", {})
        legal = case.get("statutory_legal_analysis", {})
        pio = case.get("suggested_pio", {})
        geo = case.get("geospatial_meta", {})
        status = case.get("status", "NEEDS_REVIEW")

        # Map internal status to Notion Select value
        status_map = {
            "NEEDS_REVIEW": "Needs Human Review",
            "APPROVED": "Approved & Dispatched",
            "DISPATCHED": "Approved & Dispatched",
            "TRANSFERRED_SEC_6_3": "Transferred Sec 6(3)",
            "MERGED_DUPLICATE": "Merged Duplicate"
        }
        notion_status = status_map.get(status, "Needs Human Review")

        # Prepare Notion Properties Payload
        properties = {
            "Case ID": {
                "title": [{"text": {"content": case_id}}]
            },
            "Complainant": {
                "rich_text": [{"text": {"content": f"{complainant.get('name', 'Anonymous')} ({complainant.get('address', 'Local')})"}}]
            },
            "Department": {
                "select": {"name": case.get("department", "Revenue & Land Records")[:100]}
            },
            "Status": {
                "select": {"name": notion_status}
            },
            "Merit Score": {
                "number": legal.get("case_merit_score", 90)
            },
            "SLA Days Remaining": {
                "number": case.get("sla_days_remaining", 30)
            },
            "Sec 20 Penalty (INR)": {
                "number": legal.get("section_20_penalty_liability_inr", 0)
            },
            "Nearest Assigned PIO": {
                "rich_text": [{"text": {"content": f"{pio.get('pio_name', 'Designated PIO')} — {pio.get('distance_label', 'Jurisdiction Matched')}"}}]
            }
        }

        # Multi-select IPC/BNS sections
        ipc_tags = []
        for sec in legal.get("ipc_sections", [])[:3]:
            ipc_tags.append({"name": sec.replace(",", "")[:100]})
        for sec in legal.get("bns_sections", [])[:3]:
            ipc_tags.append({"name": sec.replace(",", "")[:100]})
        if ipc_tags:
            properties["IPC & BNS Sections"] = {"multi_select": ipc_tags}

        # Document Links
        if case.get("dispatch_info"):
            properties["Tracking ID"] = {
                "rich_text": [{"text": {"content": case["dispatch_info"].get("tracking_id", "DISP-001")}}]
            }

        # Prepare Rich Human-Readable Page Content Blocks (Notion Blocks)
        children_blocks = self._build_case_notion_blocks(case, host_url)

        # Mirror locally for immediate access/testing
        self.mock_synced_pages[case_id] = {
            "case_id": case_id,
            "properties": properties,
            "blocks_count": len(children_blocks),
            "synced_at": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "status": notion_status,
            "notion_url": f"https://notion.so/arzi-workspace/{case_id}"
        }
        self.sync_stats["total_synced_cases"] += 1
        self.last_sync_timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

        # If live Notion API credentials configured, post to Notion API
        if self.is_configured() and self.cases_db_id:
            try:
                # Query if page already exists in Notion DB
                existing_page_id = self._find_notion_page_by_case_id(case_id)
                
                if existing_page_id:
                    # Update properties
                    url = f"{self.api_base}/pages/{existing_page_id}"
                    payload = {"properties": properties}
                    resp = requests.patch(url, headers=self.get_headers(), json=payload, timeout=8)
                    logger.info(f"Updated Notion page for {case_id}: {resp.status_code}")
                    return {"status": "updated", "page_id": existing_page_id, "case_id": case_id}
                else:
                    # Create new page in database
                    url = f"{self.api_base}/pages"
                    payload = {
                        "parent": {"database_id": self.cases_db_id},
                        "properties": properties,
                        "children": children_blocks[:50] # Notion block limit
                    }
                    resp = requests.post(url, headers=self.get_headers(), json=payload, timeout=10)
                    if resp.status_code in (200, 201):
                        data = resp.json()
                        return {"status": "created", "page_id": data.get("id"), "case_id": case_id, "url": data.get("url")}
                    else:
                        logger.error(f"Notion API error: {resp.text}")
                        self.sync_stats["last_error"] = f"Notion API {resp.status_code}: {resp.text[:120]}"
            except Exception as e:
                logger.error(f"Notion live sync error for {case_id}: {str(e)}")
                self.sync_stats["last_error"] = str(e)

        return {"status": "synced_mirror", "case_id": case_id, "mock_url": f"https://notion.so/arzi-workspace/{case_id}"}

    def _build_case_notion_blocks(self, case: Dict[str, Any], host_url: str) -> List[Dict[str, Any]]:
        """Constructs clean, human-readable Notion blocks matching the track requirements."""
        case_id = case.get("case_id", "ARZ")
        complainant = case.get("complainant", {})
        legal = case.get("statutory_legal_analysis", {})
        pio = case.get("suggested_pio", {})
        draft = case.get("draft_rti", {})

        blocks = [
            # 1. Executive Callout Box
            {
                "object": "block",
                "type": "callout",
                "callout": {
                    "rich_text": [{
                        "type": "text",
                        "text": {
                            "content": f"⚖️ ARZI STATUTORY LEGAL DOSSIER: Case {case_id}\n"
                                       f"• Status: {case.get('status', 'NEEDS_REVIEW')}\n"
                                       f"• Statutory Domain: {legal.get('statutory_domain', case.get('department'))}\n"
                                       f"• Case Merit: {legal.get('case_merit_score', 95)}/100 ({legal.get('win_probability', 'HIGH')})\n"
                                       f"• Section 20 Penalty Clock: ₹{legal.get('section_20_penalty_liability_inr', 0)} (₹250/day)"
                        }
                    }],
                    "icon": {"emoji": "🏛️"}
                }
            },
            # 2. Section Heading: Citizen Narrative & Facts
            {
                "object": "block",
                "type": "heading_2",
                "heading_2": {
                    "rich_text": [{"type": "text", "text": {"content": "1. Citizen Grievance & Facts"}}]
                }
            },
            {
                "object": "block",
                "type": "quote",
                "quote": {
                    "rich_text": [{"type": "text", "text": {"content": f"\"{case.get('raw_grievance', 'No statement recorded')}\""}}]
                }
            },
            {
                "object": "block",
                "type": "bulleted_list_item",
                "bulleted_list_item": {
                    "rich_text": [{"type": "text", "text": {"content": f"Complainant: {complainant.get('name')} ({complainant.get('contact', 'N/A')})"}}]
                }
            },
            {
                "object": "block",
                "type": "bulleted_list_item",
                "bulleted_list_item": {
                    "rich_text": [{"type": "text", "text": {"content": f"Address / Locality: {complainant.get('address', 'Local')}"}}]
                }
            },
            {
                "object": "block",
                "type": "bulleted_list_item",
                "bulleted_list_item": {
                    "rich_text": [{"type": "text", "text": {"content": f"Application Ref / Ack No: {case.get('application_ref_no', 'Not Provided')}"}}]
                }
            },
            # 3. Section Heading: Nearest Assigned Public Authority
            {
                "object": "block",
                "type": "heading_2",
                "heading_2": {
                    "rich_text": [{"type": "text", "text": {"content": "2. Assigned Public Authority & PIO (Haversine Match)"}}]
                }
            },
            {
                "object": "block",
                "type": "paragraph",
                "paragraph": {
                    "rich_text": [{
                        "type": "text",
                        "text": {
                            "content": f"📍 Officer: {pio.get('pio_name', 'Designated PIO')} ({pio.get('designation', 'PIO')})\n"
                                       f"🏢 Office: {pio.get('office_address', 'District Headquarters')}\n"
                                       f"🚪 Room: {pio.get('room_no', 'Room 101')}\n"
                                       f"📏 Proximity: {pio.get('distance_label', 'Matched jurisdiction')}\n"
                                       f"📧 Official Email: {pio.get('email', 'pio@gov.in')}"
                        }
                    }]
                }
            },
            # 4. Section Heading: Draft RTI Record Questions (Section 2(f))
            {
                "object": "block",
                "type": "heading_2",
                "heading_2": {
                    "rich_text": [{"type": "text", "text": {"content": "3. Record-Based RTI Questions (Section 2(f))"}}]
                }
            }
        ]

        # Append RTI Questions
        questions = draft.get("questions", [])
        for idx, q in enumerate(questions[:4]):
            blocks.append({
                "object": "block",
                "type": "numbered_list_item",
                "numbered_list_item": {
                    "rich_text": [{"type": "text", "text": {"content": f"{q}"}}]
                }
            })

        # 5. Outside World Actions & Generated PDFs
        blocks.append({
            "object": "block",
            "type": "heading_2",
            "heading_2": {
                "rich_text": [{"type": "text", "text": {"content": "4. Outside World Actions & Official PDF Documents"}}]
            }
        })
        blocks.append({
            "object": "block",
            "type": "paragraph",
            "paragraph": {
                "rich_text": [
                    {"type": "text", "text": {"content": "📄 Download Official RTI Form-A PDF: "}},
                    {"type": "text", "text": {"content": f"{host_url}/api/v1/cases/{case_id}/pdf?type=rti", "link": {"url": f"{host_url}/api/v1/cases/{case_id}/pdf?type=rti"}}}
                ]
            }
        })
        blocks.append({
            "object": "block",
            "type": "paragraph",
            "paragraph": {
                "rich_text": [
                    {"type": "text", "text": {"content": "⚖️ Download Section 19(1) First Appeal PDF: "}},
                    {"type": "text", "text": {"content": f"{host_url}/api/v1/cases/{case_id}/pdf?type=appeal", "link": {"url": f"{host_url}/api/v1/cases/{case_id}/pdf?type=appeal"}}}
                ]
            }
        })

        return blocks

    def _find_notion_page_by_case_id(self, case_id: str) -> Optional[str]:
        """Queries Notion database to find page ID by Case ID property."""
        if not self.is_configured() or not self.cases_db_id:
            return None

        url = f"{self.api_base}/databases/{self.cases_db_id}/query"
        payload = {
            "filter": {
                "property": "Case ID",
                "title": {
                    "equals": case_id
                }
            }
        }
        try:
            resp = requests.post(url, headers=self.get_headers(), json=payload, timeout=8)
            if resp.status_code == 200:
                results = resp.json().get("results", [])
                if results:
                    return results[0].get("id")
        except Exception as e:
            logger.error(f"Error querying Notion page: {e}")
        return None

    # -------------------------------------------------------------------------
    # 2. RUN LOG DATABASE OPERATIONS (IMMUTABLE AUDIT PROOF)
    # -------------------------------------------------------------------------

    def log_run_to_notion(self, log_entry: Dict[str, Any]) -> Dict[str, Any]:
        """
        Appends an immutable audit row with authentic timestamp to Notion Run Log Database.
        """
        run_id = log_entry.get("run_id", f"RLOG-{int(time.time())}")
        timestamp = log_entry.get("timestamp", datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
        event_type = log_entry.get("event_type", "SYSTEM_EVENT")
        case_id = log_entry.get("case_id", "GLOBAL")
        actor = log_entry.get("actor", "ARZI Engine")
        action = log_entry.get("action", "")
        result = log_entry.get("result", "SUCCESS")
        correlation_id = log_entry.get("correlation_id", "CORR-001")

        properties = {
            "Run ID": {
                "title": [{"text": {"content": run_id}}]
            },
            "Timestamp": {
                "rich_text": [{"text": {"content": timestamp}}]
            },
            "Event Type": {
                "select": {"name": event_type[:100]}
            },
            "Case ID": {
                "rich_text": [{"text": {"content": case_id}}]
            },
            "Actor": {
                "rich_text": [{"text": {"content": actor}}]
            },
            "Action Description": {
                "rich_text": [{"text": {"content": action[:2000]}}]
            },
            "Result": {
                "select": {"name": result[:100]}
            },
            "Correlation ID": {
                "rich_text": [{"text": {"content": correlation_id}}]
            }
        }

        # Keep in-memory mirror
        self.mock_run_log_rows.insert(0, {
            "run_id": run_id,
            "timestamp": timestamp,
            "event_type": event_type,
            "case_id": case_id,
            "actor": actor,
            "action": action,
            "result": result,
            "correlation_id": correlation_id,
            "notion_synced_at": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        })
        self.sync_stats["total_synced_run_logs"] += 1

        # If live Notion API is configured, post row to Run Log DB
        if self.is_configured() and self.run_log_db_id:
            try:
                url = f"{self.api_base}/pages"
                payload = {
                    "parent": {"database_id": self.run_log_db_id},
                    "properties": properties
                }
                resp = requests.post(url, headers=self.get_headers(), json=payload, timeout=8)
                if resp.status_code in (200, 201):
                    return {"status": "logged_to_notion_api", "run_id": run_id}
            except Exception as e:
                logger.error(f"Error writing to Notion Run Log: {e}")

        return {"status": "logged_to_notion_mirror", "run_id": run_id}

    # -------------------------------------------------------------------------
    # 3. TWO-WAY HUMAN APPROVAL & DECISION POLLING
    # -------------------------------------------------------------------------

    def poll_human_decisions_from_notion(self, store_instance) -> List[Dict[str, Any]]:
        """
        Polls Notion Cases Database for human reviewer changes (Status changed to Approved,
        Department overrides, or Decision remarks).
        Applies changes to Flask backend and executes real-world outside actions.
        """
        decisions_processed = []

        if not self.is_configured() or not self.cases_db_id:
            return decisions_processed

        try:
            url = f"{self.api_base}/databases/{self.cases_db_id}/query"
            payload = {
                "filter": {
                    "property": "Status",
                    "select": {
                        "equals": "Approved & Dispatched"
                    }
                }
            }
            resp = requests.post(url, headers=self.get_headers(), json=payload, timeout=10)
            if resp.status_code == 200:
                results = resp.json().get("results", [])
                for page in results:
                    props = page.get("properties", {})
                    case_id_prop = props.get("Case ID", {}).get("title", [])
                    if not case_id_prop:
                        continue
                    case_id = case_id_prop[0].get("text", {}).get("content", "").strip()
                    
                    case = store_instance.get_case(case_id)
                    if case and case.get("status") != "APPROVED":
                        # Human approved in Notion! Execute outside world action
                        reviewer = "Advocate Reviewer (via Notion Interface)"
                        store_instance.approve_case(case_id, reviewer=reviewer, notes="Approved directly inside Notion Cases Workspace.")
                        self.sync_stats["human_decisions_processed"] += 1
                        decisions_processed.append({
                            "case_id": case_id,
                            "action": "APPROVED_FROM_NOTION",
                            "reviewer": reviewer
                        })
                        logger.info(f"Engine processed Notion Human Approval for Case {case_id}")
        except Exception as e:
            logger.error(f"Error polling Notion decisions: {e}")

        return decisions_processed

    # -------------------------------------------------------------------------
    # 4. 1-CLICK NOTION WORKSPACE SETUP (CREATES NOTION SCHEMAS AUTOMATICALLY)
    # -------------------------------------------------------------------------

    def setup_notion_workspace_schema(self, parent_page_id: str) -> Dict[str, Any]:
        """
        Programmatically provisions the Cases and Run Log Databases under a given parent page.
        """
        if not self.api_key:
            return {"error": "Notion API key required to create workspace schema."}

        self.parent_page_id = parent_page_id

        # 1. Create Cases Database Schema
        cases_schema = {
            "parent": {"page_id": parent_page_id},
            "title": [{"type": "text", "text": {"content": "ARZI — Cases & Dockets Database"}}],
            "properties": {
                "Case ID": {"title": {}},
                "Complainant": {"rich_text": {}},
                "Department": {
                    "select": {
                        "options": [
                            {"name": "Revenue & Land Records", "color": "orange"},
                            {"name": "Food & Civil Supplies", "color": "blue"},
                            {"name": "Municipal Public Works & Drainage", "color": "purple"},
                            {"name": "Police & Law Enforcement", "color": "red"},
                            {"name": "Higher Education & Student Welfare", "color": "green"}
                        ]
                    }
                },
                "Status": {
                    "select": {
                        "options": [
                            {"name": "Needs Human Review", "color": "yellow"},
                            {"name": "Approved & Dispatched", "color": "green"},
                            {"name": "Transferred Sec 6(3)", "color": "purple"},
                            {"name": "Merged Duplicate", "color": "gray"}
                        ]
                    }
                },
                "Merit Score": {"number": {"format": "number"}},
                "SLA Days Remaining": {"number": {"format": "number"}},
                "Sec 20 Penalty (INR)": {"number": {"format": "rupee"}},
                "Nearest Assigned PIO": {"rich_text": {}},
                "IPC & BNS Sections": {"multi_select": {}},
                "Tracking ID": {"rich_text": {}}
            }
        }

        # 2. Create Run Log Database Schema
        run_log_schema = {
            "parent": {"page_id": parent_page_id},
            "title": [{"type": "text", "text": {"content": "ARZI — Immutable Run Log Database"}}],
            "properties": {
                "Run ID": {"title": {}},
                "Timestamp": {"rich_text": {}},
                "Event Type": {
                    "select": {
                        "options": [
                            {"name": "INTAKE_INGESTED", "color": "blue"},
                            {"name": "HUMAN_APPROVED", "color": "green"},
                            {"name": "DISPATCH_EXECUTED", "color": "green"},
                            {"name": "SECTION_6_3_TRANSFERRED", "color": "purple"},
                            {"name": "CUSTOM_ACT_REGISTERED", "color": "orange"},
                            {"name": "KILL_SWITCH_ENGAGED", "color": "red"}
                        ]
                    }
                },
                "Case ID": {"rich_text": {}},
                "Actor": {"rich_text": {}},
                "Action Description": {"rich_text": {}},
                "Result": {
                    "select": {
                        "options": [
                            {"name": "SUCCESS", "color": "green"},
                            {"name": "PENDING_HUMAN_APPROVAL", "color": "yellow"},
                            {"name": "DISPATCHED", "color": "green"},
                            {"name": "TRANSFERRED", "color": "purple"}
                        ]
                    }
                },
                "Correlation ID": {"rich_text": {}}
            }
        }

        created = {}
        try:
            # Create Cases DB
            resp1 = requests.post(f"{self.api_base}/databases", headers=self.get_headers(), json=cases_schema, timeout=12)
            if resp1.status_code in (200, 201):
                self.cases_db_id = resp1.json().get("id")
                created["cases_db_id"] = self.cases_db_id
                created["cases_db_url"] = resp1.json().get("url")

            # Create Run Log DB
            resp2 = requests.post(f"{self.api_base}/databases", headers=self.get_headers(), json=run_log_schema, timeout=12)
            if resp2.status_code in (200, 201):
                self.run_log_db_id = resp2.json().get("id")
                created["run_log_db_id"] = self.run_log_db_id
                created["run_log_db_url"] = resp2.json().get("url")

            return {"status": "success", "created": created}
        except Exception as e:
            return {"status": "error", "message": str(e)}

# Global Singleton Service
notion_service = NotionSyncService()

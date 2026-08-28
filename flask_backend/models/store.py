import threading
import time
import hashlib
from datetime import datetime, timedelta
from pydantic import BaseModel, ConfigDict

class YourModel(BaseModel):
    model_config = ConfigDict(protected_namespaces=()) # Add this line
    model_version: str
class DataStore:
    def __init__(self):
        self._lock = threading.RLock()
        self.cases = {}
        self.run_logs = []
        self.pio_directory = [
            {
                "department": "Revenue & Land Records",
                "pio_name": "Shri N. Goyal",
                "designation": "Tehsildar & Designated PIO",
                "office_address": "Tehsil & District Kachehri Complex, Revenue Circle 2, Mehrauli, New Delhi - 110030",
                "email": "pio.revenue.mehrauli@gov.in",
                "phone": "+91-11-26641209",
                "jurisdiction_keywords": [
                    "land", "zameen", "property", "khasra", "khatauni", "mutation", 
                    "daakhil kharij", "patwari", "tehsildar", "registry", "land deed", 
                    "katcheri", "demarcation", "seema gyan", "jamabandi", "plot", 
                    "land record", "revenue", "katcheri", "khatoni", "dakhil kharij", "lekhpal"
                ]
            },
            {
                "department": "Food & Civil Supplies",
                "pio_name": "Shri R. K. Sharma",
                "designation": "Public Information Officer & Assistant Commissioner",
                "office_address": "Office of the District Supply Officer, Sub-Divisional Tehsil Kachehri Complex, Ward 4, Civil Lines, New Delhi - 110054",
                "email": "pio.foodsupplies.ward4@gov.in",
                "phone": "+91-11-23891042",
                "jurisdiction_keywords": [
                    "ration", "rashan", "food", "khadya", "grain", "bpl", 
                    "bpl card", "ration card", "pds shop", "fair price shop", 
                    "dealer", "rasan", "khadya rasad"
                ]
            },
            {
                "department": "Municipal Public Works & Drainage",
                "pio_name": "Er. S. K. Kalra",
                "designation": "Executive Engineer (Drainage & Stormwater)",
                "office_address": "Municipal Kachehri Complex, Zone 7, Sector 12, Dwarka, New Delhi - 110075",
                "email": "pio.drainage.zone7@mc.gov.in",
                "phone": "+91-11-25083110",
                "jurisdiction_keywords": [
                    "drainage", "waterlogging", "sewer line", "gutter", "monsoon overflow", 
                    "road repair", "drain", "sewer", "nalla", "nadi", "sadak", "pothole", "municipal",
                    "nagar nigam", "naali", "kachra", "street light"
                ]
            },
            {
                "department": "Higher Education & Student Welfare",
                "pio_name": "Dr. T. Tiwari",
                "designation": "Deputy Registrar & PIO (Scholarships)",
                "office_address": "State Scholarship Cell, District Education Kachehri, Rajpur Road, New Delhi - 110007",
                "email": "scholarships.pio@edu.gov.in",
                "phone": "+91-11-23954200",
                "jurisdiction_keywords": [
                    "scholarship", "disbursement", "tuition fee waiver", "post-matric scholarship", 
                    "student grant", "college", "university", "education", "chhatravriti", "student",
                    "bhu", "kashi vidyapith", "fee waiver"
                ]
            },
            {
                "department": "Police & Law Enforcement",
                "pio_name": "Shri V. K. Malhotra",
                "designation": "Additional Deputy Commissioner of Police & Designated PIO",
                "office_address": "Police Headquarters, Civic Center Kachehri, New Delhi - 110001",
                "email": "pio.police@delhipolice.gov.in",
                "phone": "+91-11-23314567",
                "jurisdiction_keywords": [
                    "police", "fir", "complaint", "thana", "daroga", "cop", 
                    "investigation", "challan", "police station", "crime", "chori", "theft"
                ]
            },
            {
                "department": "Health & Family Welfare",
                "pio_name": "Dr. A. K. Gupta",
                "designation": "Chief Medical Officer & Designated PIO",
                "office_address": "Directorate of Health Services, Civil Hospital Complex, New Delhi - 110002",
                "email": "pio.health@dhs.gov.in",
                "phone": "+91-11-22301234",
                "jurisdiction_keywords": [
                    "health", "hospital", "doctor", "medicine", "dawa", "ilaj", 
                    "cmo", "dispensary", "medical", "treatment", "swasthya", "aspatal"
                ]
            }
        ]
        self._seed_initial_data()

    def _seed_initial_data(self):
        with self._lock:
            now = datetime.now()

            # Seed 1: Ration Card Delay Case
            c1_id = "ARZ-1042"
            c1 = {
                "case_id": c1_id,
                "complainant": {
                    "name": "Sunita Devi",
                    "contact": "+91-9876543210",
                    "address": "House No. 45, BPL Cluster, Ward 4, New Delhi",
                    "language": "Hindi / English"
                },
                "raw_grievance": "My family's BPL ration card application (Ref No. RC-88492) was submitted 6 months ago at Ward 4 supply office. We have not received the card or food grains.",
                "category": "Food & Civil Supplies",
                "department": "Food & Civil Supplies",
                "application_ref_no": "RC-88492",
                "original_submission_date": "15-Feb-2026",
                "suggested_pio": self.pio_directory[1],
                "confidence": {
                    "overall": 96,
                    "department_confidence": 96,
                    "jurisdiction_confidence": 96,
                    "location_matched": True,
                    "user_locality": "Ward 4, Civil Lines",
                    "draft_confidence": 94,
                    "risk_level": "LOW",
                    "evidence_gaps": []
                },
                "status": "NEEDS_REVIEW",
                "priority": "HIGH",
                "sla_days_remaining": 2,
                "due_date": (now + timedelta(days=28)).strftime("%Y-%m-%d"),
                "created_at": (now - timedelta(hours=3)).strftime("%Y-%m-%d %H:%M:%S"),
                "updated_at": (now - timedelta(hours=3)).strftime("%Y-%m-%d %H:%M:%S"),
                "draft_rti": {
                    "application_subject": "Application under Section 6(1) of RTI Act 2005 seeking status on pending grievance (Ref No: RC-88492, Submitted: 15-Feb-2026) in Ward 4, Civil Lines regarding Food & Civil Supplies",
                    "questions": [
                        "1. Please provide the daily progress report and certified file movement register regarding the original grievance application (Ref No: RC-88492) submitted on 15-Feb-2026 by Sunita Devi residing in Ward 4, a copy whereof is annexed herewith as Annexure-A.",
                        "2. Please specify the names, designations, and official contact details of all dealing officers/staff members at Ward 4 Civil Lines office with whom this matter remained pending beyond the 30-day statutory limit.",
                        "3. What is the prescribed timeline as per the Citizen Charter for resolving this class of public grievance?",
                        "4. Please disclose the month-wise stock position and BPL entitlement distribution register copy for the concerned Fair Price Shop serving Ward 4.",
                        "5. Please disclose certified copies of all existing file notings, office correspondence, processing sheets, inspection reports, and official orders recorded on file regarding the processing and current disposal status of the aforesaid grievance application."
                    ],
                    "fees_paid": "Rs. 10 Indian Postal Order (IPO No: 45F-992011, Dated: 15-Feb-2026, Issued by GPO Delhi) attached towards prescribed application fee under Rule 3 of RTI Rules 2012.",
                    "version": 1
                },
                "update_history": [
                    {
                        "timestamp": (now - timedelta(hours=3)).strftime("%Y-%m-%d %H:%M:%S.102"),
                        "update_type": "INTAKE_INGESTED",
                        "actor": "System Intake Gateway",
                        "field_changed": "Case Intake",
                        "old_value": "None",
                        "new_value": "Case ARZ-1042 created",
                        "remarks": "Initial ingestion of grievance for Sunita Devi"
                    }
                ],
                "reviewer": None,
                "approval_notes": None,
                "dispatch_info": None
            }
            self.cases[c1_id] = c1

            # Seed 2: Primary Target Case ARZ-1046 (With audit trail of overrides & in-place complainant fix)
            c46_id = "ARZ-1046"
            t1 = (now - timedelta(minutes=90)).strftime("%Y-%m-%d %H:%M:%S.104")
            t2 = (now - timedelta(minutes=89, seconds=45)).strftime("%Y-%m-%d 20:57:26.110")
            t3 = (now - timedelta(minutes=89, seconds=30)).strftime("%Y-%m-%d 20:57:41.892")
            t4 = (now - timedelta(minutes=79)).strftime("%Y-%m-%d 21:07:00.014")

            c46 = {
                "case_id": c46_id,
                "complainant": {
                    "name": "Shivanshu Pandey",
                    "contact": "+91-9988776655",
                    "address": "Sector 4, Mehrauli, New Delhi",
                    "language": "Hindi / English"
                },
                "raw_grievance": "My land mutation khasra 45/12 application (Ref LND-88301) submitted on 10-Jan-2026 at Tehsil office Mehrauli is pending. Patwari is not updating land record registry.",
                "category": "Revenue & Land Records",
                "department": "Revenue & Land Records",
                "application_ref_no": "LND-88301",
                "original_submission_date": "10-Jan-2026",
                "suggested_pio": self.pio_directory[0], # Revenue & Land Records
                "confidence": {
                    "overall": 98,
                    "department_confidence": 98,
                    "jurisdiction_confidence": 96,
                    "location_matched": True,
                    "user_locality": "Mehrauli",
                    "draft_confidence": 96,
                    "risk_level": "LOW",
                    "evidence_gaps": []
                },
                "status": "NEEDS_REVIEW",
                "priority": "HIGH",
                "sla_days_remaining": 14,
                "due_date": (now + timedelta(days=16)).strftime("%Y-%m-%d"),
                "created_at": t1,
                "updated_at": t4,
                "draft_rti": {
                    "application_subject": "Application under Section 6(1) of RTI Act 2005 seeking status on pending grievance (Ref No: LND-88301, Submitted: 10-Jan-2026) in Mehrauli regarding Revenue & Land Records",
                    "questions": [
                        "1. Please provide the daily progress report and certified file movement register regarding the original grievance application (Ref No: LND-88301) submitted on 10-Jan-2026 by Shivanshu Pandey residing in Mehrauli, a copy whereof is annexed herewith as Annexure-A.",
                        "2. Please specify the names, designations, and official contact details of all dealing officers/staff members at Mehrauli division office with whom this matter remained pending beyond the 30-day statutory limit.",
                        "3. What is the prescribed timeline as per the Citizen Charter for resolving this class of public grievance?",
                        "4. Please disclose certified copies of Khasra/Khatauni mutations, field inspection reports, and Patwari notes issued for the concerned land parcel in Mehrauli.",
                        "5. Please disclose certified copies of all existing file notings, office correspondence, processing sheets, inspection reports, and official orders recorded on file regarding the processing and current disposal status of the aforesaid grievance application."
                    ],
                    "fees_paid": "Rs. 10 Indian Postal Order (IPO No: 45F-LND992, Dated: 10-Jan-2026, Issued at PO Mehrauli) payable to Accounts Officer, Revenue & Land Records attached under Rule 3 & Rule 6 of Central RTI Rules 2012.",
                    "version": 3
                },
                "update_history": [
                    {
                        "timestamp": t1,
                        "update_type": "INTAKE_INGESTED",
                        "actor": "System Intake Gateway",
                        "field_changed": "Case Ingestion",
                        "old_value": "None",
                        "new_value": "Case ARZ-1046 created",
                        "remarks": "Initial grievance intake ingested (Ref: LND-88301)"
                    },
                    {
                        "timestamp": t2, # 20:57:26
                        "update_type": "DEPT_OVERRIDE_MISTAKE",
                        "actor": "Legal Operator",
                        "field_changed": "Target Department",
                        "old_value": "Revenue & Land Records",
                        "new_value": "Food & Civil Supplies",
                        "remarks": "Erroneous manual operator override"
                    },
                    {
                        "timestamp": t3, # 20:57:41 (15 sec later)
                        "update_type": "DEPT_OVERRIDE_CORRECTED",
                        "actor": "Legal Operator",
                        "field_changed": "Target Department",
                        "old_value": "Food & Civil Supplies",
                        "new_value": "Revenue & Land Records",
                        "remarks": "Operator corrected department back to Revenue & Land Records"
                    },
                    {
                        "timestamp": t4, # 21:07:00
                        "update_type": "INPLACE_COMPLAINANT_FIX",
                        "actor": "Adv. S. Kalra (Legal NGO)",
                        "field_changed": "Complainant Name & Duplicacy Resolution",
                        "old_value": "Samiksha (Accidental intake entry)",
                        "new_value": "Shivanshu Pandey (Authentic Complainant)",
                        "remarks": "Corrected complainant details in-place on ARZ-1046; merged duplicate draft ARZ-1047 into ARZ-1046."
                    }
                ],
                "reviewer": None,
                "approval_notes": None,
                "dispatch_info": None
            }
            self.cases[c46_id] = c46

            # Seed 3: Duplicate Case ARZ-1047 Marked as Merged to Avoid Loophole
            c47_id = "ARZ-1047"
            c47 = {
                "case_id": c47_id,
                "complainant": {
                    "name": "Shivanshu Pandey (Merged Duplicate)",
                    "contact": "+91-9988776655",
                    "address": "Sector 4, Mehrauli, New Delhi",
                    "language": "Hindi / English"
                },
                "raw_grievance": "Duplicate submission for land mutation khasra 45/12.",
                "category": "Revenue & Land Records",
                "department": "Revenue & Land Records",
                "application_ref_no": "LND-88301",
                "original_submission_date": "10-Jan-2026",
                "suggested_pio": self.pio_directory[0],
                "confidence": {
                    "overall": 99,
                    "risk_level": "LOW",
                    "evidence_gaps": []
                },
                "status": "MERGED_DUPLICATE",
                "priority": "LOW",
                "sla_days_remaining": 0,
                "due_date": (now + timedelta(days=16)).strftime("%Y-%m-%d"),
                "created_at": t4,
                "updated_at": t4,
                "draft_rti": {
                    "application_subject": "MERGED DUPLICATE ENTRY - SEE MASTER CASE ARZ-1046",
                    "questions": [],
                    "fees_paid": "N/A",
                    "version": 1
                },
                "update_history": [
                    {
                        "timestamp": t4,
                        "update_type": "DUPLICATE_MERGED",
                        "actor": "Adv. S. Kalra (Legal NGO)",
                        "field_changed": "Case Status",
                        "old_value": "NEEDS_REVIEW",
                        "new_value": "MERGED_DUPLICATE",
                        "remarks": "Merged duplicate entry into primary Master Case ARZ-1046 to prevent legal duplication."
                    }
                ],
                "merged_into_case_id": "ARZ-1046",
                "reviewer": "Adv. S. Kalra",
                "approval_notes": "Merged duplicate into ARZ-1046.",
                "dispatch_info": None
            }
            self.cases[c47_id] = c47

            # Seed Run Logs for Proof Audit Screen
            self.add_run_log(
                event_type="INTAKE_RECEIVED",
                case_id="ARZ-1046",
                actor="System Ingestion Gateway",
                source="Web Intake Portal",
                action="Grievance ingested for Land Mutation khasra 45/12 (Ref: LND-88301)",
                result="SUCCESS",
                correlation_id="CORR-104601"
            )
            self.add_run_log(
                event_type="DEPT_OVERRIDE_CORRECTED",
                case_id="ARZ-1046",
                actor="Legal Operator",
                source="Approval Workspace",
                action="Operator corrected department from Food & Civil Supplies -> Revenue & Land Records (15-sec correction)",
                result="OVERRIDE_SUCCESS",
                correlation_id="CORR-104602"
            )
            self.add_run_log(
                event_type="INPLACE_COMPLAINANT_FIX",
                case_id="ARZ-1046",
                actor="Adv. S. Kalra (Legal NGO)",
                source="Approval Workspace",
                action="Corrected complainant name in-place from 'Samiksha' to 'Shivanshu Pandey' & resolved duplicacy with ARZ-1047",
                result="INPLACE_UPDATE_SUCCESS",
                correlation_id="CORR-104603"
            )

    def add_case(self, case_data: dict) -> dict:
        with self._lock:
            # Check for existing duplicate by complainant contact or reference number
            ref_no = case_data.get("application_ref_no")
            contact = case_data.get("complainant", {}).get("contact")

            existing_case = None
            if ref_no and ref_no not in ("Not Provided", "Unconfirmed"):
                for c in self.cases.values():
                    if c.get("application_ref_no") == ref_no and c["status"] != "MERGED_DUPLICATE":
                        existing_case = c
                        break

            if existing_case:
                # Update existing case IN-PLACE rather than creating a duplicate case ID!
                case_id = existing_case["case_id"]
                now_str = datetime.now().strftime("%Y-%m-%d %H:%M:%S.%f")[:-3]

                old_name = existing_case["complainant"].get("name")
                new_name = case_data["complainant"].get("name")

                existing_case["complainant"] = case_data["complainant"]
                existing_case["raw_grievance"] = case_data["raw_grievance"]
                existing_case["updated_at"] = now_str[:19]

                history_entry = {
                    "timestamp": now_str,
                    "update_type": "INPLACE_GRIEVANCE_UPDATE",
                    "actor": "Intake Gateway / Legal Reviewer",
                    "field_changed": "Complainant Details & Narrative",
                    "old_value": f"Complainant: {old_name}",
                    "new_value": f"Complainant: {new_name}",
                    "remarks": f"Updated existing Master Case {case_id} in-place without spawning duplicate case ID."
                }
                existing_case.setdefault("update_history", []).append(history_entry)

                self.add_run_log(
                    event_type="INPLACE_GRIEVANCE_UPDATE",
                    case_id=case_id,
                    actor="Intake Gateway / Legal Reviewer",
                    source="Web Intake Portal",
                    action=f"Updated Master Case {case_id} in-place for complainant {new_name} (Prevented duplicate case creation)",
                    result="INPLACE_SUCCESS",
                    correlation_id=f"CORR-{hashlib.md5(case_id.encode()).hexdigest()[:6]}"
                )
                return existing_case

            # Create new case with guaranteed strictly unique Case ID (e.g. ARZ-1048, ARZ-1049, etc.)
            existing_nums = [1047]
            for cid in self.cases.keys():
                if cid.startswith("ARZ-"):
                    try:
                        num = int(cid.split("-")[1])
                        existing_nums.append(num)
                    except ValueError:
                        pass
            next_num = max(existing_nums) + 1
            case_id = f"ARZ-{next_num}"

            case_data["case_id"] = case_id
            now_str = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            case_data["created_at"] = now_str
            case_data["updated_at"] = now_str

            history_entry = {
                "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S.%f")[:-3],
                "update_type": "INTAKE_INGESTED",
                "actor": "Citizen Intake Gateway",
                "field_changed": "Case Intake",
                "old_value": "None",
                "new_value": f"Case {case_id} created",
                "remarks": f"Created new case for complainant {case_data['complainant']['name']}"
            }
            case_data["update_history"] = [history_entry]
            self.cases[case_id] = case_data

            self.add_run_log(
                event_type="INTAKE_RECEIVED",
                case_id=case_id,
                actor="Citizen Intake Gateway",
                source="Web Portal Form",
                action=f"Created case {case_id} for complainant {case_data['complainant']['name']}",
                result="SUCCESS",
                correlation_id=f"CORR-{hashlib.md5(case_id.encode()).hexdigest()[:6]}"
            )
            return case_data

    def get_case(self, case_id: str) -> dict:
        with self._lock:
            return self.cases.get(case_id)

    def get_all_cases(self) -> list:
        with self._lock:
            return list(self.cases.values())

    def update_case(self, case_id: str, updates: dict, audit_meta: dict = None) -> dict:
        with self._lock:
            if case_id in self.cases:
                now_str = datetime.now().strftime("%Y-%m-%d %H:%M:%S.%f")[:-3]
                self.cases[case_id].update(updates)
                self.cases[case_id]["updated_at"] = now_str[:19]

                if audit_meta:
                    history_entry = {
                        "timestamp": now_str,
                        "update_type": audit_meta.get("update_type", "CASE_UPDATED"),
                        "actor": audit_meta.get("actor", "Legal Operator"),
                        "field_changed": audit_meta.get("field_changed", "Case Details"),
                        "old_value": audit_meta.get("old_value", "Previous State"),
                        "new_value": audit_meta.get("new_value", "Updated State"),
                        "remarks": audit_meta.get("remarks", "Updated case details")
                    }
                    self.cases[case_id].setdefault("update_history", []).append(history_entry)

                return self.cases[case_id]
            return None

    def merge_cases(self, master_case_id: str, duplicate_case_id: str, actor: str = "Adv. S. Kalra") -> dict:
        """Merge a duplicate case ID into a primary master case ID to eliminate legal duplication."""
        with self._lock:
            master = self.cases.get(master_case_id)
            duplicate = self.cases.get(duplicate_case_id)

            if not master or not duplicate:
                return None

            now_str = datetime.now().strftime("%Y-%m-%d %H:%M:%S.%f")[:-3]
            duplicate["status"] = "MERGED_DUPLICATE"
            duplicate["merged_into_case_id"] = master_case_id
            duplicate["updated_at"] = now_str[:19]

            dup_history = {
                "timestamp": now_str,
                "update_type": "DUPLICATE_MERGED",
                "actor": actor,
                "field_changed": "Status",
                "old_value": duplicate.get("status"),
                "new_value": f"MERGED_DUPLICATE into {master_case_id}",
                "remarks": f"Merged duplicate case {duplicate_case_id} into Master Case {master_case_id} to prevent legal confusion."
            }
            duplicate.setdefault("update_history", []).append(dup_history)

            master_history = {
                "timestamp": now_str,
                "update_type": "DUPLICATE_RESOLVED",
                "actor": actor,
                "field_changed": "Case Duplicacy Status",
                "old_value": f"Duplicate Case {duplicate_case_id} Pending",
                "new_value": f"Merged {duplicate_case_id} into Master Case",
                "remarks": f"Resolved duplicate case loop; consolidated all facts into Master Case {master_case_id}."
            }
            master.setdefault("update_history", []).append(master_history)

            self.add_run_log(
                event_type="DUPLICATE_CASE_MERGED",
                case_id=master_case_id,
                actor=actor,
                source="Legal Review Workspace",
                action=f"Merged duplicate case {duplicate_case_id} into Master Case {master_case_id}",
                result="MERGE_SUCCESS",
                correlation_id=f"CORR-MERGE-{master_case_id}"
            )

            return master

    def add_run_log(self, event_type: str, case_id: str, actor: str, source: str, action: str, result: str, correlation_id: str):
        with self._lock:
            log_entry = {
                "run_id": f"RLOG-{len(self.run_logs) + 5001}",
                "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S.%f")[:-3],
                "event_type": event_type,
                "case_id": case_id,
                "actor": actor,
                "source": source,
                "action": action,
                "result": result,
                "correlation_id": correlation_id
            }
            self.run_logs.insert(0, log_entry)
            return log_entry

    def get_run_logs(self, limit: int = 50) -> list:
        with self._lock:
            return self.run_logs[:limit]

# Global store instance
db_store = DataStore()

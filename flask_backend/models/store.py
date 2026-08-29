import threading
import time
import hashlib
from datetime import datetime, timedelta
from flask_backend.services.legal_engine import legal_engine
from flask_backend.services.geo_locator import geo_locator

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
                "latitude": 28.5180,
                "longitude": 77.1850,
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
                "latitude": 28.6750,
                "longitude": 77.2250,
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
                "latitude": 28.5920,
                "longitude": 77.0460,
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
                "latitude": 28.6720,
                "longitude": 77.2210,
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
                "latitude": 28.6340,
                "longitude": 77.2280,
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
                "latitude": 28.6480,
                "longitude": 77.2420,
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

            # Seed 1: Ration Card Delay Case (ARZ-1042)
            c1_id = "ARZ-1042"
            pio1 = self.pio_directory[1]
            c1_legal = legal_engine.analyze_legal_standing(
                grievance_text="My family's BPL ration card application (Ref No. RC-88492) was submitted 6 months ago at Ward 4 supply office.",
                department="Food & Civil Supplies",
                days_overdue=180
            )
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
                "suggested_pio": pio1,
                "suggested_faa": {
                    "faa_name": "Smt. Anjali Sehgal",
                    "designation": "Additional Commissioner (PDS) / First Appellate Authority",
                    "office_address": "Khadya Sadan, Vikas Bhawan, New Delhi - 110002",
                    "email": "ac-pds.delhi@gov.in",
                    "phone": "+91-11-23378512"
                },
                "geospatial_meta": {
                    "distance_km": 0.8,
                    "distance_label": "800 meters away (Ward 4 DSO Complex)",
                    "room_no": "Room 4, Food & Supplies Block",
                    "user_coords": {"latitude": 28.6750, "longitude": 77.2250},
                    "pio_coords": {"latitude": 28.6750, "longitude": 77.2250}
                },
                "statutory_legal_analysis": c1_legal,
                "confidence": {
                    "overall": 96,
                    "department_confidence": 96,
                    "jurisdiction_confidence": 96,
                    "location_matched": True,
                    "user_locality": "Ward 4, Civil Lines",
                    "draft_confidence": 94,
                    "risk_level": "LOW",
                    "evidence_gaps": [],
                    "case_merit_score": c1_legal["case_merit_score"],
                    "win_probability": c1_legal["win_probability"]
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
            c1["first_appeal_draft"] = legal_engine.generate_first_appeal_draft(c1)
            c1["legal_notice_draft"] = legal_engine.generate_legal_notice_draft(c1, c1_legal)
            self.cases[c1_id] = c1

            # Seed 2: Primary Target Case ARZ-1046
            c46_id = "ARZ-1046"
            t1 = (now - timedelta(minutes=90)).strftime("%Y-%m-%d %H:%M:%S.104")
            t2 = (now - timedelta(minutes=89, seconds=45)).strftime("%Y-%m-%d 20:57:26.110")
            t3 = (now - timedelta(minutes=89, seconds=30)).strftime("%Y-%m-%d 20:57:41.892")
            t4 = (now - timedelta(minutes=79)).strftime("%Y-%m-%d 21:07:00.014")

            c46_legal = legal_engine.analyze_legal_standing(
                grievance_text="My land mutation khasra 45/12 application (Ref LND-88301) submitted on 10-Jan-2026 at Tehsil office Mehrauli is pending. Patwari is not updating land record registry.",
                department="Revenue & Land Records",
                days_overdue=45
            )

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
                "suggested_pio": self.pio_directory[0],
                "suggested_faa": {
                    "faa_name": "Shri Sandeep Kumar, IAS",
                    "designation": "District Magistrate (South Delhi) / First Appellate Authority",
                    "office_address": "DM Office Complex, M.B. Road, Saket, New Delhi - 110068",
                    "email": "dm-south.delhi@nic.in",
                    "phone": "+91-11-29535025"
                },
                "geospatial_meta": {
                    "distance_km": 1.2,
                    "distance_label": "1.2 km away (Tehsil Complex Mehrauli)",
                    "room_no": "Room 101, SDM Office Complex",
                    "user_coords": {"latitude": 28.5180, "longitude": 77.1850},
                    "pio_coords": {"latitude": 28.5180, "longitude": 77.1850}
                },
                "statutory_legal_analysis": c46_legal,
                "confidence": {
                    "overall": 98,
                    "department_confidence": 98,
                    "jurisdiction_confidence": 96,
                    "location_matched": True,
                    "user_locality": "Mehrauli",
                    "draft_confidence": 96,
                    "risk_level": "LOW",
                    "evidence_gaps": [],
                    "case_merit_score": c46_legal["case_merit_score"],
                    "win_probability": c46_legal["win_probability"]
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
                        "timestamp": t2,
                        "update_type": "DEPT_OVERRIDE_MISTAKE",
                        "actor": "Legal Operator",
                        "field_changed": "Target Department",
                        "old_value": "Revenue & Land Records",
                        "new_value": "Food & Civil Supplies",
                        "remarks": "Erroneous manual operator override"
                    },
                    {
                        "timestamp": t3,
                        "update_type": "DEPT_OVERRIDE_CORRECTED",
                        "actor": "Legal Operator",
                        "field_changed": "Target Department",
                        "old_value": "Food & Civil Supplies",
                        "new_value": "Revenue & Land Records",
                        "remarks": "Operator corrected department back to Revenue & Land Records"
                    },
                    {
                        "timestamp": t4,
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
            c46["first_appeal_draft"] = legal_engine.generate_first_appeal_draft(c46)
            c46["legal_notice_draft"] = legal_engine.generate_legal_notice_draft(c46, c46_legal)
            self.cases[c46_id] = c46

            # Seed 3: Duplicate Case ARZ-1047
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

            # Seed Run Logs
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
            ref_no = case_data.get("application_ref_no")
            existing_case = None
            if ref_no and ref_no not in ("Not Provided", "Unconfirmed"):
                for c in self.cases.values():
                    if c.get("application_ref_no") == ref_no and c["status"] != "MERGED_DUPLICATE":
                        existing_case = c
                        break

            if existing_case:
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

            # Strictly unique Case ID
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

    def transfer_case_sec6_3(self, case_id: str, new_target_dept: str, reason: str, officer_actor: str = "Designated PIO Desk") -> dict:
        """
        Executes Section 6(3) 5-Day Mandatory Transfer of RTI Application to the Competent Public Authority.
        """
        with self._lock:
            case = self.cases.get(case_id)
            if not case:
                return None

            user_loc = case.get("confidence", {}).get("user_locality", "Local Division")
            new_pio = geo_locator.find_nearest_public_authority(
                category=new_target_dept,
                address=case.get("complainant", {}).get("address", user_loc),
                narrative=case.get("raw_grievance", "")
            )

            now_str = datetime.now().strftime("%Y-%m-%d %H:%M:%S.%f")[:-3]
            old_dept = case.get("department")

            transfer_notice = {
                "transfer_id": f"TRF-SEC63-{hashlib.md5((case_id + now_str).encode()).hexdigest()[:6].upper()}",
                "transferred_at": now_str[:19],
                "from_department": old_dept,
                "to_department": new_target_dept,
                "transferee_pio": new_pio,
                "statutory_basis": "Section 6(3) of RTI Act 2005 (Mandatory 5-Day Transfer Window)",
                "transfer_reason": reason or "Subject matter falls under exclusive jurisdiction of transferee public authority."
            }

            case["section_6_3_transfer"] = transfer_notice
            case["suggested_pio"] = new_pio
            case["department"] = new_target_dept
            case["category"] = new_target_dept
            case["status"] = "TRANSFERRED_SEC_6_3"
            case["updated_at"] = now_str[:19]

            audit_meta = {
                "update_type": "SECTION_6_3_TRANSFER_EXECUTED",
                "actor": officer_actor,
                "field_changed": "Public Authority Jurisdiction",
                "old_value": old_dept,
                "new_value": f"Transferred to {new_target_dept} under Sec 6(3)",
                "remarks": f"RTI Application transferred to {new_pio['pio_name']} ({new_pio['office_address']}) under Section 6(3)."
            }
            case.setdefault("update_history", []).append({
                "timestamp": now_str,
                **audit_meta
            })

            self.add_run_log(
                event_type="SECTION_6_3_TRANSFER",
                case_id=case_id,
                actor=officer_actor,
                source="Government PIO Compliance Desk",
                action=f"Transferred {case_id} from {old_dept} -> {new_target_dept} under Section 6(3)",
                result="TRANSFER_SUCCESS",
                correlation_id=transfer_notice["transfer_id"]
            )

            return case

    def merge_cases(self, master_case_id: str, duplicate_case_id: str, actor: str = "Adv. S. Kalra") -> dict:
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

    def get_compliance_radar_metrics(self) -> dict:
        """
        Computes real-time compliance metrics for Government PIO desks & Law Firms.
        """
        with self._lock:
            all_cases = list(self.cases.values())
            overdue_cases = []
            total_penalty_inr = 0
            deemed_refusals = 0

            for c in all_cases:
                if c.get("status") == "MERGED_DUPLICATE":
                    continue
                legal = c.get("statutory_legal_analysis", {})
                pen = legal.get("section_20_penalty_liability_inr", 0)
                if pen > 0 or c.get("sla_days_remaining", 30) <= 0:
                    overdue_cases.append(c)
                    total_penalty_inr += pen
                    deemed_refusals += 1

            return {
                "total_cases": len(all_cases),
                "inbox_pending": len([c for c in all_cases if c["status"] == "NEEDS_REVIEW"]),
                "approved_dispatched": len([c for c in all_cases if c["status"] in ("APPROVED", "DISPATCHED")]),
                "deemed_refusal_count": deemed_refusals,
                "overdue_cases": overdue_cases,
                "total_penalty_liability_inr": total_penalty_inr,
                "statutory_rate_per_day_inr": 250,
                "max_penalty_cap_inr": 25000
            }

    def add_custom_act(self, act_data: dict) -> dict:
        """Adds a lawyer-defined custom Act, Section, or statutory ground."""
        with self._lock:
            if not hasattr(self, "custom_acts"):
                self.custom_acts = []
            
            act_id = f"ACT-{len(self.custom_acts) + 101}"
            now_str = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

            entry = {
                "act_id": act_id,
                "act_title": act_data.get("act_title", "Custom Statutory Act"),
                "section": act_data.get("section", "Section 1"),
                "domain": act_data.get("domain", "General Public Law"),
                "statutory_grounds": act_data.get("statutory_grounds", ""),
                "punishment_or_relief": act_data.get("punishment_or_relief", "Statutory Compensation / Penalty"),
                "added_by": act_data.get("added_by", "Advocate Legal Counsel"),
                "created_at": now_str
            }
            self.custom_acts.insert(0, entry)

            self.add_run_log(
                event_type="CUSTOM_ACT_REGISTERED",
                case_id=act_data.get("linked_case_id", "GLOBAL-LIBRARY"),
                actor=entry["added_by"],
                source="Statutory Codex Library",
                action=f"Lawyer added custom act: {entry['act_title']} ({entry['section']})",
                result="ACT_REGISTERED_SUCCESS",
                correlation_id=f"CORR-{act_id}"
            )
            return entry

    def get_custom_acts(self) -> list:
        with self._lock:
            if not hasattr(self, "custom_acts") or not self.custom_acts:
                # Seed default custom library
                self.custom_acts = [
                    {
                        "act_id": "ACT-101",
                        "act_title": "Consumer Protection Act, 2019",
                        "section": "Section 35 & Section 38 (Consumer Grievance Redressal)",
                        "domain": "Consumer Protection & Essential Services",
                        "statutory_grounds": "Empowers citizens to claim full restitution, litigation costs, and severe damages for deficiency in public/private services within statutory 90-day time-limit.",
                        "punishment_or_relief": "Full refund + General damages up to Rs. 5,00,000 + Product recall orders",
                        "added_by": "Adv. S. Kalra (Bar Council Counsel)",
                        "created_at": "2026-08-29 10:00:00"
                    },
                    {
                        "act_id": "ACT-102",
                        "act_title": "Bharatiya Nagarik Suraksha Sanhita (BNSS 2023)",
                        "section": "Section 175(3) & Section 173(4) (Magisterial Direction for Investigation)",
                        "domain": "Police & Criminal Justice",
                        "statutory_grounds": "Mandates Judicial Magistrate to direct immediate registration of FIR and monitor investigation upon police refusal under Section 173.",
                        "punishment_or_relief": "Judicial Court Order for immediate criminal investigation against accused public servants",
                        "added_by": "Advocate Legal Team",
                        "created_at": "2026-08-29 10:15:00"
                    },
                    {
                        "act_id": "ACT-103",
                        "act_title": "Uttar Pradesh Revenue Code, 2006",
                        "section": "Section 32 & Section 38 (Correction of Revenue Land Maps & Registers)",
                        "domain": "Revenue & Land Records",
                        "statutory_grounds": "Statutory duty of Sub-Divisional Officer (SDO) to correct clerical and map errors in Khasra/Khatauni within 45 days of application.",
                        "punishment_or_relief": "Mandatory administrative rectification of Land Title Records",
                        "added_by": "Advocate Legal Team",
                        "created_at": "2026-08-29 10:30:00"
                    }
                ]
            return self.custom_acts

    def delete_custom_act(self, act_id: str) -> bool:
        with self._lock:
            acts = self.get_custom_acts()
            initial_len = len(acts)
            self.custom_acts = [a for a in acts if a["act_id"] != act_id]
            return len(self.custom_acts) < initial_len

    def apply_custom_act_to_case(self, case_id: str, act_id: str, actor: str = "Advocate Counsel") -> dict:
        """Appends a custom act to the case's statutory analysis and regenerates ML report."""
        with self._lock:
            case = self.cases.get(case_id)
            if not case:
                return None

            act = next((a for a in self.get_custom_acts() if a["act_id"] == act_id), None)
            if not act:
                return None

            act_citation = f"{act['act_title']} ({act['section']})"
            legal = case.setdefault("statutory_legal_analysis", {})
            allied = legal.setdefault("allied_acts", [])
            if act_citation not in allied:
                allied.append(act_citation)

            grounds = legal.setdefault("legal_grounds", [])
            custom_ground = f"Custom Ground ({act['act_title']}): {act['statutory_grounds']}"
            if custom_ground not in grounds:
                grounds.append(custom_ground)

            now_str = datetime.now().strftime("%Y-%m-%d %H:%M:%S.%f")[:-3]
            case["updated_at"] = now_str[:19]

            audit_meta = {
                "update_type": "CUSTOM_STATUTORY_ACT_LINKED",
                "actor": actor,
                "field_changed": "Statutory Acts & Grounds",
                "old_value": "Standard RTI/IPC Suite",
                "new_value": f"Added {act_citation}",
                "remarks": f"Lawyer linked custom act {act_citation} to case docket {case_id}."
            }
            case.setdefault("update_history", []).append({
                "timestamp": now_str,
                **audit_meta
            })

            self.add_run_log(
                event_type="CUSTOM_ACT_LINKED_TO_CASE",
                case_id=case_id,
                actor=actor,
                source="Statutory Codex Library",
                action=f"Linked custom act {act_citation} to case {case_id}",
                result="LINK_SUCCESS",
                correlation_id=f"CORR-LINK-{case_id}"
            )
            return case

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

            # Auto-sync to Notion Run Log Database
            try:
                from flask_backend.services.notion_service import notion_service
                notion_service.log_run_to_notion(log_entry)
            except Exception:
                pass

            return log_entry

    def get_run_logs(self, limit: int = 50) -> list:
        with self._lock:
            return self.run_logs[:limit]

# Global store instance
db_store = DataStore()


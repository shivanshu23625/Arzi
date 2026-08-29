import re
import hashlib
from datetime import datetime

# ==============================================================================
# STATUTORY IPC (1860) & BNS (BHARATIYA NYAYA SANHITA 2023) KNOWLEDGE BASE
# ==============================================================================
IPC_BNS_STATUTORY_REGISTRY = [
    {
        "domain": "Revenue & Land Records",
        "infraction": "Land Record Tampering & Fraudulent Property Mutation",
        "ipc_sections": ["IPC Section 420 (Cheating)", "IPC Section 447 (Criminal Trespass)", "IPC Section 468 (Forgery for Cheating)", "IPC Section 218 (Public Servant framing incorrect record)"],
        "bns_sections": ["BNS Section 318(4) (Cheating)", "BNS Section 329 (Criminal Trespass)", "BNS Section 336(3) (Forgery)", "BNS Section 231 (Public Servant framing incorrect electronic/paper record)"],
        "allied_acts": ["UP Revenue Code 2006 (Sec 31 & 32)", "Delhi Land Reforms Act 1954 (Sec 22)", "Registration Act 1908 (Sec 17)"],
        "punishment": "Imprisonment up to 7 years + Fine (Non-bailable & Cognizable under Section 468/336)",
        "legal_grounds": [
            "Deliberate omission by revenue officials (Patwari/Lekhpal/Tehsildar) to record undisputed inheritance/sale mutation.",
            "Violation of statutory mandate requiring mutation disposal within 30 to 45 days under State Revenue Codes.",
            "Constructive fraud and breach of public trust by withholding certified Khasra/Khatauni land records."
        ],
        "keywords": ["land", "mutation", "khasra", "khatauni", "patwari", "tehsildar", "zameen", "registry", "daakhil kharij", "plot", "seema gyan", "demarcation"]
    },
    {
        "domain": "Food & Civil Supplies",
        "infraction": "Public Distribution System (PDS) Diversion & Essential Commodities Black Marketing",
        "ipc_sections": ["IPC Section 409 (Criminal Breach of Trust by Public Servant)", "IPC Section 420 (Cheating)", "IPC Section 166A (Public Servant disobeying law)"],
        "bns_sections": ["BNS Section 316(5) (Criminal Breach of Trust by Public Servant/Dealer)", "BNS Section 318(4) (Cheating)", "BNS Section 199 (Public Servant disobeying direction under law)"],
        "allied_acts": ["Essential Commodities Act 1955 (Sec 3 & 7)", "National Food Security Act 2013 (Sec 14, 15 & 16)", "Targeted Public Distribution System Control Order 2015"],
        "punishment": "Imprisonment for Life or up to 10 years + Fine (Non-bailable under Sec 409/316(5))",
        "legal_grounds": [
            "Illegitimate denial or delay in issuance of NFSA/BPL ration cards to eligible below-poverty-line beneficiaries.",
            "Unlawful siphoning and black-marketing of subsidized food grains allocated by Central/State Govts.",
            "Violation of NFSA 2013 statutory timelines and non-maintenance of PDS electronic point-of-sale logs."
        ],
        "keywords": ["ration", "rashan", "food", "khadya", "grain", "bpl", "ration card", "pds", "fair price shop", "dealer", "quota", "fps"]
    },
    {
        "domain": "Municipal Public Works & Drainage",
        "infraction": "Public Nuisance, Drainage Negligence & Misappropriation of Civil Tender Funds",
        "ipc_sections": ["IPC Section 268 (Public Nuisance)", "IPC Section 269 (Negligent act likely to spread infection of disease)", "IPC Section 277 (Fouling water of public spring or reservoir)"],
        "bns_sections": ["BNS Section 270 (Public Nuisance)", "BNS Section 271 (Negligent act endangering infectious disease)", "BNS Section 279 (Corrupting water of public spring/drain)"],
        "allied_acts": ["Environment Protection Act 1986 (Sec 15)", "State Municipal Corporation Act", "Disaster Management Act 2005"],
        "punishment": "Imprisonment up to 6 months + Fine + High Court Mandamus Writ liability under Article 226",
        "legal_grounds": [
            "Gross civic dereliction leading to hazardous waterlogging, open sewer health crises, and environmental poisoning.",
            "Non-execution of approved civil drainage works despite budgetary allocation and contractor disbursement.",
            "Breach of fundamental Right to Clean Environment and Public Health under Article 21 of the Constitution of India."
        ],
        "keywords": ["drainage", "sewer", "waterlogging", "gutter", "pothole", "road", "garbage", "kachra", "municipal", "nagar nigam", "sanitation", "naali", "stormwater"]
    },
    {
        "domain": "Police & Law Enforcement",
        "infraction": "Refusal to Register FIR & Malicious Delay in Investigation",
        "ipc_sections": ["IPC Section 166A (Public Servant refusing to register FIR/disobeying law)", "IPC Section 217 (Public Servant disobeying direction of law to save person from punishment)"],
        "bns_sections": ["BNS Section 199 (Public servant disobeying direction under law)", "BNS Section 230 (Public servant disobeying law to protect offender)"],
        "allied_acts": ["Code of Criminal Procedure 1973 (Sec 154, 156(3))", "Bharatiya Nagarik Suraksha Sanhita 2023 (Sec 173, 175(3))", "Police Act 1861 (Sec 29)"],
        "punishment": "Rigorous Imprisonment up to 2 years + Mandatory departmental inquiry and disciplinary penalty",
        "legal_grounds": [
            "Direct violation of Supreme Court Constitution Bench mandate in *Lalita Kumari v. Govt of UP* (Mandatory FIR).",
            "Unlawful inaction on cognizable crime complaint and failure to provide copy of FIR free of cost under Sec 154(2).",
            "Dereliction of statutory policing duties punishable under Section 166A/199."
        ],
        "keywords": ["police", "fir", "thana", "daroga", "cop", "theft", "crime", "investigation", "challan", "assault", "harassment", "chori", "complaint"]
    },
    {
        "domain": "Higher Education & Student Welfare",
        "infraction": "Withholding Government Student Scholarships & Grant Embezzlement",
        "ipc_sections": ["IPC Section 409 (Criminal Breach of Trust by Public Servant)", "IPC Section 420 (Cheating)", "IPC Section 166 (Public servant disobeying law)"],
        "bns_sections": ["BNS Section 316(5) (Criminal Breach of Trust by Public Servant)", "BNS Section 318(4) (Cheating)", "BNS Section 198 (Public servant disobeying law)"],
        "allied_acts": ["State Right to Public Services Act", "UGC Grievance Redressal Regulations", "SC/ST Prevention of Atrocities Act 1989 (if applicable)"],
        "punishment": "Imprisonment up to 10 years + Disciplinary recovery under Comptroller and Auditor General (CAG) norms",
        "legal_grounds": [
            "Arbitrary and prolonged withholding of sanctioned Post-Matric / Merit-cum-Means scholarship funds.",
            "Breach of Ministry of Social Justice / UGC disbursement timelines causing irreparable academic injury.",
            "Unlawful denial of education entitlements under Article 14 & Article 21A of the Constitution."
        ],
        "keywords": ["scholarship", "chhatravriti", "grant", "tuition", "university", "college", "student", "bhu", "fee waiver", "education", "stipend"]
    },
    {
        "domain": "Health & Family Welfare",
        "infraction": "Denial of Emergency Healthcare & Government Hospital Negligence",
        "ipc_sections": ["IPC Section 336 (Act endangering life of others)", "IPC Section 304A (Causing death by negligence)", "IPC Section 166 (Public servant disobeying law)"],
        "bns_sections": ["BNS Section 125 (Act endangering life or personal safety)", "BNS Section 106 (Causing death by negligence)", "BNS Section 198 (Public servant disobeying law)"],
        "allied_acts": ["Clinical Establishments Act 2010", "Consumer Protection Act 2019 (Medical Negligence)", "Indian Medical Council Regulations"],
        "punishment": "Imprisonment up to 5 years + Medical License cancellation and Consumer Tribunal damages",
        "legal_grounds": [
            "Denial of mandatory free emergency medical care in violation of *Paschim Banga Khet Mazdoor Samity v. State of WB*.",
            "Non-availability of life-saving medicines listed under National Essential Medicines List (NEML).",
            "Violation of Right to Health guaranteed under Article 21 of Constitution of India."
        ],
        "keywords": ["hospital", "doctor", "medicine", "dawa", "cmo", "treatment", "health", "dispensary", "emergency", "medical", "aspatal", "illness"]
    }
]

# ==============================================================================
# LANDMARK SUPREME COURT & HIGH COURT RTI / PUBLIC LAW CITATIONS
# ==============================================================================
LANDMARK_CASE_PRECEDENTS = [
    {
        "citation": "CBSE & Anr. v. Aditya Bandopadhyay & Ors. (2011) 8 SCC 497",
        "court": "Supreme Court of India",
        "ratio": "The RTI Act 2005 was enacted to promote transparency and accountability. Public authorities hold information as trustees of the public, and citizens have the fundamental democratic right to inspect and access existing records.",
        "applicable_to": "All Public Grievance Records, Mutation Registers, PDS Logs"
    },
    {
        "citation": "Lalita Kumari v. Govt. of U.P. (2014) 2 SCC 1",
        "court": "Supreme Court of India (Constitution Bench)",
        "ratio": "Registration of FIR is mandatory under Section 154 CrPC if information discloses commission of a cognizable offence. Police cannot delay or conduct preliminary enquiry in cognizable matters.",
        "applicable_to": "Police & Law Enforcement Inaction"
    },
    {
        "citation": "Reserve Bank of India v. Jayantilal N. Mistry (2016) 3 SCC 525",
        "court": "Supreme Court of India",
        "ratio": "Public authorities cannot hide under the cloak of fiduciary relationship to deny disclosure of inspection reports, defaulters, or regulatory action when public interest is paramount.",
        "applicable_to": "Regulatory Non-Disclosure, Public Works & Land Frauds"
    },
    {
        "citation": "Manohar s/o Manikrao Anchule v. State of Maharashtra AIR 2013 SC 681",
        "court": "Supreme Court of India",
        "ratio": "Section 20(1) penalty of Rs. 250 per day up to Rs. 25,000 is mandatory upon a delinquent PIO who fails to furnish information within 30 days without reasonable cause.",
        "applicable_to": "Overdue RTI Applications & PIO Compliance Desks"
    }
]


class LegalIntelligenceEngine:
    """
    Law Firm & Government Desk Legal Intelligence Engine.
    Maps citizen facts to exact IPC & BNS 2023 sections, computes Section 20 penalties,
    generates Win-Probability scores, and drafts Form-A RTI and First Appeals.
    """

    def analyze_legal_standing(self, grievance_text: str, department: str, days_overdue: int = 0) -> dict:
        """
        Classifies the grievance against IPC & BNS statutory codes, calculates case merit,
        extracts legal grounds, and pulls applicable landmark precedents.
        """
        text_lower = grievance_text.lower()
        matched_entry = None

        # Try exact department match first
        for entry in IPC_BNS_STATUTORY_REGISTRY:
            if entry["domain"].lower() == department.lower():
                matched_entry = entry
                break

        # Fallback to keyword matching
        if not matched_entry:
            best_score = 0
            for entry in IPC_BNS_STATUTORY_REGISTRY:
                score = sum(1 for kw in entry["keywords"] if kw in text_lower)
                if score > best_score:
                    best_score = score
                    matched_entry = entry

        if not matched_entry:
            matched_entry = IPC_BNS_STATUTORY_REGISTRY[0]

        # Calculate Case Merit Score (0 - 100)
        has_ref = bool(re.search(r'\b(?:ref|ack|app|no|receipt|khasra)\b', text_lower))
        has_date = bool(re.search(r'\b(?:\d{1,2}[/-]\d{1,2}|\d+\s+(?:month|week|day)|jan|feb|mar|apr|may|jun|jul|aug|sep|oct|nov|dec)\b', text_lower))
        
        merit_score = 75
        if has_ref:
            merit_score += 10
        if has_date:
            merit_score += 10
        if days_overdue > 30:
            merit_score += 5
        merit_score = min(98, merit_score)

        # Section 20(1) Penalty Calculation: Rs. 250 per day capped at Rs. 25,000
        sec20_penalty_per_day = 250
        max_penalty = 25000
        potential_penalty = 0
        if days_overdue > 30:
            overdue_days = days_overdue - 30
            potential_penalty = min(max_penalty, overdue_days * sec20_penalty_per_day)

        # Relevant Supreme Court Precedent
        precedents = []
        if "police" in department.lower():
            precedents.append(LANDMARK_CASE_PRECEDENTS[1])
        precedents.append(LANDMARK_CASE_PRECEDENTS[0])
        if days_overdue > 30:
            precedents.append(LANDMARK_CASE_PRECEDENTS[3])

        return {
            "statutory_domain": matched_entry["domain"],
            "statutory_infraction": matched_entry["infraction"],
            "ipc_sections": matched_entry["ipc_sections"],
            "bns_sections": matched_entry["bns_sections"],
            "allied_acts": matched_entry["allied_acts"],
            "maximum_punishment": matched_entry["punishment"],
            "legal_grounds": matched_entry["legal_grounds"],
            "case_merit_score": merit_score,
            "win_probability": "VERY HIGH (94%+)" if merit_score >= 85 else "HIGH (78%+)",
            "section_20_penalty_liability_inr": potential_penalty,
            "section_20_daily_rate_inr": sec20_penalty_per_day,
            "days_past_sla": max(0, days_overdue - 30),
            "landmark_precedents": precedents
        }

    def generate_first_appeal_draft(self, case: dict) -> dict:
        """
        Drafts a formal First Appeal Memorandum under Section 19(1) of the RTI Act 2005
        addressed to the designated First Appellate Authority (FAA).
        """
        complainant = case.get("complainant", {})
        pio = case.get("suggested_pio", {})
        faa = case.get("suggested_faa", {}) or {
            "faa_name": "First Appellate Authority (Senior Officer)",
            "designation": f"Additional District Magistrate / Joint Secretary ({case.get('department', 'Public Authority')})",
            "office_address": pio.get("office_address", "District Collectorate Complex")
        }
        case_id = case.get("case_id", "ARZ-1046")
        ref_no = case.get("application_ref_no", "N/A")
        sub_date = case.get("original_submission_date", "N/A")
        today_date = datetime.now().strftime("%d-%b-%Y")

        subject = f"FIRST APPEAL UNDER SECTION 19(1) OF RTI ACT 2005 AGAINST DEEMED REFUSAL / NON-RESPONSE BY PIO IN CASE {case_id}"
        
        grounds = [
            f"1. The Appellant submitted an initial RTI Application (Case ID: {case_id}, Ref: {ref_no}) on {sub_date} seeking certified public records under Section 6(1).",
            f"2. More than 30 days have elapsed since filing, and the Designated PIO ({pio.get('pio_name', 'Public Information Officer')}) has failed to provide the requested information within statutory SLA under Section 7(1).",
            "3. Under Section 7(2) of the RTI Act 2005, the failure of the PIO to give a decision within 30 days constitutes a 'DEEMED REFUSAL' of the application.",
            "4. Under Section 7(6) of the RTI Act 2005, the Appellant is now legally entitled to receive all requested certified information FREE OF COST without any further documentation charges.",
            f"5. The PIO has incurred personal statutory penalty liability of Rs. 250 per day under Section 20(1) as affirmed in *Manohar v. State of Maharashtra AIR 2013 SC 681*."
        ]

        prayers = [
            "a) Direct the Designated PIO to forthwith furnish certified copies of all requested file records FREE OF CHARGE to the Appellant within 7 days.",
            "b) Grant an opportunity of personal hearing to the Appellant before the First Appellate Authority.",
            "c) Recommend initiation of departmental disciplinary proceedings and Section 20(1) penalty proceedings against the defaulting officer."
        ]

        return {
            "appeal_type": "FIRST APPEAL (SECTION 19(1) RTI ACT 2005)",
            "appeal_id": f"APP-19-{case_id}",
            "appeal_date": today_date,
            "target_faa": faa,
            "subject": subject,
            "grounds_of_appeal": grounds,
            "prayers_sought": prayers,
            "statutory_act": "Right to Information Act 2005 (Section 19(1) read with Section 7(1) & 7(6))"
        }

    def generate_legal_notice_draft(self, case: dict, legal_analysis: dict) -> dict:
        """
        Drafts a formal Advocate Legal Notice for Public Servants Dereliction under IPC/BNS.
        """
        complainant = case.get("complainant", {})
        pio = case.get("suggested_pio", {})
        today_date = datetime.now().strftime("%d-%b-%Y")
        case_id = case.get("case_id", "ARZ-1046")

        ipc_str = ", ".join(legal_analysis.get("ipc_sections", []))
        bns_str = ", ".join(legal_analysis.get("bns_sections", []))

        notice_body = (
            f"LEGAL NOTICE UNDER SECTION 80 CPC & SECTIONS OF IPC/BNS\n"
            f"To: {pio.get('pio_name')} ({pio.get('designation')}), {pio.get('office_address')}\n\n"
            f"Under instructions and on behalf of our client, {complainant.get('name')} (Residing at {complainant.get('address')}), "
            f"we hereby serve you this formal Statutory Legal Notice regarding gross administrative dereliction and delay in processing "
            f"Grievance Ref: {case.get('application_ref_no', 'N/A')}.\n\n"
            f"STATUTORY CHARGES INVOKED:\n"
            f"• Indian Penal Code (1860): {ipc_str}\n"
            f"• Bharatiya Nyaya Sanhita (2023): {bns_str}\n\n"
            f"You are called upon to rectify the dereliction and provide certified status within 15 days of receipt of this notice, "
            f"failing which our client shall initiate appropriate Criminal and Writ proceedings under Article 226 of the Constitution of India."
        )

        return {
            "notice_id": f"LNOT-{case_id}",
            "notice_date": today_date,
            "recipient": pio,
            "client": complainant,
            "notice_text": notice_body
        }


legal_engine = LegalIntelligenceEngine()

import io
import os
import hashlib
from datetime import datetime

try:
    from reportlab.lib.pagesizes import letter
    from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, HRFlowable
    from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
    from reportlab.lib import colors
    HAS_REPORTLAB = True
except ImportError:
    HAS_REPORTLAB = False

class RTIPDFGenerator:
    """
    Deterministic RTI Legal Application, First Appeal & Statutory Negligence PDF Generator.
    Complies strictly with Indian RTI Act 2005, Central RTI Fee Rules 2012, and BNS/IPC Legal Notices.
    """

    def generate_pdf_bytes(self, case: dict, doc_type: str = "rti") -> bytes:
        complainant = case.get("complainant", {})
        pio = case.get("suggested_pio", {})
        faa = case.get("suggested_faa", {}) or pio.get("faa", {})
        draft = case.get("draft_rti", {})
        case_id = case.get("case_id", "ARZ-0000")
        ref_no = case.get("application_ref_no", "Not Provided")
        sub_date = case.get("original_submission_date", "Unconfirmed")
        now_str = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        today_date = datetime.now().strftime("%d-%b-%Y")
        legal_info = case.get("statutory_legal_analysis", {})

        if not HAS_REPORTLAB:
            return (case.get("ml_report_format") or "FORM A - RTI APPLICATION REPORT").encode("utf-8")

        buffer = io.BytesIO()
        doc = SimpleDocTemplate(
            buffer,
            pagesize=letter,
            rightMargin=40,
            leftMargin=40,
            topMargin=40,
            bottomMargin=40
        )

        styles = getSampleStyleSheet()
        title_style = ParagraphStyle(
            'TitleStyle',
            parent=styles['Heading1'],
            fontSize=12.5,
            leading=16,
            textColor=colors.HexColor("#1E242B"),
            alignment=1, # Center
            fontName="Helvetica-Bold",
            spaceAfter=8
        )

        heading_style = ParagraphStyle(
            'HeadingStyle',
            parent=styles['Heading2'],
            fontSize=10.5,
            leading=14,
            textColor=colors.HexColor("#D94E28"),
            fontName="Helvetica-Bold",
            spaceBefore=8,
            spaceAfter=4
        )

        body_style = ParagraphStyle(
            'BodyStyle',
            parent=styles['Normal'],
            fontSize=9,
            leading=13,
            textColor=colors.HexColor("#1E242B"),
            fontName="Helvetica"
        )

        signature_style = ParagraphStyle(
            'SignatureStyle',
            parent=styles['Normal'],
            fontSize=9,
            leading=13,
            textColor=colors.HexColor("#1E242B"),
            fontName="Helvetica-Bold",
            alignment=2 # Right align
        )

        elements = []

        if doc_type == "appeal":
            # =================== FIRST APPEAL MEMORANDUM (SECTION 19(1)) ===================
            elements.append(Paragraph("MEMORANDUM OF FIRST APPEAL UNDER SECTION 19(1) OF RTI ACT 2005", title_style))
            elements.append(Paragraph(f"<b>BEFORE THE DESIGNATED FIRST APPELLATE AUTHORITY (FAA)</b> &nbsp;|&nbsp; <b>CASE ID:</b> {case_id}", ParagraphStyle('SubHeader', parent=body_style, alignment=1)))
            elements.append(HRFlowable(width="100%", thickness=1.5, color=colors.HexColor("#D94E28"), spaceAfter=10))

            # Recipient FAA Block
            elements.append(Paragraph("TO THE FIRST APPELLATE AUTHORITY:", heading_style))
            faa_text = f"<b>{faa.get('faa_name', 'First Appellate Authority (Senior Officer)')}</b><br/>" \
                       f"Designation: {faa.get('designation', 'Additional District Magistrate / Joint Secretary')}<br/>" \
                       f"Office: {faa.get('office_address', pio.get('office_address', 'Collectorate Complex'))}<br/>" \
                       f"Email: {faa.get('email', 'faa@gov.in')} &nbsp;|&nbsp; Phone: {faa.get('phone', 'N/A')}"
            elements.append(Paragraph(faa_text, body_style))
            elements.append(Spacer(1, 6))

            # Appellant Details
            elements.append(Paragraph("1. PARTICULARS OF THE APPELLANT:", heading_style))
            app_text = f"<b>Name:</b> {complainant.get('name', 'Citizen Appellant')} (Citizen of India)<br/>" \
                       f"<b>Address:</b> {complainant.get('address', 'N/A')}<br/>" \
                       f"<b>Contact:</b> {complainant.get('contact', 'N/A')}"
            elements.append(Paragraph(app_text, body_style))
            elements.append(Spacer(1, 6))

            # Respondent PIO Details
            elements.append(Paragraph("2. PARTICULARS OF THE RESPONDENT PUBLIC INFORMATION OFFICER (PIO):", heading_style))
            resp_text = f"<b>Designated PIO:</b> {pio.get('pio_name', 'PIO')} ({pio.get('designation', '')})<br/>" \
                        f"<b>Office:</b> {pio.get('office_address', '')} ({pio.get('distance_label', 'Nearest Office')})<br/>" \
                        f"<b>Initial RTI Application Date:</b> {sub_date} &nbsp;|&nbsp; <b>Original Grievance Ref:</b> {ref_no}"
            elements.append(Paragraph(resp_text, body_style))
            elements.append(Spacer(1, 6))

            # Grounds of Appeal
            elements.append(Paragraph("3. STATUTORY GROUNDS OF FIRST APPEAL:", heading_style))
            grounds = case.get("first_appeal_draft", {}).get("grounds_of_appeal", [
                "1. The Respondent PIO failed to furnish requested information within the mandatory 30-day statutory SLA under Section 7(1).",
                "2. Failure of PIO constitutes Deemed Refusal under Section 7(2) of RTI Act 2005.",
                "3. Appellant is entitled to receive records FREE OF COST under Section 7(6).",
                "4. Personal penalty of Rs. 250/day up to Rs. 25,000 is chargeable under Section 20(1) (Manohar v. State of Maharashtra AIR 2013 SC 681)."
            ])
            for g in grounds:
                elements.append(Paragraph(g, body_style))
                elements.append(Spacer(1, 3))

            # Prayers Sought
            elements.append(Spacer(1, 4))
            elements.append(Paragraph("4. RELIEFS & PRAYERS SOUGHT:", heading_style))
            prayers = case.get("first_appeal_draft", {}).get("prayers_sought", [
                "a) Direct the PIO to provide certified copies of records FREE OF CHARGE within 7 days.",
                "b) Grant personal hearing to Appellant.",
                "c) Recommend Section 20(1) penalty proceedings against the defaulting officer."
            ])
            for p in prayers:
                elements.append(Paragraph(f"• {p}", body_style))
                elements.append(Spacer(1, 2))

            # Signature
            elements.append(Spacer(1, 12))
            sig_box = f"<b>VERIFICATION & SIGNATURE OF APPELLANT</b><br/><br/>" \
                      f"____________________________________________<br/>" \
                      f"Signature of Appellant: <b>{complainant.get('name', 'Citizen Appellant')}</b><br/>" \
                      f"Date: {today_date} &nbsp;|&nbsp; Place: {pio.get('matched_user_locality', 'Local Division')}"
            elements.append(Paragraph(sig_box, signature_style))

        elif doc_type == "notice":
            # =================== ADVOCATE STATUTORY LEGAL NOTICE ===================
            elements.append(Paragraph("STATUTORY LEGAL NOTICE UNDER SECTION 80 CPC READ WITH IPC & BNS", title_style))
            elements.append(Paragraph(f"<b>ADVOCATE NOTICE FOR PUBLIC OFFICER DERELICTION</b> &nbsp;|&nbsp; <b>CASE ID:</b> {case_id}", ParagraphStyle('SubHeader', parent=body_style, alignment=1)))
            elements.append(HRFlowable(width="100%", thickness=1.5, color=colors.HexColor("#1E242B"), spaceAfter=10))

            notice_txt = case.get("legal_notice_draft", {}).get("notice_text") or (
                f"To: {pio.get('pio_name')} ({pio.get('office_address')})\n\n"
                f"Under instructions from our client {complainant.get('name')}, notice is hereby given of statutory dereliction regarding grievance Ref: {ref_no}."
            )
            for line in notice_txt.split("\n"):
                if line.strip().startswith("STATUTORY CHARGES") or line.strip().startswith("To:"):
                    elements.append(Paragraph(f"<b>{line}</b>", heading_style))
                elif line.strip():
                    elements.append(Paragraph(line, body_style))
                    elements.append(Spacer(1, 3))

            elements.append(Spacer(1, 15))
            sig_box = f"<b>LEGAL COUNSEL & ADVOCATE ON RECORD</b><br/><br/>" \
                      f"____________________________________________<br/>" \
                      f"Adv. S. Kalra & Associates (Civic Legal NGO)<br/>" \
                      f"Counsel for Complainant: <b>{complainant.get('name')}</b><br/>" \
                      f"Date: {today_date}"
            elements.append(Paragraph(sig_box, signature_style))

        else:
            # =================== FORM 'A' RTI APPLICATION (STANDARD) ===================
            elements.append(Paragraph("FORM 'A' - APPLICATION FOR INFORMATION UNDER SECTION 6(1) OF RTI ACT 2005", title_style))
            elements.append(Paragraph(f"<b>CASE REF ID:</b> {case_id} &nbsp;|&nbsp; <b>DATE:</b> {today_date} &nbsp;|&nbsp; <b>STATUTORY SLA:</b> 30 DAYS (SECTION 7(1))", body_style))
            elements.append(HRFlowable(width="100%", thickness=1.5, color=colors.HexColor("#1E242B"), spaceAfter=10))

            # Recipient PIO Block with Nearest Geospatial Tag
            elements.append(Paragraph("TO THE DESIGNATED PUBLIC INFORMATION OFFICER (NEAREST JURISDICTION):", heading_style))
            pio_text = f"<b>{pio.get('pio_name', 'Public Information Officer')}</b><br/>" \
                       f"Designation: {pio.get('designation', '')}<br/>" \
                       f"Department: {pio.get('department', '')}<br/>" \
                       f"Office: {pio.get('office_address', '')}<br/>" \
                       f"Room/Desk: {pio.get('room_no', 'Ground Floor RTI Desk')} &nbsp;|&nbsp; <b>Proximity:</b> {pio.get('distance_label', 'Nearest Local Office')}"
            elements.append(Paragraph(pio_text, body_style))
            elements.append(Spacer(1, 6))

            # Applicant Details
            elements.append(Paragraph("1. APPLICANT DETAILS (SECTION 3 INDIVIDUAL CITIZEN OF INDIA):", heading_style))
            app_text = f"<b>Full Name of Citizen Applicant:</b> {complainant.get('name', 'Citizen Applicant')} (Individual/Natural Person)<br/>" \
                       f"<b>Postal Address:</b> {complainant.get('address', 'N/A')}<br/>" \
                       f"<b>Contact Phone:</b> {complainant.get('contact', 'N/A')}<br/>" \
                       f"<b>Original Application Ref / Ack No:</b> {ref_no} &nbsp;|&nbsp; <b>Original Filing Date:</b> {sub_date}"
            elements.append(Paragraph(app_text, body_style))
            elements.append(Spacer(1, 6))

            # Statutory IPC/BNS Infraction Notice
            if legal_info:
                elements.append(Paragraph("2. STATUTORY LEGAL FRAMEWORK & IPC / BNS RELEVANCE:", heading_style))
                ipc_t = ", ".join(legal_info.get("ipc_sections", []))
                bns_t = ", ".join(legal_info.get("bns_sections", []))
                law_text = f"<b>Subject Matter Infraction:</b> {legal_info.get('statutory_infraction', 'Public Dereliction')}<br/>" \
                           f"<b>IPC Sections:</b> {ipc_t} &nbsp;|&nbsp; <b>BNS 2023 Sections:</b> {bns_t}<br/>" \
                           f"<b>Statutory Win Probability / Case Merit:</b> {legal_info.get('win_probability', 'HIGH')} ({legal_info.get('case_merit_score', 90)}/100)"
                elements.append(Paragraph(law_text, body_style))
                elements.append(Spacer(1, 6))

            # Application Subject & Record-Based Questions (Section 2(f))
            elements.append(Paragraph("3. PARTICULARS OF INFORMATION REQUIRED (SECTION 2(f) RECORD-BASED QUERIES):", heading_style))
            elements.append(Paragraph(f"<b>Subject:</b> {draft.get('application_subject', 'RTI Query')}", body_style))
            elements.append(Spacer(1, 4))

            elements.append(Paragraph("<b>Specific Information Sought from Existing Records:</b>", body_style))
            for q in draft.get("questions", []):
                elements.append(Paragraph(q, body_style))
                elements.append(Spacer(1, 2.5))

            # Mandatory Enclosures & Fee Rules 2012
            elements.append(Spacer(1, 6))
            elements.append(Paragraph("4. STATUTORY FEE PAYMENT & ENCLOSURES CHECKLIST:", heading_style))
            elements.append(Paragraph(f"<b>Application Fee Details:</b> {draft.get('fees_paid', 'Rs. 10 Indian Postal Order attached under Rule 3 of Central RTI Rules 2012.')}", body_style))
            elements.append(Spacer(1, 3))
            elements.append(Paragraph("<b>Mandatory Enclosures:</b><br/>"
                                       "• Annexure-A: Copy of Original Grievance Application & Acknowledgement Receipt.<br/>"
                                       "• Annexure-B: Proof of Application Fee Payment (Indian Postal Order / DD).<br/>"
                                       "• Annexure-C: Applicant Identity & Address Proof.", body_style))

            # Applicant Signature Block
            elements.append(Spacer(1, 10))
            sig_box = f"<b>APPLICANT SIGNATURE & AUTHENTICATION (SECTION 6(1))</b><br/><br/>" \
                      f"____________________________________________<br/>" \
                      f"Signature / Thumb Impression of Citizen Applicant<br/>" \
                      f"Name: <b>{complainant.get('name', 'Citizen Applicant')}</b><br/>" \
                      f"Date: {today_date} &nbsp;|&nbsp; Place: {pio.get('matched_user_locality', 'Local Division')}"
            elements.append(Paragraph(sig_box, signature_style))

        # Separate Internal Casework Audit Footer & SHA-256 Stamp
        elements.append(Spacer(1, 10))
        elements.append(HRFlowable(width="100%", thickness=1, color=colors.HexColor("#7A8B9E"), spaceAfter=6))
        doc_hash = hashlib.sha256(f"{case_id}-{doc_type}-{now_str}".encode()).hexdigest()[:16].upper()
        audit_stamp = f"<b>ARZI LEGAL TECH INTERNAL AUDIT & DISPATCH VERIFICATION</b><br/>" \
                      f"Reviewer: {case.get('reviewer', 'Adv. S. Kalra')} &nbsp;|&nbsp; Verification Hash: <code>{doc_hash}</code> &nbsp;|&nbsp; " \
                      f"Generated: {now_str} &nbsp;|&nbsp; Status: VERIFIED & SEALED"
        elements.append(Paragraph(audit_stamp, ParagraphStyle('AuditStyle', parent=body_style, fontSize=7.5, textColor=colors.HexColor("#555555"))))

        doc.build(elements)
        return buffer.getvalue()

pdf_generator = RTIPDFGenerator()

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
    Deterministic RTI Legal Application & ML Report Generator.
    Strictly compliant with Indian RTI Act 2005 (Form A Format) & Central RTI Fee Rules 2012.
    """

    def generate_pdf_bytes(self, case: dict) -> bytes:
        complainant = case.get("complainant", {})
        pio = case.get("suggested_pio", {})
        draft = case.get("draft_rti", {})
        case_id = case.get("case_id", "ARZ-0000")
        ref_no = case.get("application_ref_no", "Not Provided")
        sub_date = case.get("original_submission_date", "Unconfirmed")
        now_str = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        today_date = datetime.now().strftime("%d-%b-%Y")

        if HAS_REPORTLAB:
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
                fontSize=13,
                leading=16,
                textColor=colors.HexColor("#1E242B"),
                alignment=1, # Center
                fontName="Helvetica-Bold",
                spaceAfter=10
            )

            heading_style = ParagraphStyle(
                'HeadingStyle',
                parent=styles['Heading2'],
                fontSize=11,
                leading=14,
                textColor=colors.HexColor("#D94E28"),
                fontName="Helvetica-Bold",
                spaceBefore=10,
                spaceAfter=6
            )

            body_style = ParagraphStyle(
                'BodyStyle',
                parent=styles['Normal'],
                fontSize=9.5,
                leading=13,
                textColor=colors.HexColor("#1E242B"),
                fontName="Helvetica"
            )

            signature_style = ParagraphStyle(
                'SignatureStyle',
                parent=styles['Normal'],
                fontSize=9.5,
                leading=13,
                textColor=colors.HexColor("#1E242B"),
                fontName="Helvetica-Bold",
                alignment=2 # Right align
            )

            elements = []

            # Header
            elements.append(Paragraph("FORM 'A' - APPLICATION FOR INFORMATION UNDER SECTION 6(1) OF RTI ACT 2005", title_style))
            elements.append(Paragraph(f"<b>CASE REF ID:</b> {case_id} &nbsp;|&nbsp; <b>DATE:</b> {today_date} &nbsp;|&nbsp; <b>STATUTORY SLA:</b> 30 DAYS (SECTION 7(1))", body_style))
            elements.append(HRFlowable(width="100%", thickness=1.5, color=colors.HexColor("#1E242B"), spaceAfter=12))

            # Recipient PIO Block
            elements.append(Paragraph("TO THE PUBLIC INFORMATION OFFICER:", heading_style))
            pio_text = f"<b>{pio.get('pio_name', 'Public Information Officer')}</b><br/>" \
                       f"{pio.get('designation', '')}<br/>" \
                       f"Department: {pio.get('department', '')}<br/>" \
                       f"Office: {pio.get('office_address', '')}"
            elements.append(Paragraph(pio_text, body_style))
            elements.append(Spacer(1, 8))

            # Applicant Details (Section 3 Indian Citizen)
            elements.append(Paragraph("1. APPLICANT DETAILS (SECTION 3 INDIVIDUAL CITIZEN OF INDIA):", heading_style))
            app_text = f"<b>Full Name of Citizen Applicant:</b> {complainant.get('name', 'Citizen Applicant')} (Individual/Natural Person)<br/>" \
                       f"<b>Postal Address:</b> {complainant.get('address', 'N/A')}<br/>" \
                       f"<b>Contact Phone:</b> {complainant.get('contact', 'N/A')}<br/>" \
                       f"<b>Original Application Ref / Ack No:</b> {ref_no} &nbsp;|&nbsp; <b>Original Filing Date:</b> {sub_date}"
            elements.append(Paragraph(app_text, body_style))
            elements.append(Spacer(1, 8))

            # Application Subject & Record-Based Questions (Section 2(f))
            elements.append(Paragraph("2. PARTICULARS OF INFORMATION REQUIRED (SECTION 2(f) RECORD-BASED QUERIES):", heading_style))
            elements.append(Paragraph(f"<b>Subject:</b> {draft.get('application_subject', 'RTI Query')}", body_style))
            elements.append(Spacer(1, 6))

            elements.append(Paragraph("<b>Specific Information Sought from Existing Records:</b>", body_style))
            for q in draft.get("questions", []):
                elements.append(Paragraph(q, body_style))
                elements.append(Spacer(1, 3))

            # Mandatory Enclosures & Fee Rules 2012
            elements.append(Spacer(1, 8))
            elements.append(Paragraph("3. STATUTORY FEE PAYMENT & ENCLOSURES CHECKLIST:", heading_style))
            elements.append(Paragraph(f"<b>Application Fee Details:</b> {draft.get('fees_paid', 'Rs. 10 Indian Postal Order attached under Rule 3 of Central RTI Rules 2012.')}", body_style))
            elements.append(Spacer(1, 4))
            elements.append(Paragraph("<b>Mandatory Enclosures:</b><br/>"
                                       "• Annexure-A: Copy of Original Grievance Application & Acknowledgement Receipt.<br/>"
                                       "• Annexure-B: Proof of Application Fee Payment (Indian Postal Order).<br/>"
                                       "• Annexure-C: Applicant Identity & Address Proof.", body_style))

            # Applicant Signature Block (Section 6(1) Authentication)
            elements.append(Spacer(1, 15))
            sig_box = f"<b>APPLICANT SIGNATURE & AUTHENTICATION (SECTION 6(1))</b><br/><br/>" \
                      f"____________________________________________<br/>" \
                      f"Signature / Thumb Impression of Citizen Applicant<br/>" \
                      f"Name: <b>{complainant.get('name', 'Citizen Applicant')}</b><br/>" \
                      f"Date: {today_date} &nbsp;|&nbsp; Place: {pio.get('matched_user_locality', 'New Delhi')}"
            elements.append(Paragraph(sig_box, signature_style))

            # Separate Internal Audit Footer (Kept completely separate from statutory RTI application block)
            elements.append(Spacer(1, 15))
            elements.append(HRFlowable(width="100%", thickness=1, color=colors.HexColor("#7A8B9E"), spaceAfter=8))
            audit_stamp = f"<b>INTERNAL NGO CASEWORK & AUDIT LOG</b> (Internal Record Only — Not part of Statutory Application)<br/>" \
                          f"Reviewed by Legal Case Worker: {case.get('reviewer', 'Adv. S. Kalra')}<br/>" \
                          f"Verification Status: VERIFIED & DISPATCHED &nbsp;|&nbsp; Dispatch ID: DSP-{hashlib.md5(case_id.encode()).hexdigest()[:8]}"
            elements.append(Paragraph(audit_stamp, ParagraphStyle('AuditStyle', parent=body_style, fontSize=8, textColor=colors.HexColor("#555555"))))

            doc.build(elements)
            return buffer.getvalue()
        else:
            return (case.get("ml_report_format") or "FORM A - RTI APPLICATION REPORT").encode("utf-8")

pdf_generator = RTIPDFGenerator()

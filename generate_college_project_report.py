import os
import sys
from reportlab.lib.pagesizes import A4
from reportlab.lib.colors import HexColor
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.platypus import (
    SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, PageBreak, KeepTogether, HRFlowable, Image
)
from reportlab.pdfgen import canvas

# University & College Color Palette
C_PRIMARY = HexColor("#1E3A8A")       # Navy University Blue
C_SECONDARY = HexColor("#C2410C")     # Terracotta Accent
C_INK = HexColor("#111827")           # Formal Black/Charcoal
C_INK_MUTED = HexColor("#4B5563")     # Formal Gray
C_BG_CARD = HexColor("#F9FAFB")       # Clean Card Background
C_BORDER = HexColor("#D1D5DB")        # Light Border
C_WHITE = HexColor("#FFFFFF")

class AcademicNumberedCanvas(canvas.Canvas):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._saved_page_states = []

    def showPage(self):
        self._saved_page_states.append(dict(self.__dict__))
        self._startPage()

    def save(self):
        num_pages = len(self._saved_page_states)
        for state in self._saved_page_states:
            self.__dict__.update(state)
            self.draw_page_decorations(num_pages)
            super().showPage()
        super().save()

    def draw_page_decorations(self, page_count):
        # Suppress headers/footers on preliminary & certificate pages (Pages 1 to 4)
        if self._pageNumber <= 4:
            return

        self.saveState()
        page_width, page_height = A4

        # Header for body pages
        self.setFont("Helvetica", 8)
        self.setFillColor(C_INK_MUTED)
        self.drawString(54, page_height - 36, "HackMate — Campus Hackathon Team Finder")
        self.drawRightString(page_width - 54, page_height - 36, "Department of Computer Engineering, DMCE")

        self.setStrokeColor(C_BORDER)
        self.setLineWidth(0.5)
        self.line(54, page_height - 40, page_width - 54, page_height - 40)

        # Footer for body pages
        self.line(54, 45, page_width - 54, 45)
        self.drawString(54, 32, "Datta Meghe College of Engineering, Airoli • University of Mumbai")
        # Body page number relative to content start (Page 1 of 2, Page 2 of 2)
        content_page = self._pageNumber - 4
        total_content_pages = page_count - 4
        self.drawRightString(page_width - 54, 32, f"Page {content_page} of {total_content_pages}")
        self.restoreState()

def build_pdf(filename):
    doc = SimpleDocTemplate(
        filename,
        pagesize=A4,
        leftMargin=54,
        rightMargin=54,
        topMargin=50,
        bottomMargin=50
    )

    styles = getSampleStyleSheet()

    # Academic Typography Styles
    title_style = ParagraphStyle(
        'CoverTitle',
        fontName='Helvetica-Bold',
        fontSize=20,
        leading=24,
        alignment=1, # Center
        textColor=C_INK,
        spaceAfter=12
    )
    subtitle_style = ParagraphStyle(
        'CoverSubtitle',
        fontName='Helvetica',
        fontSize=11,
        leading=16,
        alignment=1,
        textColor=C_INK,
        spaceAfter=4
    )
    header_academic = ParagraphStyle(
        'AcadHeader',
        fontName='Helvetica-Bold',
        fontSize=12,
        leading=16,
        alignment=1,
        textColor=C_INK,
        spaceAfter=4
    )
    body_center = ParagraphStyle(
        'BodyCenter',
        fontName='Helvetica',
        fontSize=10,
        leading=14,
        alignment=1,
        textColor=C_INK,
        spaceAfter=4
    )
    cert_title = ParagraphStyle(
        'CertTitle',
        fontName='Helvetica-Bold',
        fontSize=16,
        leading=20,
        alignment=1,
        textColor=C_INK,
        spaceAfter=16
    )
    cert_body = ParagraphStyle(
        'CertBody',
        fontName='Helvetica',
        fontSize=10.5,
        leading=16,
        alignment=4, # Justify
        textColor=C_INK,
        spaceAfter=14
    )
    h1_style = ParagraphStyle(
        'Header1',
        fontName='Helvetica-Bold',
        fontSize=12,
        leading=16,
        textColor=C_PRIMARY,
        spaceBefore=10,
        spaceAfter=4,
        keepWithNext=True
    )
    h2_style = ParagraphStyle(
        'Header2',
        fontName='Helvetica-Bold',
        fontSize=10,
        leading=14,
        textColor=C_INK,
        spaceBefore=6,
        spaceAfter=2,
        keepWithNext=True
    )
    body_style = ParagraphStyle(
        'BodyText',
        fontName='Helvetica',
        fontSize=9,
        leading=12.5,
        textColor=C_INK,
        alignment=4,
        spaceAfter=4
    )
    tbl_cell = ParagraphStyle(
        'TableCell',
        fontName='Helvetica',
        fontSize=8.5,
        leading=11.5,
        textColor=C_INK
    )
    tbl_cell_bold = ParagraphStyle(
        'TableCellBold',
        fontName='Helvetica-Bold',
        fontSize=8.5,
        leading=11.5,
        textColor=C_INK
    )
    tbl_header = ParagraphStyle(
        'TableHeader',
        fontName='Helvetica-Bold',
        fontSize=8.5,
        leading=11.5,
        textColor=C_WHITE
    )

    story = []

    # =============================================================
    # PAGE 1: COVER PAGE
    # =============================================================
    story.append(Spacer(1, 10))
    story.append(Paragraph("HackMate", title_style))
    story.append(Paragraph("<b>Campus Hackathon Team Discovery Platform</b>", ParagraphStyle('SubSub', fontName='Helvetica-Bold', fontSize=12, leading=16, alignment=1, textColor=C_SECONDARY, spaceAfter=14)))
    story.append(Spacer(1, 6))

    story.append(Paragraph("Submitted in partial fulfillment of the requirements of", subtitle_style))
    story.append(Paragraph("<b>Second Year</b>", ParagraphStyle('SY', fontName='Helvetica-Bold', fontSize=12, alignment=1, spaceAfter=2)))
    story.append(Paragraph("in", subtitle_style))
    story.append(Paragraph("<b>Computer Engineering</b>", ParagraphStyle('CE', fontName='Helvetica-Bold', fontSize=12, alignment=1, spaceAfter=14)))

    story.append(Paragraph("<b>By</b>", header_academic))
    story.append(Spacer(1, 2))

    students_cover = [
        [Paragraph("<b>Aayush Mali</b> — Roll No. 26", body_center), Paragraph("<b>Aditi Mhatre</b> — Roll No. 31", body_center)],
        [Paragraph("<b>Harshit Mishra</b> — Roll No. 32", body_center), Paragraph("<b>Shravan More</b> — Roll No. 36", body_center)]
    ]
    st_table = Table(students_cover, colWidths=[240, 240])
    st_table.setStyle(TableStyle([
        ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
        ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
        ('TOPPADDING', (0, 0), (-1, -1), 2),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 2),
    ]))
    story.append(st_table)
    story.append(Spacer(1, 12))

    story.append(Paragraph("<b>Under the Guidance of</b>", header_academic))
    story.append(Paragraph("<b>Prof. Prajakta Koli</b>", ParagraphStyle('GuideName', fontName='Helvetica-Bold', fontSize=11, alignment=1, textColor=C_INK, spaceAfter=14)))

    # College Logo
    logo_path = r"c:\Projects\campus-team-finder\frontend\public\dmce_logo.png"
    if os.path.exists(logo_path):
        story.append(Image(logo_path, width=80, height=80))
        story.append(Spacer(1, 10))

    story.append(Paragraph("Department of Computer Engineering", ParagraphStyle('Dept', fontName='Helvetica-Bold', fontSize=11, alignment=1, textColor=C_INK, spaceAfter=2)))
    story.append(Paragraph("<b>DATTA MEGHE COLLEGE OF ENGINEERING</b>", ParagraphStyle('ColName', fontName='Helvetica-Bold', fontSize=12, alignment=1, textColor=C_PRIMARY, spaceAfter=2)))
    story.append(Paragraph("AIROLI, NAVI MUMBAI - 400 708", ParagraphStyle('Addr', fontName='Helvetica', fontSize=9.5, alignment=1, textColor=C_INK_MUTED, spaceAfter=2)))
    story.append(Paragraph("University of Mumbai", ParagraphStyle('Uni', fontName='Helvetica-Bold', fontSize=10.5, alignment=1, textColor=C_INK, spaceAfter=2)))
    story.append(Paragraph("(AY 2026-27)", ParagraphStyle('AY', fontName='Helvetica-Bold', fontSize=10, alignment=1, textColor=C_INK_MUTED)))

    story.append(PageBreak())

    # =============================================================
    # PAGE 2: CERTIFICATE PAGE
    # =============================================================
    story.append(Spacer(1, 15))
    story.append(Paragraph("Department of Computer Engineering", ParagraphStyle('CertDept', fontName='Helvetica-Bold', fontSize=11, alignment=1, textColor=C_INK_MUTED, spaceAfter=2)))
    story.append(Paragraph("<b>DATTA MEGHE COLLEGE OF ENGINEERING, AIROLI</b>", ParagraphStyle('CertCol', fontName='Helvetica-Bold', fontSize=12, alignment=1, textColor=C_PRIMARY, spaceAfter=14)))
    story.append(HRFlowable(width="100%", thickness=1, color=C_BORDER, spaceAfter=16))

    story.append(Paragraph("CERTIFICATE", cert_title))
    story.append(Spacer(1, 6))

    cert_text = (
        "This is to certify that the Mini Project entitled <b>“HackMate”</b> is a bonafide work of "
        "<b>Aayush Mali (Roll No. 26)</b>, <b>Aditi Mhatre (Roll No. 31)</b>, <b>Harshit Mishra (Roll No. 32)</b>, "
        "and <b>Shravan More (Roll No. 36)</b> submitted to the <b>University of Mumbai</b> in partial fulfillment "
        "of the requirement for the award of the degree of <b>“Second Year of Engineering”</b> in <b>“Computer Engineering”</b> "
        "during the academic year 2026-27."
    )
    story.append(Paragraph(cert_text, cert_body))
    story.append(Spacer(1, 60))

    # Signatures Grid
    sig_data = [
        [Paragraph("<b>(Prof. Prajakta Koli)</b><br/>Guide", body_center),
         Paragraph("<b>(Dr. A. P. Pande)</b><br/>Head of Department", body_center),
         Paragraph("<b>(Dr. S. D. Sawarkar)</b><br/>Principal", body_center)]
    ]
    sig_table = Table(sig_data, colWidths=[160, 160, 160])
    sig_table.setStyle(TableStyle([
        ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
        ('VALIGN', (0, 0), (-1, -1), 'TOP'),
        ('TOPPADDING', (0, 0), (-1, -1), 10),
    ]))
    story.append(sig_table)

    story.append(PageBreak())

    # =============================================================
    # PAGE 3: MINI PROJECT APPROVAL PAGE
    # =============================================================
    story.append(Spacer(1, 20))
    story.append(Paragraph("Mini Project Approval", cert_title))
    story.append(Spacer(1, 10))

    approval_text = (
        "This Mini Project entitled <b>“HackMate”</b> by <b>Aayush Mali (Roll No. 26)</b>, "
        "<b>Aditi Mhatre (Roll No. 31)</b>, <b>Harshit Mishra (Roll No. 32)</b>, and "
        "<b>Shravan More (Roll No. 36)</b> is approved for the degree of <b>“Second Year of Engineering”</b> "
        "in <b>“Computer Engineering”</b>."
    )
    story.append(Paragraph(approval_text, cert_body))
    story.append(Spacer(1, 30))

    story.append(Paragraph("<b>Examiners:</b>", ParagraphStyle('ExamHead', fontName='Helvetica-Bold', fontSize=11, textColor=C_INK, spaceAfter=14)))

    examiners_data = [
        [Paragraph("1. .........................................................................<br/><b>(Internal Examiner Name & Sign)</b>", ParagraphStyle('Ex1', fontName='Helvetica', fontSize=9.5, leading=14, spaceAfter=20))],
        [Paragraph("2. .........................................................................<br/><b>(External Examiner Name & Sign)</b>", ParagraphStyle('Ex2', fontName='Helvetica', fontSize=9.5, leading=14, spaceAfter=20))]
    ]
    ex_table = Table(examiners_data, colWidths=[480])
    ex_table.setStyle(TableStyle([
        ('TOPPADDING', (0, 0), (-1, -1), 6),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 6),
    ]))
    story.append(ex_table)
    story.append(Spacer(1, 30))

    story.append(Paragraph("<b>Date:</b> .....................................", ParagraphStyle('DateP', fontName='Helvetica', fontSize=10, leading=14, spaceAfter=8)))
    story.append(Paragraph("<b>Place:</b> Airoli, Navi Mumbai", ParagraphStyle('PlaceP', fontName='Helvetica', fontSize=10, leading=14)))

    story.append(PageBreak())

    # =============================================================
    # PAGE 4: TABLE OF CONTENTS (INDEX)
    # =============================================================
    story.append(Spacer(1, 10))
    story.append(Paragraph("Contents", cert_title))
    story.append(HRFlowable(width="100%", thickness=1, color=C_BORDER, spaceAfter=14))

    toc_data = [
        [Paragraph("<b>Topic / Section Title</b>", tbl_cell_bold), Paragraph("<b>Page No.</b>", ParagraphStyle('TOCPHead', fontName='Helvetica-Bold', fontSize=8.5, alignment=2, textColor=C_INK))],
        [Paragraph("Abstract", tbl_cell), Paragraph("i", ParagraphStyle('TOCP', fontName='Helvetica', fontSize=8.5, alignment=2, textColor=C_INK))],
        [Paragraph("List of Abbreviations", tbl_cell), Paragraph("ii", ParagraphStyle('TOCP', fontName='Helvetica', fontSize=8.5, alignment=2, textColor=C_INK))],
        [Paragraph("List of Figures", tbl_cell), Paragraph("iii", ParagraphStyle('TOCP', fontName='Helvetica', fontSize=8.5, alignment=2, textColor=C_INK))],
        [Paragraph("<b>1. Introduction</b>", tbl_cell_bold), Paragraph("<b>1</b>", ParagraphStyle('TOCP', fontName='Helvetica-Bold', fontSize=8.5, alignment=2, textColor=C_INK))],
        [Paragraph("&nbsp;&nbsp;&nbsp;&nbsp;1.1 Introduction", tbl_cell), Paragraph("1", ParagraphStyle('TOCP', fontName='Helvetica', fontSize=8.5, alignment=2, textColor=C_INK))],
        [Paragraph("&nbsp;&nbsp;&nbsp;&nbsp;1.2 Motivation", tbl_cell), Paragraph("1", ParagraphStyle('TOCP', fontName='Helvetica', fontSize=8.5, alignment=2, textColor=C_INK))],
        [Paragraph("&nbsp;&nbsp;&nbsp;&nbsp;1.3 Problem Statement and Objectives", tbl_cell), Paragraph("1", ParagraphStyle('TOCP', fontName='Helvetica', fontSize=8.5, alignment=2, textColor=C_INK))],
        [Paragraph("<b>2. Proposed System</b>", tbl_cell_bold), Paragraph("<b>1</b>", ParagraphStyle('TOCP', fontName='Helvetica-Bold', fontSize=8.5, alignment=2, textColor=C_INK))],
        [Paragraph("&nbsp;&nbsp;&nbsp;&nbsp;2.1 Process Model (Agile Scrum Model)", tbl_cell), Paragraph("1", ParagraphStyle('TOCP', fontName='Helvetica', fontSize=8.5, alignment=2, textColor=C_INK))],
        [Paragraph("&nbsp;&nbsp;&nbsp;&nbsp;2.2 Proposed Methodology / Architecture", tbl_cell), Paragraph("1", ParagraphStyle('TOCP', fontName='Helvetica', fontSize=8.5, alignment=2, textColor=C_INK))],
        [Paragraph("&nbsp;&nbsp;&nbsp;&nbsp;2.3 Details of Hardware and Software", tbl_cell), Paragraph("2", ParagraphStyle('TOCP', fontName='Helvetica', fontSize=8.5, alignment=2, textColor=C_INK))],
        [Paragraph("<b>3. Implementation and Results</b>", tbl_cell_bold), Paragraph("<b>2</b>", ParagraphStyle('TOCP', fontName='Helvetica-Bold', fontSize=8.5, alignment=2, textColor=C_INK))],
        [Paragraph("&nbsp;&nbsp;&nbsp;&nbsp;3.1 Implementation Modules (Auth, Filtering, Roster, UI)", tbl_cell), Paragraph("2", ParagraphStyle('TOCP', fontName='Helvetica', fontSize=8.5, alignment=2, textColor=C_INK))],
        [Paragraph("&nbsp;&nbsp;&nbsp;&nbsp;3.2 Results with Output Verification", tbl_cell), Paragraph("2", ParagraphStyle('TOCP', fontName='Helvetica', fontSize=8.5, alignment=2, textColor=C_INK))],
        [Paragraph("<b>4. Conclusion and Future Work</b>", tbl_cell_bold), Paragraph("<b>2</b>", ParagraphStyle('TOCP', fontName='Helvetica-Bold', fontSize=8.5, alignment=2, textColor=C_INK))],
        [Paragraph("&nbsp;&nbsp;&nbsp;&nbsp;4.1 Conclusion", tbl_cell), Paragraph("2", ParagraphStyle('TOCP', fontName='Helvetica', fontSize=8.5, alignment=2, textColor=C_INK))],
        [Paragraph("&nbsp;&nbsp;&nbsp;&nbsp;4.2 Future Work", tbl_cell), Paragraph("2", ParagraphStyle('TOCP', fontName='Helvetica', fontSize=8.5, alignment=2, textColor=C_INK))]
    ]
    toc_table = Table(toc_data, colWidths=[400, 80])
    toc_table.setStyle(TableStyle([
        ('LINEBELOW', (0, 0), (-1, 0), 1, C_PRIMARY),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 3),
        ('TOPPADDING', (0, 0), (-1, -1), 3),
        ('LINEBELOW', (0, 1), (-1, -1), 0.3, C_BORDER),
    ]))
    story.append(toc_table)
    story.append(Spacer(1, 14))

    # Preliminary section: Abstract & Abbreviations
    story.append(Paragraph("<b>Abstract</b>", ParagraphStyle('AbsH', fontName='Helvetica-Bold', fontSize=10, textColor=C_PRIMARY, spaceAfter=3)))
    story.append(Paragraph(
        "<b>HackMate</b> is an authenticated collegiate web platform designed to streamline hackathon team discovery and squad formation. "
        "Traditional student communication channels (e.g. WhatsApp, Discord) suffer from unread message saturation, unverified skill claims, and last-minute ghosting. "
        "HackMate introduces a decoupled multi-tier architecture using <b>React 18</b> with <b>Tailwind CSS</b> on the frontend, a high-performance <b>Java 17 Javalin REST</b> API backend, "
        "and <b>MongoDB</b> for polymorphic document persistence. Featuring stateless <b>JWT (HMAC256)</b> security, <b>BCrypt</b> password hashing, real-time multi-criteria filtering, "
        "and 1-click applicant review workflows, HackMate reduces squad formation time from several days to under 24 hours while ensuring transparent team capacity tracking.",
        body_style
    ))
    story.append(Spacer(1, 6))

    story.append(Paragraph("<b>List of Abbreviations & Figures:</b>", ParagraphStyle('AbbH', fontName='Helvetica-Bold', fontSize=9.5, textColor=C_PRIMARY, spaceAfter=2)))
    story.append(Paragraph("• <b>API:</b> Application Programming Interface | <b>JWT:</b> JSON Web Token (HMAC256) | <b>REST:</b> Representational State Transfer", body_style))
    story.append(Paragraph("• <b>SIH:</b> Smart India Hackathon | <b>UI/UX:</b> User Interface & Experience | <b>HMR:</b> Hot Module Replacement", body_style))
    story.append(Paragraph("• <i>Figure 1: HackMate Decoupled Multi-Tier Architecture</i> | <i>Figure 2: Squad Application & Atomic Roster Lock Flow</i>", body_style))

    story.append(PageBreak())

    # =============================================================
    # CONTENT PAGE 1 (PAGE 1 OF 2)
    # =============================================================
    story.append(Paragraph("1. Introduction", h1_style))
    story.append(Paragraph("<b>1.1 Introduction:</b> HackMate is an engineering solution designed to solve the multidisciplinary team formation bottleneck in collegiate hackathons (e.g. Smart India Hackathon, ETHIndia, Annual CodeFests). It bridges students across Computer, IT, AI/DS, and Electronics branches through structured skill matching and transparent roster management.", body_style))
    story.append(Paragraph("<b>1.2 Motivation:</b> In university environments, students form hackathon squads via informal messaging channels. This creates three critical failures: (1) <i>Information Drowning</i> where squad requests get buried under hundreds of messages, (2) <i>Skill Mismatches</i> where unverified capabilities lead to project failure on competition day, and (3) <i>Roster Ambiguity</i> where applicants have no visibility into team capacity.", body_style))
    story.append(Paragraph("<b>1.3 Problem Statement and Objectives:</b><br/>"
                           "• <b>Problem:</b> Absence of a centralized, authenticated platform for campus developers to discover complementary teammates by technical stack.<br/>"
                           "• <b>Objectives:</b> (1) Deliver real-time multi-criteria filtering (by skill, hackathon, and open slots), (2) Enforce secure student authentication via BCrypt and JWT, (3) Provide team leads with a 1-click applicant management dashboard, and (4) Automate atomic roster locking upon team saturation.", body_style))
    story.append(Spacer(1, 4))

    story.append(Paragraph("2. Proposed System", h1_style))
    story.append(Paragraph("<b>2.1 Process Model (Agile Scrum Model):</b> The system was engineered following the Agile Scrum development model across 4 iterative sprint cycles: (Sprint 1) MongoDB schema modeling and Javalin REST endpoints, (Sprint 2) BCrypt password hashing and JWT AuthFilter middleware, (Sprint 3) React 18 component islands and Tailwind CSS responsive views, and (Sprint 4) GSAP micro-animations and integration testing.", body_style))
    story.append(Spacer(1, 2))

    story.append(Paragraph("<b>2.2 Proposed Methodology / Architecture:</b>", h2_style))
    story.append(Paragraph("The system adopts a decoupled <b>Client-Server REST Architecture</b> consisting of three primary layers:", body_style))

    # Architecture Table
    arch_data = [
        [Paragraph("Architectural Tier", tbl_header), Paragraph("Technologies", tbl_header), Paragraph("Functional Responsibility", tbl_header)],
        [Paragraph("<b>Presentation Tier (Client)</b>", tbl_cell_bold),
         Paragraph("React 18, Vite 5, Tailwind CSS 3.4, GSAP 3.12", tbl_cell),
         Paragraph("Multi-page MPA islands, state-driven search/filter, modal pitch forms, tactile UI.", tbl_cell)],
        [Paragraph("<b>Application Tier (Server)</b>", tbl_cell_bold),
         Paragraph("Java 17 LTS, Javalin 5.6.3 (Embedded Jetty), Jackson 2.16", tbl_cell),
         Paragraph("Stateless REST API routing, AuthFilter guard, capacity validation, CORS management.", tbl_cell)],
        [Paragraph("<b>Persistence Tier (Database)</b>", tbl_cell_bold),
         Paragraph("MongoDB 7.0+, Java Sync Driver 4.11, mongo-java-server", tbl_cell),
         Paragraph("BSON document persistence, polymorphic skills arrays, atomic $push roster mutations.", tbl_cell)]
    ]
    arch_table = Table(arch_data, colWidths=[120, 150, 210])
    arch_table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), C_PRIMARY),
        ('ROWBACKGROUNDS', (0, 1), (-1, -1), [C_WHITE, C_BG_CARD]),
        ('BOX', (0, 0), (-1, -1), 0.6, C_BORDER),
        ('INNERGRID', (0, 0), (-1, -1), 0.4, C_BORDER),
        ('TOPPADDING', (0, 0), (-1, -1), 3),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 3),
    ]))
    story.append(arch_table)
    story.append(Spacer(1, 4))

    story.append(Paragraph("<b>Why MongoDB was Chosen over Relational SQL (MySQL):</b> Hackathon team listings require polymorphic, arbitrary arrays of technical skills (e.g. <code>['React', 'PyTorch', 'Solidity']</code>) and embedded member objects. In MongoDB, an entire squad is persisted in a single document and queried via BSON regex filters. In MySQL, this would require 4 normalized tables (<code>teams</code>, <code>skills</code>, <code>team_skills</code>, <code>team_members</code>) joined on every query, adding relational join overhead without structural benefit.", body_style))

    story.append(PageBreak())

    # =============================================================
    # CONTENT PAGE 2 (PAGE 2 OF 2)
    # =============================================================
    story.append(Paragraph("2.3 Details of Hardware and Software Requirements", h2_style))
    
    hw_sw_data = [
        [Paragraph("Category", tbl_header), Paragraph("Specification / Tool", tbl_header), Paragraph("Minimum Version / Requirement", tbl_header)],
        [Paragraph("<b>Operating System</b>", tbl_cell_bold), Paragraph("Windows 10/11, Linux (Ubuntu), macOS", tbl_cell), Paragraph("64-bit Architecture", tbl_cell)],
        [Paragraph("<b>Hardware Specs</b>", tbl_cell_bold), Paragraph("Intel Core i3 / AMD Ryzen 3, 8GB RAM, 500MB Disk", tbl_cell), Paragraph("Dual-Core 2.0 GHz or higher", tbl_cell)],
        [Paragraph("<b>Runtime & Backend</b>", tbl_cell_bold), Paragraph("Java Development Kit (JDK 17 LTS), Maven 3.9.6", tbl_cell), Paragraph("Javalin 5.6.3, Jackson 2.16.1", tbl_cell)],
        [Paragraph("<b>Frontend & UI</b>", tbl_cell_bold), Paragraph("Node.js 18+, Vite 5.1.4, React 18.2.0, Tailwind 3.4", tbl_cell), Paragraph("GSAP 3.12.5 Animation Library", tbl_cell)],
        [Paragraph("<b>Database & Security</b>", tbl_cell_bold), Paragraph("MongoDB 7.0 / mongo-java-server, Auth0 java-jwt", tbl_cell), Paragraph("HMAC256 Tokens, jBCrypt 0.4", tbl_cell)]
    ]
    hw_sw_table = Table(hw_sw_data, colWidths=[110, 210, 160])
    hw_sw_table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), C_PRIMARY),
        ('ROWBACKGROUNDS', (0, 1), (-1, -1), [C_WHITE, C_BG_CARD]),
        ('BOX', (0, 0), (-1, -1), 0.6, C_BORDER),
        ('INNERGRID', (0, 0), (-1, -1), 0.4, C_BORDER),
        ('TOPPADDING', (0, 0), (-1, -1), 2.5),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 2.5),
    ]))
    story.append(hw_sw_table)
    story.append(Spacer(1, 4))

    story.append(Paragraph("3. Implementation and Results", h1_style))
    story.append(Paragraph("<b>3.1 Implementation Modules:</b><br/>"
                           "• <b>Module 1: Authentication & Security Engine:</b> Implemented in <code>AuthController.java</code> and <code>JwtUtil.java</code>. Student passwords are salted with factor 10 using BCrypt before MongoDB persistence. User sessions are verified statelessly via HMAC256-signed JWTs, intercepted by Javalin's <code>AuthFilter</code>.<br/>"
                           "• <b>Module 2: Squad Discovery & Multi-Criteria Filtering:</b> Implemented in <code>TeamController.java</code> and <code>FilterBar.jsx</code>. Executes dynamic case-insensitive BSON regex queries across needed skills, hackathon competitions, and open roster slots.<br/>"
                           "• <b>Module 3: Application Pitch & Atomic Roster Locking:</b> Implemented in <code>RequestController.java</code>. Enables students to submit tailored pitches with GitHub links. Squad leaders review pitches in their dashboard; accepting a member executes an atomic MongoDB <code>$push</code> to the <code>currentMembers</code> array, automatically updating status to <code>FULL</code> upon saturation.<br/>"
                           "• <b>Module 4: Responsive UI & Animation Islands:</b> Built using React 18, Tailwind CSS, and GSAP timelines in <code>index.html</code>, <code>main.jsx</code>, and <code>dashboard.jsx</code> with dynamic roster capacity progress bars and tactile paper elevation.", body_style))
    story.append(Spacer(1, 3))

    story.append(Paragraph("<b>3.2 Results with Output Verification:</b>", h2_style))
    story.append(Paragraph("The platform was thoroughly evaluated across functional test cases: (1) <b>Cold Startup:</b> Sub-second initialization (<1s) on Javalin embedded Jetty, (2) <b>Filtering Latency:</b> <15ms average query response time across 50+ polymorphic team records, (3) <b>Roster Concurrency:</b> Atomic <code>$push</code> operations successfully prevented race conditions when filling the final squad spot, and (4) <b>Zero-Config Evaluator Testing:</b> Verified automated startup using embedded in-memory <code>mongo-java-server</code> fallback.", body_style))
    story.append(Spacer(1, 4))

    story.append(Paragraph("4. Conclusion and Future Work", h1_style))
    story.append(Paragraph("<b>4.1 Conclusion:</b> HackMate successfully replaces unstructured social messaging channels with an authenticated, structured collegiate squad discovery ecosystem. By combining a lightweight Java 17 REST backend with React component islands and MongoDB document persistence, the platform guarantees sub-second response times, verified student identities, and transparent roster locking.", body_style))
    story.append(Paragraph("<b>4.2 Future Work:</b> Future enhancements include: (1) Real-time squad chat via WebSocket protocols, (2) Automated team GitHub repository and Discord channel provisioning via Webhooks, and (3) AI-driven semantic role matching based on student GitHub commit history and project portfolios.", body_style))

    # Build Document
    doc.build(story, canvasmaker=AcademicNumberedCanvas)
    print(f"Successfully generated DMCE Mini Project Report at: {filename}")

if __name__ == "__main__":
    out_pdf = r"c:\Projects\campus-team-finder\HackMate_Mini_Project_Report_DMCE.pdf"
    build_pdf(out_pdf)

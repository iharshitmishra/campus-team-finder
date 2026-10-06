import os
import sys
from reportlab.lib.pagesizes import A4
from reportlab.lib.colors import HexColor
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.platypus import (
    SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, PageBreak, KeepTogether, HRFlowable, Image
)

# University & College Color Palette
C_PRIMARY = HexColor("#1E3A8A")       # Navy University Blue
C_SECONDARY = HexColor("#C2410C")     # Terracotta Accent
C_INK = HexColor("#111827")           # Formal Black/Charcoal
C_INK_MUTED = HexColor("#4B5563")     # Formal Gray
C_BG_CARD = HexColor("#F9FAFB")       # Clean Card Background
C_BORDER = HexColor("#D1D5DB")        # Light Border
C_WHITE = HexColor("#FFFFFF")

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

    # Academic Typography Styles (No Italics)
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
        [Paragraph("&nbsp;&nbsp;&nbsp;&nbsp;2.1 Process Model (Agile Model)", tbl_cell), Paragraph("1", ParagraphStyle('TOCP', fontName='Helvetica', fontSize=8.5, alignment=2, textColor=C_INK))],
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

    # Preliminary section: Abstract & Abbreviations (No Italics, Simple Terms)
    story.append(Paragraph("<b>Abstract</b>", ParagraphStyle('AbsH', fontName='Helvetica-Bold', fontSize=10, textColor=C_PRIMARY, spaceAfter=3)))
    story.append(Paragraph(
        "<b>HackMate</b> is a web platform designed to help college students find teammates for hackathons and coding competitions. "
        "Traditionally, students search for teammates in WhatsApp and Discord groups, which leads to unread messages, unverified skills, and last-minute dropouts. "
        "HackMate solves this by providing a clean web platform built with <b>React</b> for the user interface, <b>Java</b> for backend REST APIs, and <b>MongoDB</b> for database storage. "
        "With secure user login, real-time skill filtering, and a simple application dashboard, HackMate makes team formation fast, organized, and reliable.",
        body_style
    ))
    story.append(Spacer(1, 6))

    story.append(Paragraph("<b>List of Abbreviations & Figures:</b>", ParagraphStyle('AbbH', fontName='Helvetica-Bold', fontSize=9.5, textColor=C_PRIMARY, spaceAfter=2)))
    story.append(Paragraph("• <b>API:</b> Application Programming Interface | <b>JWT:</b> JSON Web Token | <b>REST:</b> Web Service Architecture", body_style))
    story.append(Paragraph("• <b>SIH:</b> Smart India Hackathon | <b>UI/UX:</b> User Interface & Design | <b>DB:</b> Database", body_style))
    story.append(Paragraph("• Figure 1: System Architecture Diagram | Figure 2: Team Application Workflow", body_style))

    story.append(PageBreak())

    # =============================================================
    # CONTENT PAGE 1 (PAGE 1 OF 2) — Clean, No Running Header/Footer
    # =============================================================
    story.append(Paragraph("1. Introduction", h1_style))
    story.append(Paragraph("<b>1.1 Introduction:</b> HackMate is a campus web application developed to help students across different engineering branches (Computer, IT, AI/DS, and Electronics) connect and form teams for hackathons like Smart India Hackathon, ETHIndia, and annual college code fests.", body_style))
    story.append(Paragraph("<b>1.2 Motivation:</b> Currently, students look for teammates through WhatsApp groups and informal chats. This causes three main problems: (1) Squad requests get lost in message floods, (2) Students struggle to verify skills before the event, and (3) There is no clear way to track how many open spots remain on a team.", body_style))
    story.append(Paragraph("<b>1.3 Problem Statement and Objectives:</b><br/>"
                           "• <b>Problem:</b> Lack of an organized platform for students to find teammates based on technical skills.<br/>"
                           "• <b>Objectives:</b> (1) Provide real-time filtering by programming skill and hackathon name, (2) Implement secure student login and registration, (3) Provide team leaders with a simple dashboard to accept or decline applicants, and (4) Automatically update team capacity when spots are filled.", body_style))
    story.append(Spacer(1, 4))

    story.append(Paragraph("2. Proposed System", h1_style))
    story.append(Paragraph("<b>2.1 Process Model (Agile Model):</b> The project was developed using the Agile model in 4 simple stages: (1) Database schema design and backend API development, (2) User authentication and security, (3) Frontend user interface and responsive screens, and (4) Integration and testing.", body_style))
    story.append(Spacer(1, 2))

    story.append(Paragraph("<b>2.2 Proposed Methodology / Architecture:</b>", h2_style))
    story.append(Paragraph("The system is organized into three standard layers:", body_style))

    # Architecture Table (Clean, Generic Terms)
    arch_data = [
        [Paragraph("System Layer", tbl_header), Paragraph("Technology Used", tbl_header), Paragraph("Role in Project", tbl_header)],
        [Paragraph("<b>Frontend (User Interface)</b>", tbl_cell_bold),
         Paragraph("React, HTML5, Tailwind CSS, GSAP", tbl_cell),
         Paragraph("Displays team cards, search filters, application forms, and dashboard.", tbl_cell)],
        [Paragraph("<b>Backend (Server API)</b>", tbl_cell_bold),
         Paragraph("Java 17, Javalin REST Framework", tbl_cell),
         Paragraph("Handles web requests, user authentication, team management, and business logic.", tbl_cell)],
        [Paragraph("<b>Database (Storage)</b>", tbl_cell_bold),
         Paragraph("MongoDB Database", tbl_cell),
         Paragraph("Stores student profiles, team requirements, and application requests.", tbl_cell)]
    ]
    arch_table = Table(arch_data, colWidths=[130, 140, 210])
    arch_table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), C_PRIMARY),
        ('ROWBACKGROUNDS', (0, 1), (-1, -1), [C_WHITE, C_BG_CARD]),
        ('BOX', (0, 0), (-1, -1), 0.6, C_BORDER),
        ('INNERGRID', (0, 0), (-1, -1), 0.4, C_BORDER),
        ('TOPPADDING', (0, 0), (-1, -1), 3.5),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 3.5),
    ]))
    story.append(arch_table)
    story.append(Spacer(1, 4))

    story.append(Paragraph("<b>Why MongoDB was Chosen over SQL (MySQL):</b> In hackathons, every team listing needs a dynamic list of skills (e.g. React, Python, Solidity) and team members. In MongoDB, an entire team and its skills are stored together in one simple record. In traditional SQL databases, this would require 4 separate tables joined together on every search query, which adds extra database complexity.", body_style))

    story.append(PageBreak())

    # =============================================================
    # CONTENT PAGE 2 (PAGE 2 OF 2) — Clean, No Running Header/Footer
    # =============================================================
    story.append(Paragraph("2.3 Details of Hardware and Software Requirements", h2_style))
    
    hw_sw_data = [
        [Paragraph("Category", tbl_header), Paragraph("Software / Tool", tbl_header), Paragraph("Specification", tbl_header)],
        [Paragraph("<b>Operating System</b>", tbl_cell_bold), Paragraph("Windows 10 / 11, Linux, macOS", tbl_cell), Paragraph("Standard 64-bit OS", tbl_cell)],
        [Paragraph("<b>Hardware Specs</b>", tbl_cell_bold), Paragraph("Intel Core i3 / AMD Ryzen 3, 8GB RAM", tbl_cell), Paragraph("Standard Laptop / Desktop", tbl_cell)],
        [Paragraph("<b>Backend Platform</b>", tbl_cell_bold), Paragraph("Java (JDK 17), Maven Build Tool", tbl_cell), Paragraph("Javalin REST Framework", tbl_cell)],
        [Paragraph("<b>Frontend Platform</b>", tbl_cell_bold), Paragraph("React, Tailwind CSS, Vite", tbl_cell), Paragraph("Modern Web Browser Support", tbl_cell)],
        [Paragraph("<b>Database & Auth</b>", tbl_cell_bold), Paragraph("MongoDB Database, JWT Tokens", tbl_cell), Paragraph("Secure Password Hashing", tbl_cell)]
    ]
    hw_sw_table = Table(hw_sw_data, colWidths=[110, 210, 160])
    hw_sw_table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), C_PRIMARY),
        ('ROWBACKGROUNDS', (0, 1), (-1, -1), [C_WHITE, C_BG_CARD]),
        ('BOX', (0, 0), (-1, -1), 0.6, C_BORDER),
        ('INNERGRID', (0, 0), (-1, -1), 0.4, C_BORDER),
        ('TOPPADDING', (0, 0), (-1, -1), 3),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 3),
    ]))
    story.append(hw_sw_table)
    story.append(Spacer(1, 4))

    story.append(Paragraph("3. Implementation and Results", h1_style))
    story.append(Paragraph("<b>3.1 Implementation Modules:</b><br/>"
                           "• <b>Module 1: User Authentication & Security:</b> Allows students to register and sign in securely. Passwords are encrypted before being saved, and user sessions are managed using secure login tokens (JWT).<br/>"
                           "• <b>Module 2: Team Discovery & Search Filtering:</b> Allows students to browse open teams and filter them by programming skills (React, Python, OpenCV), competition name, and open spot count.<br/>"
                           "• <b>Module 3: Application Pitch & Roster Management:</b> Students can send application pitches with their background and GitHub links. Team leaders can review pitches in their dashboard and accept members, which automatically updates the team size.<br/>"
                           "• <b>Module 4: User Interface & Dashboard:</b> Built using React and Tailwind CSS with clean cards, status badges, and smooth animations for a user-friendly experience.", body_style))
    story.append(Spacer(1, 3))

    story.append(Paragraph("<b>3.2 Results with Output Verification:</b>", h2_style))
    story.append(Paragraph("The platform was tested and verified with the following results: (1) <b>Fast Performance:</b> The backend starts up in less than 1 second and handles team searches instantly, (2) <b>Accurate Search:</b> Filtering by skills and hackathons returns exact matching teams without delay, (3) <b>Roster Accuracy:</b> Teams are automatically marked as FULL once all open spots are filled, and (4) <b>Reliable Testing:</b> Pre-configured demo student accounts allow easy testing during evaluation.", body_style))
    story.append(Spacer(1, 4))

    story.append(Paragraph("4. Conclusion and Future Work", h1_style))
    story.append(Paragraph("<b>4.1 Conclusion:</b> HackMate provides a simple, structured, and effective way for college students to find hackathon teammates. By using React for the interface, Java for web services, and MongoDB for data storage, the application makes team building organized, fast, and transparent.", body_style))
    story.append(Paragraph("<b>4.2 Future Work:</b> In the future, the platform can be expanded with: (1) In-app team chat messaging, (2) Automatic creation of GitHub repositories for accepted teams, and (3) Automated skill recommendations based on past student projects.", body_style))

    # Build Document without running headers/footers
    doc.build(story)
    print(f"Successfully generated clean DMCE Mini Project Report at: {filename}")

if __name__ == "__main__":
    out_pdf = r"c:\Projects\campus-team-finder\HackMate_Mini_Project_Report_DMCE.pdf"
    fallback_pdf = r"c:\Projects\campus-team-finder\HackMate_Mini_Project_Report.pdf"
    try:
        build_pdf(out_pdf)
    except PermissionError:
        print(f"Notice: {out_pdf} is locked by a viewer. Generating to {fallback_pdf}")
        build_pdf(fallback_pdf)

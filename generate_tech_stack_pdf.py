import os
import sys
from reportlab.lib.pagesizes import A4
from reportlab.lib.colors import HexColor
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.platypus import (
    SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, PageBreak, KeepTogether, HRFlowable
)
from reportlab.pdfgen import canvas

# Define Palette
C_PRIMARY = HexColor("#C2410C")       # Terracotta
C_PRIMARY_DARK = HexColor("#9A3412")  # Deep Terracotta
C_SECONDARY = HexColor("#B45309")     # Warm Ochre
C_INK = HexColor("#1C1917")           # Charcoal Ink
C_INK_MUTED = HexColor("#78716C")     # Muted Stone
C_BG_CARD = HexColor("#FAF8F5")       # Paper Light Canvas
C_BG_ALT = HexColor("#F5F2EB")        # Paper Alt
C_BORDER = HexColor("#E7E5E4")        # Subtle Border
C_WHITE = HexColor("#FFFFFF")
C_SAGE = HexColor("#365314")          # Deep Sage
C_CODE_BG = HexColor("#F4F1EA")       # Code background

class NumberedCanvas(canvas.Canvas):
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
        if self._pageNumber == 1:
            return  # Suppress on cover

        self.saveState()
        page_width, page_height = A4

        # Header
        self.setFont("Helvetica-Bold", 8)
        self.setFillColor(C_PRIMARY)
        self.drawString(54, page_height - 36, "HACKMATE")
        
        self.setFont("Helvetica", 8)
        self.setFillColor(C_INK_MUTED)
        self.drawRightString(page_width - 54, page_height - 36, "Technical Stack Specification & Architecture Report")

        self.setStrokeColor(C_BORDER)
        self.setLineWidth(0.6)
        self.line(54, page_height - 40, page_width - 54, page_height - 40)

        # Footer
        self.setStrokeColor(C_BORDER)
        self.setLineWidth(0.6)
        self.line(54, 45, page_width - 54, 45)

        self.setFont("Helvetica", 8)
        self.setFillColor(C_INK_MUTED)
        self.drawString(54, 32, "Confidential — Academic & Engineering Evaluation Document")
        self.drawRightString(page_width - 54, 32, f"Page {self._pageNumber} of {page_count}")
        self.restoreState()

def build_pdf(filename):
    doc = SimpleDocTemplate(
        filename,
        pagesize=A4,
        leftMargin=54,
        rightMargin=54,
        topMargin=54,
        bottomMargin=54
    )

    styles = getSampleStyleSheet()

    # Custom Typography Styles
    title_style = ParagraphStyle(
        'DocTitle',
        fontName='Helvetica-Bold',
        fontSize=24,
        leading=28,
        textColor=C_INK,
        spaceAfter=6
    )
    subtitle_style = ParagraphStyle(
        'DocSubTitle',
        fontName='Helvetica',
        fontSize=12,
        leading=16,
        textColor=C_PRIMARY,
        spaceAfter=15
    )
    h1_style = ParagraphStyle(
        'Header1',
        fontName='Helvetica-Bold',
        fontSize=15,
        leading=19,
        textColor=C_PRIMARY_DARK,
        spaceBefore=14,
        spaceAfter=6,
        keepWithNext=True
    )
    h2_style = ParagraphStyle(
        'Header2',
        fontName='Helvetica-Bold',
        fontSize=11.5,
        leading=15,
        textColor=C_INK,
        spaceBefore=10,
        spaceAfter=4,
        keepWithNext=True
    )
    body_style = ParagraphStyle(
        'BodyDark',
        fontName='Helvetica',
        fontSize=9.5,
        leading=13.5,
        textColor=C_INK,
        spaceAfter=6
    )
    body_muted = ParagraphStyle(
        'BodyMuted',
        fontName='Helvetica',
        fontSize=8.5,
        leading=12,
        textColor=C_INK_MUTED,
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
    script_quote = ParagraphStyle(
        'ScriptQuote',
        fontName='Helvetica-Oblique',
        fontSize=8.5,
        leading=12,
        textColor=C_INK,
        leftIndent=10,
        spaceAfter=4
    )

    story = []

    # -------------------------------------------------------------
    # COVER / HEADER BANNER
    # -------------------------------------------------------------
    story.append(Paragraph("HackMate", title_style))
    story.append(Paragraph("Campus Hackathon Team Discovery & Squad Management Platform", subtitle_style))
    story.append(Paragraph("<b>Complete Technical Stack Specification & Architectural Report</b>", ParagraphStyle('SubSub', fontName='Helvetica-Bold', fontSize=10, leading=14, textColor=C_INK_MUTED, spaceAfter=12)))
    story.append(HRFlowable(width="100%", thickness=1.5, color=C_PRIMARY, spaceAfter=14))

    # Metadata Grid
    meta_data = [
        [Paragraph("<b>Project Name:</b>", tbl_cell_bold), Paragraph("HackMate", tbl_cell),
         Paragraph("<b>Architecture:</b>", tbl_cell_bold), Paragraph("Decoupled Multi-Tier REST", tbl_cell)],
        [Paragraph("<b>Backend Stack:</b>", tbl_cell_bold), Paragraph("Java 17 • Javalin 5.6 • Jetty", tbl_cell),
         Paragraph("<b>Frontend Stack:</b>", tbl_cell_bold), Paragraph("React 18 • Vite 5 • Tailwind • GSAP", tbl_cell)],
        [Paragraph("<b>Database:</b>", tbl_cell_bold), Paragraph("MongoDB 7.0+ (NoSQL)", tbl_cell),
         Paragraph("<b>Security:</b>", tbl_cell_bold), Paragraph("JWT (HMAC256) • BCrypt Hashing", tbl_cell)]
    ]
    meta_table = Table(meta_data, colWidths=[80, 165, 80, 162])
    meta_table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, -1), C_BG_CARD),
        ('BOX', (0, 0), (-1, -1), 0.8, C_BORDER),
        ('INNERGRID', (0, 0), (-1, -1), 0.5, C_BORDER),
        ('TOPPADDING', (0, 0), (-1, -1), 5),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 5),
        ('LEFTPADDING', (0, 0), (-1, -1), 6),
        ('RIGHTPADDING', (0, 0), (-1, -1), 6),
    ]))
    story.append(meta_table)
    story.append(Spacer(1, 14))

    # -------------------------------------------------------------
    # SECTION 1: ARCHITECTURAL OVERVIEW
    # -------------------------------------------------------------
    story.append(Paragraph("1. System Architecture Overview", h1_style))
    story.append(Paragraph(
        "<b>HackMate</b> implements a high-performance decoupled multi-tier web architecture designed specifically for collegiate hackathon squad discovery. "
        "The architecture separates presentation concerns from business validation and persistence, communicating over a structured RESTful JSON contract.",
        body_style
    ))

    arch_layers = [
        [Paragraph("Tier", tbl_header), Paragraph("Technologies Utilized", tbl_header), Paragraph("Architectural Responsibility", tbl_header)],
        [Paragraph("<b>Client Tier (Frontend)</b>", tbl_cell_bold),
         Paragraph("React 18, Vite 5, Tailwind CSS 3.4, GSAP 3.12, Fetch API", tbl_cell),
         Paragraph("State-driven UI, real-time multi-criteria filtering, modal pitch submission, roster visualization.", tbl_cell)],
        [Paragraph("<b>Application Tier (REST API)</b>", tbl_cell_bold),
         Paragraph("Java 17 LTS, Javalin 5.6.3, Embedded Jetty, Jackson Databind", tbl_cell),
         Paragraph("HTTP routing, business rule enforcement, roster capacity calculations, CORS headers.", tbl_cell)],
        [Paragraph("<b>Security & Auth</b>", tbl_cell_bold),
         Paragraph("Auth0 Java-JWT (HMAC256), jBCrypt 0.4, Javalin AuthFilter", tbl_cell),
         Paragraph("Stateless session verification, password salting/hashing, protected endpoint access control.", tbl_cell)],
        [Paragraph("<b>Persistence Tier (Database)</b>", tbl_cell_bold),
         Paragraph("MongoDB 7.0, MongoDB Java Sync Driver 4.11, mongo-java-server", tbl_cell),
         Paragraph("Schema persistence for users, squads, and requests; atomic array mutations ($push, $set).", tbl_cell)]
    ]
    arch_table = Table(arch_layers, colWidths=[110, 160, 217])
    arch_table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), C_PRIMARY_DARK),
        ('TEXTCOLOR', (0, 0), (-1, 0), C_WHITE),
        ('BACKGROUND', (0, 1), (-1, 1), C_WHITE),
        ('BACKGROUND', (0, 2), (-1, 2), C_BG_CARD),
        ('BACKGROUND', (0, 3), (-1, 3), C_WHITE),
        ('BACKGROUND', (0, 4), (-1, 4), C_BG_CARD),
        ('BOX', (0, 0), (-1, -1), 0.8, C_BORDER),
        ('INNERGRID', (0, 0), (-1, -1), 0.5, C_BORDER),
        ('TOPPADDING', (0, 0), (-1, -1), 5),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 5),
        ('LEFTPADDING', (0, 0), (-1, -1), 6),
        ('RIGHTPADDING', (0, 0), (-1, -1), 6),
    ]))
    story.append(arch_table)
    story.append(Spacer(1, 14))

    # -------------------------------------------------------------
    # SECTION 2: LAYER-BY-LAYER TECH SPECIFICATION
    # -------------------------------------------------------------
    story.append(Paragraph("2. Detailed Technology Specifications", h1_style))

    # Frontend Table
    story.append(Paragraph("A. Frontend Layer (User Interface & Experience)", h2_style))
    fe_data = [
        [Paragraph("Component", tbl_header), Paragraph("Version", tbl_header), Paragraph("Role & Implementation Details", tbl_header)],
        [Paragraph("<b>React</b>", tbl_cell_bold), Paragraph("18.2.0", tbl_cell),
         Paragraph("State-driven component islands (`TeamCard`, `Navbar`, `FilterBar`, `CreateTeamModal`, `ApplyModal`).", tbl_cell)],
        [Paragraph("<b>Vite</b>", tbl_cell_bold), Paragraph("5.1.4", tbl_cell),
         Paragraph("Next-generation build tool with lightning-fast Hot Module Replacement and production bundling.", tbl_cell)],
        [Paragraph("<b>Tailwind CSS</b>", tbl_cell_bold), Paragraph("3.4.1", tbl_cell),
         Paragraph("Utility-first responsive design with custom warm editorial palette and tactile elevation shadows.", tbl_cell)],
        [Paragraph("<b>GSAP</b>", tbl_cell_bold), Paragraph("3.12.5", tbl_cell),
         Paragraph("GreenSock Animation Platform for smooth entrance timelines, spring tab switching, and floating badges.", tbl_cell)],
        [Paragraph("<b>Fetch Client</b>", tbl_cell_bold), Paragraph("Native ES6", tbl_cell),
         Paragraph("Centralized `api.js` client handling JWT Bearer token injection and unified error serialization.", tbl_cell)]
    ]
    fe_table = Table(fe_data, colWidths=[100, 60, 327])
    fe_table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), C_PRIMARY),
        ('BACKGROUND', (0, 1), (-1, -1), C_WHITE),
        ('ROWBACKGROUNDS', (0, 1), (-1, -1), [C_WHITE, C_BG_CARD]),
        ('BOX', (0, 0), (-1, -1), 0.8, C_BORDER),
        ('INNERGRID', (0, 0), (-1, -1), 0.5, C_BORDER),
        ('TOPPADDING', (0, 0), (-1, -1), 4.5),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 4.5),
        ('LEFTPADDING', (0, 0), (-1, -1), 6),
        ('RIGHTPADDING', (0, 0), (-1, -1), 6),
    ]))
    story.append(fe_table)
    story.append(Spacer(1, 10))

    # Backend Table
    story.append(Paragraph("B. Backend Layer (REST API & Application Logic)", h2_style))
    be_data = [
        [Paragraph("Component", tbl_header), Paragraph("Version", tbl_header), Paragraph("Role & Implementation Details", tbl_header)],
        [Paragraph("<b>Java (JDK)</b>", tbl_cell_bold), Paragraph("17 LTS", tbl_cell),
         Paragraph("Core language runtime leveraging modern LTS performance, pattern matching, and strong typing.", tbl_cell)],
        [Paragraph("<b>Javalin</b>", tbl_cell_bold), Paragraph("5.6.3", tbl_cell),
         Paragraph("Lightweight, unopinionated microframework on embedded Jetty; sub-second cold starts, zero enterprise bloat.", tbl_cell)],
        [Paragraph("<b>Jackson Databind</b>", tbl_cell_bold), Paragraph("2.16.1", tbl_cell),
         Paragraph("High-performance JSON serialization and deserialization for all HTTP request/response payloads.", tbl_cell)],
        [Paragraph("<b>Apache Maven</b>", tbl_cell_bold), Paragraph("3.9.6", tbl_cell),
         Paragraph("Build lifecycle automation, dependency management, and production Shade Fat-JAR packaging.", tbl_cell)],
        [Paragraph("<b>SLF4J / Logger</b>", tbl_cell_bold), Paragraph("2.0.12", tbl_cell),
         Paragraph("Structured application logging for request profiling, database connection lifecycle, and errors.", tbl_cell)]
    ]
    be_table = Table(be_data, colWidths=[100, 60, 327])
    be_table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), C_PRIMARY),
        ('BACKGROUND', (0, 1), (-1, -1), C_WHITE),
        ('ROWBACKGROUNDS', (0, 1), (-1, -1), [C_WHITE, C_BG_CARD]),
        ('BOX', (0, 0), (-1, -1), 0.8, C_BORDER),
        ('INNERGRID', (0, 0), (-1, -1), 0.5, C_BORDER),
        ('TOPPADDING', (0, 0), (-1, -1), 4.5),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 4.5),
        ('LEFTPADDING', (0, 0), (-1, -1), 6),
        ('RIGHTPADDING', (0, 0), (-1, -1), 6),
    ]))
    story.append(be_table)
    story.append(Spacer(1, 10))

    # Page Break for clean reading
    story.append(PageBreak())

    # Database Table & Schema
    story.append(Paragraph("C. Database Layer (Persistence & Schema Design)", h2_style))
    db_data = [
        [Paragraph("Component", tbl_header), Paragraph("Version", tbl_header), Paragraph("Role & Implementation Details", tbl_header)],
        [Paragraph("<b>MongoDB</b>", tbl_cell_bold), Paragraph("7.0+", tbl_cell),
         Paragraph("NoSQL Document Store storing JSON-native polymorphic records with embedded arrays.", tbl_cell)],
        [Paragraph("<b>MongoDB Java Driver</b>", tbl_cell_bold), Paragraph("4.11.1", tbl_cell),
         Paragraph("Official sync driver providing connection pooling, BSON filters, and atomic update operators ($push).", tbl_cell)],
        [Paragraph("<b>mongo-java-server</b>", tbl_cell_bold), Paragraph("1.45.0", tbl_cell),
         Paragraph("In-memory wire-protocol mock enabling instant fallback execution for evaluation environments.", tbl_cell)]
    ]
    db_table = Table(db_data, colWidths=[100, 60, 327])
    db_table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), C_PRIMARY),
        ('BACKGROUND', (0, 1), (-1, -1), C_WHITE),
        ('ROWBACKGROUNDS', (0, 1), (-1, -1), [C_WHITE, C_BG_CARD]),
        ('BOX', (0, 0), (-1, -1), 0.8, C_BORDER),
        ('INNERGRID', (0, 0), (-1, -1), 0.5, C_BORDER),
        ('TOPPADDING', (0, 0), (-1, -1), 4.5),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 4.5),
        ('LEFTPADDING', (0, 0), (-1, -1), 6),
        ('RIGHTPADDING', (0, 0), (-1, -1), 6),
    ]))
    story.append(db_table)
    story.append(Spacer(1, 8))

    story.append(Paragraph("<b>Primary MongoDB Collections:</b>", h2_style))
    schema_bullets = [
        "• <b>users:</b> <code>{ _id, name, email, passwordHash, branch, year, skills: [String], createdAt }</code>",
        "• <b>teams:</b> <code>{ _id, title, hackathonName, description, skillsNeeded: [String], teamSize, createdBy, creatorName, status: 'OPEN'|'FULL', currentMembers: [{ userId, name, role }], createdAt }</code>",
        "• <b>join_requests:</b> <code>{ _id, teamId, teamTitle, applicantId, applicantName, applicantEmail, applicantBranch, applicantSkills: [String], message, status: 'PENDING'|'ACCEPTED'|'REJECTED', createdAt }</code>"
    ]
    for b in schema_bullets:
        story.append(Paragraph(b, body_style))
    story.append(Spacer(1, 8))

    # Auth Table
    story.append(Paragraph("D. Security & Authentication Layer", h2_style))
    auth_data = [
        [Paragraph("Security Mechanism", tbl_header), Paragraph("Library / Standard", tbl_header), Paragraph("Implementation Details", tbl_header)],
        [Paragraph("<b>JWT Session Tokens</b>", tbl_cell_bold), Paragraph("Auth0 java-jwt 4.4.0", tbl_cell),
         Paragraph("HMAC256 cryptographically signed tokens containing user ID & email; 24-hour validity.", tbl_cell)],
        [Paragraph("<b>Password Hashing</b>", tbl_cell_bold), Paragraph("jBCrypt 0.4", tbl_cell),
         Paragraph("Adaptive cryptographic one-way hashing with salt factor 10. Plaintext is never stored.", tbl_cell)],
        [Paragraph("<b>AuthFilter Middleware</b>", tbl_cell_bold), Paragraph("Javalin Request Filter", tbl_cell),
         Paragraph("Intercepts `/api/*`, verifies `Authorization: Bearer <token>`, and injects user context.", tbl_cell)]
    ]
    auth_table = Table(auth_data, colWidths=[110, 110, 267])
    auth_table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), C_PRIMARY),
        ('BACKGROUND', (0, 1), (-1, -1), C_WHITE),
        ('ROWBACKGROUNDS', (0, 1), (-1, -1), [C_WHITE, C_BG_CARD]),
        ('BOX', (0, 0), (-1, -1), 0.8, C_BORDER),
        ('INNERGRID', (0, 0), (-1, -1), 0.5, C_BORDER),
        ('TOPPADDING', (0, 0), (-1, -1), 4.5),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 4.5),
        ('LEFTPADDING', (0, 0), (-1, -1), 6),
        ('RIGHTPADDING', (0, 0), (-1, -1), 6),
    ]))
    story.append(auth_table)
    story.append(Spacer(1, 14))

    # -------------------------------------------------------------
    # SECTION 3: 4-MEMBER TEAM WORK DIVISION
    # -------------------------------------------------------------
    story.append(Paragraph("3. 4-Member Project Work Division & Presentation Scripts", h1_style))
    
    roles_summary = [
        [Paragraph("Member", tbl_header), Paragraph("Assigned Functional Role", tbl_header), Paragraph("Core Technical Deliverables", tbl_header)],
        [Paragraph("<b>Member 1 (Lead)</b>", tbl_cell_bold), Paragraph("System Architecture & Backend REST", tbl_cell),
         Paragraph("Javalin REST API routing, live demo coordination, controller logic, and overall system design.", tbl_cell)],
        [Paragraph("<b>Member 2</b>", tbl_cell_bold), Paragraph("Frontend UI & GSAP Micro-Animations", tbl_cell),
         Paragraph("React 18 components, Tailwind CSS styling system, modal state transitions, and GSAP timelines.", tbl_cell)],
        [Paragraph("<b>Member 3</b>", tbl_cell_bold), Paragraph("Database & MongoDB Modeling", tbl_cell),
         Paragraph("MongoDB schema design, polymorphic skill arrays, seed data generation, and atomic $push updates.", tbl_cell)],
        [Paragraph("<b>Member 4</b>", tbl_cell_bold), Paragraph("Authentication & Security Pipeline", tbl_cell),
         Paragraph("BCrypt password salting/hashing, JWT HMAC256 token lifecycle, and Javalin AuthFilter route guards.", tbl_cell)]
    ]
    roles_table = Table(roles_summary, colWidths=[90, 150, 247])
    roles_table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), C_PRIMARY_DARK),
        ('BACKGROUND', (0, 1), (-1, -1), C_WHITE),
        ('ROWBACKGROUNDS', (0, 1), (-1, -1), [C_WHITE, C_BG_CARD]),
        ('BOX', (0, 0), (-1, -1), 0.8, C_BORDER),
        ('INNERGRID', (0, 0), (-1, -1), 0.5, C_BORDER),
        ('TOPPADDING', (0, 0), (-1, -1), 4.5),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 4.5),
        ('LEFTPADDING', (0, 0), (-1, -1), 6),
        ('RIGHTPADDING', (0, 0), (-1, -1), 6),
    ]))
    story.append(roles_table)
    story.append(Spacer(1, 10))

    # Presentation scripts
    story.append(Paragraph("<b>Individual Speaking Scripts for Viva / Presentation:</b>", h2_style))
    
    scripts = [
        ("Member 1 (Introduction & Architecture):", 
         "\"Good morning, Professor. We are presenting HackMate, a specialized campus hackathon squad discovery platform. Traditional WhatsApp groups suffer from unread message floods and unverified claims. HackMate provides verified student profiles, real-time roster meters, and structured 1-click pitch reviews using React, Java 17 Javalin REST APIs, and MongoDB.\""),
        ("Member 2 (Frontend & Animations):", 
         "\"I developed the Frontend UI using React 18 and Tailwind CSS, creating modular components like TeamCard, FilterBar, and dynamic application modals. I also integrated GSAP for smooth entrance timelines and spring tab transitions between Sign In and Registration.\""),
        ("Member 3 (Database & Modeling):", 
         "\"I designed the MongoDB database layer across users, teams, and join_requests. MongoDB was chosen because hackathon squads have dynamic skill arrays and nested rosters, allowing atomic updates with $push without multi-table SQL JOIN overhead.\""),
        ("Member 4 (Authentication & Security):", 
         "\"I implemented the security pipeline. Student passwords are salted and hashed using BCrypt. User sessions use stateless JWT tokens signed with HMAC256, and a global Javalin AuthFilter protects private endpoints.\"" )
    ]

    for speaker, text in scripts:
        story.append(Paragraph(f"<b>{speaker}</b>", ParagraphStyle('Spk', fontName='Helvetica-Bold', fontSize=9, textColor=C_PRIMARY)))
        story.append(Paragraph(text, script_quote))
    
    story.append(Spacer(1, 10))

    # -------------------------------------------------------------
    # SECTION 4: EVALUATOR FAQ & TECHNICAL JUSTIFICATIONS
    # -------------------------------------------------------------
    story.append(Paragraph("4. Key Technical Justifications for Evaluators", h1_style))
    
    faq = [
        ("Q1: Why use MongoDB instead of a Relational Database like MySQL?",
         "Hackathon team postings are inherently polymorphic—each team requires arbitrary, dynamic arrays of technologies (e.g. ['React', 'FastAPI', 'PyTorch', 'Solidity']) and maintains an embedded list of accepted members with dynamic roles. In MongoDB, these are stored natively inside the squad document and queried directly. In MySQL, this would require 4 separate normalized tables (teams, skills, team_skills, team_members) joined on every card render, adding significant latency without relational benefits."),
        ("Q2: Why choose Javalin over Spring Boot?",
         "Spring Boot introduces heavy reflection, extensive annotation scanning, and high memory overhead (~400MB+ heap). Javalin provides an ultra-lightweight, expressive REST routing model built directly on embedded Jetty with sub-second startup times (<1s) and explicit, transparent request lifecycles without hidden magic."),
        ("Q3: How does the system handle concurrent applications?",
         "MongoDB executes atomic `$push` and `$set` operators on the team's `currentMembers` array. When a squad reaches its designated `teamSize`, the controller atomically flips the team status to `FULL`, preventing race conditions.")
    ]

    for q, a in faq:
        story.append(Paragraph(f"<b>{q}</b>", ParagraphStyle('FaqQ', fontName='Helvetica-Bold', fontSize=9, textColor=C_INK)))
        story.append(Paragraph(a, ParagraphStyle('FaqA', fontName='Helvetica', fontSize=8.5, leading=12, textColor=C_INK_MUTED, spaceAfter=6)))

    # Build Document
    doc.build(story, canvasmaker=NumberedCanvas)
    print(f"Successfully generated PDF at: {filename}")

if __name__ == "__main__":
    out_pdf = r"c:\Projects\campus-team-finder\HackMate_Tech_Stack_Specification.pdf"
    build_pdf(out_pdf)

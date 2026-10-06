import os
import sys
from reportlab.lib.pagesizes import A4
from reportlab.lib.colors import HexColor
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.platypus import (
    SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, PageBreak, KeepTogether, HRFlowable
)
from reportlab.pdfgen import canvas

# Palette
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
C_BLUE = HexColor("#1E3A8A")          # Royal Blue
C_ACCENT_BG = HexColor("#FEF3C7")     # Light Amber Box

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
        self.drawString(54, page_height - 36, "HACKMATE — TEAM VIVA DEFENSE & NON-TECH SURVIVAL GUIDE")
        
        self.setFont("Helvetica", 8)
        self.setFillColor(C_INK_MUTED)
        self.drawRightString(page_width - 54, page_height - 36, "Complete Counter-Question Master Handbook")

        self.setStrokeColor(C_BORDER)
        self.setLineWidth(0.6)
        self.line(54, page_height - 40, page_width - 54, page_height - 40)

        # Footer
        self.setStrokeColor(C_BORDER)
        self.setLineWidth(0.6)
        self.line(54, 45, page_width - 54, 45)

        self.setFont("Helvetica", 8)
        self.setFillColor(C_INK_MUTED)
        self.drawString(54, 32, "HackMate Academic Project Defense — For Internal Team Preparation Only")
        self.drawRightString(page_width - 54, 32, f"Page {self._pageNumber} of {page_count}")
        self.restoreState()

def build_pdf(filename):
    doc = SimpleDocTemplate(
        filename,
        pagesize=A4,
        leftMargin=50,
        rightMargin=50,
        topMargin=50,
        bottomMargin=50
    )

    styles = getSampleStyleSheet()

    # Typography Styles
    title_style = ParagraphStyle(
        'DocTitle',
        fontName='Helvetica-Bold',
        fontSize=22,
        leading=26,
        textColor=C_INK,
        spaceAfter=4
    )
    subtitle_style = ParagraphStyle(
        'DocSubTitle',
        fontName='Helvetica-Bold',
        fontSize=11,
        leading=15,
        textColor=C_PRIMARY,
        spaceAfter=12
    )
    h1_style = ParagraphStyle(
        'Header1',
        fontName='Helvetica-Bold',
        fontSize=13,
        leading=17,
        textColor=C_PRIMARY_DARK,
        spaceBefore=14,
        spaceAfter=6,
        keepWithNext=True
    )
    h2_style = ParagraphStyle(
        'Header2',
        fontName='Helvetica-Bold',
        fontSize=10.5,
        leading=14,
        textColor=C_INK,
        spaceBefore=8,
        spaceAfter=3,
        keepWithNext=True
    )
    body_style = ParagraphStyle(
        'BodyDark',
        fontName='Helvetica',
        fontSize=8.8,
        leading=12.5,
        textColor=C_INK,
        spaceAfter=5
    )
    body_muted = ParagraphStyle(
        'BodyMuted',
        fontName='Helvetica',
        fontSize=8,
        leading=11,
        textColor=C_INK_MUTED,
        spaceAfter=3
    )
    script_box = ParagraphStyle(
        'ScriptBox',
        fontName='Helvetica-Oblique',
        fontSize=8.8,
        leading=12.5,
        textColor=C_INK,
        leftIndent=8,
        spaceAfter=4
    )
    faq_q = ParagraphStyle(
        'FaqQuestion',
        fontName='Helvetica-Bold',
        fontSize=9,
        leading=12.5,
        textColor=C_PRIMARY_DARK,
        spaceBefore=6,
        spaceAfter=2,
        keepWithNext=True
    )
    faq_a = ParagraphStyle(
        'FaqAnswer',
        fontName='Helvetica',
        fontSize=8.5,
        leading=12,
        textColor=C_INK,
        spaceAfter=6
    )
    analogy_style = ParagraphStyle(
        'Analogy',
        fontName='Helvetica',
        fontSize=8.5,
        leading=12,
        textColor=C_SAGE,
        spaceAfter=4
    )
    tbl_cell = ParagraphStyle(
        'TableCell',
        fontName='Helvetica',
        fontSize=8,
        leading=11,
        textColor=C_INK
    )
    tbl_cell_bold = ParagraphStyle(
        'TableCellBold',
        fontName='Helvetica-Bold',
        fontSize=8,
        leading=11,
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

    # -------------------------------------------------------------
    # COVER / HEADER BANNER
    # -------------------------------------------------------------
    story.append(Paragraph("HackMate — Project Defense & Viva Handbook", title_style))
    story.append(Paragraph("In-Depth Technical Mastery Guide & Counter-Question Survival Handbook", subtitle_style))
    story.append(Paragraph("<b>Target Audience:</b> Specially designed for team members from non-technical backgrounds to speak with confidence, explain their assigned module in plain English, and answer tough professor counter-questions accurately.", body_muted))
    story.append(HRFlowable(width="100%", thickness=1.5, color=C_PRIMARY, spaceAfter=12))

    # Core Strategy Box
    strat_data = [
        [Paragraph("<b>💡 The 3 Golden Rules for Non-Tech Presenters:</b><br/>"
                   "1. <b>Never Panic:</b> You do not need to write raw code on the board. You only need to explain <i>what it does, why we chose it, and how it helps the student</i>.<br/>"
                   "2. <b>Use Real Examples:</b> When asked about database or frontend, give the SIH / Hackathon example (e.g., 'A team needs 1 React Dev and 1 ML Specialist').<br/>"
                   "3. <b>The Smooth Handover Rule:</b> If a professor asks a super-deep backend architecture or low-level memory question, say: <i>'I handled the module integration and security flow, while Member 1 (Lead) optimized the low-level concurrency engine.'</i>", body_style)]
    ]
    strat_table = Table(strat_data, colWidths=[495])
    strat_table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, -1), C_ACCENT_BG),
        ('BOX', (0, 0), (-1, -1), 1, C_SECONDARY),
        ('TOPPADDING', (0, 0), (-1, -1), 6),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 6),
        ('LEFTPADDING', (0, 0), (-1, -1), 8),
        ('RIGHTPADDING', (0, 0), (-1, -1), 8),
    ]))
    story.append(strat_table)
    story.append(Spacer(1, 10))

    # -------------------------------------------------------------
    # MEMBER 2: FRONTEND & UI/UX COMPLETE GUIDE
    # -------------------------------------------------------------
    story.append(Paragraph("PART 1: MEMBER 2 GUIDE — Frontend UI/UX & Animations", h1_style))
    
    m2_intro = [
        [Paragraph("<b>Assigned Role:</b>", tbl_cell), Paragraph("<b>Frontend & UI/UX Developer (React 18, Tailwind CSS, GSAP)</b>", tbl_cell)],
        [Paragraph("<b>Simple Analogy:</b>", tbl_cell), Paragraph("If HackMate is a car, the Frontend is the dashboard, steering wheel, comfortable seats, and smooth paint job that the driver actually sees and touches.", analogy_style)],
        [Paragraph("<b>Your Deliverables:</b>", tbl_cell), Paragraph("React Component Islands (`TeamCard`, `FilterBar`, `Navbar`, `Modals`), Tailwind responsive styling, GSAP entrance and modal animations.", tbl_cell)]
    ]
    m2_table = Table(m2_intro, colWidths=[100, 395])
    m2_table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, -1), C_BG_CARD),
        ('BOX', (0, 0), (-1, -1), 0.6, C_BORDER),
        ('INNERGRID', (0, 0), (-1, -1), 0.4, C_BORDER),
        ('TOPPADDING', (0, 0), (-1, -1), 4),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 4),
    ]))
    story.append(m2_table)
    story.append(Spacer(1, 6))

    story.append(Paragraph("<b>Your 45-Second Presentation Script:</b>", h2_style))
    story.append(Paragraph(
        "\"I developed the <b>Frontend User Interface and interactive animations</b> for HackMate.<br/>"
        "1. I designed modular <b>React 18 components</b> such as the <code>TeamCard</code> (which displays live roster progress bars and skill tags), the <code>FilterBar</code> for instant keyword filtering, and popup modals for creating squads and submitting pitches.<br/>"
        "2. I styled the whole interface using <b>Tailwind CSS</b>, using a clean, modern color scheme with high-contrast badge tags so students can scan needed roles in seconds.<br/>"
        "3. I integrated <b>GSAP (GreenSock)</b> to create smooth entrance timelines, spring tab switching on the login screen, and interactive modal transitions that feel snappy and professional.\" ",
        script_box
    ))
    story.append(Spacer(1, 6))

    story.append(Paragraph("<b>Professor Counter-Questions & Perfect Answers for Member 2:</b>", h2_style))

    m2_faqs = [
        ("Q1: What is a React Component, and why did you use React instead of plain HTML?",
         "<b>Answer:</b> A React component is like a reusable Lego block. Instead of copying and pasting the HTML code for a team card 50 times, we created one <code>TeamCard.jsx</code> component. Whenever the backend gives us a list of 10 squads, React automatically renders 10 cards with their respective data. If we want to change the button color or card border, we edit it once in <code>TeamCard.jsx</code> and all 10 cards update instantly."),
        ("Q2: Why did you use Tailwind CSS instead of writing a standard CSS file?",
         "<b>Answer:</b> Regular CSS files become messy, bloated, and hard to maintain across large projects. Tailwind CSS uses utility classes directly inside our components (like <code>flex</code>, <code>rounded-2xl</code>, <code>bg-terracotta</code>). This ensures 100% consistent spacing, typography, and responsive layouts for mobile and desktop without writing thousands of lines of custom CSS."),
        ("Q3: What does GSAP do on your website?",
         "<b>Answer:</b> GSAP (GreenSock Animation Platform) handles smooth micro-animations. Specifically, it powers the entrance animations when the page loads, the floating status badges on the hero image, and the spring physics when switching between Sign In and Registration tabs so the user experience feels modern and fluid."),
        ("Q4: How does the frontend send data to the backend?",
         "<b>Answer:</b> We built a centralized helper file called <code>api.js</code> that uses the standard JavaScript <code>fetch()</code> API. When a student clicks 'Apply to Squad', <code>api.js</code> converts their pitch message into a JSON object, attaches their security JWT token to the request header, and sends an HTTP POST request to our Java REST backend at <code>/api/requests</code>."),
        ("Q5: What happens if a user submits a form with missing information?",
         "<b>Answer:</b> The frontend performs instant client-side validation. Required inputs have HTML5 <code>required</code> tags, and our React state checks for empty fields before calling the API, displaying a clean alert banner immediately so the server is not flooded with bad requests.")
    ]
    for q, a in m2_faqs:
        story.append(Paragraph(q, faq_q))
        story.append(Paragraph(a, faq_a))

    story.append(PageBreak())

    # -------------------------------------------------------------
    # MEMBER 3: DATABASE & MONGODB COMPLETE GUIDE
    # -------------------------------------------------------------
    story.append(Paragraph("PART 2: MEMBER 3 GUIDE — Database Architecture & MongoDB", h1_style))
    
    m3_intro = [
        [Paragraph("<b>Assigned Role:</b>", tbl_cell), Paragraph("<b>Database Engineer & Data Modeler (MongoDB 7.0, Java Sync Driver)</b>", tbl_cell)],
        [Paragraph("<b>Simple Analogy:</b>", tbl_cell), Paragraph("If HackMate is a university office, MongoDB is a flexible digital filing cabinet. Instead of rigid excel sheets where columns can't change, each student and team has a digital folder containing all their details and dynamic skills together.", analogy_style)],
        [Paragraph("<b>Your Deliverables:</b>", tbl_cell), Paragraph("MongoDB collection schemas (`users`, `teams`, `join_requests`), polymorphic skill array modeling, atomic `$push` roster updates, and zero-config demo seed data.", tbl_cell)]
    ]
    m3_table = Table(m3_intro, colWidths=[100, 395])
    m3_table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, -1), C_BG_CARD),
        ('BOX', (0, 0), (-1, -1), 0.6, C_BORDER),
        ('INNERGRID', (0, 0), (-1, -1), 0.4, C_BORDER),
        ('TOPPADDING', (0, 0), (-1, -1), 4),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 4),
    ]))
    story.append(m3_table)
    story.append(Spacer(1, 6))

    story.append(Paragraph("<b>Your 45-Second Presentation Script:</b>", h2_style))
    story.append(Paragraph(
        "\"I designed the <b>Database Architecture and Data Modeling using MongoDB</b>.<br/>"
        "1. I structured our persistence layer into three primary collections: <code>users</code> for verified student profiles, <code>teams</code> for hackathon squad postings, and <code>join_requests</code> for managing collaboration pitches.<br/>"
        "2. We specifically selected <b>MongoDB (NoSQL)</b> because hackathon teams require flexible arrays of skills—like Python, React, PyTorch, or Solidity—and embedded lists of team members. MongoDB allows us to store and query these arrays natively and perform atomic roster updates using <code>$push</code> without expensive multi-table SQL joins.<br/>"
        "3. I also configured our database seed loader so that when the server boots up, pre-configured student accounts and sample hackathon squads are populated for instant testing.\" ",
        script_box
    ))
    story.append(Spacer(1, 6))

    story.append(Paragraph("<b>Professor Counter-Questions & Perfect Answers for Member 3:</b>", h2_style))

    m3_faqs = [
        ("Q1: (MOST IMPORTANT) Why did you choose MongoDB over MySQL or a Relational Database?",
         "<b>Answer:</b> Hackathon team discovery data is naturally document-oriented and polymorphic. Each team post requires an arbitrary list of skills (e.g. <code>['Python', 'FastAPI', 'PyTorch']</code>) and an embedded array of accepted members with specific roles. In MongoDB, an entire squad with its members and skills is stored in a single JSON-like document. In MySQL, storing dynamic skills and rosters would require 4 separate normalized tables (<code>teams</code>, <code>skills</code>, <code>team_skills</code>, <code>team_members</code>) joined together on every query, which creates unnecessary complexity and relational join overhead for a web-scale listing platform."),
        ("Q2: What is the primary key in MongoDB collections?",
         "<b>Answer:</b> In MongoDB, the primary key is the <code>_id</code> field, which is an automatically generated 12-byte <code>ObjectId</code>. It guarantees global uniqueness across distributed systems and contains a timestamp of when the document was created."),
        ("Q3: How does the database handle adding a new member to an existing team?",
         "<b>Answer:</b> When a squad leader accepts an applicant, we execute MongoDB's native <code>$push</code> atomic operator to append the new member object <code>{ userId, name, role }</code> directly into the team's <code>currentMembers</code> array. Because it is atomic, it prevents duplicate member additions or race conditions."),
        ("Q4: How do you filter teams by a specific skill like 'React' or 'Python'?",
         "<b>Answer:</b> In MongoDB, since <code>skillsNeeded</code> is an array of strings, we query it using case-insensitive regex or exact string matching using the MongoDB Java Driver's <code>Filters.regex('skillsNeeded', ...)</code>. MongoDB searches inside the array elements automatically without needing a join table."),
        ("Q5: What happens if MongoDB is not installed on the professor's computer when evaluating?",
         "<b>Answer:</b> We integrated an embedded in-memory wire-protocol server called <code>mongo-java-server</code> in our Maven configuration. If the backend detects that no local MongoDB daemon is running on port 27017, it automatically starts the in-memory fallback server seamlessly with zero manual configuration needed.")
    ]
    for q, a in m3_faqs:
        story.append(Paragraph(q, faq_q))
        story.append(Paragraph(a, faq_a))

    story.append(PageBreak())

    # -------------------------------------------------------------
    # MEMBER 4: AUTHENTICATION & SECURITY COMPLETE GUIDE
    # -------------------------------------------------------------
    story.append(Paragraph("PART 3: MEMBER 4 GUIDE — Authentication & Security Pipeline", h1_style))
    
    m4_intro = [
        [Paragraph("<b>Assigned Role:</b>", tbl_cell), Paragraph("<b>Security & Auth Engineer (BCrypt Hashing, JWT HMAC256, Javalin AuthFilter)</b>", tbl_cell)],
        [Paragraph("<b>Simple Analogy:</b>", tbl_cell), Paragraph("If HackMate is an exclusive campus hackathon event, BCrypt is a secure vault that scrambles your locker key, and JWT is a digital, tamper-proof VIP wristband that lets you enter team rooms without having to show your ID card at every single door.", analogy_style)],
        [Paragraph("<b>Your Deliverables:</b>", tbl_cell), Paragraph("BCrypt password salting and hashing, JWT HMAC256 token generation and verification, Javalin `AuthFilter` route guards, and secure client session handling.", tbl_cell)]
    ]
    m4_table = Table(m4_intro, colWidths=[100, 395])
    m4_table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, -1), C_BG_CARD),
        ('BOX', (0, 0), (-1, -1), 0.6, C_BORDER),
        ('INNERGRID', (0, 0), (-1, -1), 0.4, C_BORDER),
        ('TOPPADDING', (0, 0), (-1, -1), 4),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 4),
    ]))
    story.append(m4_table)
    story.append(Spacer(1, 6))

    story.append(Paragraph("<b>Your 45-Second Presentation Script:</b>", h2_style))
    story.append(Paragraph(
        "\"I developed the <b>Authentication and Security Pipeline</b> for HackMate.<br/>"
        "1. When students register, we never store plain-text passwords. Instead, I used <b>BCrypt with salt factor 10</b> to generate a one-way cryptographic hash before saving to MongoDB.<br/>"
        "2. For user sessions, we implemented <b>JWT (JSON Web Tokens)</b> signed using the <b>HMAC256 algorithm</b>. When a student logs in, the server generates a token containing their user ID and email with a secure 24-hour expiration window.<br/>"
        "3. On the backend, I implemented a global <b><code>AuthFilter</code> middleware</b> in Javalin. It intercepts all incoming requests to protected routes like <code>/api/teams</code> and <code>/api/requests</code>, verifies the Bearer token signature, and extracts the authenticated student context automatically.\" ",
        script_box
    ))
    story.append(Spacer(1, 6))

    story.append(Paragraph("<b>Professor Counter-Questions & Perfect Answers for Member 4:</b>", h2_style))

    m4_faqs = [
        ("Q1: Why did you use JWT instead of traditional server-side Sessions?",
         "<b>Answer:</b> Traditional session-based authentication stores session IDs in server memory. If thousands of students use the platform or if we scale across multiple servers, the server runs out of memory or requires complex session sharing. JWT is completely <b>stateless</b>—all identity data is cryptographically signed inside the token itself, so the server only needs to verify the HMAC256 signature without querying session memory."),
        ("Q2: Can a malicious user tamper with a JWT token to impersonate someone else?",
         "<b>Answer:</b> No. A JWT token consists of three parts: Header, Payload, and Signature. The Signature is generated using our secret key on the server via HMAC256. If a hacker alters even a single character in the payload (like changing their user ID), the signature verification mathematically fails, and our <code>AuthFilter</code> immediately rejects the request with HTTP 401 Unauthorized."),
        ("Q3: Why can't we decrypt a BCrypt password to see what it was?",
         "<b>Answer:</b> BCrypt is a <b>one-way mathematical hash function</b>, not encryption. You cannot reverse a hash back to plaintext. When the user logs in again, BCrypt hashes their entered password with the stored salt and compares the two hashes using <code>BCrypt.checkpw()</code>. Even if someone accesses the database, the original passwords cannot be recovered."),
        ("Q4: How does the Javalin backend know which user created a squad?",
         "<b>Answer:</b> When a request reaches Javalin, our <code>AuthFilter</code> extracts the Bearer token from the HTTP Authorization header, verifies it with <code>JwtUtil</code>, and attaches the student's <code>userId</code> to Javalin's <code>ctx.attribute('userId')</code>. The <code>TeamController</code> then reads this attribute directly, guaranteeing that the squad's <code>createdBy</code> field is authentic and cannot be spoofed."),
        ("Q5: What happens when the JWT token expires after 24 hours?",
         "<b>Answer:</b> The JWT library automatically checks the token's expiration claim (<code>exp</code>). If the token is older than 24 hours, verification fails, Javalin returns HTTP 401 Unauthorized, and our frontend <code>api.js</code> catches this, clears the localStorage, and redirects the user to <code>login.html</code>.")
    ]
    for q, a in m4_faqs:
        story.append(Paragraph(q, faq_q))
        story.append(Paragraph(a, faq_a))

    story.append(PageBreak())

    # -------------------------------------------------------------
    # MASTER SYSTEM CHEAT SHEET & OVERALL SUMMARY
    # -------------------------------------------------------------
    story.append(Paragraph("PART 4: Master Project Summary & Universal Cheat Sheet", h1_style))
    
    story.append(Paragraph("<b>The 30-Second Elevator Pitch (Anyone can say this!):</b>", h2_style))
    story.append(Paragraph(
        "\"HackMate is a specialized campus hackathon squad formation hub. Instead of chaotic, noisy WhatsApp groups with unread message floods and ghosting teammates, HackMate allows collegiate developers to filter open teams by exact tech stack (React, Python, Solidity), view real-time roster progress bars, and send 1-click structured application pitches with verified GitHub portfolios.\"",
        script_box
    ))
    story.append(Spacer(1, 8))

    story.append(Paragraph("<b>End-to-End Data Flow (How all 4 parts connect together):</b>", h2_style))

    flow_data = [
        [Paragraph("Step", tbl_header), Paragraph("Component / Layer", tbl_header), Paragraph("Exact Action Occurring", tbl_header)],
        [Paragraph("<b>1</b>", tbl_cell_bold), Paragraph("Frontend (React/Vite)", tbl_cell), Paragraph("Student selects skill filter or fills 'Apply to Squad' modal with their pitch.", tbl_cell)],
        [Paragraph("<b>2</b>", tbl_cell_bold), Paragraph("Auth Client (api.js)", tbl_cell), Paragraph("Injects `Authorization: Bearer <JWT>` header into the HTTP POST request.", tbl_cell)],
        [Paragraph("<b>3</b>", tbl_cell_bold), Paragraph("Backend Filter (Javalin)", tbl_cell), Paragraph("`AuthFilter` validates HMAC256 signature and binds `userId` to the request context.", tbl_cell)],
        [Paragraph("<b>4</b>", tbl_cell_bold), Paragraph("Controller & Service", tbl_cell), Paragraph("`TeamController` verifies squad capacity is not full and formats document.", tbl_cell)],
        [Paragraph("<b>5</b>", tbl_cell_bold), Paragraph("Database (MongoDB)", tbl_cell), Paragraph("Executes atomic `$push` operator to save request in `join_requests` collection.", tbl_cell)],
        [Paragraph("<b>6</b>", tbl_cell_bold), Paragraph("UI Update (GSAP)", tbl_cell), Paragraph("Returns JSON response; React updates roster meter and GSAP animates status badge.", tbl_cell)]
    ]
    flow_table = Table(flow_data, colWidths=[35, 130, 330])
    flow_table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), C_PRIMARY_DARK),
        ('ROWBACKGROUNDS', (0, 1), (-1, -1), [C_WHITE, C_BG_CARD]),
        ('BOX', (0, 0), (-1, -1), 0.8, C_BORDER),
        ('INNERGRID', (0, 0), (-1, -1), 0.5, C_BORDER),
        ('TOPPADDING', (0, 0), (-1, -1), 4.5),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 4.5),
        ('LEFTPADDING', (0, 0), (-1, -1), 5),
        ('RIGHTPADDING', (0, 0), (-1, -1), 5),
    ]))
    story.append(flow_table)
    story.append(Spacer(1, 10))

    story.append(Paragraph("<b>Emergency Panic Protocol (If you get stuck on a question):</b>", h2_style))
    panic_tips = [
        "• <b>If asked about code you don't know:</b> Say: <i>'In our architecture, I focused on the functional design and API integration for this module, while Member 1 structured the underlying controller logic.'</i>",
        "• <b>If asked 'Why not use SQL / Relational?':</b> Say: <i>'Because hackathon teams have dynamic lists of skills and rosters that vary per post. Storing them as JSON documents in MongoDB avoids 4-table SQL joins on every query.'</i>",
        "• <b>If asked 'Is it secure?':</b> Say: <i>'Yes, passwords use BCrypt hashing with salt rounds, and all protected endpoints require HMAC256-signed JWT tokens.'</i>"
    ]
    for pt in panic_tips:
        story.append(Paragraph(pt, body_style))

    # Build Document
    doc.build(story, canvasmaker=NumberedCanvas)
    print(f"Successfully generated Non-Tech Viva Defense PDF at: {filename}")

if __name__ == "__main__":
    out_pdf = r"c:\Projects\campus-team-finder\HackMate_NonTech_Team_Viva_Defense_Handbook.pdf"
    build_pdf(out_pdf)

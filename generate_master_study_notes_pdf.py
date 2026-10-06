import os
import sys
from reportlab.lib.pagesizes import A4
from reportlab.lib.colors import HexColor
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.platypus import (
    SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, PageBreak, KeepTogether, HRFlowable
)
from reportlab.pdfgen import canvas
import pypdf

# Professional Engineering Palette
C_PRIMARY = HexColor("#0F172A")       # Deep Slate Navy
C_ACCENT = HexColor("#2563EB")        # Vibrant Royal Blue
C_ACCENT_DARK = HexColor("#1D4ED8")   # Deep Blue
C_SECONDARY = HexColor("#0D9488")     # Emerald Teal
C_TEXT = HexColor("#1E293B")          # Charcoal Body Text
C_MUTED = HexColor("#64748B")         # Slate Muted Text
C_BG_CARD = HexColor("#F8FAFC")       # Off-white Card Background
C_BG_ALT = HexColor("#F1F5F9")        # Light Slate Box
C_BG_CODE = HexColor("#0F172A")       # Dark Code Box
C_CODE_TEXT = HexColor("#E2E8F0")     # Light Monospace Text
C_CODE_KEYWORD = HexColor("#93C5FD")  # Light Blue Code Accent
C_BORDER = HexColor("#CBD5E1")        # Subtle Border
C_BORDER_LIGHT = HexColor("#E2E8F0")  # Very Light Border
C_WHITE = HexColor("#FFFFFF")
C_GREEN = HexColor("#15803D")         # Forest Green
C_AMBER = HexColor("#B45309")         # Warm Amber
C_AMBER_BG = HexColor("#FEF3C7")      # Light Amber Card
C_RED = HexColor("#B91C1C")           # Crimson Red

PAGE_WIDTH, PAGE_HEIGHT = A4

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
        self.saveState()
        
        # Header (pages 2+)
        if self._pageNumber > 1:
            self.setFont("Helvetica-Bold", 8)
            self.setFillColor(C_ACCENT)
            self.drawString(40, PAGE_HEIGHT - 28, "HACKMATE")
            self.setFont("Helvetica-Bold", 8)
            self.setFillColor(C_PRIMARY)
            self.drawString(95, PAGE_HEIGHT - 28, "— MASTER STUDY NOTES & CODEBREAKDOWN HANDBOOK")
            
            self.setFont("Helvetica", 8)
            self.setFillColor(C_MUTED)
            self.drawRightString(PAGE_WIDTH - 40, PAGE_HEIGHT - 28, "Exam & Viva Defense Guide")

            self.setStrokeColor(C_BORDER)
            self.setLineWidth(0.6)
            self.line(40, PAGE_HEIGHT - 32, PAGE_WIDTH - 40, PAGE_HEIGHT - 32)

        # Footer (all pages)
        self.setStrokeColor(C_BORDER)
        self.setLineWidth(0.6)
        self.line(40, 36, PAGE_WIDTH - 40, 36)

        self.setFont("Helvetica", 8)
        self.setFillColor(C_MUTED)
        self.drawString(40, 24, "HackMate • Campus Hackathon Discovery Platform • DMCE Mumbai University")
        self.drawRightString(PAGE_WIDTH - 40, 24, f"Page {self._pageNumber} of {page_count}")
        
        self.restoreState()


def build_pdf():
    output_filename = "HackMate_Master_Study_Notes_and_Code_Breakdown.pdf"
    doc = SimpleDocTemplate(
        output_filename,
        pagesize=A4,
        leftMargin=40,
        rightMargin=40,
        topMargin=42,
        bottomMargin=46
    )

    styles = getSampleStyleSheet()

    # Custom Typography Styles
    title_style = ParagraphStyle(
        'DocTitle',
        fontName='Helvetica-Bold',
        fontSize=20,
        leading=24,
        textColor=C_PRIMARY,
        spaceAfter=3
    )
    subtitle_style = ParagraphStyle(
        'DocSubTitle',
        fontName='Helvetica-Bold',
        fontSize=10,
        leading=13,
        textColor=C_ACCENT,
        spaceAfter=8
    )
    h1_style = ParagraphStyle(
        'ChapterH1',
        fontName='Helvetica-Bold',
        fontSize=13,
        leading=16,
        textColor=C_PRIMARY,
        spaceBefore=8,
        spaceAfter=5,
        keepWithNext=True
    )
    h2_style = ParagraphStyle(
        'SectionH2',
        fontName='Helvetica-Bold',
        fontSize=10,
        leading=13,
        textColor=C_ACCENT_DARK,
        spaceBefore=6,
        spaceAfter=3,
        keepWithNext=True
    )
    body_style = ParagraphStyle(
        'BodyTextCustom',
        fontName='Helvetica',
        fontSize=8.5,
        leading=11.5,
        textColor=C_TEXT,
        spaceAfter=4
    )
    body_bold = ParagraphStyle(
        'BodyBoldCustom',
        fontName='Helvetica-Bold',
        fontSize=8.5,
        leading=11.5,
        textColor=C_PRIMARY,
        spaceAfter=4
    )
    bullet_style = ParagraphStyle(
        'BulletCustom',
        fontName='Helvetica',
        fontSize=8.5,
        leading=11.5,
        textColor=C_TEXT,
        leftIndent=12,
        spaceAfter=2
    )
    callout_text = ParagraphStyle(
        'CalloutText',
        fontName='Helvetica',
        fontSize=8,
        leading=11,
        textColor=C_TEXT
    )
    callout_bold = ParagraphStyle(
        'CalloutBold',
        fontName='Helvetica-Bold',
        fontSize=8,
        leading=11,
        textColor=C_PRIMARY
    )
    code_inline = ParagraphStyle(
        'CodeInline',
        fontName='Courier',
        fontSize=7.5,
        leading=10,
        textColor=C_CODE_KEYWORD
    )
    code_block = ParagraphStyle(
        'CodeBlock',
        fontName='Courier',
        fontSize=7,
        leading=9.5,
        textColor=C_CODE_TEXT
    )
    table_cell = ParagraphStyle(
        'TableCell',
        fontName='Helvetica',
        fontSize=8,
        leading=10.5,
        textColor=C_TEXT
    )
    table_cell_bold = ParagraphStyle(
        'TableCellBold',
        fontName='Helvetica-Bold',
        fontSize=8,
        leading=10.5,
        textColor=C_PRIMARY
    )
    table_header = ParagraphStyle(
        'TableHeader',
        fontName='Helvetica-Bold',
        fontSize=8,
        leading=10.5,
        textColor=C_WHITE
    )
    qa_q = ParagraphStyle(
        'QAQuestion',
        fontName='Helvetica-Bold',
        fontSize=8.5,
        leading=11.5,
        textColor=C_ACCENT_DARK,
        spaceBefore=4,
        spaceAfter=2,
        keepWithNext=True
    )
    qa_a = ParagraphStyle(
        'QAAnswer',
        fontName='Helvetica',
        fontSize=8,
        leading=11,
        textColor=C_TEXT,
        spaceAfter=4
    )

    story = []
    avail_w = PAGE_WIDTH - 80 # 515 pt

    def make_card(content_list, bg_color=C_BG_CARD, border_color=C_BORDER, padding=6):
        t = Table([[content_list]], colWidths=[avail_w])
        t.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, -1), bg_color),
            ('BOX', (0, 0), (-1, -1), 0.8, border_color),
            ('TOPPADDING', (0, 0), (-1, -1), padding),
            ('BOTTOMPADDING', (0, 0), (-1, -1), padding),
            ('LEFTPADDING', (0, 0), (-1, -1), padding + 2),
            ('RIGHTPADDING', (0, 0), (-1, -1), padding + 2),
        ]))
        return t

    def make_code_box(code_lines, title="CODE SNIPPET"):
        content = [
            Paragraph(f"<b>{title}</b>", ParagraphStyle('CodeTitle', fontName='Helvetica-Bold', fontSize=7.5, leading=10, textColor=HexColor("#38BDF8"))),
            Spacer(1, 2)
        ]
        formatted_code = "<br/>".join([line.replace(" ", "&nbsp;").replace("<", "&lt;").replace(">", "&gt;") for line in code_lines])
        content.append(Paragraph(formatted_code, code_block))
        
        t = Table([[content]], colWidths=[avail_w])
        t.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, -1), C_BG_CODE),
            ('BOX', (0, 0), (-1, -1), 0.8, HexColor("#334155")),
            ('TOPPADDING', (0, 0), (-1, -1), 5),
            ('BOTTOMPADDING', (0, 0), (-1, -1), 5),
            ('LEFTPADDING', (0, 0), (-1, -1), 8),
            ('RIGHTPADDING', (0, 0), (-1, -1), 8),
        ]))
        return t

    # =========================================================================
    # PAGE 1: TITLE, EXECUTIVE OVERVIEW & ARCHITECTURE BLUEPRINT
    # =========================================================================
    story.append(Paragraph("HACKMATE — MASTER STUDY NOTES & CODEBREAKDOWN", title_style))
    story.append(Paragraph("A Complete Zero-to-Hero Technical Guide, Line-by-Line Code Breakdown & Viva Defense Manual", subtitle_style))
    
    meta_table = Table([
        [
            Paragraph("<b>Institution:</b> Datta Meghe College of Engineering, Airoli", table_cell),
            Paragraph("<b>Academic Term:</b> Mini Project 2026", table_cell),
            Paragraph("<b>Target Presentation:</b> 9:00 AM Viva Defense", table_cell)
        ],
        [
            Paragraph("<b>Team Lead & Backend:</b> Harshit Mishra (Roll 32)", table_cell_bold),
            Paragraph("<b>Auth & Database:</b> Aayush Mali (Roll 26)", table_cell),
            Paragraph("<b>Frontend & UI:</b> Aditi Mhatre (Roll 31)", table_cell)
        ],
        [
            Paragraph("<b>Testing & Docs:</b> Shravan More (Roll 36)", table_cell),
            Paragraph("<b>Project Mentor:</b> Prof. Prajakta Koli", table_cell_bold),
            Paragraph("<b>Repository:</b> github.com/iharshitmishra/campus-team-finder", table_cell)
        ]
    ], colWidths=[175, 170, 170])
    meta_table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, -1), C_BG_ALT),
        ('BOX', (0, 0), (-1, -1), 0.8, C_BORDER),
        ('INNERGRID', (0, 0), (-1, -1), 0.5, C_BORDER_LIGHT),
        ('TOPPADDING', (0, 0), (-1, -1), 4),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 4),
        ('LEFTPADDING', (0, 0), (-1, -1), 6),
        ('RIGHTPADDING', (0, 0), (-1, -1), 6),
    ]))
    story.append(meta_table)
    story.append(Spacer(1, 6))

    story.append(Paragraph("1. Executive Summary & Purpose of This Guide", h1_style))
    story.append(Paragraph(
        "<b>HackMate</b> is a specialized web platform engineered to eliminate team formation friction in collegiate hackathons (e.g., Smart India Hackathon, ETHIndia). Conventional campus team formation relies on unorganized WhatsApp groups and Discord threads, resulting in mismatched skill sets, ghosted invitations, and incomplete registrations. HackMate resolves this through structured team creation, dynamic skill-tagged search queries, custom pitch-based join requests, and an atomic roster management engine.",
        body_style
    ))
    story.append(Paragraph(
        "<b>Why this handbook is vital tonight:</b> If you are presenting tomorrow at 9:00 AM, and especially if this is your first time working with Java on the backend, this document breaks down every single technology, file, algorithm, and line of code into plain, defensible concepts. It arms you with technical clarity so you can explain <i>what</i> was written, <i>why</i> it was chosen, and <i>how</i> it executes under the hood.",
        body_style
    ))

    story.append(Paragraph("2. System Architecture Blueprint", h1_style))
    arch_data = [
        [Paragraph("Layer", table_header), Paragraph("Technologies Used", table_header), Paragraph("Core Responsibility in HackMate", table_header)],
        [
            Paragraph("<b>Presentation Layer</b><br/>(Client Browser)", table_cell),
            Paragraph("HTML5, Tailwind CSS, JavaScript (ES6+), React 18 Islands, GSAP, Lucide Icons", table_cell),
            Paragraph("Renders responsive UI, handles client routing, manages reactive filter states, captures user inputs, and executes asynchronous REST calls with Bearer tokens.", table_cell)
        ],
        [
            Paragraph("<b>API & Routing</b><br/>(Web Engine)", table_cell),
            Paragraph("Javalin 5.6.3 REST Microframework, Embedded Jetty 11 HTTP Server", table_cell),
            Paragraph("Listens on Port 7070, executes global CORS policy, binds REST endpoints, validates HTTP headers, and routes requests to appropriate controllers.", table_cell)
        ],
        [
            Paragraph("<b>Security & Filter</b><br/>(Middleware)", table_cell),
            Paragraph("AuthFilter, Auth0 Java-JWT (HMAC256), BCrypt Password Hashing (10 Rounds)", table_cell),
            Paragraph("Intercepts protected routes (`/api/requests/*`, `/api/users/me`, team mutations), validates JWT tokens, extracts authenticated userId, and blocks unauthorized traffic.", table_cell)
        ],
        [
            Paragraph("<b>Business Logic</b><br/>(Controllers)", table_cell),
            Paragraph("AuthController, TeamController, RequestController, UserController", table_cell),
            Paragraph("Implements domain logic: duplicate email checks, regex skill queries, team creation, join pitch submission, applicant approval, and atomic roster locking.", table_cell)
        ],
        [
            Paragraph("<b>Persistence Layer</b><br/>(Database)", table_cell),
            Paragraph("MongoDB Sync Driver 4.11.1, Mongo-Java-Server 1.45.0, Localhost:27017", table_cell),
            Paragraph("Provides schemaless BSON document persistence across `users`, `teams`, and `join_requests` collections with disk snapshot JSON backup and automatic zero-config fallback.", table_cell)
        ]
    ]
    arch_t = Table(arch_data, colWidths=[95, 140, 280])
    arch_t.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), C_PRIMARY),
        ('BOX', (0, 0), (-1, -1), 0.8, C_BORDER),
        ('INNERGRID', (0, 0), (-1, -1), 0.5, C_BORDER_LIGHT),
        ('TOPPADDING', (0, 0), (-1, -1), 4),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 4),
        ('LEFTPADDING', (0, 0), (-1, -1), 5),
        ('RIGHTPADDING', (0, 0), (-1, -1), 5),
    ]))
    story.append(arch_t)
    story.append(PageBreak())

    # =========================================================================
    # PAGE 2: PROBLEM STATEMENT, SOLUTION & PORT ASSIGNMENTS
    # =========================================================================
    story.append(Paragraph("3. Detailed Problem Statement & Engineered Solution", h1_style))
    story.append(Paragraph(
        "To defend this project effectively, you must articulate the precise engineering challenges that HackMate addresses. Professors often ask: <i>'Why did you build this? What is technically unique about it compared to a generic message board?'</i>",
        body_style
    ))
    
    prob_sol_data = [
        [Paragraph("The Real-World Campus Problem", table_header), Paragraph("The HackMate Technical Solution", table_header)],
        [
            Paragraph("<b>1. Information Asymmetry:</b> Students cannot find teammates with matching tech stacks (e.g., finding a PyTorch developer for SIH when everyone in their friend group knows only HTML/CSS).", table_cell),
            Paragraph("<b>Skill-Indexed Filtering:</b> Teams declare exact required skills (`skillsNeeded: ['React', 'FastAPI']`). The backend uses case-insensitive BSON regular expressions to return matching squads instantly.", table_cell)
        ],
        [
            Paragraph("<b>2. Unqualified Spam Applications:</b> Squad leaders get overwhelmed with generic 'add me' messages without knowing the applicant's experience, branch, or capabilities.", table_cell),
            Paragraph("<b>Structured Pitch Pipeline:</b> Applicants must submit a targeted pitch message. The system embeds the applicant's branch, academic year, and verified skill tags directly into the join request.", table_cell)
        ],
        [
            Paragraph("<b>3. Accidental Over-Enrollment & Ghosting:</b> Leaders verbally accept too many members or lose track of confirmations, causing hackathon submission disqualifications.", table_cell),
            Paragraph("<b>Atomic Roster State Machine:</b> When a leader clicks 'Accept', the system appends the user to `currentMembers`. If member count reaches `teamSize`, team status atomically shifts to `FULL`, locking further applications.", table_cell)
        ],
        [
            Paragraph("<b>4. Setup Complexity on Evaluator Machines:</b> Running external databases like MongoDB requires local daemons, environment configs, and port setups that often fail during vivas.", table_cell),
            Paragraph("<b>Dual-Mode Persistence Waterfall:</b> DbConfig attempts connection to external MongoDB or local 27017 daemon, and automatically boots an embedded wire-protocol in-memory server if unavailable.", table_cell)
        ]
    ]
    prob_sol_t = Table(prob_sol_data, colWidths=[250, 265])
    prob_sol_t.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), C_PRIMARY),
        ('BOX', (0, 0), (-1, -1), 0.8, C_BORDER),
        ('INNERGRID', (0, 0), (-1, -1), 0.5, C_BORDER_LIGHT),
        ('TOPPADDING', (0, 0), (-1, -1), 4),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 4),
        ('LEFTPADDING', (0, 0), (-1, -1), 6),
        ('RIGHTPADDING', (0, 0), (-1, -1), 6),
    ]))
    story.append(prob_sol_t)
    story.append(Spacer(1, 6))

    story.append(Paragraph("4. Port Allocations, Network Boundaries & Communication Protocols", h1_style))
    story.append(Paragraph(
        "Understanding how the different processes communicate on your local machine is essential. When running HackMate, three distinct port boundaries operate simultaneously:",
        body_style
    ))

    port_data = [
        [Paragraph("Port", table_header), Paragraph("Service / Process", table_header), Paragraph("Protocol", table_header), Paragraph("Description & Role in HackMate", table_header)],
        [
            Paragraph("<b>7070</b>", table_cell_bold),
            Paragraph("Javalin REST Server<br/>(Embedded Jetty)", table_cell),
            Paragraph("HTTP / JSON", table_cell),
            Paragraph("Backend entry point. Listens for REST API requests (`/api/*`), parses JSON request bodies, checks JWT authentication headers, executes business logic, and returns HTTP responses.", table_cell)
        ],
        [
            Paragraph("<b>5173</b>", table_cell_bold),
            Paragraph("Vite Dev Server / Frontend", table_cell),
            Paragraph("HTTP / WebSockets", table_cell),
            Paragraph("Frontend development server. Serves HTML5 pages, transpiles JSX (React 18), compiles Tailwind CSS, and provides Hot Module Replacement (HMR) during development.", table_cell)
        ],
        [
            Paragraph("<b>27017</b>", table_cell_bold),
            Paragraph("MongoDB Server / In-Memory Daemon", table_cell),
            Paragraph("MongoDB Wire Protocol", table_cell),
            Paragraph("Database layer. Communicates with Java backend via binary BSON protocol. If local MongoDB service is absent, `MongoServer` binds this port in memory.", table_cell)
        ]
    ]
    port_t = Table(port_data, colWidths=[45, 110, 85, 275])
    port_t.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), C_PRIMARY),
        ('BOX', (0, 0), (-1, -1), 0.8, C_BORDER),
        ('INNERGRID', (0, 0), (-1, -1), 0.5, C_BORDER_LIGHT),
        ('TOPPADDING', (0, 0), (-1, -1), 4),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 4),
        ('LEFTPADDING', (0, 0), (-1, -1), 5),
        ('RIGHTPADDING', (0, 0), (-1, -1), 5),
    ]))
    story.append(port_t)
    story.append(Spacer(1, 6))

    story.append(make_card([
        Paragraph("<b>Key Concept to Remember:</b>", callout_bold),
        Paragraph("The frontend at <code>http://localhost:5173</code> and the backend at <code>http://localhost:7070</code> are distinct origins. When the browser makes a <code>fetch()</code> call from port 5173 to port 7070, the browser executes a Cross-Origin Request (CORS). The backend explicitly allows this via Javalin's <code>CorsPluginConfig::anyHost</code>.", callout_text)
    ], bg_color=C_AMBER_BG, border_color=C_AMBER))

    story.append(PageBreak())

    # =========================================================================
    # PAGE 3: JAVA & JAVALIN ECOSYSTEM FOR BEGINNERS
    # =========================================================================
    story.append(Paragraph("5. Java & Javalin Ecosystem — Concepts Explained from Scratch", h1_style))
    story.append(Paragraph(
        "If Java backend development is new to you, the terminology might feel unfamiliar. Here is a clear, plain-English breakdown of every core building block in the Java backend ecosystem.",
        body_style
    ))

    story.append(Paragraph("A. What is Javalin and Why is it Better Than Spring Boot for This Project?", h2_style))
    story.append(Paragraph(
        "<b>Javalin</b> is an extremely lightweight, modern web framework for Java (inspired by Express.js in Node.js and Sinatra in Ruby). In standard college projects, students often struggle with <b>Spring Boot</b> because Spring is a heavyweight framework containing millions of lines of code, hundreds of annotations (<code>@Autowired</code>, <code>@RestController</code>, <code>@Service</code>), complex reflection, and 15-second cold startup times.",
        body_style
    ))
    story.append(Paragraph(
        "In contrast, Javalin provides <b>zero boilerplate</b> and total transparency. Routes are declared explicitly in plain Java code (e.g., <code>app.get('/api/teams', TeamController::listTeams)</code>). It starts in under <b>200 milliseconds</b> and consumes less than 30MB of RAM. You can trace every line of execution without hidden 'magic'.",
        body_style
    ))

    story.append(Paragraph("B. What is Embedded Jetty?", h2_style))
    story.append(Paragraph(
        "In traditional Java enterprise web apps, you had to install an external Application Server like Apache Tomcat or GlassFish, build a <code>.war</code> file, and deploy it. Javalin comes with <b>Embedded Jetty</b>. Jetty is a high-performance HTTP web server embedded directly inside the Java code as a library. When you call <code>app.start(7070)</code>, Jetty initializes its HTTP socket listener and thread pool within your application process.",
        body_style
    ))

    story.append(Paragraph("C. What is Jackson (JSON Serialization / Deserialization)?", h2_style))
    story.append(Paragraph(
        "Web browsers communicate using <b>JSON text</b> (e.g., <code>{\"email\": \"aarav@campus.edu\"}</code>). Java code operates on <b>BSON Documents and Java Objects</b>. <b>Jackson (ObjectMapper)</b> is the JSON processing library that translates between raw HTTP text and structured Java objects automatically. When you call <code>ctx.json(responseMap)</code> in Javalin, Jackson converts the Java Map into a valid JSON string and sets the HTTP header <code>Content-Type: application/json</code>.",
        body_style
    ))

    story.append(Paragraph("D. What is Apache Maven and the <code>pom.xml</code> File?", h2_style))
    story.append(Paragraph(
        "<b>Maven</b> is the standard build automation and dependency management tool for Java. The <code>pom.xml</code> (Project Object Model) file acts as the single source of truth for the project. Instead of manually downloading JAR files, Maven downloads all required libraries from Maven Central Repository and compiles your source code.",
        body_style
    ))

    maven_table_data = [
        [Paragraph("pom.xml Section", table_header), Paragraph("Declared Artifact", table_header), Paragraph("Why It Is Required in HackMate", table_header)],
        [
            Paragraph("<code>&lt;dependency&gt;</code>", table_cell),
            Paragraph("<code>io.javalin:javalin:5.6.3</code>", table_cell),
            Paragraph("Provides the REST routing engine, request context handling, and embedded Jetty server.", table_cell)
        ],
        [
            Paragraph("<code>&lt;dependency&gt;</code>", table_cell),
            Paragraph("<code>org.mongodb:mongodb-driver-sync:4.11.1</code>", table_cell),
            Paragraph("Official MongoDB Java driver providing BSON document parsing, filters, and socket communication.", table_cell)
        ],
        [
            Paragraph("<code>&lt;dependency&gt;</code>", table_cell),
            Paragraph("<code>de.bwaldvogel:mongo-java-server:1.45.0</code>", table_cell),
            Paragraph("In-memory MongoDB wire-protocol server allowing zero-install database operation during presentations.", table_cell)
        ],
        [
            Paragraph("<code>&lt;dependency&gt;</code>", table_cell),
            Paragraph("<code>org.mindrot:jbcrypt:0.4</code>", table_cell),
            Paragraph("Cryptographic library implementing the Blowfish-based BCrypt password hashing and salting algorithm.", table_cell)
        ],
        [
            Paragraph("<code>&lt;dependency&gt;</code>", table_cell),
            Paragraph("<code>com.auth0:java-jwt:4.4.0</code>", table_cell),
            Paragraph("Industry-standard Auth0 library for creating, signing, and verifying HMAC256 JSON Web Tokens.", table_cell)
        ],
        [
            Paragraph("<code>&lt;plugin&gt;</code>", table_cell),
            Paragraph("<code>exec-maven-plugin:3.1.1</code>", table_cell),
            Paragraph("Allows running the backend directly from the command line targeting <code>com.vexoria.Main</code>.", table_cell)
        ]
    ]
    maven_t = Table(maven_table_data, colWidths=[100, 160, 255])
    maven_t.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), C_PRIMARY),
        ('BOX', (0, 0), (-1, -1), 0.8, C_BORDER),
        ('INNERGRID', (0, 0), (-1, -1), 0.5, C_BORDER_LIGHT),
        ('TOPPADDING', (0, 0), (-1, -1), 3.5),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 3.5),
        ('LEFTPADDING', (0, 0), (-1, -1), 5),
        ('RIGHTPADDING', (0, 0), (-1, -1), 5),
    ]))
    story.append(maven_t)

    story.append(PageBreak())

    # =========================================================================
    # PAGE 4: BACKEND RUN COMMAND LINE-BY-LINE EXPLANATION
    # =========================================================================
    story.append(Paragraph("6. Backend Run Command — Line-by-Line Breakdown", h1_style))
    story.append(Paragraph(
        "A classic viva question is: <i>'Open PowerShell and show me how the server starts. What does each part of your startup command actually do?'</i> Here is the complete breakdown of <code>start-backend.ps1</code> and Maven execution.",
        body_style
    ))

    script_lines = [
        "# start-backend.ps1",
        "$ErrorActionPreference = \"Stop\"",
        "$toolsDir = \"$env:USERPROFILE\\tools\"",
        "$jdkPath = Get-ChildItem \"$toolsDir\" -Filter \"*jdk*\" -Directory | Select-Object -First 1 -ExpandProperty FullName",
        "if ($jdkPath) {",
        "    $env:JAVA_HOME = $jdkPath",
        "    $env:PATH = \"$jdkPath\\bin;$env:PATH\"",
        "}",
        "$mvnDir = Get-ChildItem \"$toolsDir\" -Filter \"*apache-maven*\" -Directory | Select-Object -First 1 -ExpandProperty FullName",
        "if ($mvnDir -and (Test-Path \"$mvnDir\\bin\\mvn.cmd\")) {",
        "    $env:PATH = \"$mvnDir\\bin;$env:PATH\"",
        "}",
        "Set-Location \"$PSScriptRoot\\backend\"",
        "mvn clean compile exec:java"
    ]
    story.append(make_code_box(script_lines, title="start-backend.ps1 SCRIPT CONTENT"))
    story.append(Spacer(1, 5))

    cmd_breakdown = [
        [Paragraph("Script Line / Command Element", table_header), Paragraph("Technical Meaning & Exact Operation in Windows PowerShell", table_header)],
        [
            Paragraph("<code>$ErrorActionPreference = 'Stop'</code>", table_cell_bold),
            Paragraph("Sets PowerShell execution to fail-fast mode. If any command or path lookup encounters an error, the script immediately halts execution instead of continuing into a broken state.", table_cell)
        ],
        [
            Paragraph("<code>$env:JAVA_HOME = $jdkPath</code>", table_cell_bold),
            Paragraph("Configures the <code>JAVA_HOME</code> environment variable for the current PowerShell process session. Maven strictly requires <code>JAVA_HOME</code> to point to a valid Java Development Kit (JDK 17) directory to locate compilers and header files.", table_cell)
        ],
        [
            Paragraph("<code>$env:PATH = \"$jdkPath\\bin;...\"</code>", table_cell_bold),
            Paragraph("Prepends the JDK's <code>bin/</code> folder to the system execution search path. This ensures commands like <code>javac.exe</code> (compiler) and <code>java.exe</code> (JVM runtime) can be found immediately without modifying global Windows registry settings.", table_cell)
        ],
        [
            Paragraph("<code>$env:PATH = \"$mvnDir\\bin;...\"</code>", table_cell_bold),
            Paragraph("Prepends Apache Maven's binary folder to <code>PATH</code>, making the <code>mvn.cmd</code> batch script executable in the current terminal session.", table_cell)
        ],
        [
            Paragraph("<code>Set-Location \"$PSScriptRoot\\backend\"</code>", table_cell_bold),
            Paragraph("Changes the active working directory to the <code>backend/</code> folder containing <code>pom.xml</code>. <code>$PSScriptRoot</code> is an automatic PowerShell variable that resolves to the directory containing the running script.", table_cell)
        ],
        [
            Paragraph("<code>mvn clean</code>", table_cell_bold),
            Paragraph("<b>Build Lifecycle Phase 1:</b> Deletes the entire <code>target/</code> build directory. This removes previously compiled <code>.class</code> bytecode and cached dependencies, ensuring a 100% clean, bug-free compilation.", table_cell)
        ],
        [
            Paragraph("<code>mvn compile</code>", table_cell_bold),
            Paragraph("<b>Build Lifecycle Phase 2:</b> Invokes the <code>maven-compiler-plugin</code>. Reads all <code>.java</code> source files from <code>src/main/java/</code> and compiles them into JVM-executable <code>.class</code> bytecode inside <code>target/classes/</code> using Java 17.", table_cell)
        ],
        [
            Paragraph("<code>mvn exec:java</code>", table_cell_bold),
            Paragraph("<b>Execution Phase:</b> Invokes the <code>exec-maven-plugin</code> configured in <code>pom.xml</code>. It launches the JVM, loads all runtime dependencies into the classpath, and calls the static entry point method <code>com.vexoria.Main.main(String[] args)</code>.", table_cell)
        ]
    ]
    cmd_t = Table(cmd_breakdown, colWidths=[150, 365])
    cmd_t.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), C_PRIMARY),
        ('BOX', (0, 0), (-1, -1), 0.8, C_BORDER),
        ('INNERGRID', (0, 0), (-1, -1), 0.5, C_BORDER_LIGHT),
        ('TOPPADDING', (0, 0), (-1, -1), 3.5),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 3.5),
        ('LEFTPADDING', (0, 0), (-1, -1), 5),
        ('RIGHTPADDING', (0, 0), (-1, -1), 5),
    ]))
    story.append(cmd_t)
    story.append(Spacer(1, 5))

    story.append(make_card([
        Paragraph("<b>JDK vs JRE Distinction (Crucial Viva Defense Note):</b>", callout_bold),
        Paragraph("The <b>JRE (Java Runtime Environment)</b> only contains the JVM and libraries needed to <i>run</i> pre-compiled Java bytecode. The <b>JDK (Java Development Kit)</b> contains the JRE plus development tools including the Java compiler (<code>javac</code>), debugger, and documentation tools. Maven requires a <b>JDK</b> to compile <code>.java</code> source files into <code>.class</code> files.", callout_text)
    ], bg_color=C_BG_CARD, border_color=C_BORDER))

    story.append(PageBreak())

    # =========================================================================
    # PAGE 5: BACKEND DEEP DIVE — MAIN.JAVA & DBCONFIG.JAVA
    # =========================================================================
    story.append(Paragraph("7. Backend Codebase Deep Dive — Main.java & DbConfig.java", h1_style))
    story.append(Paragraph(
        "Here is the detailed structural analysis of the core initialization files: <code>Main.java</code> (server entry point) and <code>DbConfig.java</code> (database connection manager).",
        body_style
    ))

    story.append(Paragraph("A. Main.java — Server Bootstrapper & Routing Table", h2_style))
    main_code = [
        "public class Main {",
        "    public static void main(String[] args) {",
        "        int port = 7070; // Default port or System.getenv(\"PORT\")",
        "        DbConfig.init(); // 1. Connect database & create indexes",
        "        seedInitialDataIfEmpty(); // 2. Insert mock SIH/ETHIndia squads",
        "        Javalin app = Javalin.create(config -> {",
        "            config.plugins.enableCors(cors -> cors.add(CorsPluginConfig::anyHost));",
        "        });",
        "        app.before(\"/api/*\", AuthFilter::filter); // 3. Global Auth Middleware",
        "        app.post(\"/api/auth/register\", AuthController::register);",
        "        app.post(\"/api/auth/login\", AuthController::login);",
        "        app.get(\"/api/teams\", TeamController::listTeams);",
        "        app.post(\"/api/requests\", RequestController::sendRequest);",
        "        app.start(port); // 4. Boot Embedded Jetty on port 7070",
        "    }",
        "}"
    ]
    story.append(make_code_box(main_code, title="backend/src/main/java/com/vexoria/Main.java"))
    story.append(Spacer(1, 4))

    story.append(Paragraph("<b>Main.java Execution Steps:</b>", body_bold))
    story.append(Paragraph("• <b>Port Resolution (Lines 23-27):</b> Checks if a cloud host provided a <code>PORT</code> environment variable (e.g., Render, Railway, AWS). Defaults to <code>7070</code> for local execution.", bullet_style))
    story.append(Paragraph("• <b>CORS Configuration (Lines 34-36):</b> Configures Javalin's CORS plugin with <code>anyHost()</code>. This adds the HTTP response header <code>Access-Control-Allow-Origin: *</code> so the browser on port 5173 can send requests without being blocked by the Same-Origin Policy.", bullet_style))
    story.append(Paragraph("• <b>Route Registration (Lines 41-69):</b> Uses Java 8 method references (e.g., <code>TeamController::listTeams</code>) to map HTTP verbs and URL paths directly to static controller methods.", bullet_style))
    story.append(Paragraph("• <b>Data Seeding (Lines 74-177):</b> <code>seedInitialDataIfEmpty()</code> checks if users and teams exist. If empty, it creates 3 realistic campus profiles (Aarav, Ananya, Kabir) and 3 hackathon squads (AgriPulse SIH 2026, ProofOfSkill ETHIndia 2026, PulseShuttle CodeFest 2026) with BCrypt-hashed passwords (<code>student123</code>).", bullet_style))

    story.append(Spacer(1, 4))
    story.append(Paragraph("B. DbConfig.java — Resilience & In-Memory Fallback Engine", h2_style))
    story.append(Paragraph(
        "<code>DbConfig.java</code> implements a resilient connection waterfall that guarantees the application will run anywhere without manual database installation:",
        body_style
    ))

    db_waterfall_data = [
        [Paragraph("Waterfall Stage", table_header), Paragraph("Connection Target", table_header), Paragraph("Behavior & Fallback Condition", table_header)],
        [
            Paragraph("<b>Stage 1</b><br/>Cloud URI", table_cell_bold),
            Paragraph("<code>System.getenv(\"MONGODB_URI\")</code>", table_cell),
            Paragraph("Checks for a remote MongoDB Atlas connection string. If provided and reachable, connects immediately.", table_cell)
        ],
        [
            Paragraph("<b>Stage 2</b><br/>Local Daemon", table_cell_bold),
            Paragraph("<code>mongodb://localhost:27017</code>", table_cell),
            Paragraph("Attempts connection to a local MongoDB service with a strict <b>1500ms timeout</b>. If MongoDB is installed locally as a Windows service, it uses it.", table_cell)
        ],
        [
            Paragraph("<b>Stage 3</b><br/>In-Memory Server", table_cell_bold),
            Paragraph("<code>new MongoServer(new MemoryBackend())</code>", table_cell),
            Paragraph("<b>Zero-Config Fallback:</b> Starts an embedded in-memory MongoDB wire server on an ephemeral port. Fully compliant with BSON queries.", table_cell)
        ]
    ]
    db_w_t = Table(db_waterfall_data, colWidths=[90, 160, 265])
    db_w_t.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), C_PRIMARY),
        ('BOX', (0, 0), (-1, -1), 0.8, C_BORDER),
        ('INNERGRID', (0, 0), (-1, -1), 0.5, C_BORDER_LIGHT),
        ('TOPPADDING', (0, 0), (-1, -1), 3),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 3),
        ('LEFTPADDING', (0, 0), (-1, -1), 5),
        ('RIGHTPADDING', (0, 0), (-1, -1), 5),
    ]))
    story.append(db_w_t)
    story.append(Spacer(1, 4))

    story.append(Paragraph(
        "<b>Disk Persistence Engine (Lines 116-184):</b> Whenever data changes, <code>DbConfig.saveCollection(name)</code> serializes all BSON documents into formatted JSON files inside the <code>data/</code> folder (e.g., <code>data/teams.json</code>). On subsequent restarts, <code>loadPersistentData()</code> reloads them. This ensures data created during testing is never lost even when using the in-memory fallback server!",
        body_style
    ))

    story.append(PageBreak())

    # =========================================================================
    # PAGE 6: BACKEND DEEP DIVE — AUTHFILTER & JWTUTIL
    # =========================================================================
    story.append(Paragraph("8. Backend Security Pipeline — AuthFilter.java & JwtUtil.java", h1_style))
    story.append(Paragraph(
        "Security in HackMate is enforced through a combination of HTTP Middleware (<code>AuthFilter</code>) and Cryptographic Token Verification (<code>JwtUtil</code>).",
        body_style
    ))

    story.append(Paragraph("A. AuthFilter.java — Request Interception & Context Injection", h2_style))
    authfilter_code = [
        "public class AuthFilter {",
        "    public static void filter(Context ctx) {",
        "        String path = ctx.path();",
        "        String method = ctx.method().name();",
        "        boolean needsAuth = false;",
        "        if (path.startsWith(\"/api/users/me\") || path.startsWith(\"/api/requests\")) needsAuth = true;",
        "        else if (path.startsWith(\"/api/teams\")) {",
        "            if (\"POST\".equalsIgnoreCase(method) || \"PUT\".equalsIgnoreCase(method) || \"DELETE\".equalsIgnoreCase(method))",
        "                needsAuth = true; // GET /api/teams is public",
        "        }",
        "        if (!needsAuth) return; // Allow public routes through",
        "        String authHeader = ctx.header(\"Authorization\");",
        "        if (authHeader == null || !authHeader.startsWith(\"Bearer \")) {",
        "            ctx.status(401).json(Map.of(\"error\", \"Missing or invalid Authorization header\"));",
        "            throw new UnauthorizedResponse();",
        "        }",
        "        String token = authHeader.substring(7).trim();",
        "        DecodedJWT jwt = JwtUtil.verifyToken(token); // Verify HMAC256 signature",
        "        ctx.attribute(\"userId\", JwtUtil.getUserId(jwt)); // Inject userId for downstream controllers",
        "        ctx.attribute(\"userEmail\", JwtUtil.getEmail(jwt));",
        "    }",
        "}"
    ]
    story.append(make_code_box(authfilter_code, title="backend/src/main/java/com/vexoria/middleware/AuthFilter.java"))
    story.append(Spacer(1, 4))

    story.append(Paragraph("<b>Detailed Interceptor Mechanism:</b>", body_bold))
    story.append(Paragraph("1. <b>Route Path Evaluation:</b> Public routes like <code>POST /api/auth/login</code>, <code>POST /api/auth/register</code>, and <code>GET /api/teams</code> bypass the filter immediately.", bullet_style))
    story.append(Paragraph("2. <b>Header Extraction:</b> For mutating operations (creating teams, sending pitches, accepting applicants), the filter checks for the <code>Authorization: Bearer &lt;token&gt;</code> header.", bullet_style))
    story.append(Paragraph("3. <b>Token Verification:</b> <code>JwtUtil.verifyToken()</code> cryptographically verifies the token's HMAC256 signature and checks that the expiration timestamp has not passed.", bullet_style))
    story.append(Paragraph("4. <b>Context Attribute Binding:</b> Once verified, the user's MongoDB <code>ObjectId</code> hex string is bound to <code>ctx.attribute(\"userId\", ...)</code>. Downstream controllers can safely access <code>ctx.attribute(\"userId\")</code> without re-verifying credentials.", bullet_style))

    story.append(Spacer(1, 4))
    story.append(Paragraph("B. JwtUtil.java — Stateless HMAC256 Token Engine", h2_style))
    jwt_code = [
        "public class JwtUtil {",
        "    private static final String SECRET = System.getenv().getOrDefault(\"JWT_SECRET\", \"vexoria_secret_2026\");",
        "    private static final Algorithm ALGORITHM = Algorithm.HMAC256(SECRET);",
        "    private static final JWTVerifier VERIFIER = JWT.require(ALGORITHM).build();",
        "    public static String generateToken(User user) {",
        "        return JWT.create()",
        "            .withSubject(user.getId())",
        "            .withClaim(\"email\", user.getEmail())",
        "            .withClaim(\"name\", user.getName())",
        "            .withExpiresAt(Instant.now().plus(7, ChronoUnit.DAYS))",
        "            .sign(ALGORITHM);",
        "    }",
        "    public static DecodedJWT verifyToken(String token) { return VERIFIER.verify(token); }",
        "    public static String getUserId(DecodedJWT jwt) { return jwt.getSubject(); }",
        "}"
    ]
    story.append(make_code_box(jwt_code, title="backend/src/main/java/com/vexoria/util/JwtUtil.java"))
    story.append(Spacer(1, 4))

    story.append(Paragraph(
        "<b>Why JWT is Stateless:</b> Unlike legacy PHP/Java EE sessions that store user session state in server RAM (which breaks if the server restarts or scales horizontally), a JWT is self-contained. The server does not query the database to verify identity; it only checks the mathematical HMAC256 signature. If an attacker modifies the payload (e.g., tampering with <code>userId</code>), the signature mismatch causes instant rejection.",
        body_style
    ))

    story.append(PageBreak())

    # =========================================================================
    # PAGE 7: BACKEND DEEP DIVE — AUTHCONTROLLER & TEAMCONTROLLER
    # =========================================================================
    story.append(Paragraph("9. Backend Controllers — AuthController.java & TeamController.java", h1_style))
    story.append(Paragraph(
        "Controllers encapsulate the business logic of HackMate. Here is how user registration, authentication, and team search algorithms are executed.",
        body_style
    ))

    story.append(Paragraph("A. AuthController.java — Registration & Login Logic", h2_style))
    auth_ctrl_code = [
        "// Registration Snippet",
        "String hashedPassword = BCrypt.hashpw(password, BCrypt.gensalt(10)); // 10 Salt Rounds",
        "Document userDoc = new Document(\"_id\", new ObjectId())",
        "    .append(\"name\", name.trim())",
        "    .append(\"email\", normalizedEmail) // Lowercase deduplication",
        "    .append(\"passwordHash\", hashedPassword)",
        "    .append(\"branch\", branch).append(\"year\", year).append(\"skills\", skills);",
        "usersCol.insertOne(userDoc);",
        "String token = JwtUtil.generateToken(user); // Instant session token",
        "",
        "// Login Snippet",
        "Document userDoc = usersCol.find(Filters.eq(\"email\", normalizedEmail)).first();",
        "if (userDoc == null) { ctx.status(404).json(Map.of(\"error\", \"No account found\")); return; }",
        "if (!BCrypt.checkpw(password, userDoc.getString(\"passwordHash\"))) {",
        "    ctx.status(401).json(Map.of(\"error\", \"Incorrect password\")); return;",
        "}"
    ]
    story.append(make_code_box(auth_ctrl_code, title="backend/src/main/java/com/vexoria/controllers/AuthController.java"))
    story.append(Spacer(1, 4))

    story.append(Paragraph("<b>Security Safeguards in AuthController:</b>", body_bold))
    story.append(Paragraph("• <b>Email Normalization:</b> <code>email.toLowerCase().trim()</code> prevents duplicate registrations like <code>Aarav@campus.edu</code> and <code>aarav@campus.edu</code>.", bullet_style))
    story.append(Paragraph("• <b>BCrypt Salting (Work Factor 10):</b> <code>BCrypt.gensalt(10)</code> creates a unique 128-bit cryptographic salt for every user. Two users with the password 'password123' will have completely different hashes, neutralizing Rainbow Table attacks.", bullet_style))
    story.append(Paragraph("• <b>Sanitized Response:</b> The raw password and password hash are never returned to the frontend. Only the user profile and JWT are sent back.", bullet_style))

    story.append(Spacer(1, 4))
    story.append(Paragraph("B. TeamController.java — Multi-Param Dynamic Search Engine", h2_style))
    story.append(Paragraph(
        "<code>TeamController.listTeams()</code> implements dynamic query compounding using MongoDB BSON filters:",
        body_style
    ))

    team_search_code = [
        "public static void listTeams(Context ctx) {",
        "    List<Bson> filters = new ArrayList<>();",
        "    String statusFilter = ctx.queryParam(\"status\");",
        "    String skillFilter = ctx.queryParam(\"skill\");",
        "    String searchQuery = ctx.queryParam(\"search\");",
        "    if (statusFilter != null && !statusFilter.isBlank())",
        "        filters.add(Filters.eq(\"status\", statusFilter.trim().toUpperCase()));",
        "    if (skillFilter != null && !skillFilter.isBlank()) {",
        "        Pattern p = Pattern.compile(Pattern.quote(skillFilter.trim()), Pattern.CASE_INSENSITIVE);",
        "        filters.add(Filters.regex(\"skillsNeeded\", p));",
        "    }",
        "    if (searchQuery != null && !searchQuery.isBlank()) {",
        "        Pattern p = Pattern.compile(Pattern.quote(searchQuery.trim()), Pattern.CASE_INSENSITIVE);",
        "        filters.add(Filters.or(Filters.regex(\"title\", p), Filters.regex(\"hackathonName\", p), Filters.regex(\"description\", p)));",
        "    }",
        "    Bson query = filters.isEmpty() ? new Document() : Filters.and(filters);",
        "    List<Document> teams = DbConfig.getTeamsCollection().find(query).sort(Sorts.descending(\"createdAt\")).into(new ArrayList<>());",
        "    ctx.json(teams.stream().map(TeamController::serializeTeam).toList());",
        "}"
    ]
    story.append(make_code_box(team_search_code, title="backend/src/main/java/com/vexoria/controllers/TeamController.java"))
    story.append(Spacer(1, 4))

    story.append(Paragraph(
        "<b>Regex Injection Protection:</b> Notice the use of <code>Pattern.quote(input)</code>. If a malicious user searches for regex characters like <code>.*</code> or <code>[a-z]+</code>, <code>Pattern.quote()</code> escapes them into literal characters, preventing catastrophic regex backtracking (ReDoS).",
        body_style
    ))

    story.append(PageBreak())

    # =========================================================================
    # PAGE 8: BACKEND DEEP DIVE — REQUESTCONTROLLER & ATOMIC ROSTER ENGINE
    # =========================================================================
    story.append(Paragraph("10. Join Requests & Atomic Roster Engine — RequestController.java", h1_style))
    story.append(Paragraph(
        "The join request workflow is the most critical business feature in HackMate. It handles pitch submission, duplicate application prevention, and automatic squad roster locking.",
        body_style
    ))

    story.append(Paragraph("A. sendRequest() — 4 Strict Pre-Application Validation Guards", h2_style))
    req_guard_code = [
        "// 1. Cannot apply to own team",
        "if (userId.equals(teamDoc.getString(\"createdBy\"))) {",
        "    ctx.status(400).json(Map.of(\"error\", \"You cannot apply to your own team\")); return;",
        "}",
        "// 2. Team must be OPEN",
        "if (!\"OPEN\".equalsIgnoreCase(teamDoc.getString(\"status\"))) {",
        "    ctx.status(400).json(Map.of(\"error\", \"This team is currently not open to new members\")); return;",
        "}",
        "// 3. User cannot already be a member of the roster",
        "List<Document> members = (List<Document>) teamDoc.get(\"currentMembers\");",
        "if (members.stream().anyMatch(m -> userId.equals(m.getString(\"userId\")))) {",
        "    ctx.status(400).json(Map.of(\"error\", \"You are already a member of this team\")); return;",
        "}",
        "// 4. Duplicate pending request guard",
        "Document existing = reqsCol.find(Filters.and(",
        "    Filters.eq(\"teamId\", teamId), Filters.eq(\"userId\", userId), Filters.in(\"status\", \"PENDING\", \"ACCEPTED\")",
        ")).first();",
        "if (existing != null) {",
        "    ctx.status(409).json(Map.of(\"error\", \"You have already submitted an active request\")); return;",
        "}"
    ]
    story.append(make_code_box(req_guard_code, title="backend/src/main/java/com/vexoria/controllers/RequestController.java (Guards)"))
    story.append(Spacer(1, 4))

    story.append(Paragraph("B. updateRequestStatus() — Atomic Member Insertion & Team Status Locking", h2_style))
    story.append(Paragraph(
        "When a squad leader approves an applicant on the dashboard, the following atomic update sequence executes:",
        body_style
    ))

    roster_lock_code = [
        "// Verified: Current user is the team owner",
        "if (\"ACCEPTED\".equals(newStatus)) {",
        "    Document teamDoc = teamsCol.find(Filters.eq(\"_id\", new ObjectId(teamId))).first();",
        "    List<Document> members = (List<Document>) teamDoc.get(\"currentMembers\");",
        "    int maxTeamSize = teamDoc.getInteger(\"teamSize\", 4);",
        "    Document newMember = new Document(\"userId\", reqDoc.getString(\"userId\"))",
        "        .append(\"name\", reqDoc.getString(\"userName\"))",
        "        .append(\"role\", \"Member\");",
        "    members.add(newMember); // Append applicant to squad roster",
        "    // If roster reaches capacity, lock status to FULL automatically!",
        "    String updatedStatus = (members.size() >= maxTeamSize) ? \"FULL\" : teamDoc.getString(\"status\");",
        "    teamsCol.updateOne(Filters.eq(\"_id\", new ObjectId(teamId)), Updates.combine(",
        "        Updates.set(\"currentMembers\", members),",
        "        Updates.set(\"status\", updatedStatus)",
        "    ));",
        "    DbConfig.saveCollection(\"teams\");",
        "}",
        "reqsCol.updateOne(Filters.eq(\"_id\", new ObjectId(reqId)), Updates.set(\"status\", newStatus));",
        "DbConfig.saveCollection(\"join_requests\");"
    ]
    story.append(make_code_box(roster_lock_code, title="backend/src/main/java/com/vexoria/controllers/RequestController.java (Roster Lock)"))
    story.append(Spacer(1, 4))

    story.append(Paragraph(
        "<b>Why this is technically impressive for viva:</b> The roster status transitions automatically from <code>OPEN</code> to <code>FULL</code> as soon as the team capacity limit is reached. No further join requests can be submitted to that squad.",
        body_style
    ))

    story.append(PageBreak())

    # =========================================================================
    # PAGE 9: DATABASE DESIGN & MONGODB MODELING
    # =========================================================================
    story.append(Paragraph("11. Database Design & MongoDB Schema Modeling", h1_style))
    story.append(Paragraph(
        "HackMate utilizes <b>MongoDB</b>, a document-oriented NoSQL database. Documents are stored in BSON (Binary JSON) format. Here is the formal schema specification across the 3 primary collections:",
        body_style
    ))

    story.append(Paragraph("A. `users` Collection Schema", h2_style))
    users_schema_data = [
        [Paragraph("Field Name", table_header), Paragraph("BSON Type", table_header), Paragraph("Indexed", table_header), Paragraph("Description & Sample Value", table_header)],
        [Paragraph("<code>_id</code>", table_cell_bold), Paragraph("ObjectId", table_cell), Paragraph("PRIMARY", table_cell), Paragraph("Unique 12-byte hexadecimal MongoDB identifier.", table_cell)],
        [Paragraph("<code>name</code>", table_cell_bold), Paragraph("String", table_cell), Paragraph("No", table_cell), Paragraph("Full student name (e.g., 'Aarav Mehta').", table_cell)],
        [Paragraph("<code>email</code>", table_cell_bold), Paragraph("String", table_cell), Paragraph("UNIQUE", table_cell), Paragraph("Campus email in lowercase (e.g., 'aarav@campus.edu').", table_cell)],
        [Paragraph("<code>passwordHash</code>", table_cell_bold), Paragraph("String", table_cell), Paragraph("No", table_cell), Paragraph("60-character BCrypt salted hash string (<code>$2a$10$...</code>).", table_cell)],
        [Paragraph("<code>branch</code>", table_cell_bold), Paragraph("String", table_cell), Paragraph("No", table_cell), Paragraph("Academic branch (e.g., 'Computer Science & Engineering').", table_cell)],
        [Paragraph("<code>year</code>", table_cell_bold), Paragraph("String", table_cell), Paragraph("No", table_cell), Paragraph("Academic year (e.g., '3rd Year').", table_cell)],
        [Paragraph("<code>skills</code>", table_cell_bold), Paragraph("Array&lt;String&gt;", table_cell), Paragraph("No", table_cell), Paragraph("List of declared skill tags: <code>['Python', 'PyTorch', 'React']</code>.", table_cell)],
        [Paragraph("<code>createdAt</code>", table_cell_bold), Paragraph("Date", table_cell), Paragraph("No", table_cell), Paragraph("Account creation timestamp.", table_cell)]
    ]
    u_sch_t = Table(users_schema_data, colWidths=[80, 75, 55, 305])
    u_sch_t.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), C_PRIMARY),
        ('BOX', (0, 0), (-1, -1), 0.8, C_BORDER),
        ('INNERGRID', (0, 0), (-1, -1), 0.5, C_BORDER_LIGHT),
        ('TOPPADDING', (0, 0), (-1, -1), 3),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 3),
        ('LEFTPADDING', (0, 0), (-1, -1), 5),
        ('RIGHTPADDING', (0, 0), (-1, -1), 5),
    ]))
    story.append(u_sch_t)
    story.append(Spacer(1, 4))

    story.append(Paragraph("B. `teams` Collection Schema", h2_style))
    teams_schema_data = [
        [Paragraph("Field Name", table_header), Paragraph("BSON Type", table_header), Paragraph("Indexed", table_header), Paragraph("Description & Sample Value", table_header)],
        [Paragraph("<code>_id</code>", table_cell_bold), Paragraph("ObjectId", table_cell), Paragraph("PRIMARY", table_cell), Paragraph("Unique team identifier.", table_cell)],
        [Paragraph("<code>hackathonName</code>", table_cell_bold), Paragraph("String", table_cell), Paragraph("No", table_cell), Paragraph("Name of target hackathon (e.g., 'Smart India Hackathon 2026').", table_cell)],
        [Paragraph("<code>title</code>", table_cell_bold), Paragraph("String", table_cell), Paragraph("No", table_cell), Paragraph("Project title (e.g., 'AgriPulse – AI Crop Diagnostics').", table_cell)],
        [Paragraph("<code>description</code>", table_cell_bold), Paragraph("String", table_cell), Paragraph("No", table_cell), Paragraph("Detailed problem statement and scope explanation.", table_cell)],
        [Paragraph("<code>skillsNeeded</code>", table_cell_bold), Paragraph("Array&lt;String&gt;", table_cell), Paragraph("No", table_cell), Paragraph("Skills sought: <code>['FastAPI', 'Tailwind CSS', 'TensorFlow']</code>.", table_cell)],
        [Paragraph("<code>teamSize</code>", table_cell_bold), Paragraph("Integer", table_cell), Paragraph("No", table_cell), Paragraph("Maximum team capacity limit (e.g., 4).", table_cell)],
        [Paragraph("<code>currentMembers</code>", table_cell_bold), Paragraph("Array&lt;Doc&gt;", table_cell), Paragraph("No", table_cell), Paragraph("Embedded array of members: <code>[{userId, name, role}]</code>.", table_cell)],
        [Paragraph("<code>createdBy</code>", table_cell_bold), Paragraph("String", table_cell), Paragraph("No", table_cell), Paragraph("MongoDB hex ID of team creator.", table_cell)],
        [Paragraph("<code>status</code>", table_cell_bold), Paragraph("String", table_cell), Paragraph("ASCENDING", table_cell), Paragraph("Roster status: <code>'OPEN'</code> or <code>'FULL'</code>.", table_cell)],
        [Paragraph("<code>createdAt</code>", table_cell_bold), Paragraph("Date", table_cell), Paragraph("DESCENDING", table_cell), Paragraph("Timestamp for sorting listings.", table_cell)]
    ]
    t_sch_t = Table(teams_schema_data, colWidths=[85, 75, 65, 290])
    t_sch_t.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), C_PRIMARY),
        ('BOX', (0, 0), (-1, -1), 0.8, C_BORDER),
        ('INNERGRID', (0, 0), (-1, -1), 0.5, C_BORDER_LIGHT),
        ('TOPPADDING', (0, 0), (-1, -1), 3),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 3),
        ('LEFTPADDING', (0, 0), (-1, -1), 5),
        ('RIGHTPADDING', (0, 0), (-1, -1), 5),
    ]))
    story.append(t_sch_t)
    story.append(Spacer(1, 4))

    story.append(Paragraph("C. `join_requests` Collection Schema", h2_style))
    story.append(Paragraph(
        "Fields: <code>_id</code> (ObjectId), <code>teamId</code> (String, Indexed), <code>teamTitle</code> (String), <code>hackathonName</code> (String), <code>teamOwnerId</code> (String), <code>userId</code> (String, Indexed), <code>userName</code> (String), <code>userEmail</code> (String), <code>userBranch</code> (String), <code>userYear</code> (String), <code>userSkills</code> (Array), <code>message</code> (String), <code>status</code> (<code>'PENDING' | 'ACCEPTED' | 'REJECTED'</code>), <code>createdAt</code> (Date).",
        body_style
    ))
    story.append(Paragraph(
        "<b>Why User Details are Embedded in Requests:</b> Denormalizing the applicant's name, branch, year, and skills into the request document allows the Squad Leader's dashboard to render in a single query without executing expensive multi-collection <code>$lookup</code> joins.",
        body_style
    ))

    story.append(PageBreak())

    # =========================================================================
    # PAGE 10: AUTHENTICATION & CRYPTOGRAPHY PIPELINE
    # =========================================================================
    story.append(Paragraph("12. Authentication, Cryptography & Security Mechanisms", h1_style))
    story.append(Paragraph(
        "Professors frequently inspect the security implementation to verify that passwords and sessions are protected using industry standards.",
        body_style
    ))

    story.append(Paragraph("A. BCrypt vs SHA-256 — Why Hashing is Not Encryption", h2_style))
    story.append(Paragraph(
        "A critical viva distinction: <b>Encryption</b> is a two-way mathematical process (Plaintext &harr; Ciphertext using a secret key). <b>Hashing</b> is a one-way mathematical function (Plaintext &rarr; Hash). Passwords must <i>never</i> be encrypted; they must be <b>one-way hashed</b> so that even database administrators cannot view plaintext passwords.",
        body_style
    ))

    crypto_comp_data = [
        [Paragraph("Hashing Algorithm", table_header), Paragraph("Speed / Rounds", table_header), Paragraph("Salt Mechanism", table_header), Paragraph("Vulnerability to GPU Attacks", table_header)],
        [
            Paragraph("<b>Plain MD5 / SHA-256</b><br/>(Insecure for Passwords)", table_cell),
            Paragraph("Ultra-fast (billions of hashes/sec on modern GPU).", table_cell),
            Paragraph("No salt by default; identical passwords produce identical hashes.", table_cell),
            Paragraph("<b>Extremely Vulnerable:</b> Attackers can crack 8-character passwords in minutes using precomputed Rainbow Tables.", table_cell)
        ],
        [
            Paragraph("<b>BCrypt (Work Factor 10)</b><br/>(Used in HackMate)", table_cell_bold),
            Paragraph("Intentionally slow (2<sup>10</sup> = 1024 iterations of Blowfish cipher).", table_cell),
            Paragraph("Automatic 16-byte random salt generated per hash (<code>BCrypt.gensalt(10)</code>).", table_cell),
            Paragraph("<b>Highly Secure:</b> Slow execution makes brute-force attacks computationally impossible on consumer GPUs.", table_cell)
        ]
    ]
    crypto_t = Table(crypto_comp_data, colWidths=[115, 120, 110, 170])
    crypto_t.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), C_PRIMARY),
        ('BOX', (0, 0), (-1, -1), 0.8, C_BORDER),
        ('INNERGRID', (0, 0), (-1, -1), 0.5, C_BORDER_LIGHT),
        ('TOPPADDING', (0, 0), (-1, -1), 4),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 4),
        ('LEFTPADDING', (0, 0), (-1, -1), 5),
        ('RIGHTPADDING', (0, 0), (-1, -1), 5),
    ]))
    story.append(crypto_t)
    story.append(Spacer(1, 6))

    story.append(Paragraph("B. Anatomy of a JSON Web Token (JWT)", h2_style))
    story.append(Paragraph(
        "A JSON Web Token consists of three base64url-encoded parts separated by periods (<code>.</code>):",
        body_style
    ))

    jwt_parts_data = [
        [Paragraph("JWT Segment", table_header), Paragraph("Raw JSON Content", table_header), Paragraph("Cryptographic Role", table_header)],
        [
            Paragraph("<b>1. Header</b>", table_cell_bold),
            Paragraph("<code>{\"alg\": \"HS256\", \"typ\": \"JWT\"}</code>", table_cell),
            Paragraph("Declares the cryptographic signing algorithm (HMAC with SHA-256).", table_cell)
        ],
        [
            Paragraph("<b>2. Payload</b>", table_cell_bold),
            Paragraph("<code>{\"sub\": \"65df...\", \"email\": \"aarav@campus.edu\", \"exp\": 1775...}</code>", table_cell),
            Paragraph("Contains the claims: User MongoDB ObjectId (<code>sub</code>), email, name, and expiration time.", table_cell)
        ],
        [
            Paragraph("<b>3. Signature</b>", table_cell_bold),
            Paragraph("<code>HMACSHA256(base64Url(Header) + \".\" + base64Url(Payload), secret)</code>", table_cell),
            Paragraph("Ensures integrity. Generated using server's private secret key. Any tampering invalidates the signature.", table_cell)
        ]
    ]
    jwt_t = Table(jwt_parts_data, colWidths=[80, 200, 235])
    jwt_t.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), C_PRIMARY),
        ('BOX', (0, 0), (-1, -1), 0.8, C_BORDER),
        ('INNERGRID', (0, 0), (-1, -1), 0.5, C_BORDER_LIGHT),
        ('TOPPADDING', (0, 0), (-1, -1), 4),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 4),
        ('LEFTPADDING', (0, 0), (-1, -1), 5),
        ('RIGHTPADDING', (0, 0), (-1, -1), 5),
    ]))
    story.append(jwt_t)
    story.append(Spacer(1, 6))

    story.append(Paragraph("C. Cross-Origin Resource Sharing (CORS) Mechanics", h2_style))
    story.append(Paragraph(
        "Web browsers enforce the <b>Same-Origin Policy (SOP)</b> to prevent malicious websites from making unauthorized requests on behalf of a user. An origin is defined by the tuple <code>(Protocol, Domain, Port)</code>. Because HackMate's frontend runs on port <code>5173</code> and the backend runs on <code>7070</code>, the browser initiates a <b>Preflight OPTIONS request</b> asking the server for permission. Javalin handles this via <code>CorsPluginConfig::anyHost</code>, returning <code>Access-Control-Allow-Origin: *</code> and <code>Access-Control-Allow-Headers: Authorization, Content-Type</code>.",
        body_style
    ))

    story.append(PageBreak())

    # =========================================================================
    # PAGE 11: FRONTEND ARCHITECTURE & REACT ISLANDS
    # =========================================================================
    story.append(Paragraph("13. Frontend Architecture & React Island Integration", h1_style))
    story.append(Paragraph(
        "HackMate utilizes a <b>Hybrid Multi-Page Application (MPA) with React 18 Islands</b> architecture. Here is why this design was selected over a monolithic Single Page Application (SPA).",
        body_style
    ))

    story.append(Paragraph("A. Why Multi-Page React Islands?", h2_style))
    story.append(Paragraph(
        "In a conventional Single Page Application (like Create React App), the browser downloads a massive 2MB JavaScript bundle before rendering a single pixel. If client-side routing crashes, the entire website breaks.",
        body_style
    ))
    story.append(Paragraph(
        "In HackMate's <b>React Island architecture</b>, standard pages (<code>index.html</code>, <code>login.html</code>, <code>register.html</code>) are pure, ultra-fast static HTML5 styled with Tailwind CSS. High-interactivity pages (<code>browse-teams.html</code> and <code>dashboard.html</code>) mount isolated <b>React 18 roots</b> (<code>src/main.jsx</code> and <code>src/dashboard.jsx</code>) directly into specific DOM containers (<code>&lt;div id=\"root\"&gt;&lt;/div&gt;</code>). This delivers instantaneous page loads with rich reactive components where needed.",
        body_style
    ))

    story.append(Paragraph("B. The Centralized REST API Client — frontend/src/api.js", h2_style))
    story.append(Paragraph(
        "All HTTP network communication in the frontend is abstracted through <code>frontend/src/api.js</code>:",
        body_style
    ))

    api_js_code = [
        "// frontend/src/api.js",
        "export const auth = {",
        "  getToken: () => localStorage.getItem('htf_token'),",
        "  getUser: () => JSON.parse(localStorage.getItem('htf_user') || 'null'),",
        "  setAuth: (token, user) => {",
        "    localStorage.setItem('htf_token', token);",
        "    localStorage.setItem('htf_user', JSON.stringify(user));",
        "  },",
        "  clearAuth: () => { localStorage.removeItem('htf_token'); localStorage.removeItem('htf_user'); }",
        "};",
        "export async function apiCall(endpoint, options = {}) {",
        "  const token = auth.getToken();",
        "  const headers = { 'Content-Type': 'application/json', ...(options.headers || {}) };",
        "  if (token) headers['Authorization'] = `Bearer ${token}`; // Automatic Token Injection",
        "  const res = await fetch(`${API_BASE}${endpoint}`, { ...options, headers });",
        "  const data = await res.json().catch(() => ({}));",
        "  if (!res.ok) throw new Error(data.error || `Request failed with status ${res.status}`);",
        "  return data;",
        "}"
    ]
    story.append(make_code_box(api_js_code, title="frontend/src/api.js — REST Client & Interceptor"))
    story.append(Spacer(1, 4))

    story.append(Paragraph("<b>Key Features of api.js:</b>", body_bold))
    story.append(Paragraph("• <b>Bearer Token Auto-Injection:</b> Checks <code>localStorage</code> for <code>htf_token</code> on every outgoing call and automatically attaches the <code>Authorization: Bearer &lt;token&gt;</code> header.", bullet_style))
    story.append(Paragraph("• <b>Global Error Interception:</b> If the backend returns a non-2xx HTTP status, <code>apiCall</code> parses the JSON error message and throws a JavaScript <code>Error</code> caught by React components.", bullet_style))
    story.append(Paragraph("• <b>Automatic Session Invalidation:</b> In <code>api.getMe()</code>, if a 401 Unauthorized is returned (e.g., token expired after 7 days), <code>auth.clearAuth()</code> runs automatically to clean stale session data.", bullet_style))

    story.append(PageBreak())

    # =========================================================================
    # PAGE 12: FRONTEND COMPONENT BREAKDOWN
    # =========================================================================
    story.append(Paragraph("14. Frontend Components & UI Engineering", h1_style))
    story.append(Paragraph(
        "Here is the breakdown of React components located inside <code>frontend/src/components/</code> and their state responsibilities:",
        body_style
    ))

    fe_comp_data = [
        [Paragraph("Component File", table_header), Paragraph("State & Hooks Used", table_header), Paragraph("UI Responsibility & Interaction Flow", table_header)],
        [
            Paragraph("<b>Navbar.jsx</b>", table_cell_bold),
            Paragraph("<code>useState(user)</code>,<br/><code>auth.isLoggedIn()</code>", table_cell),
            Paragraph("Global navigation bar. Detects session state. If logged out, displays 'Sign In' and 'Register' buttons. If logged in, displays active user name initials badge, 'Dashboard' link, and 'Logout' action.", table_cell)
        ],
        [
            Paragraph("<b>TeamCard.jsx</b>", table_cell_bold),
            Paragraph("Props: <code>team</code>, <code>currentUser</code>,<br/><code>onApply(team)</code>", table_cell),
            Paragraph("Card displaying hackathon name, squad title, description, required skill badges, capacity progress (e.g., '1/4 Members'), roster avatars, and dynamic 'Apply' button (disabled if team is full or user is owner).", table_cell)
        ],
        [
            Paragraph("<b>FilterBar.jsx</b>", table_cell_bold),
            Paragraph("<code>useState(search, skill, hackathon, status)</code>", table_cell),
            Paragraph("Interactive search bar and filter controls. Contains quick-select hackathon pills (SIH, ETHIndia), skill dropdowns, status toggles (All vs Open Only), and debounced search input.", table_cell)
        ],
        [
            Paragraph("<b>CreateTeamModal.jsx</b>", table_cell_bold),
            Paragraph("<code>useState(formData, loading, error)</code>", table_cell),
            Paragraph("Modal dialog for squad leaders. Captures hackathon name, title, description, team size limit, and skill tag pills. Validates inputs and triggers <code>api.createTeam()</code>.", table_cell)
        ],
        [
            Paragraph("<b>ApplyModal.jsx</b>", table_cell_bold),
            Paragraph("<code>useState(pitchMessage, submitting)</code>", table_cell),
            Paragraph("Application dialog allowing students to compose a personalized pitch explaining their qualifications. Submits payload to <code>api.sendRequest()</code>.", table_cell)
        ],
        [
            Paragraph("<b>dashboard.jsx</b>", table_cell_bold),
            Paragraph("<code>useState(activeTab, receivedReqs, sentReqs)</code>", table_cell),
            Paragraph("Dual-view dashboard. <b>Tab 1 (Received):</b> Squad leaders review incoming applicant pitches and click 'Accept' or 'Reject'. <b>Tab 2 (Sent):</b> Students track submitted pitches with real-time status badges.", table_cell)
        ]
    ]
    fe_comp_t = Table(fe_comp_data, colWidths=[100, 115, 300])
    fe_comp_t.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), C_PRIMARY),
        ('BOX', (0, 0), (-1, -1), 0.8, C_BORDER),
        ('INNERGRID', (0, 0), (-1, -1), 0.5, C_BORDER_LIGHT),
        ('TOPPADDING', (0, 0), (-1, -1), 4),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 4),
        ('LEFTPADDING', (0, 0), (-1, -1), 5),
        ('RIGHTPADDING', (0, 0), (-1, -1), 5),
    ]))
    story.append(fe_comp_t)
    story.append(Spacer(1, 6))

    story.append(Paragraph("Styling & Animation Implementation", h2_style))
    story.append(Paragraph(
        "• <b>Tailwind CSS (Utility-First Styling):</b> Provides responsive layout grids, glassmorphism backdrops (<code>backdrop-blur-md</code>), and custom color tokens (<code>orange-600</code>, <code>slate-900</code>) compiled via PostCSS.",
        bullet_style
    ))
    story.append(Paragraph(
        "• <b>GSAP (GreenSock Animation Platform):</b> Applied on landing page hero sections (<code>index.html</code>) for smooth entry transitions and floating badge micro-interactions.",
        bullet_style
    ))
    story.append(Paragraph(
        "• <b>Lucide Icons:</b> Lightweight SVG icon set embedded for crystal-clear visual iconography across all viewport resolutions.",
        bullet_style
    ))

    story.append(PageBreak())

    # =========================================================================
    # PAGE 13: END-TO-END EXECUTION TRACE #1 (AUTH)
    # =========================================================================
    story.append(Paragraph("15. End-to-End Execution Trace #1 — User Registration & Login", h1_style))
    story.append(Paragraph(
        "Professors love asking: <i>'Trace what happens when I click the Sign In button from the browser all the way to the database and back.'</i> Here is the complete step-by-step lifecycle:",
        body_style
    ))

    trace1_data = [
        [Paragraph("Step", table_header), Paragraph("Layer", table_header), Paragraph("Exact Operation & Code Execution Flow", table_header)],
        [
            Paragraph("<b>1</b>", table_cell_bold),
            Paragraph("Browser<br/>(Client UI)", table_cell),
            Paragraph("User enters <code>aarav@campus.edu</code> and <code>student123</code> on <code>login.html</code> and clicks 'Sign In'. Form submit listener intercepts event, prevents default page refresh, and invokes <code>api.login(email, password)</code>.", table_cell)
        ],
        [
            Paragraph("<b>2</b>", table_cell_bold),
            Paragraph("REST Client<br/>(frontend/api.js)", table_cell),
            Paragraph("<code>apiCall('/auth/login', { method: 'POST', body: JSON.stringify({ email, password }) })</code> issues an asynchronous HTTP <code>POST</code> request to <code>http://localhost:7070/api/auth/login</code> with JSON body.", table_cell)
        ],
        [
            Paragraph("<b>3</b>", table_cell_bold),
            Paragraph("Web Server<br/>(Javalin / Jetty)", table_cell),
            Paragraph("Embedded Jetty receives TCP connection on port 7070. Javalin router checks route table and invokes <code>AuthController::login(Context ctx)</code>.", table_cell)
        ],
        [
            Paragraph("<b>4</b>", table_cell_bold),
            Paragraph("Controller<br/>(AuthController.java)", table_cell),
            Paragraph("<code>AuthController.login()</code> parses JSON body with <code>Document.parse(ctx.body())</code>. Normalizes email to lowercase (<code>email.toLowerCase().trim()</code>).", table_cell)
        ],
        [
            Paragraph("<b>5</b>", table_cell_bold),
            Paragraph("Database<br/>(MongoDB / BSON)", table_cell),
            Paragraph("Executes query <code>DbConfig.getUsersCollection().find(Filters.eq(\"email\", \"aarav@campus.edu\")).first()</code>. Returns matching BSON document containing <code>passwordHash</code>.", table_cell)
        ],
        [
            Paragraph("<b>6</b>", table_cell_bold),
            Paragraph("Cryptography<br/>(jBCrypt)", table_cell),
            Paragraph("Calls <code>BCrypt.checkpw(\"student123\", storedHash)</code>. BCrypt extracts the salt from the stored hash, hashes the candidate password, and performs a constant-time comparison. Returns <code>true</code>.", table_cell)
        ],
        [
            Paragraph("<b>7</b>", table_cell_bold),
            Paragraph("Token Engine<br/>(JwtUtil.java)", table_cell),
            Paragraph("Calls <code>JwtUtil.generateToken(user)</code>. Encodes user <code>ObjectId</code> and email into claims, signs with HMAC256 using <code>JWT_SECRET</code>, and produces signed JWT string.", table_cell)
        ],
        [
            Paragraph("<b>8</b>", table_cell_bold),
            Paragraph("HTTP Response<br/>(Javalin)", table_cell),
            Paragraph("Returns HTTP <code>200 OK</code> with JSON body containing <code>token</code> and sanitized <code>user</code> profile map.", table_cell)
        ],
        [
            Paragraph("<b>9</b>", table_cell_bold),
            Paragraph("Client State<br/>(localStorage)", table_cell),
            Paragraph("Client receives response, calls <code>auth.setAuth(data.token, data.user)</code> to persist session in browser <code>localStorage</code>, and redirects user to <code>browse-teams.html</code>.", table_cell)
        ]
    ]
    t1_t = Table(trace1_data, colWidths=[30, 85, 400])
    t1_t.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), C_PRIMARY),
        ('BOX', (0, 0), (-1, -1), 0.8, C_BORDER),
        ('INNERGRID', (0, 0), (-1, -1), 0.5, C_BORDER_LIGHT),
        ('TOPPADDING', (0, 0), (-1, -1), 3.5),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 3.5),
        ('LEFTPADDING', (0, 0), (-1, -1), 5),
        ('RIGHTPADDING', (0, 0), (-1, -1), 5),
    ]))
    story.append(t1_t)

    story.append(PageBreak())

    # =========================================================================
    # PAGE 14: END-TO-END EXECUTION TRACE #2 (TEAM SEARCH)
    # =========================================================================
    story.append(Paragraph("16. End-to-End Execution Trace #2 — Dynamic Team Search & Filtering", h1_style))
    story.append(Paragraph(
        "Here is the detailed step-by-step execution trace when a student searches for teams matching a specific skill or keyword:",
        body_style
    ))

    trace2_data = [
        [Paragraph("Step", table_header), Paragraph("Layer", table_header), Paragraph("Exact Operation & Code Execution Flow", table_header)],
        [
            Paragraph("<b>1</b>", table_cell_bold),
            Paragraph("User Input<br/>(FilterBar.jsx)", table_cell),
            Paragraph("User types <code>'Python'</code> in the search input on <code>browse-teams.html</code>. React state <code>search</code> updates, triggering a debounced effect hook.", table_cell)
        ],
        [
            Paragraph("<b>2</b>", table_cell_bold),
            Paragraph("HTTP Query<br/>(api.getTeams)", table_cell),
            Paragraph("Constructs query string <code>/api/teams?search=Python</code>. Issues HTTP <code>GET</code> request via Fetch API to Javalin backend.", table_cell)
        ],
        [
            Paragraph("<b>3</b>", table_cell_bold),
            Paragraph("Filter Check<br/>(AuthFilter.java)", table_cell),
            Paragraph("<code>AuthFilter</code> inspects route path (<code>/api/teams</code>) and method (<code>GET</code>). Determines that browsing teams is a public read operation, allowing request to pass without token.", table_cell)
        ],
        [
            Paragraph("<b>4</b>", table_cell_bold),
            Paragraph("Controller<br/>(TeamController.java)", table_cell),
            Paragraph("<code>TeamController.listTeams(Context ctx)</code> extracts query param <code>ctx.queryParam(\"search\")</code>. Compiles case-insensitive regex <code>Pattern.compile(Pattern.quote(\"Python\"), Pattern.CASE_INSENSITIVE)</code>.", table_cell)
        ],
        [
            Paragraph("<b>5</b>", table_cell_bold),
            Paragraph("Compound BSON Query<br/>(MongoDB)", table_cell),
            Paragraph("Constructs BSON filter using <code>Filters.or()</code> matching <code>title</code>, <code>hackathonName</code>, or <code>description</code>. Combines with status filter using <code>Filters.and()</code>.", table_cell)
        ],
        [
            Paragraph("<b>6</b>", table_cell_bold),
            Paragraph("Query Execution<br/>(BSON Driver)", table_cell),
            Paragraph("MongoDB scans index/collection, retrieves matching documents, and sorts results by <code>createdAt DESC</code> (newest squads first).", table_cell)
        ],
        [
            Paragraph("<b>7</b>", table_cell_bold),
            Paragraph("Serialization<br/>(TeamController)", table_cell),
            Paragraph("Iterates over documents, converting BSON <code>ObjectId</code> to hex strings and formatting nested member subdocuments via <code>serializeTeam()</code>.", table_cell)
        ],
        [
            Paragraph("<b>8</b>", table_cell_bold),
            Paragraph("UI Re-render<br/>(React 18 Virtual DOM)", table_cell),
            Paragraph("Client receives JSON array. React calls <code>setTeams(data)</code>, compares Virtual DOM diff, and smoothly re-renders the grid with matching <code>&lt;TeamCard&gt;</code> components.", table_cell)
        ]
    ]
    t2_t = Table(trace2_data, colWidths=[30, 90, 395])
    t2_t.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), C_PRIMARY),
        ('BOX', (0, 0), (-1, -1), 0.8, C_BORDER),
        ('INNERGRID', (0, 0), (-1, -1), 0.5, C_BORDER_LIGHT),
        ('TOPPADDING', (0, 0), (-1, -1), 4),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 4),
        ('LEFTPADDING', (0, 0), (-1, -1), 5),
        ('RIGHTPADDING', (0, 0), (-1, -1), 5),
    ]))
    story.append(t2_t)

    story.append(PageBreak())

    # =========================================================================
    # PAGE 15: END-TO-END EXECUTION TRACE #3 (PITCH & ACCEPTANCE)
    # =========================================================================
    story.append(Paragraph("17. End-to-End Execution Trace #3 — Pitch Application & Roster Lock", h1_style))
    story.append(Paragraph(
        "Here is the trace of a student applying to a squad, the squad leader accepting the pitch, and the system automatically locking the roster:",
        body_style
    ))

    trace3_data = [
        [Paragraph("Step", table_header), Paragraph("Layer", table_header), Paragraph("Exact Operation & Code Execution Flow", table_header)],
        [
            Paragraph("<b>1</b>", table_cell_bold),
            Paragraph("Pitch Modal<br/>(ApplyModal.jsx)", table_cell),
            Paragraph("Applicant clicks 'Apply' on AgriPulse card, enters pitch: <i>'3rd year CSE with PyTorch & OpenCV experience'</i>, and clicks 'Submit Pitch'.", table_cell)
        ],
        [
            Paragraph("<b>2</b>", table_cell_bold),
            Paragraph("Protected API Call<br/>(api.sendRequest)", table_cell),
            Paragraph("Sends <code>POST /api/requests</code> with body <code>{ teamId, message }</code> and header <code>Authorization: Bearer &lt;JWT&gt;</code>.", table_cell)
        ],
        [
            Paragraph("<b>3</b>", table_cell_bold),
            Paragraph("Auth Middleware<br/>(AuthFilter.java)", table_cell),
            Paragraph("Validates JWT token, extracts applicant's <code>userId</code>, and injects into <code>ctx.attribute(\"userId\")</code>.", table_cell)
        ],
        [
            Paragraph("<b>4</b>", table_cell_bold),
            Paragraph("Validation & Insert<br/>(RequestController)", table_cell),
            Paragraph("Validates applicant is not owner, team is <code>OPEN</code>, and no duplicate active request exists. Fetches applicant profile and inserts new document into <code>join_requests</code> collection with status <code>PENDING</code>.", table_cell)
        ],
        [
            Paragraph("<b>5</b>", table_cell_bold),
            Paragraph("Leader Review<br/>(dashboard.jsx)", table_cell),
            Paragraph("Squad leader logs in and opens Dashboard. <code>GET /api/requests/received</code> fetches all pending applicant pitches for their teams.", table_cell)
        ],
        [
            Paragraph("<b>6</b>", table_cell_bold),
            Paragraph("Approval Action<br/>(Leader Click)", table_cell),
            Paragraph("Leader clicks 'Accept Applicant'. Calls <code>PUT /api/requests/{id}</code> with body <code>{ status: 'ACCEPTED' }</code>.", table_cell)
        ],
        [
            Paragraph("<b>7</b>", table_cell_bold),
            Paragraph("Atomic Roster Push<br/>(RequestController)", table_cell),
            Paragraph("Controller appends applicant <code>{ userId, name, role: 'Member' }</code> to <code>teams.currentMembers</code> array.", table_cell)
        ],
        [
            Paragraph("<b>8</b>", table_cell_bold),
            Paragraph("Capacity Lock<br/>(State Machine)", table_cell),
            Paragraph("Checks <code>currentMembers.size() &gt;= teamSize</code>. If team reaches capacity limit (e.g., 4/4), team status is updated to <code>FULL</code>.", table_cell)
        ],
        [
            Paragraph("<b>9</b>", table_cell_bold),
            Paragraph("Disk Backup<br/>(DbConfig.save)", table_cell),
            Paragraph("Updates request status to <code>ACCEPTED</code> and triggers <code>DbConfig.saveCollection()</code> to persist changes to disk.", table_cell)
        ]
    ]
    t3_t = Table(trace3_data, colWidths=[30, 95, 390])
    t3_t.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), C_PRIMARY),
        ('BOX', (0, 0), (-1, -1), 0.8, C_BORDER),
        ('INNERGRID', (0, 0), (-1, -1), 0.5, C_BORDER_LIGHT),
        ('TOPPADDING', (0, 0), (-1, -1), 4),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 4),
        ('LEFTPADDING', (0, 0), (-1, -1), 5),
        ('RIGHTPADDING', (0, 0), (-1, -1), 5),
    ]))
    story.append(t3_t)

    story.append(PageBreak())

    # =========================================================================
    # PAGE 16: TOP 25 VIVA COUNTER-QUESTIONS (PART 1: BACKEND & JAVA)
    # =========================================================================
    story.append(Paragraph("18. Top 25 Toughest Viva Questions & Winning Answers (Part 1)", h1_style))
    story.append(Paragraph(
        "Study these exact technical answers to defend the backend and Java implementation with complete authority:",
        body_style
    ))

    qas_part1 = [
        ("Q1: Why did you choose Javalin instead of Spring Boot or Express.js?",
         "<b>Winning Answer:</b> Spring Boot has heavy reflection overhead, slow 15-second cold starts, and excessive annotation magic that obscures execution flow. Express.js lacks compile-time type safety. Javalin offers the best of both worlds: zero-boilerplate explicit routing in modern Java 17, sub-200ms cold boot times, embedded Jetty server, and complete transparency suitable for high-performance microservices."),
        
        ("Q2: What is the difference between JDK and JRE, and which one does Maven require?",
         "<b>Winning Answer:</b> The JRE (Java Runtime Environment) only executes pre-compiled bytecode. The JDK (Java Development Kit) includes the compiler (<code>javac</code>) and development tools. Maven strictly requires a JDK (specifically JDK 17 configured via <code>JAVA_HOME</code>) because Maven compiles raw <code>.java</code> source files into <code>.class</code> bytecode during <code>mvn compile</code>."),

        ("Q3: How does the server handle concurrency if multiple students access the API simultaneously?",
         "<b>Winning Answer:</b> Javalin runs on Embedded Jetty, which maintains a managed thread pool (defaulting to 200 worker threads). Each incoming HTTP request is assigned a dedicated thread from the pool. Database operations use thread-safe static singletons and atomic MongoDB operators (<code>$push</code>, <code>$set</code>) to prevent race conditions during simultaneous reads/writes."),

        ("Q4: What is the purpose of AuthFilter and how does it prevent code duplication?",
         "<b>Winning Answer:</b> <code>AuthFilter</code> is an HTTP interceptor executed before request handlers via <code>app.before('/api/*', AuthFilter::filter)</code>. Instead of writing JWT validation boilerplate inside every controller method, <code>AuthFilter</code> centralizes token verification, rejects invalid requests with 401 Unauthorized, and injects the authenticated <code>userId</code> into request context attributes."),

        ("Q5: What happens if MongoDB is not installed on the examiner's machine?",
         "<b>Winning Answer:</b> <code>DbConfig.java</code> has a 3-stage connection waterfall. If external MongoDB Atlas and local <code>localhost:27017</code> are unavailable, it starts an in-memory embedded MongoDB wire-protocol server (<code>de.bwaldvogel.mongo.MongoServer</code>) and restores data from disk JSON snapshots. The app is 100% portable with zero setup."),

        ("Q6: How does the backend prevent NoSQL Injection in search queries?",
         "<b>Winning Answer:</b> We wrap all user-supplied search strings in <code>Pattern.quote(input)</code> before compiling BSON regular expressions. This treats user input strictly as literal text, neutralizing special regex metacharacters and preventing ReDoS (Regular Expression Denial of Service) or unauthorized operator injection."),

        ("Q7: What is the purpose of seedInitialDataIfEmpty()?",
         "<b>Winning Answer:</b> It ensures that upon first boot, the platform is pre-populated with verified campus accounts (Aarav, Ananya, Kabir) and active hackathon squads (SIH 2026, ETHIndia 2026) with BCrypt-hashed passwords. It is idempotent: if records exist, it returns immediately without duplicating data."),

        ("Q8: Why did you use Document.parse(ctx.body()) instead of Java DTO classes?",
         "<b>Winning Answer:</b> Javalin integrates with MongoDB BSON <code>Document</code> natively. Parsing directly into BSON documents provides dynamic flexibility when handling partial JSON updates (e.g., updating only team size or description in <code>PUT /api/teams/:id</code>) without maintaining dozens of redundant DTO classes.")
    ]

    for q, a in qas_part1:
        story.append(Paragraph(q, qa_q))
        story.append(Paragraph(a, qa_a))

    story.append(PageBreak())

    # =========================================================================
    # PAGE 17: TOP 25 VIVA COUNTER-QUESTIONS (PART 2: DATABASE & SECURITY)
    # =========================================================================
    story.append(Paragraph("19. Top 25 Toughest Viva Questions & Winning Answers (Part 2)", h1_style))
    story.append(Paragraph(
        "Master these database, cryptography, and security defense responses:",
        body_style
    ))

    qas_part2 = [
        ("Q9: Why MongoDB (NoSQL) instead of MySQL (RDBMS) for HackMate?",
         "<b>Winning Answer:</b> Hackathon squads require dynamic, schemaless properties (variable skill tags, dynamic embedded member rosters with varying roles). In SQL, this requires 4-table joins across <code>users</code>, <code>teams</code>, <code>team_members</code>, and <code>skills</code>. MongoDB document model embeds members directly inside the team document, allowing single-query reads and atomic updates."),

        ("Q10: Why did you choose BCrypt over SHA-256 for password storage?",
         "<b>Winning Answer:</b> SHA-256 is a general-purpose cryptographic hash designed to be fast. Modern GPUs can calculate billions of SHA-256 hashes per second, making them vulnerable to brute-force dictionary attacks. BCrypt is an intentionally slow adaptive hashing algorithm based on Blowfish with an exponential cost factor (work factor 10 = 1024 rounds) and automatic random salting, making GPU cracking unfeasible."),

        ("Q11: What is a Salt in cryptography and why is it necessary?",
         "<b>Winning Answer:</b> A salt is a random 16-byte cryptographic sequence added to the plaintext password before hashing. It ensures that if two users choose the same password (e.g., 'student123'), their resulting hashes are completely different. This completely defeats precomputed Rainbow Table attacks."),

        ("Q12: Is JWT token verification vulnerable if the database goes down?",
         "<b>Winning Answer:</b> No. JWT verification is completely stateless. The server verifies the token by calculating the HMAC256 signature using the server's private secret key and comparing it against the signature segment in the token header. No database connection or query is needed to verify token validity."),

        ("Q13: How do you prevent an attacker from modifying their userId in the JWT payload?",
         "<b>Winning Answer:</b> If an attacker base64-decodes the payload, changes <code>userId</code> to another student's ID, and re-encodes it, the cryptographic signature (calculated over <code>header.payload</code>) will no longer match. The server will reject the token with 401 Unauthorized during <code>verifier.verify(token)</code>."),

        ("Q14: How does HackMate handle race conditions when two students apply for the last spot simultaneously?",
         "<b>Winning Answer:</b> In <code>RequestController.updateRequestStatus()</code>, the squad leader manually reviews and accepts applicants sequentially. When an applicant is accepted, the server verifies current roster size against <code>teamSize</code> in an atomic update operation, shifting status to <code>FULL</code> and rejecting any subsequent pending approvals."),

        ("Q15: Why are applicant skills and names duplicated inside the join_requests collection?",
         "<b>Winning Answer:</b> This is an intentional NoSQL denormalization strategy. When a squad leader opens their dashboard, the backend queries <code>join_requests</code> in a single indexed read and immediately renders applicant names, branches, and skills without performing N+1 queries back to the <code>users</code> collection."),

        ("Q16: What is the purpose of database indexes in your DbConfig class?",
         "<b>Winning Answer:</b> We created a unique index on <code>users.email</code> to enforce email uniqueness at the storage engine level, and single-field ascending indexes on <code>teams.status</code>, <code>join_requests.teamId</code>, and <code>join_requests.userId</code> to ensure $O(\\log N)$ lookup performance during high-frequency searches.")
    ]

    for q, a in qas_part2:
        story.append(Paragraph(q, qa_q))
        story.append(Paragraph(a, qa_a))

    story.append(PageBreak())

    # =========================================================================
    # PAGE 18: TOP 25 VIVA COUNTER-QUESTIONS (PART 3: FRONTEND & ARCHITECTURE)
    # =========================================================================
    story.append(Paragraph("20. Top 25 Toughest Viva Questions & Winning Answers (Part 3)", h1_style))
    story.append(Paragraph(
        "Master these frontend, architecture, and system defense responses:",
        body_style
    ))

    qas_part3 = [
        ("Q17: Why did you use React Islands instead of building a full React Single Page Application (SPA)?",
         "<b>Winning Answer:</b> React Islands provide faster First Contentful Paint (FCP) because static marketing pages (landing, login, register) load immediately as lightweight HTML5/CSS without waiting for large JS bundles to download and parse. React is only mounted where complex stateful UI is required (team browsing, dashboard management)."),

        ("Q18: Where is the JWT token stored on the client and what are its security implications?",
         "<b>Winning Answer:</b> The token is stored in browser <code>localStorage</code> under <code>htf_token</code>. This allows seamless session persistence across page reloads. In a high-security banking production system, we would store it in an <code>HttpOnly</code>, <code>SameSite=Strict</code> secure cookie to protect against Cross-Site Scripting (XSS). For this campus platform, <code>localStorage</code> provides clean client-side token injection."),

        ("Q19: How does the frontend handle token expiration after 7 days?",
         "<b>Winning Answer:</b> In <code>frontend/src/api.js</code>, when <code>api.getMe()</code> receives a 401 Unauthorized response from the backend, <code>auth.clearAuth()</code> is triggered automatically, wiping the expired token and user object from <code>localStorage</code> and cleanly updating the navigation bar."),

        ("Q20: What happens if a team member tries to edit or delete a squad created by someone else?",
         "<b>Winning Answer:</b> In <code>TeamController.updateTeam()</code> and <code>deleteTeam()</code>, the backend extracts the authenticated <code>userId</code> from <code>ctx.attribute(\"userId\")</code> and compares it against <code>teamDoc.getString(\"createdBy\")</code>. If they do not match, the server immediately aborts the operation and returns HTTP 403 Forbidden."),

        ("Q21: What happens to join requests when a team is deleted by its creator?",
         "<b>Winning Answer:</b> In <code>TeamController.deleteTeam()</code>, we execute a cascade cleanup: <code>DbConfig.getJoinRequestsCollection().deleteMany(Filters.eq(\"teamId\", id))</code>. This prevents orphaned request records in the database."),

        ("Q22: How does the search bar implement debouncing in React?",
         "<b>Winning Answer:</b> In <code>FilterBar.jsx</code>, user keystrokes update local state immediately, while the API fetch call is delayed by 300ms using a <code>setTimeout</code> hook. If the user continues typing within 300ms, the previous timer is cancelled. This prevents sending an unnecessary HTTP request for every single keystroke."),

        ("Q23: How would you scale HackMate to handle 50,000 students across 20 universities?",
         "<b>Winning Answer:</b> 1) Deploy Javalin stateless backend instances behind an NGINX load balancer. 2) Migrate MongoDB to a sharded MongoDB Atlas replica set with compound indexes on <code>universityId + hackathonName</code>. 3) Cache popular hackathon team listings in a Redis in-memory cache. 4) Move static frontend assets to a Cloudflare CDN edge network."),

        ("Q24: What are the main limitations of the current implementation and what would you add next?",
         "<b>Winning Answer:</b> Current limitations: 1) Email verification is not enforced via SMTP OTP. 2) Real-time notifications rely on dashboard polling rather than WebSockets. In the next sprint, we will add WebSocket-based live chat between accepted squad members and automated AI skill matching based on GitHub profile analysis.")
    ]

    for q, a in qas_part3:
        story.append(Paragraph(q, qa_q))
        story.append(Paragraph(a, qa_a))

    story.append(PageBreak())

    # =========================================================================
    # PAGE 19: VIVA DAY CHEAT SHEET, RUN GUIDE & EMERGENCY TROUBLESHOOTING
    # =========================================================================
    story.append(Paragraph("21. Viva Day Startup Cheatsheet & Emergency Guide", h1_style))
    story.append(Paragraph(
        "Keep this page open during your presentation for instant startup commands, demo credentials, and emergency port conflict resolution.",
        body_style
    ))

    story.append(Paragraph("A. Master Startup Commands (PowerShell)", h2_style))
    start_cmds_data = [
        [Paragraph("Process", table_header), Paragraph("Exact PowerShell Command", table_header), Paragraph("Expected Terminal Output", table_header)],
        [
            Paragraph("<b>Backend</b><br/>(Port 7070)", table_cell_bold),
            Paragraph("<code>powershell -ExecutionPolicy Bypass -File .\\start-backend.ps1</code>", table_cell),
            Paragraph("<code>[OK] Using Java from: ...\\jdk17<br/>Hackathon Team Finder backend running at http://localhost:7070</code>", table_cell)
        ],
        [
            Paragraph("<b>Frontend</b><br/>(Port 5173)", table_cell_bold),
            Paragraph("<code>powershell -ExecutionPolicy Bypass -File .\\start-frontend.ps1</code><br/><i>(or: <code>cd frontend; npm run dev</code>)</i>", table_cell),
            Paragraph("<code>VITE v5.x.x ready in 300 ms<br/>➜ Local: http://localhost:5173/</code>", table_cell)
        ]
    ]
    start_t = Table(start_cmds_data, colWidths=[80, 220, 215])
    start_t.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), C_PRIMARY),
        ('BOX', (0, 0), (-1, -1), 0.8, C_BORDER),
        ('INNERGRID', (0, 0), (-1, -1), 0.5, C_BORDER_LIGHT),
        ('TOPPADDING', (0, 0), (-1, -1), 4),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 4),
        ('LEFTPADDING', (0, 0), (-1, -1), 5),
        ('RIGHTPADDING', (0, 0), (-1, -1), 5),
    ]))
    story.append(start_t)
    story.append(Spacer(1, 5))

    story.append(Paragraph("B. Default Seed Accounts for Live Demonstration", h2_style))
    seed_data = [
        [Paragraph("Student Name", table_header), Paragraph("Login Email", table_header), Paragraph("Password", table_header), Paragraph("Branch & Role in Seed Squad", table_header)],
        [Paragraph("<b>Aarav Mehta</b>", table_cell_bold), Paragraph("<code>aarav.mehta@campus.edu</code>", table_cell), Paragraph("<code>student123</code>", table_cell), Paragraph("CSE 3rd Year • Leader of AgriPulse (SIH 2026)", table_cell)],
        [Paragraph("<b>Ananya Deshmukh</b>", table_cell_bold), Paragraph("<code>ananya.d@campus.edu</code>", table_cell), Paragraph("<code>student123</code>", table_cell), Paragraph("IT 4th Year • Leader of ProofOfSkill (ETHIndia 2026)", table_cell)],
        [Paragraph("<b>Kabir Roy</b>", table_cell_bold), Paragraph("<code>kabir.roy@campus.edu</code>", table_cell), Paragraph("<code>student123</code>", table_cell), Paragraph("EXTC 2nd Year • Leader of PulseShuttle (CodeFest)", table_cell)]
    ]
    seed_t = Table(seed_data, colWidths=[105, 160, 80, 170])
    seed_t.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), C_PRIMARY),
        ('BOX', (0, 0), (-1, -1), 0.8, C_BORDER),
        ('INNERGRID', (0, 0), (-1, -1), 0.5, C_BORDER_LIGHT),
        ('TOPPADDING', (0, 0), (-1, -1), 3.5),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 3.5),
        ('LEFTPADDING', (0, 0), (-1, -1), 5),
        ('RIGHTPADDING', (0, 0), (-1, -1), 5),
    ]))
    story.append(seed_t)
    story.append(Spacer(1, 5))

    story.append(Paragraph("C. Emergency Troubleshooting Guide", h2_style))
    story.append(Paragraph("• <b>Port 7070 already in use error:</b> Run <code>netstat -ano | findstr :7070</code> to find the PID, then kill it using <code>taskkill /PID &lt;PID&gt; /F</code>.", bullet_style))
    story.append(Paragraph("• <b>Port 5173 occupied:</b> Vite will automatically fall back to <code>http://localhost:5174</code>. You can access the app there without issues.", bullet_style))
    story.append(Paragraph("• <b>Java compiler error:</b> Verify <code>$env:JAVA_HOME</code> points to JDK 17 (not JRE). <code>start-backend.ps1</code> handles this automatically.", bullet_style))

    story.append(Spacer(1, 4))
    story.append(make_card([
        Paragraph("<b>60-Second Opening Pitch for the Professor:</b>", callout_bold),
        Paragraph("<i>'Good morning, Professors. We are presenting HackMate, a full-stack campus hackathon discovery platform. Conventional campus team formation is plagued by skill mismatch, ghosted invites, and chaotic WhatsApp groups. HackMate provides a structured platform built with a high-performance Java 17 Javalin backend, MongoDB BSON persistence with automated fallback, BCrypt salting, stateless JWT authentication, and a responsive React 18 island frontend. It features atomic roster capacity locking and multi-parameter skill search. Let us demonstrate the live workflow.'</i>", callout_text)
    ], bg_color=C_BG_CARD, border_color=C_BORDER))

    story.append(PageBreak())

    # =========================================================================
    # PAGE 20: CODE FILE INDEX & SYMBOL MAP
    # =========================================================================
    story.append(Paragraph("22. Master Codebase Index & Symbol Reference", h1_style))
    story.append(Paragraph(
        "Use this lookup table during code inspection to navigate directly to any class, method, or endpoint requested by the examiner:",
        body_style
    ))

    code_index_data = [
        [Paragraph("File Path", table_header), Paragraph("Key Classes / Functions", table_header), Paragraph("Primary Technical Responsibility", table_header)],
        [
            Paragraph("<code>backend/pom.xml</code>", table_cell_bold),
            Paragraph("Maven Dependencies", table_cell),
            Paragraph("Declares Java 17, Javalin 5.6.3, MongoDB sync driver, jBCrypt, Auth0 JWT, and Shade fat-jar plugin.", table_cell)
        ],
        [
            Paragraph("<code>backend/.../Main.java</code>", table_cell_bold),
            Paragraph("<code>main()</code>, <code>seedInitialDataIfEmpty()</code>", table_cell),
            Paragraph("Initializes database, configures CORS, binds all REST routes, and boots embedded Jetty server on port 7070.", table_cell)
        ],
        [
            Paragraph("<code>backend/.../config/DbConfig.java</code>", table_cell_bold),
            Paragraph("<code>init()</code>, <code>getDatabase()</code>, <code>saveCollection()</code>", table_cell),
            Paragraph("Manages MongoDB connections, in-memory fallback wire server, indexes, and disk JSON persistence.", table_cell)
        ],
        [
            Paragraph("<code>backend/.../middleware/AuthFilter.java</code>", table_cell_bold),
            Paragraph("<code>filter(Context ctx)</code>", table_cell),
            Paragraph("Intercepts protected HTTP endpoints, verifies JWT tokens, and attaches authenticated userId to context attributes.", table_cell)
        ],
        [
            Paragraph("<code>backend/.../util/JwtUtil.java</code>", table_cell_bold),
            Paragraph("<code>generateToken()</code>, <code>verifyToken()</code>", table_cell),
            Paragraph("Constructs and cryptographically verifies HMAC256 signed JSON Web Tokens with 7-day expiration.", table_cell)
        ],
        [
            Paragraph("<code>backend/.../controllers/AuthController.java</code>", table_cell_bold),
            Paragraph("<code>register()</code>, <code>login()</code>", table_cell),
            Paragraph("Handles email deduplication, 10-round BCrypt password hashing, credential verification, and JWT issuance.", table_cell)
        ],
        [
            Paragraph("<code>backend/.../controllers/TeamController.java</code>", table_cell_bold),
            Paragraph("<code>listTeams()</code>, <code>createTeam()</code>, <code>deleteTeam()</code>", table_cell),
            Paragraph("Implements dynamic BSON regex search across skills/hackathons, ownership checks, and cascade deletions.", table_cell)
        ],
        [
            Paragraph("<code>backend/.../controllers/RequestController.java</code>", table_cell_bold),
            Paragraph("<code>sendRequest()</code>, <code>updateRequestStatus()</code>", table_cell),
            Paragraph("Executes 4-guard pitch validation, approval state transitions, and atomic squad capacity locking (OPEN &rarr; FULL).", table_cell)
        ],
        [
            Paragraph("<code>backend/.../controllers/UserController.java</code>", table_cell_bold),
            Paragraph("<code>getCurrentUser()</code>", table_cell),
            Paragraph("Returns authenticated user profile (<code>/api/users/me</code>) excluding sensitive password hashes.", table_cell)
        ],
        [
            Paragraph("<code>frontend/src/api.js</code>", table_cell_bold),
            Paragraph("<code>auth</code>, <code>apiCall()</code>, <code>api.*</code>", table_cell),
            Paragraph("Centralized REST client with automatic Bearer token injection, session storage, and 401 error handling.", table_cell)
        ],
        [
            Paragraph("<code>frontend/src/main.jsx</code>", table_cell_bold),
            Paragraph("<code>App</code>, Team Grid", table_cell),
            Paragraph("React 18 root for team discovery, reactive filter synchronization, and pitch modal triggers.", table_cell)
        ],
        [
            Paragraph("<code>frontend/src/dashboard.jsx</code>", table_cell_bold),
            Paragraph("<code>DashboardApp</code>", table_cell),
            Paragraph("React 18 root for reviewing incoming applicant pitches (Accept/Reject) and tracking submitted applications.", table_cell)
        ]
    ]
    idx_t = Table(code_index_data, colWidths=[140, 150, 225])
    idx_t.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), C_PRIMARY),
        ('BOX', (0, 0), (-1, -1), 0.8, C_BORDER),
        ('INNERGRID', (0, 0), (-1, -1), 0.5, C_BORDER_LIGHT),
        ('TOPPADDING', (0, 0), (-1, -1), 3),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 3),
        ('LEFTPADDING', (0, 0), (-1, -1), 5),
        ('RIGHTPADDING', (0, 0), (-1, -1), 5),
    ]))
    story.append(idx_t)
    story.append(Spacer(1, 8))

    story.append(make_card([
        Paragraph("<b>Final Viva Defense Reminder:</b>", callout_bold),
        Paragraph("You built an authentic, high-performance full-stack platform. Walk into the examination with complete confidence. Explain the architecture cleanly, demonstrate the running application, reference the exact code files when asked, and you will score top marks. Best of luck for your 9:00 AM presentation!", callout_text)
    ], bg_color=C_BG_ALT, border_color=C_BORDER))

    # Build document
    doc.build(story, canvasmaker=NumberedCanvas)
    print(f"Successfully generated {output_filename}")

    # Verify page count
    reader = pypdf.PdfReader(output_filename)
    page_count = len(reader.pages)
    print(f"Total Page Count: {page_count} pages")

if __name__ == "__main__":
    build_pdf()

# Campus Hackathon Team Finder
*Student Collaboration Hub*

A lightweight campus platform where students can post hackathon squad requirements, discover teammates by technical skill or competition, and manage join applications with a live team roster.

---

## 1. Project Concept & Core Loop

- **Post a Team Requirement**: Specify hackathon name (e.g. Smart India Hackathon, ETHIndia), target squad size, project vision, and needed competencies.
- **Browse & Filter**: Filter teams dynamically by technical skills (React, Python, Solidity, Java, etc.) or hackathon event.
- **Pitch & Apply**: Send an application pitch detailing your background.
- **Manual Leader Review**: Team creator reviews applicant pitches from their dashboard and manually accepts or declines. Once capacity is reached, the team status automatically locks to `FULL`.

---

## 2. Tech Stack & Architectural Decisions

Built to keep code concise, fast, and maintainable without bloated enterprise frameworks:

| Layer | Choice | Why |
| :--- | :--- | :--- |
| **Backend Framework** | **Javalin 5.6** | Thin wrapper over Jetty (~50-line REST endpoints, 0ms reflection bloat). |
| **Authentication** | **Plain Java: BCrypt + Auth0 JWT** | Pure Java security with no Spring Security boilerplate. 7-day HMAC256 tokens. |
| **Database** | **MongoDB (Sync Driver 4.11)** | Document model with embedded wire-protocol memory fallback and JSON disk persistence. |
| **Frontend Architecture** | **Multi-Page App (MPA) + React Islands** | Plain HTML+Tailwind for Landing/Login/Register, mounting React only on dynamic pages (`browse-teams.html` and `dashboard.html`). Cuts React overhead by 70%. |
| **Build Tools** | **Apache Maven 3.9 + Vite 5** | Standard, minimal configuration. |

---

## 3. Aesthetic & Design System

- **Canvas / Background**: Warm off-white / parchment (`#FAF8F5`, `#F3EFEA`).
- **Surfaces**: Crisp ivory card surfaces (`#FFFFFF`) with subtle warm hairline borders (`#E6E0D6`) and tactile paper shadows.
- **Typography**: Bold geometric headings (**Outfit**) paired with clean body typography (**Plus Jakarta Sans**) and monospace technical tags (**JetBrains Mono**).
- **Accents**: Terracotta / Burnt Sienna (`#C2410C`, hover `#9A3412`) and Warm Ochre / Amber badges (`#B45309`).
- **Status Pills**: Earthy sage olive (`#3F4E22`) for Open teams; warm clay for Full teams.

---

## 4. Folder Structure

```
javamini/
├── backend/
│   ├── pom.xml
│   └── src/main/java/com/vexoria/
│       ├── Main.java                          # Javalin setup, CORS, routes & demo seeder
│       ├── config/DbConfig.java               # MongoDB driver + embedded wire fallback
│       ├── models/
│       │   ├── User.java                      # Student account model
│       │   ├── Team.java                      # Team & roster model
│       │   └── JoinRequest.java               # Application model
│       ├── controllers/
│       │   ├── AuthController.java            # Register, Login (BCrypt + JWT)
│       │   ├── UserController.java            # Current user profile (/api/users/me)
│       │   ├── TeamController.java            # Team CRUD & multi-field filtering
│       │   └── RequestController.java         # Join requests & roster updating
│       ├── util/JwtUtil.java                  # HMAC256 token signer & verifier
│       └── middleware/AuthFilter.java         # Javalin before() filter for Bearer token
│
├── frontend/
│   ├── package.json
│   ├── vite.config.js                         # Multi-page Vite configuration
│   ├── tailwind.config.js                     # Custom terracotta & warm paper theme
│   ├── index.html                             # Landing page (HTML + Tailwind)
│   ├── login.html                             # Student Sign In
│   ├── register.html                          # Student Registration
│   ├── browse-teams.html                      # Mounts TeamListingApp React island
│   ├── dashboard.html                         # Mounts DashboardApp React island
│   └── src/
│       ├── api.js                             # Fetch wrapper with Bearer token
│       ├── style.css                          # Custom typography & card elevation
│       ├── main.jsx                           # Browse Teams React entry
│       ├── dashboard.jsx                      # Student Dashboard React entry
│       └── components/
│           ├── Navbar.jsx                     # Global campus navigation
│           ├── FilterBar.jsx                  # Skill pills & search controls
│           ├── TeamCard.jsx                   # Team metadata & roster view
│           ├── CreateTeamModal.jsx            # Post team modal dialog
│           └── ApplyModal.jsx                 # Application pitch dialog
│
├── start-backend.ps1                          # Backend launcher script
└── start-frontend.ps1                         # Frontend launcher script
```

---

## 5. Quick Start Instructions

### Prerequisites
- **Java 17+** & **Maven 3.8+**
- **Node.js 18+** & **npm**
- **MongoDB** *(Optional — the backend includes a built-in embedded wire-protocol server that activates automatically if local MongoDB is not running!)*

### Running the Backend
```powershell
cd backend
mvn clean compile exec:java
```
*The backend starts at `http://localhost:7070`.*

### Running the Frontend
```powershell
cd frontend
npm install
npm run dev
```
*The frontend starts at `http://localhost:5173`.*

---

## 6. Pre-seeded Demo Accounts

For instant testing and evaluation, the backend seeds realistic campus student accounts and hackathons on first startup:

| Name | Campus Email | Password | Role / Focus |
| :--- | :--- | :--- | :--- |
| **Aarav Mehta** | `aarav.mehta@campus.edu` | `student123` | Team Lead — SIH 2026 (AgriPulse AI) |
| **Ananya Deshmukh** | `ananya.d@campus.edu` | `student123` | Web3 Dev — ETHIndia 2026 (ProofOfSkill) |
| **Kabir Roy** | `kabir.roy@campus.edu` | `student123` | Backend Architect — Campus CodeFest 2026 |

---

## 7. REST API Endpoints Reference

| Method | Endpoint | Auth Required | Purpose |
| :--- | :--- | :---: | :--- |
| `POST` | `/api/auth/register` | No | Creates student account, hashes password, returns JWT |
| `POST` | `/api/auth/login` | No | Validates credentials, returns JWT |
| `GET` | `/api/users/me` | **Yes** | Returns authenticated student profile |
| `GET` | `/api/teams` | No | Lists teams with `?skill=`, `?hackathon=`, `?status=` |
| `GET` | `/api/teams/:id` | No | Team details & roster |
| `POST` | `/api/teams` | **Yes** | Post new team (creator automatically added as leader) |
| `PUT` | `/api/teams/:id` | **Yes** (Owner) | Edit team metadata or close recruitment |
| `DELETE` | `/api/teams/:id` | **Yes** (Owner) | Delete team and associated requests |
| `POST` | `/api/requests` | **Yes** | Send application pitch to join a team |
| `GET` | `/api/requests/received` | **Yes** | Applications sent to teams created by user |
| `GET` | `/api/requests/sent` | **Yes** | Applications submitted by user |
| `PUT` | `/api/requests/:id` | **Yes** (Owner) | Accept or decline request (adds member to roster) |

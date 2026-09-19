package com.vexoria;

import com.vexoria.config.DbConfig;
import com.vexoria.controllers.AuthController;
import com.vexoria.controllers.RequestController;
import com.vexoria.controllers.TeamController;
import com.vexoria.controllers.UserController;
import com.vexoria.middleware.AuthFilter;
import io.javalin.Javalin;
import io.javalin.plugin.bundled.CorsPluginConfig;
import org.bson.Document;
import org.bson.types.ObjectId;
import org.mindrot.jbcrypt.BCrypt;
import org.slf4j.Logger;
import org.slf4j.LoggerFactory;

import java.util.*;

public class Main {
    private static final Logger log = LoggerFactory.getLogger(Main.class);

    public static void main(String[] args) {
        int port = 7070;
        String portEnv = System.getenv("PORT");
        if (portEnv != null) {
            try { port = Integer.parseInt(portEnv); } catch (NumberFormatException ignored) {}
        }

        log.info("Initializing database connection...");
        DbConfig.init();
        seedInitialDataIfEmpty();

        Javalin app = Javalin.create(config -> {
            config.plugins.enableCors(cors -> {
                cors.add(CorsPluginConfig::anyHost);
            });
            config.showJavalinBanner = false;
        });

        // Global Auth Filter for protected paths
        app.before("/api/*", AuthFilter::filter);

        // System Health
        app.get("/api/health", ctx -> ctx.json(Map.of(
                "status", "UP",
                "platform", "Campus Hackathon Team Finder",
                "version", "1.0.0"
        )));

        // Auth routes
        app.post("/api/auth/register", AuthController::register);
        app.post("/api/auth/login", AuthController::login);

        // User profile
        app.get("/api/users/me", UserController::getCurrentUser);

        // Team routes
        app.get("/api/teams", TeamController::listTeams);
        app.get("/api/teams/{id}", TeamController::getTeamById);
        app.post("/api/teams", TeamController::createTeam);
        app.put("/api/teams/{id}", TeamController::updateTeam);
        app.delete("/api/teams/{id}", TeamController::deleteTeam);

        // Join Request routes
        app.post("/api/requests", RequestController::sendRequest);
        app.get("/api/requests/received", RequestController::getReceivedRequests);
        app.get("/api/requests/sent", RequestController::getSentRequests);
        app.put("/api/requests/{id}", RequestController::updateRequestStatus);

        app.start(port);
        log.info("Hackathon Team Finder backend running at http://localhost:{}", port);
    }

    private static void seedInitialDataIfEmpty() {
        if (DbConfig.getTeamsCollection().countDocuments() > 0) {
            return;
        }

        log.info("Seeding realistic campus hackathon teams and demo accounts...");

        // Create Demo Students
        ObjectId user1Id = new ObjectId();
        ObjectId user2Id = new ObjectId();
        ObjectId user3Id = new ObjectId();

        String hash = BCrypt.hashpw("student123", BCrypt.gensalt(10));

        Document u1 = new Document("_id", user1Id)
                .append("name", "Aarav Mehta")
                .append("email", "aarav.mehta@campus.edu")
                .append("passwordHash", hash)
                .append("branch", "Computer Science & Engineering")
                .append("year", "3rd Year")
                .append("skills", List.of("Python", "FastAPI", "PyTorch", "React"))
                .append("createdAt", new Date());

        Document u2 = new Document("_id", user2Id)
                .append("name", "Ananya Deshmukh")
                .append("email", "ananya.d@campus.edu")
                .append("passwordHash", hash)
                .append("branch", "Information Technology")
                .append("year", "4th Year")
                .append("skills", List.of("Solidity", "Web3.js", "Next.js", "Node.js"))
                .append("createdAt", new Date());

        Document u3 = new Document("_id", user3Id)
                .append("name", "Kabir Roy")
                .append("email", "kabir.roy@campus.edu")
                .append("passwordHash", hash)
                .append("branch", "Electronics & Communication")
                .append("year", "2nd Year")
                .append("skills", List.of("Java", "PostgreSQL", "Docker", "Figma"))
                .append("createdAt", new Date());

        DbConfig.getUsersCollection().insertMany(List.of(u1, u2, u3));

        // Team 1: SIH 2026
        Document t1 = new Document("_id", new ObjectId())
                .append("hackathonName", "Smart India Hackathon 2026")
                .append("title", "AgriPulse – AI Drone Crop Health Diagnostics")
                .append("description", "Building real-time aerial image segmentation to spot crop blight, pest infestation, and moisture deficits for smallholder farmers. Need a frontend engineer and an ML researcher.")
                .append("skillsNeeded", List.of("React", "Tailwind CSS", "TensorFlow", "Computer Vision"))
                .append("teamSize", 4)
                .append("currentMembers", List.of(
                        new Document("userId", user1Id.toHexString()).append("name", "Aarav Mehta").append("role", "Team Leader / Backend")
                ))
                .append("createdBy", user1Id.toHexString())
                .append("creatorName", "Aarav Mehta")
                .append("creatorEmail", "aarav.mehta@campus.edu")
                .append("status", "OPEN")
                .append("createdAt", new Date(System.currentTimeMillis() - 86400000L * 2));

        // Team 2: ETHIndia 2026
        Document t2 = new Document("_id", new ObjectId())
                .append("hackathonName", "ETHIndia 2026")
                .append("title", "ProofOfSkill – Verifiable Degree & Hackathon Badges")
                .append("description", "A decentralized campus identity protocol issuing tamper-proof ERC-4337 soulbound credentials for academic accomplishments and verified hackathon wins.")
                .append("skillsNeeded", List.of("Solidity", "Rust", "Smart Contracts", "Ethers.js"))
                .append("teamSize", 3)
                .append("currentMembers", List.of(
                        new Document("userId", user2Id.toHexString()).append("name", "Ananya Deshmukh").append("role", "Lead Smart Contract Dev")
                ))
                .append("createdBy", user2Id.toHexString())
                .append("creatorName", "Ananya Deshmukh")
                .append("creatorEmail", "ananya.d@campus.edu")
                .append("status", "OPEN")
                .append("createdAt", new Date(System.currentTimeMillis() - 86400000L));

        // Team 3: Campus CodeFest 2026
        Document t3 = new Document("_id", new ObjectId())
                .append("hackathonName", "Campus CodeFest 2026")
                .append("title", "PulseShuttle – On-Demand Campus Transit Optimizer")
                .append("description", "Dynamic route scheduling and crowd load forecasting for campus electric shuttles. Real-time GPS tracker integration with offline mesh backup.")
                .append("skillsNeeded", List.of("Java", "WebSockets", "Leaflet.js", "UI/UX Design"))
                .append("teamSize", 4)
                .append("currentMembers", List.of(
                        new Document("userId", user3Id.toHexString()).append("name", "Kabir Roy").append("role", "Team Leader / Architect")
                ))
                .append("createdBy", user3Id.toHexString())
                .append("creatorName", "Kabir Roy")
                .append("creatorEmail", "kabir.roy@campus.edu")
                .append("status", "OPEN")
                .append("createdAt", new Date());

        DbConfig.getTeamsCollection().insertMany(List.of(t1, t2, t3));
        DbConfig.saveCollection("users");
        DbConfig.saveCollection("teams");
        log.info("Demo data successfully seeded and saved.");
    }
}

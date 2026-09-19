package com.vexoria.controllers;

import com.mongodb.client.MongoCollection;
import com.mongodb.client.model.Filters;
import com.mongodb.client.model.Sorts;
import com.mongodb.client.model.Updates;
import com.vexoria.config.DbConfig;
import io.javalin.http.Context;
import org.bson.Document;
import org.bson.types.ObjectId;

import java.util.*;

public class RequestController {

    public static void sendRequest(Context ctx) {
        String userId = ctx.attribute("userId");
        if (userId == null) {
            ctx.status(401).json(Map.of("error", "Unauthorized"));
            return;
        }

        Document body = Document.parse(ctx.body());
        String teamId = body.getString("teamId");
        String message = body.getString("message");

        if (teamId == null || teamId.isBlank()) {
            ctx.status(400).json(Map.of("error", "Team ID is required"));
            return;
        }

        MongoCollection<Document> teamsCol = DbConfig.getTeamsCollection();
        Document teamDoc = null;
        try {
            teamDoc = teamsCol.find(Filters.eq("_id", new ObjectId(teamId))).first();
        } catch (Exception ignored) {}

        if (teamDoc == null) {
            ctx.status(404).json(Map.of("error", "Team not found"));
            return;
        }

        String teamOwnerId = teamDoc.getString("createdBy");
        if (userId.equals(teamOwnerId)) {
            ctx.status(400).json(Map.of("error", "You cannot apply to your own team"));
            return;
        }

        if (!"OPEN".equalsIgnoreCase(teamDoc.getString("status"))) {
            ctx.status(400).json(Map.of("error", "This team is currently not open to new members"));
            return;
        }

        @SuppressWarnings("unchecked")
        List<Document> members = (List<Document>) teamDoc.get("currentMembers");
        if (members != null) {
            for (Document m : members) {
                if (userId.equals(m.getString("userId"))) {
                    ctx.status(400).json(Map.of("error", "You are already a member of this team"));
                    return;
                }
            }
        }

        MongoCollection<Document> reqsCol = DbConfig.getJoinRequestsCollection();
        Document existingReq = reqsCol.find(Filters.and(
                Filters.eq("teamId", teamId),
                Filters.eq("userId", userId),
                Filters.in("status", "PENDING", "ACCEPTED")
        )).first();

        if (existingReq != null) {
            ctx.status(409).json(Map.of("error", "You have already submitted an active request to this team"));
            return;
        }

        MongoCollection<Document> usersCol = DbConfig.getUsersCollection();
        Document userDoc = usersCol.find(Filters.eq("_id", new ObjectId(userId))).first();
        String userName = userDoc != null ? userDoc.getString("name") : "Student";
        String userEmail = userDoc != null ? userDoc.getString("email") : "";
        String userBranch = userDoc != null ? userDoc.getString("branch") : "";
        String userYear = userDoc != null ? userDoc.getString("year") : "";
        Object userSkills = userDoc != null ? userDoc.get("skills") : new ArrayList<>();

        ObjectId reqId = new ObjectId();
        Document reqDoc = new Document("_id", reqId)
                .append("teamId", teamId)
                .append("teamTitle", teamDoc.getString("title"))
                .append("hackathonName", teamDoc.getString("hackathonName"))
                .append("teamOwnerId", teamOwnerId)
                .append("userId", userId)
                .append("userName", userName)
                .append("userEmail", userEmail)
                .append("userBranch", userBranch)
                .append("userYear", userYear)
                .append("userSkills", userSkills)
                .append("message", message != null ? message.trim() : "")
                .append("status", "PENDING")
                .append("createdAt", new Date());

        reqsCol.insertOne(reqDoc);
        DbConfig.saveCollection("join_requests");

        ctx.status(201).json(serializeRequest(reqDoc));
    }

    public static void getReceivedRequests(Context ctx) {
        String userId = ctx.attribute("userId");
        if (userId == null) {
            ctx.status(401).json(Map.of("error", "Unauthorized"));
            return;
        }

        MongoCollection<Document> reqsCol = DbConfig.getJoinRequestsCollection();
        List<Document> list = reqsCol.find(Filters.eq("teamOwnerId", userId))
                .sort(Sorts.descending("createdAt"))
                .into(new ArrayList<>());

        List<Map<String, Object>> result = new ArrayList<>();
        for (Document d : list) {
            result.add(serializeRequest(d));
        }

        ctx.json(result);
    }

    public static void getSentRequests(Context ctx) {
        String userId = ctx.attribute("userId");
        if (userId == null) {
            ctx.status(401).json(Map.of("error", "Unauthorized"));
            return;
        }

        MongoCollection<Document> reqsCol = DbConfig.getJoinRequestsCollection();
        List<Document> list = reqsCol.find(Filters.eq("userId", userId))
                .sort(Sorts.descending("createdAt"))
                .into(new ArrayList<>());

        List<Map<String, Object>> result = new ArrayList<>();
        for (Document d : list) {
            result.add(serializeRequest(d));
        }

        ctx.json(result);
    }

    public static void updateRequestStatus(Context ctx) {
        String userId = ctx.attribute("userId");
        String reqId = ctx.pathParam("id");

        if (userId == null) {
            ctx.status(401).json(Map.of("error", "Unauthorized"));
            return;
        }

        MongoCollection<Document> reqsCol = DbConfig.getJoinRequestsCollection();
        Document reqDoc = null;
        try {
            reqDoc = reqsCol.find(Filters.eq("_id", new ObjectId(reqId))).first();
        } catch (Exception ignored) {}

        if (reqDoc == null) {
            ctx.status(404).json(Map.of("error", "Request not found"));
            return;
        }

        // Verify that current user is the owner of the team
        if (!userId.equals(reqDoc.getString("teamOwnerId"))) {
            ctx.status(403).json(Map.of("error", "Only the team owner can respond to join requests"));
            return;
        }

        Document body = Document.parse(ctx.body());
        String newStatus = body.getString("status");
        if (newStatus == null || (!"ACCEPTED".equalsIgnoreCase(newStatus) && !"REJECTED".equalsIgnoreCase(newStatus))) {
            ctx.status(400).json(Map.of("error", "Status must be ACCEPTED or REJECTED"));
            return;
        }

        newStatus = newStatus.toUpperCase();

        if ("ACCEPTED".equals(newStatus)) {
            String teamId = reqDoc.getString("teamId");
            MongoCollection<Document> teamsCol = DbConfig.getTeamsCollection();
            Document teamDoc = teamsCol.find(Filters.eq("_id", new ObjectId(teamId))).first();

            if (teamDoc != null) {
                @SuppressWarnings("unchecked")
                List<Document> members = (List<Document>) teamDoc.get("currentMembers");
                if (members == null) members = new ArrayList<>();

                int teamSize = teamDoc.getInteger("teamSize", 4);

                String applicantUserId = reqDoc.getString("userId");
                boolean alreadyIn = false;
                for (Document m : members) {
                    if (applicantUserId != null && applicantUserId.equals(m.getString("userId"))) {
                        alreadyIn = true;
                        break;
                    }
                }
                if (!alreadyIn) {
                    Document newMember = new Document("userId", applicantUserId)
                            .append("name", reqDoc.getString("userName"))
                            .append("role", "Member");
                    members.add(newMember);

                    String updatedTeamStatus = members.size() >= teamSize ? "FULL" : teamDoc.getString("status");

                    teamsCol.updateOne(Filters.eq("_id", new ObjectId(teamId)),
                            Updates.combine(
                                    Updates.set("currentMembers", members),
                                    Updates.set("status", updatedTeamStatus)
                            )
                    );
                    DbConfig.saveCollection("teams");
                }
            }
        }

        reqsCol.updateOne(Filters.eq("_id", new ObjectId(reqId)), Updates.set("status", newStatus));
        DbConfig.saveCollection("join_requests");
        Document updated = reqsCol.find(Filters.eq("_id", new ObjectId(reqId))).first();

        ctx.json(serializeRequest(updated));
    }

    private static Map<String, Object> serializeRequest(Document doc) {
        Map<String, Object> map = new LinkedHashMap<>();
        map.put("id", doc.getObjectId("_id").toHexString());
        map.put("teamId", doc.getString("teamId"));
        map.put("teamTitle", doc.getString("teamTitle"));
        map.put("hackathonName", doc.getString("hackathonName"));
        map.put("teamOwnerId", doc.getString("teamOwnerId"));
        map.put("userId", doc.getString("userId"));
        map.put("userName", doc.getString("userName"));
        map.put("userEmail", doc.getString("userEmail"));
        map.put("userBranch", doc.getString("userBranch"));
        map.put("userYear", doc.getString("userYear"));
        map.put("userSkills", doc.get("userSkills"));
        map.put("message", doc.getString("message"));
        map.put("status", doc.getString("status"));
        map.put("createdAt", doc.get("createdAt"));
        return map;
    }
}

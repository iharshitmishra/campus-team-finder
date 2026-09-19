package com.vexoria.controllers;

import com.mongodb.client.MongoCollection;
import com.mongodb.client.model.Filters;
import com.mongodb.client.model.Sorts;
import com.mongodb.client.model.Updates;
import com.vexoria.config.DbConfig;
import io.javalin.http.Context;
import org.bson.Document;
import org.bson.conversions.Bson;
import org.bson.types.ObjectId;

import java.util.*;
import java.util.regex.Pattern;

public class TeamController {

    public static void listTeams(Context ctx) {
        String skillFilter = ctx.queryParam("skill");
        String hackathonFilter = ctx.queryParam("hackathon");
        String statusFilter = ctx.queryParam("status");
        String searchQuery = ctx.queryParam("search");

        List<Bson> filters = new ArrayList<>();

        if (statusFilter != null && !statusFilter.isBlank()) {
            filters.add(Filters.eq("status", statusFilter.trim().toUpperCase()));
        }

        if (skillFilter != null && !skillFilter.isBlank()) {
            Pattern p = Pattern.compile(Pattern.quote(skillFilter.trim()), Pattern.CASE_INSENSITIVE);
            filters.add(Filters.regex("skillsNeeded", p));
        }

        if (hackathonFilter != null && !hackathonFilter.isBlank()) {
            Pattern p = Pattern.compile(Pattern.quote(hackathonFilter.trim()), Pattern.CASE_INSENSITIVE);
            filters.add(Filters.regex("hackathonName", p));
        }

        if (searchQuery != null && !searchQuery.isBlank()) {
            Pattern p = Pattern.compile(Pattern.quote(searchQuery.trim()), Pattern.CASE_INSENSITIVE);
            filters.add(Filters.or(
                    Filters.regex("title", p),
                    Filters.regex("hackathonName", p),
                    Filters.regex("description", p)
            ));
        }

        Bson combined = filters.isEmpty() ? new Document() : Filters.and(filters);

        MongoCollection<Document> teamsCol = DbConfig.getTeamsCollection();
        List<Document> teams = teamsCol.find(combined)
                .sort(Sorts.descending("createdAt"))
                .into(new ArrayList<>());

        List<Map<String, Object>> response = new ArrayList<>();
        for (Document doc : teams) {
            response.add(serializeTeam(doc));
        }

        ctx.json(response);
    }

    public static void getTeamById(Context ctx) {
        String id = ctx.pathParam("id");
        MongoCollection<Document> teamsCol = DbConfig.getTeamsCollection();

        Document doc = null;
        try {
            doc = teamsCol.find(Filters.eq("_id", new ObjectId(id))).first();
        } catch (Exception ignored) {}

        if (doc == null) {
            ctx.status(404).json(Map.of("error", "Team not found"));
            return;
        }

        ctx.json(serializeTeam(doc));
    }

    public static void createTeam(Context ctx) {
        String userId = ctx.attribute("userId");
        if (userId == null) {
            ctx.status(401).json(Map.of("error", "Unauthorized"));
            return;
        }

        Document body = Document.parse(ctx.body());
        String hackathonName = body.getString("hackathonName");
        String title = body.getString("title");
        String description = body.getString("description");
        Integer teamSize = body.getInteger("teamSize", 4);

        @SuppressWarnings("unchecked")
        List<String> skillsNeeded = (List<String>) body.get("skillsNeeded");
        if (skillsNeeded == null) skillsNeeded = new ArrayList<>();

        if (hackathonName == null || title == null || hackathonName.isBlank() || title.isBlank()) {
            ctx.status(400).json(Map.of("error", "Hackathon name and team title are required"));
            return;
        }

        MongoCollection<Document> usersCol = DbConfig.getUsersCollection();
        Document userDoc = usersCol.find(Filters.eq("_id", new ObjectId(userId))).first();
        String creatorName = userDoc != null ? userDoc.getString("name") : "Student";
        String creatorEmail = userDoc != null ? userDoc.getString("email") : "";

        ObjectId teamId = new ObjectId();
        Document leaderMember = new Document("userId", userId)
                .append("name", creatorName)
                .append("role", "Team Leader");

        List<Document> members = new ArrayList<>();
        members.add(leaderMember);

        Document teamDoc = new Document("_id", teamId)
                .append("hackathonName", hackathonName.trim())
                .append("title", title.trim())
                .append("description", description != null ? description.trim() : "")
                .append("skillsNeeded", skillsNeeded)
                .append("teamSize", teamSize != null && teamSize >= 2 ? teamSize : 4)
                .append("currentMembers", members)
                .append("createdBy", userId)
                .append("creatorName", creatorName)
                .append("creatorEmail", creatorEmail)
                .append("status", "OPEN")
                .append("createdAt", new Date());

        DbConfig.getTeamsCollection().insertOne(teamDoc);
        DbConfig.saveCollection("teams");

        ctx.status(201).json(serializeTeam(teamDoc));
    }

    public static void updateTeam(Context ctx) {
        String userId = ctx.attribute("userId");
        String id = ctx.pathParam("id");

        MongoCollection<Document> teamsCol = DbConfig.getTeamsCollection();
        Document teamDoc = null;
        try {
            teamDoc = teamsCol.find(Filters.eq("_id", new ObjectId(id))).first();
        } catch (Exception ignored) {}

        if (teamDoc == null) {
            ctx.status(404).json(Map.of("error", "Team not found"));
            return;
        }

        if (!userId.equals(teamDoc.getString("createdBy"))) {
            ctx.status(403).json(Map.of("error", "Only the team creator can edit this team"));
            return;
        }

        Document body = Document.parse(ctx.body());
        List<Bson> updates = new ArrayList<>();

        if (body.containsKey("title")) updates.add(Updates.set("title", body.getString("title")));
        if (body.containsKey("hackathonName")) updates.add(Updates.set("hackathonName", body.getString("hackathonName")));
        if (body.containsKey("description")) updates.add(Updates.set("description", body.getString("description")));
        if (body.containsKey("skillsNeeded")) updates.add(Updates.set("skillsNeeded", body.get("skillsNeeded")));
        if (body.containsKey("teamSize")) updates.add(Updates.set("teamSize", body.getInteger("teamSize")));
        if (body.containsKey("status")) updates.add(Updates.set("status", body.getString("status").toUpperCase()));

        if (!updates.isEmpty()) {
            teamsCol.updateOne(Filters.eq("_id", new ObjectId(id)), Updates.combine(updates));
            DbConfig.saveCollection("teams");
        }

        Document updated = teamsCol.find(Filters.eq("_id", new ObjectId(id))).first();
        ctx.json(serializeTeam(updated));
    }

    public static void deleteTeam(Context ctx) {
        String userId = ctx.attribute("userId");
        String id = ctx.pathParam("id");

        MongoCollection<Document> teamsCol = DbConfig.getTeamsCollection();
        Document teamDoc = null;
        try {
            teamDoc = teamsCol.find(Filters.eq("_id", new ObjectId(id))).first();
        } catch (Exception ignored) {}

        if (teamDoc == null) {
            ctx.status(404).json(Map.of("error", "Team not found"));
            return;
        }

        if (!userId.equals(teamDoc.getString("createdBy"))) {
            ctx.status(403).json(Map.of("error", "Only the team creator can delete this team"));
            return;
        }

        teamsCol.deleteOne(Filters.eq("_id", new ObjectId(id)));
        DbConfig.getJoinRequestsCollection().deleteMany(Filters.eq("teamId", id));
        DbConfig.saveCollection("teams");
        DbConfig.saveCollection("join_requests");

        ctx.json(Map.of("message", "Team deleted successfully", "id", id));
    }

    public static Map<String, Object> serializeTeam(Document doc) {
        Map<String, Object> map = new LinkedHashMap<>();
        map.put("id", doc.getObjectId("_id").toHexString());
        map.put("hackathonName", doc.getString("hackathonName"));
        map.put("title", doc.getString("title"));
        map.put("description", doc.getString("description"));
        map.put("skillsNeeded", doc.get("skillsNeeded"));
        map.put("teamSize", doc.getInteger("teamSize", 4));

        @SuppressWarnings("unchecked")
        List<Document> membersDocs = (List<Document>) doc.get("currentMembers");
        List<Map<String, Object>> membersList = new ArrayList<>();
        if (membersDocs != null) {
            for (Document m : membersDocs) {
                membersList.add(Map.of(
                        "userId", m.getString("userId"),
                        "name", m.getString("name"),
                        "role", m.getString("role") != null ? m.getString("role") : "Member"
                ));
            }
        }
        map.put("currentMembers", membersList);
        map.put("createdBy", doc.getString("createdBy"));
        map.put("creatorName", doc.getString("creatorName"));
        map.put("creatorEmail", doc.getString("creatorEmail"));
        map.put("status", doc.getString("status"));
        map.put("createdAt", doc.get("createdAt"));
        return map;
    }
}

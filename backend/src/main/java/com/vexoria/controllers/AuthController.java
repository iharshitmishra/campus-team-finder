package com.vexoria.controllers;

import com.mongodb.client.MongoCollection;
import com.mongodb.client.model.Filters;
import com.vexoria.config.DbConfig;
import com.vexoria.models.User;
import com.vexoria.util.JwtUtil;
import io.javalin.http.Context;
import org.bson.Document;
import org.bson.types.ObjectId;
import org.mindrot.jbcrypt.BCrypt;

import java.util.*;

public class AuthController {

    public static void register(Context ctx) {
        Document body = Document.parse(ctx.body());
        String name = body.getString("name");
        String email = body.getString("email");
        String password = body.getString("password");
        String branch = body.getString("branch");
        String year = body.getString("year");

        @SuppressWarnings("unchecked")
        List<String> skills = (List<String>) body.get("skills");
        if (skills == null) skills = new ArrayList<>();

        if (name == null || email == null || password == null || name.isBlank() || email.isBlank() || password.isBlank()) {
            ctx.status(400).json(Map.of("error", "Name, email, and password are required"));
            return;
        }

        MongoCollection<Document> usersCol = DbConfig.getUsersCollection();
        String normalizedEmail = email.toLowerCase().trim();
        Document existing = usersCol.find(Filters.eq("email", normalizedEmail)).first();
        if (existing != null) {
            ctx.status(409).json(Map.of("error", "An account with this email already exists. Please sign in instead."));
            return;
        }

        String hashedPassword = BCrypt.hashpw(password, BCrypt.gensalt(10));
        ObjectId id = new ObjectId();
        Date now = new Date();

        Document userDoc = new Document("_id", id)
                .append("name", name.trim())
                .append("email", normalizedEmail)
                .append("passwordHash", hashedPassword)
                .append("branch", branch != null && !branch.isBlank() ? branch.trim() : "General Engineering")
                .append("year", year != null && !year.isBlank() ? year.trim() : "3rd Year")
                .append("skills", skills)
                .append("createdAt", now);

        usersCol.insertOne(userDoc);
        DbConfig.saveCollection("users");

        User user = new User(id.toHexString(), name.trim(), normalizedEmail, null, branch, year, skills);
        String token = JwtUtil.generateToken(user);

        Map<String, Object> userMap = new LinkedHashMap<>();
        userMap.put("id", id.toHexString());
        userMap.put("name", user.getName());
        userMap.put("email", user.getEmail());
        userMap.put("branch", user.getBranch());
        userMap.put("year", user.getYear());
        userMap.put("skills", user.getSkills());

        ctx.status(201).json(Map.of(
                "token", token,
                "user", userMap,
                "message", "Account registered successfully"
        ));
    }

    public static void login(Context ctx) {
        Document body = Document.parse(ctx.body());
        String email = body.getString("email");
        String password = body.getString("password");

        if (email == null || password == null || email.isBlank() || password.isBlank()) {
            ctx.status(400).json(Map.of("error", "Email and password are required"));
            return;
        }

        MongoCollection<Document> usersCol = DbConfig.getUsersCollection();
        String normalizedEmail = email.toLowerCase().trim();
        Document userDoc = usersCol.find(Filters.eq("email", normalizedEmail)).first();

        if (userDoc == null) {
            ctx.status(404).json(Map.of(
                    "error", "No student account found with this email. Please register to create your profile.",
                    "notFound", true,
                    "email", normalizedEmail
            ));
            return;
        }

        String storedHash = userDoc.getString("passwordHash");
        if (storedHash == null || !BCrypt.checkpw(password, storedHash)) {
            ctx.status(401).json(Map.of("error", "Incorrect password. Please verify and try again."));
            return;
        }

        String idHex = userDoc.getObjectId("_id").toHexString();
        String name = userDoc.getString("name");
        String branch = userDoc.getString("branch");
        String year = userDoc.getString("year");

        @SuppressWarnings("unchecked")
        List<String> skills = (List<String>) userDoc.get("skills");
        if (skills == null) skills = new ArrayList<>();

        User user = new User(idHex, name, normalizedEmail, null, branch, year, skills);
        String token = JwtUtil.generateToken(user);

        Map<String, Object> userMap = new LinkedHashMap<>();
        userMap.put("id", idHex);
        userMap.put("name", name);
        userMap.put("email", normalizedEmail);
        userMap.put("branch", branch);
        userMap.put("year", year);
        userMap.put("skills", skills);

        ctx.json(Map.of(
                "token", token,
                "user", userMap,
                "message", "Login successful"
        ));
    }
}

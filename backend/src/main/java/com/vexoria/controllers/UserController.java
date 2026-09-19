package com.vexoria.controllers;

import com.mongodb.client.MongoCollection;
import com.mongodb.client.model.Filters;
import com.vexoria.config.DbConfig;
import io.javalin.http.Context;
import org.bson.Document;
import org.bson.types.ObjectId;

import java.util.ArrayList;
import java.util.LinkedHashMap;
import java.util.List;
import java.util.Map;

public class UserController {

    public static void getCurrentUser(Context ctx) {
        String userId = ctx.attribute("userId");
        if (userId == null) {
            ctx.status(401).json(Map.of("error", "Unauthorized"));
            return;
        }

        MongoCollection<Document> usersCol = DbConfig.getUsersCollection();
        Document userDoc = null;
        try {
            userDoc = usersCol.find(Filters.eq("_id", new ObjectId(userId))).first();
        } catch (Exception ignored) {}

        if (userDoc == null) {
            ctx.status(404).json(Map.of("error", "User not found"));
            return;
        }

        @SuppressWarnings("unchecked")
        List<String> skills = (List<String>) userDoc.get("skills");
        if (skills == null) skills = new ArrayList<>();

        Map<String, Object> resp = new LinkedHashMap<>();
        resp.put("id", userDoc.getObjectId("_id").toHexString());
        resp.put("name", userDoc.getString("name"));
        resp.put("email", userDoc.getString("email"));
        resp.put("branch", userDoc.getString("branch"));
        resp.put("year", userDoc.getString("year"));
        resp.put("skills", skills);
        resp.put("createdAt", userDoc.get("createdAt"));

        ctx.json(resp);
    }
}

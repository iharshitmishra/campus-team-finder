package com.vexoria.config;

import com.mongodb.ConnectionString;
import com.mongodb.MongoClientSettings;
import com.mongodb.client.MongoClient;
import com.mongodb.client.MongoClients;
import com.mongodb.client.MongoCollection;
import com.mongodb.client.MongoDatabase;
import com.mongodb.client.model.IndexOptions;
import com.mongodb.client.model.Indexes;
import de.bwaldvogel.mongo.MongoServer;
import de.bwaldvogel.mongo.backend.memory.MemoryBackend;
import org.bson.Document;
import org.slf4j.Logger;
import org.slf4j.LoggerFactory;

import java.io.File;
import java.io.FileWriter;
import java.net.InetSocketAddress;
import java.nio.file.Files;
import java.nio.file.Path;
import java.util.ArrayList;
import java.util.List;
import java.util.concurrent.TimeUnit;

public class DbConfig {
    private static final Logger log = LoggerFactory.getLogger(DbConfig.class);
    private static final String DB_NAME = "hackathon_team_finder";
    private static final String DATA_DIR = "data";
    private static MongoClient mongoClient;
    private static MongoDatabase database;
    private static MongoServer memoryServer;

    public static synchronized void init() {
        if (database != null) return;

        String uri = System.getenv("MONGODB_URI");

        if (uri != null && !uri.isBlank()) {
            try {
                log.info("Connecting to MongoDB via MONGODB_URI...");
                mongoClient = MongoClients.create(uri);
                database = mongoClient.getDatabase(DB_NAME);
                database.runCommand(new Document("ping", 1));
                log.info("Successfully connected to external MongoDB.");
            } catch (Exception e) {
                log.warn("Failed to connect via MONGODB_URI: {}. Falling back.", e.getMessage());
            }
        }

        if (database == null) {
            try {
                log.info("Testing local MongoDB on localhost:27017...");
                MongoClientSettings settings = MongoClientSettings.builder()
                        .applyConnectionString(new ConnectionString("mongodb://localhost:27017"))
                        .applyToClusterSettings(b -> b.serverSelectionTimeout(1500, TimeUnit.MILLISECONDS))
                        .applyToSocketSettings(b -> b.connectTimeout(1500, TimeUnit.MILLISECONDS))
                        .build();
                MongoClient localClient = MongoClients.create(settings);
                MongoDatabase testDb = localClient.getDatabase(DB_NAME);
                testDb.runCommand(new Document("ping", 1));
                mongoClient = localClient;
                database = testDb;
                log.info("Successfully connected to local MongoDB daemon.");
            } catch (Exception ex) {
                log.info("Starting embedded MongoDB wire-protocol server...");
                try {
                    memoryServer = new MongoServer(new MemoryBackend());
                    InetSocketAddress serverAddress = memoryServer.bind();
                    String fallbackUri = "mongodb://" + serverAddress.getHostString() + ":" + serverAddress.getPort();
                    mongoClient = MongoClients.create(fallbackUri);
                    database = mongoClient.getDatabase(DB_NAME);
                    log.info("Embedded MongoDB wire server running at {}", fallbackUri);
                } catch (Exception e) {
                    log.error("Failed to start embedded Mongo server", e);
                    throw new RuntimeException("Could not initialize database", e);
                }
            }
        }

        setupIndexes();
        loadPersistentData();
    }

    private static void setupIndexes() {
        try {
            getUsersCollection().createIndex(Indexes.ascending("email"), new IndexOptions().unique(true));
            getTeamsCollection().createIndex(Indexes.ascending("status"));
            getJoinRequestsCollection().createIndex(Indexes.ascending("teamId"));
            getJoinRequestsCollection().createIndex(Indexes.ascending("userId"));
        } catch (Exception e) {
            log.warn("Index setup note: {}", e.getMessage());
        }
    }

    public static MongoDatabase getDatabase() {
        if (database == null) init();
        return database;
    }

    public static MongoCollection<Document> getUsersCollection() {
        return getDatabase().getCollection("users");
    }

    public static MongoCollection<Document> getTeamsCollection() {
        return getDatabase().getCollection("teams");
    }

    public static MongoCollection<Document> getJoinRequestsCollection() {
        return getDatabase().getCollection("join_requests");
    }

    /**
     * Persists a collection's documents to disk so data is never lost across server restarts
     */
    public static synchronized void saveCollection(String name) {
        try {
            File dir = new File(DATA_DIR);
            if (!dir.exists()) dir.mkdirs();

            MongoCollection<Document> col = getDatabase().getCollection(name);
            List<Document> docs = col.find().into(new ArrayList<>());

            File file = new File(dir, name + ".json");
            try (FileWriter writer = new FileWriter(file)) {
                writer.write("[\n");
                for (int i = 0; i < docs.size(); i++) {
                    writer.write(docs.get(i).toJson());
                    if (i < docs.size() - 1) writer.write(",\n");
                }
                writer.write("\n]");
            }
        } catch (Exception e) {
            log.warn("Error saving collection {}: {}", name, e.getMessage());
        }
    }

    /**
     * Reloads previously saved collections from disk if present
     */
    private static void loadPersistentData() {
        try {
            File dir = new File(DATA_DIR);
            if (!dir.exists()) return;

            loadCollectionFromFile("users", getUsersCollection());
            loadCollectionFromFile("teams", getTeamsCollection());
            loadCollectionFromFile("join_requests", getJoinRequestsCollection());
        } catch (Exception e) {
            log.warn("Notice loading persistent data: {}", e.getMessage());
        }
    }

    private static void loadCollectionFromFile(String name, MongoCollection<Document> col) {
        try {
            File file = new File(DATA_DIR, name + ".json");
            if (!file.exists() || col.countDocuments() > 0) return;

            String content = Files.readString(Path.of(file.getAbsolutePath()));
            if (content.isBlank() || content.trim().equals("[]")) return;

            // Strip leading [ and trailing ]
            content = content.trim();
            if (content.startsWith("[") && content.endsWith("]")) {
                content = content.substring(1, content.length() - 1).trim();
            }

            if (!content.isBlank()) {
                String[] parts = content.split("(?<=\\}),\\s*(?=\\{)");
                List<Document> docs = new ArrayList<>();
                for (String part : parts) {
                    if (!part.isBlank()) {
                        docs.add(Document.parse(part.trim()));
                    }
                }
                if (!docs.isEmpty()) {
                    col.insertMany(docs);
                    log.info("Restored {} records for collection {}", docs.size(), name);
                }
            }
        } catch (Exception e) {
            log.warn("Notice loading file for {}: {}", name, e.getMessage());
        }
    }

    public static void close() {
        saveCollection("users");
        saveCollection("teams");
        saveCollection("join_requests");

        if (mongoClient != null) {
            mongoClient.close();
        }
        if (memoryServer != null) {
            memoryServer.shutdown();
        }
    }
}

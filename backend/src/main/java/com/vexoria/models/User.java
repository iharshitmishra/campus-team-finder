package com.vexoria.models;

import java.util.ArrayList;
import java.util.Date;
import java.util.List;

public class User {
    private String id;
    private String name;
    private String email;
    private String passwordHash;
    private String branch;
    private String year;
    private List<String> skills = new ArrayList<>();
    private Date createdAt = new Date();

    public User() {}

    public User(String id, String name, String email, String passwordHash, String branch, String year, List<String> skills) {
        this.id = id;
        this.name = name;
        this.email = email;
        this.passwordHash = passwordHash;
        this.branch = branch;
        this.year = year;
        this.skills = skills != null ? skills : new ArrayList<>();
        this.createdAt = new Date();
    }

    public String getId() { return id; }
    public void setId(String id) { this.id = id; }

    public String getName() { return name; }
    public void setName(String name) { this.name = name; }

    public String getEmail() { return email; }
    public void setEmail(String email) { this.email = email; }

    public String getPasswordHash() { return passwordHash; }
    public void setPasswordHash(String passwordHash) { this.passwordHash = passwordHash; }

    public String getBranch() { return branch; }
    public void setBranch(String branch) { this.branch = branch; }

    public String getYear() { return year; }
    public void setYear(String year) { this.year = year; }

    public List<String> getSkills() { return skills; }
    public void setSkills(List<String> skills) { this.skills = skills; }

    public Date getCreatedAt() { return createdAt; }
    public void setCreatedAt(Date createdAt) { this.createdAt = createdAt; }
}

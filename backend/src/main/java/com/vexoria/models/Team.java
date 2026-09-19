package com.vexoria.models;

import java.util.ArrayList;
import java.util.Date;
import java.util.List;

public class Team {
    private String id;
    private String hackathonName;
    private String title;
    private String description;
    private List<String> skillsNeeded = new ArrayList<>();
    private int teamSize = 4;
    private List<Member> currentMembers = new ArrayList<>();
    private String createdBy; // userId of creator
    private String creatorName;
    private String creatorEmail;
    private String status = "OPEN"; // OPEN, FULL, CLOSED
    private Date createdAt = new Date();

    public static class Member {
        private String userId;
        private String name;
        private String role;

        public Member() {}

        public Member(String userId, String name, String role) {
            this.userId = userId;
            this.name = name;
            this.role = role;
        }

        public String getUserId() { return userId; }
        public void setUserId(String userId) { this.userId = userId; }
        public String getName() { return name; }
        public void setName(String name) { this.name = name; }
        public String getRole() { return role; }
        public void setRole(String role) { this.role = role; }
    }

    public Team() {}

    public String getId() { return id; }
    public void setId(String id) { this.id = id; }

    public String getHackathonName() { return hackathonName; }
    public void setHackathonName(String hackathonName) { this.hackathonName = hackathonName; }

    public String getTitle() { return title; }
    public void setTitle(String title) { this.title = title; }

    public String getDescription() { return description; }
    public void setDescription(String description) { this.description = description; }

    public List<String> getSkillsNeeded() { return skillsNeeded; }
    public void setSkillsNeeded(List<String> skillsNeeded) { this.skillsNeeded = skillsNeeded; }

    public int getTeamSize() { return teamSize; }
    public void setTeamSize(int teamSize) { this.teamSize = teamSize; }

    public List<Member> getCurrentMembers() { return currentMembers; }
    public void setCurrentMembers(List<Member> currentMembers) { this.currentMembers = currentMembers; }

    public String getCreatedBy() { return createdBy; }
    public void setCreatedBy(String createdBy) { this.createdBy = createdBy; }

    public String getCreatorName() { return creatorName; }
    public void setCreatorName(String creatorName) { this.creatorName = creatorName; }

    public String getCreatorEmail() { return creatorEmail; }
    public void setCreatorEmail(String creatorEmail) { this.creatorEmail = creatorEmail; }

    public String getStatus() { return status; }
    public void setStatus(String status) { this.status = status; }

    public Date getCreatedAt() { return createdAt; }
    public void setCreatedAt(Date createdAt) { this.createdAt = createdAt; }
}

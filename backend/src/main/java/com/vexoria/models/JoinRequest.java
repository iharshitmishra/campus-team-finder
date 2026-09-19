package com.vexoria.models;

import java.util.Date;
import java.util.List;

public class JoinRequest {
    private String id;
    private String teamId;
    private String teamTitle;
    private String hackathonName;
    private String teamOwnerId;
    private String userId;
    private String userName;
    private String userEmail;
    private String userBranch;
    private String userYear;
    private List<String> userSkills;
    private String message;
    private String status = "PENDING"; // PENDING, ACCEPTED, REJECTED
    private Date createdAt = new Date();

    public JoinRequest() {}

    public String getId() { return id; }
    public void setId(String id) { this.id = id; }

    public String getTeamId() { return teamId; }
    public void setTeamId(String teamId) { this.teamId = teamId; }

    public String getTeamTitle() { return teamTitle; }
    public void setTeamTitle(String teamTitle) { this.teamTitle = teamTitle; }

    public String getHackathonName() { return hackathonName; }
    public void setHackathonName(String hackathonName) { this.hackathonName = hackathonName; }

    public String getTeamOwnerId() { return teamOwnerId; }
    public void setTeamOwnerId(String teamOwnerId) { this.teamOwnerId = teamOwnerId; }

    public String getUserId() { return userId; }
    public void setUserId(String userId) { this.userId = userId; }

    public String getUserName() { return userName; }
    public void setUserName(String userName) { this.userName = userName; }

    public String getUserEmail() { return userEmail; }
    public void setUserEmail(String userEmail) { this.userEmail = userEmail; }

    public String getUserBranch() { return userBranch; }
    public void setUserBranch(String userBranch) { this.userBranch = userBranch; }

    public String getUserYear() { return userYear; }
    public void setUserYear(String userYear) { this.userYear = userYear; }

    public List<String> getUserSkills() { return userSkills; }
    public void setUserSkills(List<String> userSkills) { this.userSkills = userSkills; }

    public String getMessage() { return message; }
    public void setMessage(String message) { this.message = message; }

    public String getStatus() { return status; }
    public void setStatus(String status) { this.status = status; }

    public Date getCreatedAt() { return createdAt; }
    public void setCreatedAt(Date createdAt) { this.createdAt = createdAt; }
}

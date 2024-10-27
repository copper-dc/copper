package org.Elysium.Database.User;


import org.bson.Document;

public class User {
    public final String userId;
    public final String username;
    public final String currentRegion;
    public final String elementalAffinity;
    public int experiencePoints;
    public int coins;

    public User(String userId, String username, String currentRegion, String elementalAffinity, int experiencePoints, int coins) {
        this.userId = userId;
        this.username = username;
        this.currentRegion = currentRegion;
        this.elementalAffinity = elementalAffinity;
        this.experiencePoints = experiencePoints;
        this.coins = coins;
    }

    public Document toDocument() {
        return new Document("user_id", userId)
                .append("username", username)
                .append("current_region", currentRegion)
                .append("elemental_affinity", elementalAffinity)
                .append("experience_points", experiencePoints)
                .append("coins", coins);
    }

    public static User fromDocument(Document doc) {
        return new User(
                doc.getString("user_id"),
                doc.getString("username"),
                doc.getString("current_region"),
                doc.getString("elemental_affinity"),
                doc.getInteger("experience_points"),
                doc.getInteger("coins")
        );
    }

    public String getUserId() {
        return userId;
    }

    public String getUsername() {
        return username;
    }

    public String getCurrentRegion() {
        return currentRegion;
    }

    public String getElementalAffinity() {
        return elementalAffinity;
    }

    public int getExperiencePoints() {
        return experiencePoints;
    }

    public void setExperiencePoints(int experiencePoints) {
        this.experiencePoints = experiencePoints;
    }



}

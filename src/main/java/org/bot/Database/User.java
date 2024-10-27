package org.bot.Database;

import org.bson.Document;

public class User {
    private String username;
    private String userId;
    private double balance;


    public User(String username, String userId, double balance) {
        this.username = username;
        this.userId = userId;
        this.balance = balance;
    }

    public Document toDocument() {
        Document document = new Document("username", username)
                .append("userid", userId)
                .append("balance", balance);
        return document;
    }

    public static User fromDocument(Document document) {
        return new User(
                document.getString("username"),
                document.getString("userid"),
                document.getDouble("balance"));
    }

    // Getters and setters
    public String getUsername() { return username; }
    public String getUserId() { return userId; }
    public double getBalance() { return balance; }
    public void setBalance(double balance) { this.balance = balance; }
}

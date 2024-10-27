package org.bot.Database;

import com.mongodb.client.MongoClient;
import com.mongodb.client.MongoClients;
import com.mongodb.client.MongoCollection;
import com.mongodb.client.MongoDatabase;
import com.mongodb.client.model.Filters;
import org.bson.Document;

import static com.mongodb.client.model.Updates.inc;

public class CopperDB {
    private MongoCollection<Document> userCollection;
    private MongoClient mongoClient;

    public CopperDB(String databaseName, String collectionName) {
        String connectionString = System.getenv("MONGODB_CONNECTION_STRING");
        mongoClient = MongoClients.create(connectionString);
        MongoDatabase database = mongoClient.getDatabase(databaseName.toLowerCase());
        userCollection = database.getCollection(collectionName);
    }

    public String createUser(User user) {
        if (findUser(user.getUsername()) != null) {
            return "User already exists";
        }

        userCollection.insertOne(user.toDocument());
        return "User created successfully";
    }

    public User findUser(String username) {
        Document document = userCollection.find(Filters.eq("username", username)).first();
        return document != null ? User.fromDocument(document) : null;
    }

    public void addMoney(String username, double amount) {
        userCollection.updateOne(Filters.eq("username", username), inc("balance", amount));
    }

    public void close() {
        mongoClient.close();
    }
}

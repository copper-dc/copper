package org.bot.Database;

import com.mongodb.client.MongoClient;
import com.mongodb.client.MongoClients;
import com.mongodb.client.MongoCollection;
import com.mongodb.client.MongoDatabase;
import com.mongodb.client.model.Filters;
import org.bson.Document;

import static com.mongodb.client.model.Updates.inc;

public class CopperDB {

    private final MongoCollection<Document> userCollection;

    public CopperDB(String databaseName, String collectionName) {
        MongoClient mongoClient = MongoClients.create(System.getenv("MONGODB_CONNECTION_STRING"));
        MongoDatabase database = mongoClient.getDatabase(databaseName);
        userCollection = database.getCollection(collectionName);
    }


    public void createUser(String username, String userid, double initialBalance) {
        Document newUser = new Document("username", username)
                .append("userid", userid)
                .append("balance", initialBalance);
        userCollection.insertOne(newUser);
    }

    public Document findUser(String username) {
        return userCollection.find(Filters.eq("username", username)).first();
    }

    public void addMoney(String username, double amount) {
        userCollection.updateOne(Filters.eq("username", username), inc("balance", amount));
    }




}

package org.Elysium.Database.MongoDB;

import com.mongodb.client.MongoClient;
import com.mongodb.client.MongoClients;
import com.mongodb.client.MongoCollection;
import com.mongodb.client.MongoDatabase;
import org.Elysium.Utils.User.User;
import org.bson.Document;
import org.bson.conversions.Bson;

import java.util.ArrayList;
import java.util.List;

import static com.mongodb.client.model.Filters.eq;
import static com.mongodb.client.model.Updates.*;

public class MongoDBConnector {

    private final MongoClient mongoClient;
    private final MongoDatabase mongoDatabase;

    public MongoDBConnector(String connectionString, String databaseName) {
        this.mongoClient = MongoClients.create(connectionString);
        this.mongoDatabase = mongoClient.getDatabase(databaseName);
    }

    public void insertUser(User user, String collectionName) {
        MongoCollection<Document> userCollection = mongoDatabase.getCollection(collectionName);
        Document userDocument = user.toDocument();
        userCollection.insertOne(userDocument);
    }



    // Find user by user ID from the appropriate region collection
    public User findUserById(String userId, String currentRegion) {
        String regionCollectionName = currentRegion.toLowerCase().replace(" ", ""); // Format for collection name
        MongoCollection<Document> userCollection = mongoDatabase.getCollection(regionCollectionName);
        Document userDocument = userCollection.find(new Document("user_id", userId)).first();
        return userDocument != null ? User.fromDocument(userDocument) : null;
    }

    // Update user fields in the appropriate region collection
    public void updateUser(String userId, String currentRegion, String newUsername, String newRegion, String newElementalAffinity, Integer newExperiencePoints, Integer newCoins) {
        String regionCollectionName = currentRegion.toLowerCase().replace(" ", ""); // Format for collection name
        MongoCollection<Document> userCollection = mongoDatabase.getCollection(regionCollectionName);

        List<Bson> updates = new ArrayList<>();

        if (newUsername != null) {
            updates.add(set("username", newUsername));
        }
        if (newRegion != null) {
            updates.add(set("current_region", newRegion));
        }
        if (newElementalAffinity != null) {
            updates.add(set("elemental_affinity", newElementalAffinity));
        }
        if (newExperiencePoints != null) {
            updates.add(set("experience_points", newExperiencePoints));
        }
        if (newCoins != null) {
            updates.add(set("coins", newCoins));
        }

        userCollection.updateOne(eq("user_id", userId), combine(updates));
    }

    // Update user coins
    public void updateCoins(String userId, String currentRegion, int rewards) {
        String regionCollectionName = currentRegion.toLowerCase().replace(" ", ""); // Format for collection name
        MongoCollection<Document> userCollection = mongoDatabase.getCollection(regionCollectionName);
        Bson update = inc("coins", rewards);
        userCollection.updateOne(eq("user_id", userId), update);
    }

    public void close() {
        mongoClient.close();
    }
}

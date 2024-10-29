package org.Elysium.Database.MongoDB;

import com.mongodb.client.MongoClient;
import com.mongodb.client.MongoClients;
import com.mongodb.client.MongoCollection;
import com.mongodb.client.MongoDatabase;
import org.Elysium.Utils.User.User;
import org.bson.Document;
import org.bson.conversions.Bson;

import java.util.ArrayList;
import java.util.Arrays;
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

    public String insertUser(User user, String collectionName) {
        String message = null;
        String userId = user.getUserId();

        String UserRegion = findUserInAnyRegion(userId);
        if(UserRegion==null) {
            MongoCollection<Document> userCollection = mongoDatabase.getCollection(collectionName);
            Document userDocument = user.toDocument();
            userCollection.insertOne(userDocument);

            return message;
        }

        return " was already created in `"+UserRegion+"`";

    }



    // Find user by user ID from the appropriate region collection
    public User findUserById(String userId) {
        List<String> regions = Arrays.asList("Starli Cove", "Tiaga Luminia", "Eternal Sands", "DopplerGorge");

        for (String region : regions) {
            String regionCollectionName = region.toLowerCase().replace(" ", "");
            MongoCollection<Document> userCollection = mongoDatabase.getCollection(regionCollectionName);
            Document userDocument = userCollection.find(new Document("user_id", userId)).first();
            if(userDocument!=null) {
            return User.fromDocument(userDocument);
            }
        }
        return null;
    }

    public String findUserInAnyRegion(String userId) {

        List<String> regions = Arrays.asList("Starli Cove", "Tiaga Luminia", "Eternal Sands", "DopplerGorge");

        for (String region : regions) {
            String regionCollectionName = region.toLowerCase().replace(" ", "");
            MongoCollection<Document> userCollection = mongoDatabase.getCollection(regionCollectionName);
            Document userDocument = userCollection.find(new Document("user_id", userId)).first();

            if (userDocument != null) {
                return region;
            }
        }

        return null; // User not found in any region
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

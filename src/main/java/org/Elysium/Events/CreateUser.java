package org.Elysium.Events;

import net.dv8tion.jda.api.events.message.MessageReceivedEvent;
import net.dv8tion.jda.api.hooks.ListenerAdapter;
import org.Elysium.Database.MongoDB.MongoDBConnector;
import org.Elysium.Utils.User.User;
import org.Elysium.Utils.Inventory.Weapons.Sword;  // Import the Sword class
import org.jetbrains.annotations.NotNull;

import java.util.Random;

public class CreateUser extends ListenerAdapter {

    private final MongoDBConnector mongoDBConnector;

    public CreateUser(MongoDBConnector mongoDBConnector) {
        this.mongoDBConnector = mongoDBConnector;
    }

    @Override
    public void onMessageReceived(@NotNull MessageReceivedEvent event) {
        String[] command = event.getMessage().getContentRaw().split(" ");

        if (command[0].equalsIgnoreCase("!createuser")) {
            String userId = event.getAuthor().getId();
            String username = event.getAuthor().getName();

            String[] regions = {"Tiaga Luminia", "Eternal Sands", "Dopplergorge", "Starli Cove"};
            String[] collectionRegionNames = {"tiagaluminia", "eternalsands", "dopplergorge", "starlicove"};

            // Get random index for region
            int regionIDX = new Random().nextInt(regions.length);
            String currentRegion = regions[regionIDX];
            String currentCollection = collectionRegionNames[regionIDX]; // Corresponding collection name

            String elementalAffinity = "None";

            // Create the new user
            User newUser = new User(userId, username, currentRegion, elementalAffinity, 0, 100);
            // Add an initial sword to the user's inventory
            newUser.addWeapon(new Sword("sword_001", "Basic Sword", currentRegion)); // Adjusted constructor

            // Store user in the corresponding region collection
            mongoDBConnector.insertUser(newUser, currentCollection);

            event.getChannel().sendMessage("User created successfully! Welcome, " + event.getAuthor().getAsMention() + " to " + currentRegion + "!").queue();
        }
    }
}

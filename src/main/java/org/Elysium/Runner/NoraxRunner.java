package org.Elysium.Runner;

import net.dv8tion.jda.api.JDA;
import net.dv8tion.jda.api.JDABuilder;
import net.dv8tion.jda.api.entities.Activity;
import net.dv8tion.jda.api.hooks.ListenerAdapter;
import net.dv8tion.jda.api.interactions.commands.OptionType;
import net.dv8tion.jda.api.interactions.commands.build.CommandData;
import net.dv8tion.jda.api.interactions.commands.build.OptionData;
import net.dv8tion.jda.api.requests.GatewayIntent;
import org.Elysium.Database.MongoDB.MongoDBConnector;
import org.Elysium.Events.CreateUser;
import org.Elysium.Events.Ping;

import static net.dv8tion.jda.api.JDABuilder.*;

public class NoraxRunner extends ListenerAdapter {
    JDA NoraxBot;
    public NoraxRunner() {

        MongoDBConnector mongoDBConnector = new MongoDBConnector(System.getenv("MONGODB_CONNECTION_STRING"),"Regions");
        JDABuilder Noraxbuilder = createDefault(System.getenv("DISCORD_TOKEN"));
        Noraxbuilder.enableIntents(GatewayIntent.GUILD_MEMBERS,GatewayIntent.GUILD_MESSAGES,GatewayIntent.MESSAGE_CONTENT,GatewayIntent.GUILD_PRESENCES);
        Noraxbuilder.setActivity(Activity.playing("In this planet..."));

        Noraxbuilder.addEventListeners(new Ping());
        Noraxbuilder.addEventListeners(new CreateUser(mongoDBConnector));


        JDA NoraxBot = Noraxbuilder.build();


    }
}

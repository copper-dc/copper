package org.Elysium.Runner;

import net.dv8tion.jda.api.JDA;
import net.dv8tion.jda.api.JDABuilder;
import net.dv8tion.jda.api.entities.Activity;
import net.dv8tion.jda.api.hooks.ListenerAdapter;
import net.dv8tion.jda.api.interactions.commands.OptionType;
import net.dv8tion.jda.api.interactions.commands.build.CommandData;
import net.dv8tion.jda.api.interactions.commands.build.Commands;
import net.dv8tion.jda.api.interactions.commands.build.SlashCommandData;
import net.dv8tion.jda.api.requests.GatewayIntent;
import net.dv8tion.jda.api.requests.restaction.CommandListUpdateAction;
import org.Elysium.CommandListener.CommandListener;
import org.Elysium.Database.MongoDB.MongoDBConnector;
import org.Elysium.Events.Ping;
import org.Elysium.Events.UserCommands;

import static net.dv8tion.jda.api.JDABuilder.*;

public class NoraxRunner extends ListenerAdapter {
    JDA NoraxBot;
    public NoraxRunner() throws InterruptedException {

        MongoDBConnector mongoDBConnector = new MongoDBConnector(System.getenv("MONGODB_CONNECTION_STRING"),"Regions");
        JDABuilder Noraxbuilder = createDefault(System.getenv("DISCORD_TOKEN"));
        Noraxbuilder.enableIntents(GatewayIntent.GUILD_MEMBERS,GatewayIntent.GUILD_MESSAGES,GatewayIntent.MESSAGE_CONTENT,GatewayIntent.GUILD_PRESENCES);
        Noraxbuilder.setActivity(Activity.playing("In this planet..."));

        Noraxbuilder.addEventListeners(new Ping());
        Noraxbuilder.addEventListeners(new UserCommands(mongoDBConnector));
        Noraxbuilder.addEventListeners(new CommandListener());

        JDA NoraxBot = Noraxbuilder.build().awaitReady();

        CommandListUpdateAction commands = Noraxbuilder.build().updateCommands();

        commands.addCommands(Commands.slash("hello","Say hello to Norax planet!")).queue();



    }



}

package org.bot.Runner;

import net.dv8tion.jda.api.JDA;
import net.dv8tion.jda.api.JDABuilder;
import net.dv8tion.jda.api.entities.Activity;
import net.dv8tion.jda.api.requests.GatewayIntent;
import org.bot.Events.Greeting;

public class CopperRunner {
    JDA CopperBot;
    public CopperRunner() {
        JDABuilder Copperbuilder = JDABuilder.createDefault(System.getenv("DISCORD_TOKEN"));
        Copperbuilder.enableIntents(GatewayIntent.GUILD_MEMBERS,GatewayIntent.GUILD_MESSAGES,GatewayIntent.MESSAGE_CONTENT,GatewayIntent.GUILD_PRESENCES);
        Copperbuilder.setActivity(Activity.playing("In this planet..."));

        Copperbuilder.addEventListeners(new Greeting());


        CopperBot = Copperbuilder.build();

    }
}

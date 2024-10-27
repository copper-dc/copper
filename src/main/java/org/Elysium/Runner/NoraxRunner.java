package org.Elysium.Runner;

import net.dv8tion.jda.api.JDA;
import net.dv8tion.jda.api.JDABuilder;
import net.dv8tion.jda.api.entities.Activity;
import net.dv8tion.jda.api.requests.GatewayIntent;
import org.Elysium.Events.Greeting;
import org.Elysium.Events.Ping;
import org.Elysium.Events.UserCreate;

import static net.dv8tion.jda.api.JDABuilder.*;

public class NoraxRunner {
    JDA CopperBot;
    public NoraxRunner() {
        JDABuilder Noraxbuilder = createDefault(System.getenv("DISCORD_TOKEN"));
        Noraxbuilder.enableIntents(GatewayIntent.GUILD_MEMBERS,GatewayIntent.GUILD_MESSAGES,GatewayIntent.MESSAGE_CONTENT,GatewayIntent.GUILD_PRESENCES);
        Noraxbuilder.setActivity(Activity.playing("In this planet..."));

        Noraxbuilder.addEventListeners(new Ping());


        CopperBot = Noraxbuilder.build();

    }
}

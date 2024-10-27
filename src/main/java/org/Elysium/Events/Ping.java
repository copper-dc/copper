package org.Elysium.Events;

import net.dv8tion.jda.api.events.message.MessageReceivedEvent;
import net.dv8tion.jda.api.hooks.ListenerAdapter;

public class Ping extends ListenerAdapter {
    @Override
    public void onMessageReceived(MessageReceivedEvent event) {
        String channelId = event.getMessage().getChannelId();
        if (!event.getAuthor().isBot()){
            if (event.getMessage().getContentRaw().equals("!ping")){
                event.getGuild().getTextChannelById(channelId).sendMessage("pong "+event.getAuthor().getAsMention()).queue();
            }
        }

    }

}

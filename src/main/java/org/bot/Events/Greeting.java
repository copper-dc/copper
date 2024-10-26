package org.bot.Events;

import net.dv8tion.jda.api.events.message.MessageReceivedEvent;
import net.dv8tion.jda.api.hooks.ListenerAdapter;

public class Greeting extends ListenerAdapter {
    @Override
    public void onMessageReceived(MessageReceivedEvent event) {
        String channelId = event.getMessage().getChannelId();
        if (!event.getAuthor().isBot()){
            if (event.getMessage().getContentRaw().equals("!hello")){
                event.getGuild().getTextChannelById(channelId).sendMessage("Hello "+event.getAuthor().getAsMention()).queue();
            }
        }

    }

}

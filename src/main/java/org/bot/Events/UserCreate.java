package org.bot.Events;

import net.dv8tion.jda.api.events.interaction.command.SlashCommandInteractionEvent;
import net.dv8tion.jda.api.events.message.MessageReceivedEvent;
import net.dv8tion.jda.api.hooks.ListenerAdapter;
import org.bot.Database.CopperDB;
import org.bson.Document;
import org.jetbrains.annotations.NotNull;

public class UserCreate extends ListenerAdapter {
    CopperDB copperDBManager;
    double initial_amount = 100;


    @Override
    public void onMessageReceived(@NotNull MessageReceivedEvent event) {
        if (!event.getAuthor().isBot()) {
            if (event.getMessage().getContentRaw().equals("!createuser")) {
                String channelId = event.getMessage().getChannelId();
                copperDBManager = new CopperDB("discord", "users");
                String username = String.valueOf(copperDBManager.findUser(event.getAuthor().getAsMention()));
                String userid = String.valueOf(copperDBManager.findUser(event.getAuthor().getId()));
                if (username != null && userid != null) {
                    event.getGuild().getTextChannelById(channelId).sendMessage(event.getAuthor().getAsMention() + " You have been already created!").queue();
                } else {
                    copperDBManager.createUser(username, userid, initial_amount);
                    event.getGuild().getTextChannelById(channelId).sendMessage(event.getAuthor().getAsMention() + " You have been created!").queue();
                }
            }
        }


    }
}

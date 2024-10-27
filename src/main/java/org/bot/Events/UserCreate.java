package org.bot.Events;

import net.dv8tion.jda.api.events.message.MessageReceivedEvent;
import net.dv8tion.jda.api.hooks.ListenerAdapter;
import org.bot.Database.CopperDB;
import org.bot.Database.User;
import org.jetbrains.annotations.NotNull;

public class UserCreate extends ListenerAdapter {
    private CopperDB copperDBManager;
    private double initialAmount = 100;

    @Override
    public void onMessageReceived(@NotNull MessageReceivedEvent event) {
        if (!event.getAuthor().isBot() && event.getMessage().getContentRaw().equals("!createuser")) {
            String username = event.getAuthor().getName();
            String userId = event.getAuthor().getId();
            copperDBManager = new CopperDB("discord", "users");

            User user = new User(username, userId, initialAmount);
            String result = event.getAuthor().getAsMention() + ", " + copperDBManager.createUser(user);
            event.getChannel().sendMessage(result).queue();
        }
    }
}

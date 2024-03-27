import discord
import os
from typing import Final
from discord.ext import commands
from discord import Client, Message
from dotenv import load_dotenv


load_dotenv()

TOKEN: Final[str] = os.getenv('DISCORD_TOKEN')

global strings
strings = ["hello","hi","yahallo","yo","yooo","good morning","good night","good afternoon","good evening","bye","goodbye","cya"]

# Define the intents your bot will use
intents = discord.Intents.default()
intents.message_content = True  # Enable message events

# Create a bot instance with intents
# bot: Client = Client(intents=intents) <- this or below one will do
bot = commands.Bot(command_prefix='/', intents=intents)


@bot.hybrid_command #apparently slash commad area according to a ytber
async def aiko(cxt: commands.Context):
    await cxt.send("nya?")


# Define event for when the bot is ready
@bot.event
async def on_ready():
    print(f'Logged in as {bot.user.name}')
    await bot.tree.sync() #syncing slash commands? something like that

# Define event for when a message is received
@bot.event
async def on_message(message):
    # Check if the message starts with strings[]
    for string in strings:
        if ((message.content.startswith("?"))): #private 
                if message.author != bot.user:
                 await message.author.send(f"{message.content} {message.author.mention}!")
                 break


        elif message.content.lower().startswith(string): #in any channel
            if message.author != bot.user:
                await message.channel.send(f'{string.capitalize()} {message.author.mention}!')
            break
        # Send a response mentioning the user who sent the message
        
        



        
        


# Run the bot with your token
bot.run(TOKEN)